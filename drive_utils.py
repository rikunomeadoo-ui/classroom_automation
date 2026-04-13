import os
from googleapiclient.http import MediaIoBaseDownload

def download_textbook_from_drive(drive_service, filename, dest_dir, folder_id=None):
    """
    Google Drive上で指定されたファイル名を検索し、
    見つかった場合は指定ディレクトリにダウンロードする。
    
    戻り値: (ダウンロードしたファイルのローカルパス, 成功したかどうかの真偽値)
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)
        
    dest_path = os.path.join(dest_dir, filename)
    
    # 既にローカルに存在する場合はスキップ
    if os.path.exists(dest_path):
        return dest_path, True
        
    try:
        # Driveからファイル名で検索
        # mimeType != 'application/vnd.google-apps.folder' でフォルダを除外
        query = f"name = '{filename}' and trashed = false and mimeType != 'application/vnd.google-apps.folder'"
        if folder_id:
            query += f" and '{folder_id}' in parents"
        
        results = drive_service.files().list(
            q=query,
            fields="nextPageToken, files(id, name)",
            spaces='drive'
        ).execute()
        
        items = results.get('files', [])
        
        if not items:
            print(f"⚠️ Google Driveに '{filename}' が見つかりませんでした。")
            return None, False
            
        # 同じ名前のファイルが複数ある場合は最初のものを取得
        file_id = items[0]['id']
        print(f"☁️ Google Driveから '{filename}' (ID: {file_id}) をダウンロード中...")
        
        request = drive_service.files().get_media(fileId=file_id)
        with open(dest_path, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                if status:
                    print(f"  - ダウンロード進捗: {int(status.progress() * 100)}%")
                    
        print(f"✅ ダウンロード完了: {dest_path}")
        return dest_path, True
        
    except Exception as e:
        print(f"❌ Google Driveからの '{filename}' のダウンロードに失敗しました: {e}")
        # 失敗した場合は中途半端なファイルを削除
        if os.path.exists(dest_path):
            try:
                os.remove(dest_path)
            except:
                pass
        return None, False
