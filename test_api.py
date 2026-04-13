import os
import datetime
from dotenv import load_dotenv
from auth import get_google_services
from google import genai

# 環境変数の読み込み (.envファイル)
load_dotenv()

def test_google_apis():
    print("=== Google API 接続テスト ===")
    calendar_service, classroom_service, drive_service, sheets_service = get_google_services()
    print("✅認証とサービスクライアントの生成に成功しました。")

    # 1. カレンダーのテスト
    target_calendar_id = os.environ.get('TARGET_CALENDAR_ID')
    if target_calendar_id:
        print(f"\n[Calendar] カレンダー({target_calendar_id})の直近3件の予定を取得します...")
        try:
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # UTC時間
            events_result = calendar_service.events().list(
                calendarId=target_calendar_id, 
                timeMin=now,
                maxResults=3, 
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            events = events_result.get('items', [])

            if not events:
                print('直近の予定は見つかりませんでした。')
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(f"  - {start}: {event['summary']}")
            print("✅カレンダーの読み取りに成功しました。")
        except Exception as e:
            print(f"❌カレンダーの取得でエラーが発生しました。権限やIDが正しいか確認してください。\n詳細: {e}")
    else:
        print("\n[Calendar] .envにTARGET_CALENDAR_IDが設定されていないためスキップします。")

    # 2. Classroomのテスト
    print("\n[Classroom] 参加しているクラス一覧を取得します...")
    try:
        results = classroom_service.courses().list(pageSize=10).execute()
        courses = results.get('courses', [])

        if not courses:
            print('  参加している/作成したクラスは見つかりませんでした。')
        else:
            for course in courses:
                print(f"  - {course.get('name')} (ID: {course.get('id')})")
        print("✅Classroomの読み取りに成功しました。")
    except Exception as e:
        print(f"❌Classroomの取得でエラーが発生しました。\n詳細: {e}")

def test_gemini_api():
    print("\n=== Gemini API 接続テスト ===")
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key or api_key == "ここにGeminiの無料APIキーを貼り付けてください":
         print("❌ .envファイルにGemini APIキーが設定されていないか、デフォルト値のままです。")
         return

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents='こんにちは！挨拶を1文で返してください。'
        )
        print("レスポンス:", response.text)
        print("✅Gemini APIの接続に成功しました。")
    except Exception as e:
         print(f"❌Gemini APIの接続でエラーが発生しました。\n詳細: {e}")

if __name__ == '__main__':
    test_google_apis()
    test_gemini_api()
