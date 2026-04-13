import os
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 指定するスコープ（カレンダーの読み取り、Classroomの読み書き、Driveの読み書き、Driveファイルの読み取り）
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/classroom.courses',
    'https://www.googleapis.com/auth/classroom.announcements',
    'https://www.googleapis.com/auth/classroom.coursework.students',
    'https://www.googleapis.com/auth/classroom.topics'
]

def get_google_services():
    """
    Google Calendar, Classroom, DriveのAPIサービスクライアントを返す
    初回はブラウザで認証画面が開きます。
    """
    creds = None
    # 以前の認証情報があるかチェック
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # 認証情報がないか、期限切れの場合
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        # 次回用に保存
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # 各サービスを構築して返す
    calendar_service = build('calendar', 'v3', credentials=creds)
    classroom_service = build('classroom', 'v1', credentials=creds)
    
    return calendar_service, classroom_service

if __name__ == '__main__':
    # 単独実行時は認証のみ行う
    print("Google APIの認証を開始します...")
    get_google_services()
    print("認証に成功しました！ token.json が生成されています。")
