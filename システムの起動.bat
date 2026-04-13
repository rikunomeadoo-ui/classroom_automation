@echo off
chcp 65001 > nul
echo ===================================================
echo     Classroom Meetリンク自動予約システム
echo ===================================================
echo.
echo システムを起動しています...
echo.

cd /d "%~dp0"

if not exist venv\Scripts\activate.bat (
    echo [初回セットアップ] 仮想環境が見つかりません。自動で作成します...
    python -m venv venv
    if errorlevel 1 (
        echo エラー: Pythonが見つかりません。
        echo Pythonをインストールしてください: https://www.python.org/downloads/
        echo ※インストール時に「Add Python to PATH」にチェックを入れてください
        pause
        exit /b 1
    )
    call venv\Scripts\activate.bat
    echo 必要なパッケージをインストール中...
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv google-genai PyMuPDF Pillow
) else (
    call venv\Scripts\activate.bat
)

python main.py

echo.
echo 処理が完了しました。
pause
