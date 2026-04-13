import os
import fitz  # PyMuPDF
from PIL import Image
from dotenv import load_dotenv
from google import genai

# 環境変数の読み込み (.envファイル)
load_dotenv()

def extract_pdf_page_and_ocr(pdf_path, page_number):
    """
    指定されたPDFのページを画像化し、Gemini APIでLaTeX形式のテキストとして抽出する
    page_number: 1始まりのページ番号
    """
    print(f"=== PDFテキスト抽出テスト: {pdf_path} (P.{page_number}) ===")
    
    # --- 1. PDFから画像を切り出す ---
    try:
        doc = fitz.open(pdf_path)
        # ページインデックスは0始まり
        page_index = page_number - 1
        
        if page_index < 0 or page_index >= len(doc):
            print(f"エラー: ページ P.{page_number} が見つかりませんでした。(全 {len(doc)} ページ)")
            return
        
        page = doc.load_page(page_index)
        
        # 解像度を上げて画像化 (zoom x2)
        zoom = 2.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        # 一時保存用の画像ファイルパス
        img_temp_path = "temp_page.png"
        pix.save(img_temp_path)
        print(f"✅ 画像を抽出しました: {img_temp_path} (サイズ: {pix.width}x{pix.height})")
    except Exception as e:
        print(f"❌ PDFの読み込みまたは画像化でエラーが発生しました。\n詳細: {e}")
        return

    # --- 2. Gemini APIで画像を読み取る ---
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("❌ Gemini APIキーが設定されていません。")
        return

    try:
        print("🤖 Gemini APIに画像解析リクエストを送信中...")
        client = genai.Client(api_key=api_key)
        
        # PILで画像を開く
        img = Image.open(img_temp_path)
        
        # 抽出指示のプロンプト
        prompt = (
            "この画像は数学の参考書（問題集）の1ページです。"
            "画像内に含まれている「問題文」「数式」「（もしあれば）解答や解説」をすべて正確に文字起こしし、"
            "数式部分はインライン数式($...$)やブロック数式($$...$$)など、標準的なLaTeX形式で出力してください。"
            "不必要なレイアウト装飾（枠線や色など）の再現は不要で、純粋なテキストとLaTeXコードのみを出力してください。"
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, img]
        )
        
        result_text = response.text
        
        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(result_text)
            
        print("\n=== 抽出結果を result.txt に保存しました ===")
        print("✅ テスト完了（Classroomへの投稿処理は行っていません）")
        
    except Exception as e:
        print(f"❌ Gemini APIの解析処理でエラーが発生しました。\n詳細: {e}")
    finally:
        # 後片付け（一時画像の削除）
        if os.path.exists(img_temp_path):
            os.remove(img_temp_path)

if __name__ == "__main__":
    # テスト対象のPDFファイルとページ
    target_pdf = r"C:\Users\81702\Documents\塾講\松本 向史\数学1・A入門問題精講 _compressed.pdf"
    target_page = 20
    
    extract_pdf_page_and_ocr(target_pdf, target_page)
