import os
import subprocess
import shutil

# 定数：生成するファイル名（固定にして毎回上書きし、容量を節約する）
TEMP_TEX_FILE = "temp_worksheet.tex"
TEMP_DVI_FILE = "temp_worksheet.dvi"
TEMP_PDF_FILE = "temp_worksheet.pdf"
TEMPLATE_PATH = os.path.join("templates", "template.tex")

def generate_pdf_from_text(extracted_text, custom_title="確認テスト"):
    """
    抽出されたLaTeXテキストをテンプレートに埋め込み、PDF化する。
    毎回同じファイル名で上書きするため、ディスク容量を圧迫しない。
    """
    print("=== LaTeX PDF生成プロセス ===")
    
    # 1. テンプレートの読み込み
    if not os.path.exists(TEMPLATE_PATH):
        print(f"❌ テンプレートファイルが見つかりません: {TEMPLATE_PATH}")
        return False
        
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template_content = f.read()
        
    # 2. テキストの埋め込み (さらにタイトルも置換できる仕組みにしておく)
    template_content = template_content.replace("確認テスト", custom_title)
    
    # Geminiの出力にはMarkdownのコードブロック(```latex ... ```)が付くことがあるので除去
    clean_text = extracted_text.replace("```latex", "").replace("```", "").strip()
    
    final_tex = template_content.replace("%---CONTENTS---%", clean_text)
    
    # 3. .texファイルの上書き保存
    with open(TEMP_TEX_FILE, "w", encoding="utf-8") as f:
        f.write(final_tex)
    print(f"✅ {TEMP_TEX_FILE} を作成・上書きしました。")
    
    # 4. コンパイル (uplatex -> dvipdfmx)
    try:
        print(">> uplatex コンパイル中...")
        subprocess.run(["uplatex", "-interaction=nonstopmode", TEMP_TEX_FILE], check=True, capture_output=True)
        
        print(">> dvipdfmx PDF変換中...")
        subprocess.run(["dvipdfmx", TEMP_DVI_FILE], check=True, capture_output=True)
        print(f"✅ PDFの生成に成功しました: {TEMP_PDF_FILE}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ コンパイル中にエラーが発生しました。\nログ:\n{e.output.decode('utf-8', errors='ignore')}")
        return False
    finally:
        # 中間ファイルのクリーンアップ (.aux, .log, .dvi など)
        for ext in [".aux", ".log", ".dvi"]:
            temp_file = TEMP_TEX_FILE.replace(".tex", ext)
            if os.path.exists(temp_file):
                os.remove(temp_file)
        print("✅ 不要な中間ファイルを削除しました（PC容量の節約）。")
        
    return True

if __name__ == "__main__":
    # extract_test.pyで保存した result.txt を読み込んでテストする
    if os.path.exists("result.txt"):
        with open("result.txt", "r", encoding="utf-8") as f:
            text = f.read()
        generate_pdf_from_text(text, "数学1・A 第1章")
    else:
        print("result.txt が見つかりません。先に extract_test.py を実行してください。")
