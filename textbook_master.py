# この辞書は、Google Drive上のファイル名と印字ページのオフセット（ズレ）を管理するマスターです。
# 生徒カルテのテキスト名に対して部分一致で検索を行い、もっとも適したものを返します。

TEXTBOOK_MASTER = {
    # 共通テスト系
    "〈きめる!共通テスト〉数学1･A _compressed.pdf": 4,
    "〈きめる!共通テスト〉数学2･B･C _compressed.pdf": 4,
    "きめる!共通テスト 数学Ⅰ･A 増補改訂版 迫田 昂輝,田井 智暁_compressed.pdf": 6,
    "きめる!共通テスト 数学Ⅱ･B･C 増補改訂版 迫田 昂輝,田井 智暁 (1)_compressed.pdf": 6,
    "2025共通テスト総合問題集 数学Ⅰ,数学A 河合塾_compressed.pdf": 4,
    "2025共通テスト総合問題集 数学Ⅱ,数学B,数学C 河合塾_compressed.pdf": 4,

    # 4STEP系
    "4STEP数学1+A 解答編.pdf": 2,
    "4STEP数学1+A.pdf": 4,
    "4STEP数学2+B 解答編.pdf": 2,
    "4STEP数学2+B+C.pdf": 4,
    "4STEP数学3+C 解答編_compressed.pdf": 2,
    "4STEP数学3+C.pdf": 4,

    # 重要問題集
    "2024 実戦 数学重要問題集 数学I・II・III・A・B・C 理系_compressed.pdf": 6,
    "2025 実戦 数学重要問題集 数学Ⅰ・Ⅱ・Ⅲ・A・B・C（理系） _compressed.pdf": 6,

    # Focus Gold
    "Focus Gold 数学Ⅰ+A 解答編_compressed.pdf": 2,
    "Focus Gold 数学Ⅰ+A_compressed.pdf": 2,
    "Focus Gold 数学Ⅱ+B+ベクトル 解答編_compressed.pdf": 2,
    "Focus Gold 数学Ⅱ+B+ベクトル_compressed.pdf": 4,
    "Focus Gold 数学Ⅲ+複素数平面 式と曲線 解答編_compressed.pdf": 2,
    "Focus Gold 数学Ⅲ+複素数平面 式と曲線_compressed.pdf": 4,

    # NEW ACTION LEGEND
    "NEW ACTION LEGEND 数学1+A ②(P599~)_compressed.pdf": 598,
    "NEW ACTION LEGEND 数学1+A-①(表紙~P598)_compressed.pdf": 4,
    "NEW ACTION LEGEND 数学2+B ②(P695~)_compressed.pdf": 694,
    "NEW ACTION LEGEND 数学2+B②(表紙~P694)_compressed.pdf": 4,
    "NEW ACTION LEGEND 数学3_compressed.pdf": 4,
    "New action legend数学C _ 思考と戦略 _compressed.pdf": 4,

    # チャート式系
    "チャート式 解法と演習数学 I+A_compressed.pdf": 6,  # 黄チャート
    "チャート式 解法と演習数学 II+B_compressed.pdf": 6,
    "チャート式 解法と演習数学 III+C ①(表紙~P574)_compressed.pdf": 6,
    "チャート式 解法と演習数学 III+C ②(P575~)_compressed.pdf": 574,
    
    "チャート式 基礎からの数学 I+A ①(表紙~P562)_compressed.pdf": 6, # 青チャート
    "チャート式 基礎からの数学 I+A ②(P564~)_compressed.pdf": 563,
    "チャート式 基礎からの数学 II+B(~P553)_compressed.pdf": 8,
    "チャート式 基礎からの数学 II+B（P554~）_compressed.pdf": 553,
    "チャート式 基礎からの数学 III+C(P687~)_compressed.pdf": 686,
    "チャート式 基礎からの数学 III+C(表紙~P686)_compressed.pdf": 6,
    
    "チャート式 数学 I+A (2)_compressed.pdf": 6,    # その他のチャート
    "チャート式 数学 II+B_compressed.pdf": 6,
    "チャート式 数学 III+C ①(表紙~P566)_compressed.pdf": 6,
    "チャート式 数学 III+C ②(P567~)_compressed.pdf": 566,

    # よくわかる高校数学
    "よくわかる高校数学 I・A (1)_compressed.pdf": 6,
    "よくわかる高校数学 II・B (1)_compressed.pdf": 6,
    "よくわかる高校数学 III・C_compressed.pdf": 6,

    # 合格るシリーズ
    "合格る確率+場合の数 広瀬 和之_compressed.pdf": 4,
    "合格る計算 数学Ⅰ・Ａ・Ⅱ・Ｂ［数列］・Ｃ［ベクトル］ 広瀬 和之_compressed.pdf": 4,
    "合格る計算 数学Ⅲ･C[複素数平面･2次曲線] 広瀬 和之_compressed.pdf": 4,

    # 問題精講シリーズ
    "数学1・A入門問題精講 _compressed.pdf": 6,
    "数学1・A基礎問題精講 _compressed.pdf": 6,
    "数学1・A標準問題精講 _compressed.pdf": 4,
    
    "数学Ⅱ・B＋ベクトル 基礎問題精講 (1)_compressed.pdf": 6,
    "数学Ⅱ・B＋ベクトル 標準問題精講_compressed.pdf": 4,
    
    "数学Ⅲ・C 入門問題精講_compressed.pdf": 6,
    "数学Ⅲ・C 標準問題精講_compressed.pdf": 4,
    
    "数学Ⅰ＋A＋Ⅱ＋B＋ベクトル 上級問題精講_compressed.pdf": 4,
    "数学Ⅲ＋C 上級問題精講_compressed.pdf": 4,

    # その他
    "数学III 重要事項完全習得編_compressed.pdf": 6,
    "数学III・Ｃ　重要事項完全習得編　改訂版 堀尾　豊孝,石部　拓也,影平　俊郎_compressed.pdf": 4,
    "文系の数学. 重要事項完全習得編 _compressed.pdf": 4,
    "大学への数学 1対1対応の演習 数学A.pdf": 4,
    "大学への数学 1対1対応の演習 数学B.pdf": 4,
    "大学への数学 1対1対応の演習 数学Ⅲ.pdf のコピー": 4,
    "文系数学入試の核心.pdf のコピー": 6,
    "理系数学 入試の核心 標準編_compressed.pdf": 6,
    "理系数学の良問プラチカ _ 数学3・C .pdf": 6,
    "理系数学入試の核心 難関大編 .pdf": 4
}

