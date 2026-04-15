import os
import json
import datetime
import sys

# Windows環境での絵文字出力(✅など)によるエラーを防ぐため、標準出力をUTF-8に強制 (Macでも問題なし)
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
from auth import get_google_services

def find_student_events_for_week(calendar_service, calendar_id, student_name):
    """
    指定された生徒の向こう1週間のカレンダー予定を探す。
    戻り値: イベント開始時刻(datetime.datetime)のリスト
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    end_of_period = now + datetime.timedelta(days=7)
    now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_str = end_of_period.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    events_result = calendar_service.events().list(
        calendarId=calendar_id, 
        timeMin=now_str,
        timeMax=end_str,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    start_times = []
    
    # 振り替えなど、授業がないことを示すキーワード（全角・半角）
    furi_markers = ['(フリ)', '（フリ）', '(ふり)', '（ふり）', '(振)', '（振）']
    
    for event in events:
        summary = event.get('summary', '')
        # 予定タイトルと生徒名のスペースを除外して比較
        summary_clean = summary.replace(' ', '').replace('　', '')
        
        # 振り替えの予定はスキップ
        if any(marker in summary_clean for marker in furi_markers):
            continue
            
        student_name_clean = student_name.replace(' ', '').replace('　', '')
        if student_name_clean in summary_clean:
            start_str = event['start'].get('dateTime', event['start'].get('date'))
            # dateTimeがある場合のみ（終日予定は除外）
            if 'T' in start_str:
                start_dt = datetime.datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                start_times.append(start_dt)
    
    return start_times

def schedule_announcement(classroom_service, course_id, text, scheduled_time, materials=None):
    scheduled_time_str = scheduled_time.astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    announcement = {
        'text': text,
        'state': 'DRAFT',
        'scheduledTime': scheduled_time_str
    }
    if materials:
        announcement['materials'] = materials
        
    res = classroom_service.courses().announcements().create(courseId=course_id, body=announcement).execute()
    return res

def main():
    print("=== Classroom Meetリンク自動予約システム ===")
    
    load_dotenv()
    calendar_id = os.environ.get('TARGET_CALENDAR_ID')
    
    # Meet URLは .env から読み込む
    meet_url = os.environ.get('MEET_URL', '')
    
    # 担当者名は .env から読み込む（例: TEACHER_NAME="山田 太郎"）
    teacher_name = os.environ.get('TEACHER_NAME', '担当講師')
    
    # 授業開始の何分前に通知するか（デフォルト: 60分前 = 1時間前）
    # .env に NOTIFY_MINUTES_BEFORE=60 のように設定できます
    notify_minutes = int(os.environ.get('NOTIFY_MINUTES_BEFORE', '60'))
    
    if not calendar_id:
        print("❌ .envの設定が不足しています。(TARGET_CALENDAR_ID を設定してください。)")
        return

    # 1. API準備
    calendar_service, classroom_service = get_google_services()
    print("✅ Google APIの認証に成功しました。")

    # 2. studentsディレクトリ内の各生徒を処理
    students_dir = "students"
    if not os.path.exists(students_dir):
        print(f"📁 {students_dir} ディレクトリが存在しません。")
        return

    for student_name in os.listdir(students_dir):
        student_path = os.path.join(students_dir, student_name)
        if not os.path.isdir(student_path):
            continue
            
        settings_path = os.path.join(student_path, "settings.json")
        if not os.path.exists(settings_path):
            print(f"⚠️ {student_name} の設定ファイル (settings.json) がありません。スキップします。")
            continue

        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
            
        if not settings.get("is_active", False):
            print(f"ℹ️ {student_name} の自動生成はオフになっています。")
            continue

        course_id = settings.get('course_id')
        if not course_id:
            print(f"⚠️ {student_name} の settings.json に course_id がないため、Classroom連携をスキップします。")
            continue

        print(f"\n👨‍🎓 生徒: {student_name} の処理を開始します。")
        
        # 3. カレンダーから向こう1週間の授業時間を取得
        start_times = find_student_events_for_week(calendar_service, calendar_id, student_name)
        if not start_times:
            print(f"ℹ️ {student_name} の向こう1週間の授業予定が見つかりませんでした。")
            continue
            
        for start_time in start_times:
            print(f"\n📅 授業日時: {start_time.strftime('%Y-%m-%d %H:%M')}")
            
            # 授業開始時刻の notify_minutes 分前（.envで設定可能）
            post_time = start_time - datetime.timedelta(minutes=notify_minutes)
            
            print(f"🏫 Classroomへ予約投稿を設定中...")
            
            try:
                # お知らせ投稿（授業開始 notify_minutes 分前） - 文章・URL添付のみ
                announcement_msg = (
                    f"こんにちは！\n担当の{teacher_name}です！\n"
                    f"本日 {start_time.strftime('%H:%M')}〜 より指導があるので時間になったら下のリンクからお入りください！"
                )
                announcement_materials = [
                    {
                        'link': {
                            'url': meet_url
                        }
                    }
                ]
                
                schedule_announcement(classroom_service, course_id, announcement_msg, post_time, announcement_materials)
                print(f"  - お知らせ（Meetリンク込み）を {post_time.strftime('%H:%M')} に予約しました")
                
                print(f"🎉 {start_time.strftime('%m/%d')} 分の予約投稿が完了しました！\n")
            except Exception as e:
                print(f"❌ Classroom連携に失敗しました: {e}")
                continue

        print(f"🌟 {student_name} の全スケジュールの処理が完了しました。")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        with open("traceback_log.txt", "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
        raise
