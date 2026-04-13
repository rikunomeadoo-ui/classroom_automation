import os
import datetime
from auth import get_google_services
from main import get_homework_range_from_sheet

def test_fetch():
    print("=== スプレッドシートからの動的取得テスト ===")
    calendar_service, classroom_service, drive_service, sheets_service = get_google_services()
    
    spreadsheet_id = "1E7rHtMFTX3oVdw9BkI7dQGxMUQomderAYRR0gatlpKg"
    sheet_name = "2年・3月"
    subject = "数学"
    text_name = "数学1・A入門問題精講"
    
    print(f"対象シート: {sheet_name}")
    try:
        for week in range(1, 4):
            start, end = get_homework_range_from_sheet(sheets_service, spreadsheet_id, sheet_name, subject, text_name, week)
            print(f"-> 第 {week} 週の取得結果: 開始ページ {start}, 終了ページ {end}")
    except Exception as e:
        print("エラー:", e)

if __name__ == "__main__":
    test_fetch()
