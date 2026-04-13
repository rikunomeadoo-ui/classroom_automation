import os
import subprocess

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "template.tex")

def generate_pdf(content_text, output_dir, file_prefix, title):
    """
    指定されたテキストをテンプレートに埋め込み、output_dir内にコンパイルする。
    例: file_prefix="worksheet_q" -> worksheet_q.tex / worksheet_q.pdf
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    tex_path = os.path.join(output_dir, f"{file_prefix}.tex")
    dvi_path = os.path.join(output_dir, f"{file_prefix}.dvi")
    pdf_path = os.path.join(output_dir, f"{file_prefix}.pdf")
    
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template_content = f.read()
        
    # タイトルとコンテンツの置換
    template_content = template_content.replace("課題確認テスト", title)
    final_tex = template_content.replace("%---CONTENTS---%", content_text)
    
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(final_tex)
        
    print(f"[{file_prefix}] LaTeXファイルを生成しました: {tex_path}")
    
    # 元のディレクトリを記憶し、コンパイル先ディレクトリに移動
    original_cwd = os.getcwd()
    os.chdir(output_dir)
    
    try:
        print(f"[{file_prefix}] uplatex コンパイル中...")
        subprocess.run(["uplatex", "-interaction=nonstopmode", f"{file_prefix}.tex"], check=True, capture_output=True)
        
        print(f"[{file_prefix}] dvipdfmx PDF変換中...")
        subprocess.run(["dvipdfmx", f"{file_prefix}.dvi"], check=True, capture_output=True)
        
        print(f"✅ PDFを作成しました: {pdf_path}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ コンパイルエラー ({file_prefix}):\n{e.output.decode('utf-8', errors='ignore')}")
        return None
    finally:
        # 中間ファイルの削除 (容量節約)
        for ext in [".aux", ".log", ".dvi"]:
            temp_file = f"{file_prefix}{ext}"
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        # 元のディレクトリに戻る
        os.chdir(original_cwd)
        
    return pdf_path
