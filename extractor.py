import os
import fitz  # PyMuPDF
from PIL import Image
from google import genai
import time

def extract_content_with_gemini(pdf_path, start_page, end_page, extract_condition, api_key, page_offset=0):
    """
    指定ページ範囲のPDFを画像化し、Geminiに条件付きで解析させる。
    戻り値: (問題文のLaTeX文字列, 解答のLaTeX文字列)
    """
    print(f"--- PDF抽出処理開始: {pdf_path} (PDF: P.{start_page}〜{end_page}, 印字: P.{start_page - page_offset}〜{end_page - page_offset}) ---")
    
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"❌ PDFの読み込みに失敗しました: {e}")
        return None, None

    images = []
    # ページインデックスは0始まり
    for p_num in range(start_page, end_page + 1):
        idx = p_num - 1
        if idx < 0 or idx >= len(doc):
            print(f"⚠️ ページ {p_num} がスキップされました（範囲外）")
            continue
            
        page = doc.load_page(idx)
        zoom = 2.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        img_temp = f"temp_page_{p_num}.png"
        pix.save(img_temp)
        images.append((p_num, img_temp, Image.open(img_temp)))

    if not images:
        print("❌ 抽出対象の画像がありませんでした。")
        return None, None

    print(f"🤖 Gemini APIに解析リクエストを送信中... (条件: {extract_condition})")
    
    # 対象の印字ページ範囲を計算
    printed_start = start_page - page_offset
    printed_end = end_page - page_offset
    
    # 問題用のプロンプト
    prompt_q = (
        f"これらの画像は数学の参考書（印字ページ番号: P.{printed_start} 〜 P.{printed_end}）です。以下の条件に従って『問題文のみ』を抽出してください。\n"
        f"【抽出条件】: {extract_condition}\n"
        "【出力形式と厳密な制約】:\n"
        "1. 各問題を必ず \\begin{problembox} と \\end{problembox} の中に記述してください。\n"
        "2. 問題文の先頭には、必ず `\\textcolor{probblue}{\\textbf{第O問}}` のように通し番号を記載し、その直後に必ず改行（`\\\\`）または全角スペースを入れてから問題の文章を開始してください。\n"
        "3. **重要**: 生徒向けのテスト用紙を作成するため、問題文に「P.XX」のような出典ページ番号は【絶対に記載しないでください】。\n"
        "4. 問題文内に(1)(2)(3)などの小問がある場合は、インラインで繋げるのではなく、改行や \\begin{enumerate} 等を用いて縦に見やすく並べてください。画像にある小問は【絶対に１つも省略せずに】すべて出力してください。\n"
        "5. 数式はLaTeX形式($...$ や $$...$$)として正しく記述してください。\n"
        "   - **注意**: 循環小数（上に・がつく小数）は、必ず `0.\\dot{1}\\dot{2}` のように `\\dot{}` を用いて表現してください。\n"
        "   - **重要**: 極限(`\\lim`)、シグマ(`\\sum`)、積分(`\\int`)、分数(`\\frac`)をインライン数式(`$...$`)で用いる場合は、必ず `$\\displaystyle ...$` のように先頭に `\\displaystyle` をつけて見やすく出力してください。\n"
        "6. **重要**: AIとしての前置きや案内文は【一切出力しないでください】。\n"
        "7. **重要**: Markdown形式の強調記号（** や *）は【一切使用禁止】です。\n"
        "8. 解答や解説が含まれている場合、それらは出力から除外してください。"
    )
    
    client = genai.Client(api_key=api_key)
    
    try:
        # 1. まず問題を抽出
        contents_q = [prompt_q]
        for p_num, _, img in images:
            printed_p_num = p_num - page_offset
            contents_q.append(f"【参考書 {printed_p_num} ページ目 (実際のPDFは {p_num} ページ目) の画像】")
            contents_q.append(img)
            
        for attempt in range(5):
            try:
                res_q = client.models.generate_content(model='gemini-2.5-flash', contents=contents_q)
                break
            except Exception as e:
                err_str = str(e).lower()
                if '429' in err_str or 'exhausted' in err_str or 'quota' in err_str:
                    if attempt < 4:
                        wait_time = 15 * (attempt + 1)
                        print(f"⚠️ API制限(問題抽出) -> {wait_time}秒待機してリトライします... ({attempt+1}/5)")
                        time.sleep(wait_time)
                        continue
                raise e
                
        text_q = res_q.text.replace("```latex", "").replace("```", "").strip()
        
        # 2. 抽出された問題をベースに解答生成を指示 (独立抽出によるズレを防止)
        prompt_a = (
            f"以下の【抽出された問題文】に対応する、問題と『詳しい解答・計算過程』のセットをLaTeX形式で作成してください。\n"
            "※対象のPDF画像の中に解答があればそれを参考にし、なければあなた自身の推論で正しい解答を生成してください。\n"
            f"【抽出された問題文】:\n{text_q}\n\n"
            "【出力形式と厳密な制約】:\n"
            "1. 必ず、各問題につき【問題テキストのボックス】と【解答テキストのボックス】をセットで出力してください。\n"
            "   - 小問が複数(1)(2)(3)...と存在する場合は、【必ずすべての小問に対する解答・解説を作成】してください。(3)以降の解答が欠落するなどの途中省略は絶対に許されません。\n"
            "2. まず、問題文全体を `\\begin{problembox}` ... `\\end{problembox}` の中に出力してください。このとき、問題文の先頭に `\\textcolor{probblue}{\\textbf{第O問 (対象ファイル P.XX)}}` と対象ページを記載し、直後に改行(`\\\\`)または全角スペースを入れてから問題文を開始してください。\n"
            "3. 続けて、対応する解答を `\\begin{answerbox}` ... `\\end{answerbox}` の中に出力してください。\n"
            "4. 解答の先頭には、必ず `\\textcolor{ansgreen}{\\textbf{【着眼点と解答】}}` と記載してください。\n"
            "5. **最重要**: 数式の計算過程は、必ず `\\begin{mathexplain}` と `\\end{mathexplain}` 環境を用いて、【左側に数式、右側に式の解説行】という2カラム形式で記述してください。\n"
            "   - 書式: `\\step{左側の数式（必ず $...$ 等で囲む）}{右側の解説テキスト}`\n"
            "   - 例: `\\begin{mathexplain} \\step{$x^2 - 4 = 0$}{} \\step{$(x-2)(x+2)=0$}{左辺を因数分解する} \\step{$x=2, -2$}{} \\end{mathexplain}`\n"
            "   - 小問ごとに `\\textbf{(1)}` などの見出しをつけてから `\\begin{mathexplain}` を開始すると見やすいです。\n"
            "6. 最終的な答えだけでなく、途中の式変形や解説（あれば）を上記の `\\step` の第2引数に記述してください。第1引数には日本語のテキストを含めないでください。\n"
            "7. **注意**: 循環小数（上に・がつく小数）は、必ず `0.\\dot{1}\\dot{2}` のように `\\dot{}` を用いて表記してください。\n"
            "8. **重要**: 極限(`\\lim`)、シグマ(`\\sum`)、積分(`\\int`)、分数(`\\frac`)をインライン数式(`$...$`)で用いる場合は、必ず `$\\displaystyle ...$` のように先頭に `\\displaystyle` をつけて見やすく出力してください。\n"
            "9. **重要**: AIとしての前置きや案内文、およびMarkdown記法(**や*)は【一切使用禁止】です。"
        )
        
        # 解答の生成 (画像と新しいプロンプトを渡す)
        contents_a = [prompt_a]
        for p_num, _, img in images:
            printed_p_num = p_num - page_offset
            contents_a.append(f"【参考書 {printed_p_num} ページ目 (実際のPDFは {p_num} ページ目) の画像】")
            contents_a.append(img)
            
        for attempt in range(5):
            try:
                res_a = client.models.generate_content(model='gemini-2.5-flash', contents=contents_a)
                break
            except Exception as e:
                err_str = str(e).lower()
                if '429' in err_str or 'exhausted' in err_str or 'quota' in err_str:
                    if attempt < 4:
                        wait_time = 15 * (attempt + 1)
                        print(f"⚠️ API制限(解答生成) -> {wait_time}秒待機してリトライします... ({attempt+1}/5)")
                        time.sleep(wait_time)
                        continue
                raise e
                
        text_a = res_a.text.replace("```latex", "").replace("```", "").strip()
        
        # 不要になった一時画像を削除
        for _, img_path, _ in images:
            if os.path.exists(img_path):
                os.remove(img_path)
                
        # コードブロックの表記揺れを除去
        text_q = res_q.text.replace("```latex", "").replace("```", "").strip()
        text_a = res_a.text.replace("```latex", "").replace("```", "").strip()
        
        print("✅ 問題と解答の抽出に成功しました！")
        return text_q, text_a

    except Exception as e:
        print(f"❌ Gemini APIの解析処理でエラーが発生しました。\n詳細: {e}")
        for _, img_path, _ in images:
            if os.path.exists(img_path):
                os.remove(img_path)
        return None, None
