import os
from auth import get_google_services
from drive_utils import download_textbook_from_drive
from dotenv import load_dotenv

load_dotenv()
_, _, drive_service, _ = get_google_services()
folder_id = os.environ.get('REFERENCE_BOOKS_FOLDER_ID')
dest = 'c:/Users/81702/Documents/塾講/classroom_automation/参考書'

filename = '数学1・A入門問題精講 _compressed.pdf'
p = os.path.join(dest, filename)

if os.path.exists(p):
    print(f"Renaming {filename} to .bak")
    os.rename(p, p + '.bak')

print('Downloading...')
path, success = download_textbook_from_drive(drive_service, filename, dest, folder_id)
print('Success:', success)

if os.path.exists(p):
    print('File downloaded exists!')
    os.remove(p)

if os.path.exists(p + '.bak'):
    print(f"Restoring {filename}")
    os.rename(p + '.bak', p)