def find_textbook_info(text_name):
    """
    カルテのテキスト名 (例: "数学1・A入門問題精講") から
    辞書を部分一致で検索して、一番マッチしそうな
    (ファイル名, オフセット) を返す。
    見つからなければ (None, 0) を返す。
    """
    if not text_name:
        return None, 0
        
    def normalize_text(t):
        # スペース、全角スペース、アンダースコア等を削除し小文字化
        # さらにローマ数字や数字の表記揺れをある程度吸収する
        t = t.replace(' ', '').replace('　', '').replace('_', '').lower()
        t = t.replace('ⅰ', 'i').replace('ⅱ', 'ii').replace('ⅲ', 'iii')
        t = t.replace('1', 'i').replace('2', 'ii').replace('3', 'iii')
        t = t.replace('＋', '+').replace('・', '')
        return t

    text_clean = normalize_text(text_name)
    
    # 解答編かどうかを判定
    is_answer_book = '解答' in text_name
    
    # 1. 完全一致を先に探す
    for file_name, offset in TEXTBOOK_MASTER.items():
        if text_name == file_name:
            return file_name, offset
            
    # 2. 部分一致（マスタのファイル名の中に、探したいテキスト名が含まれているか）
    for file_name, offset in TEXTBOOK_MASTER.items():
        is_file_answer_book = '解答' in file_name
        if is_answer_book != is_file_answer_book:
            continue
            
        fn_clean = normalize_text(file_name.replace('compressed', '').replace('.pdf', ''))
        if text_clean in fn_clean:
            return file_name, offset
            
    # 3. 逆に、探したいテキスト名の中に、マスタのファイル名が含まれているか
    for file_name, offset in TEXTBOOK_MASTER.items():
        is_file_answer_book = '解答' in file_name
        if is_answer_book != is_file_answer_book:
            continue
            
        fn_clean = normalize_text(file_name.replace('compressed', '').replace('.pdf', ''))
        if fn_clean in text_clean:
            return file_name, offset
            
    # どこにも引っかからなかった場合
    return None, 0
