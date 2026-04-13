#!/bin/bash
echo "==================================================="
echo "    Classroom Meetリンク自動予約システム"
echo "==================================================="
echo ""
echo "システムを起動しています..."
echo ""

cd "$(dirname "$0")"
source venv/bin/activate
python3 main.py

echo ""
echo "処理が完了しました。"
read -n 1 -s -r -p "何かキーを押して終了してください..."
