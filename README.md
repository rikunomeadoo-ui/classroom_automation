# 📚 授業自動通知システム

Google カレンダーの授業予定を自動で読み取り、授業開始前に生徒の Google Classroom へ **Meet リンクを自動投稿**するシステムです。

---

## 📋 目次

1. [このシステムでできること](#1-このシステムでできること)
2. [まず最初にやること：Antigravity を使えるようにする](#2-まず最初にやることantigravity-を使えるようにする)
3. [このシステムをダウンロードする](#3-このシステムをダウンロードする)
4. [Python をインストールする](#4-python-をインストールする)
5. [必要なパッケージをインストールする](#5-必要なパッケージをインストールする)
6. [設定ファイル（.env）を作る](#6-設定ファイルenvを作る)
7. [Google Cloud の認証情報を取得する](#7-google-cloud-の認証情報を取得する)
8. [初回認証を行う](#8-初回認証を行う)
9. [生徒の設定をする](#9-生徒の設定をする)
10. [起動する](#10-起動する)
11. [設定のカスタマイズ早見表](#11-設定のカスタマイズ早見表)
12. [よくあるエラーと対処法](#12-よくあるエラーと対処法)

---

## 1. このシステムでできること

- 📅 **カレンダーから自動取得**：向こう1週間の生徒の授業予定を自動で読み取る
- 📢 **自動投稿**：授業開始前（デフォルト1時間前）に Google Classroom へ Meet リンク付きのお知らせを投稿
- ⚙️ **柔軟な設定**：投稿タイミング・担当者名・メッセージ内容をカスタマイズ可能
- 🤖 **AI拡張**：Gemini AI で参考書 PDF から問題・解答を自動抽出（オプション機能）

---

## 2. まず最初にやること：Antigravity を使えるようにする

> **Antigravity とは？**  
> AI がコードや設定を代わりにやってくれるツールです。  
> 「エラーが出た」「メッセージを変えたい」など、**日本語で話しかけるだけ**で解決してくれます。

### 2-1. VS Code をインストールする

| OS | ダウンロード先 | インストール方法 |
|----|--------------|----------------|
| **Mac** | [code.visualstudio.com](https://code.visualstudio.com) →「Download for Mac」| ダウンロードしたファイルを Applications フォルダへドラッグ |
| **Windows** | [code.visualstudio.com](https://code.visualstudio.com) →「Download for Windows」| インストーラーを実行（すべてデフォルトでOK） |

### 2-2. Antigravity をインストールする

1. VS Code を起動する
2. 左サイドバーの「Extensions（四角が4つのアイコン）」をクリック
3. 検索欄に `Antigravity` と入力
4. 「Antigravity」をクリックして「**Install**」を押す
5. 左サイドバーに Antigravity のアイコンが追加される

### 2-3. ログインする

1. Antigravity のアイコンをクリック
2. 「**Sign in with Google**」をクリック → ブラウザが開く
3. Google アカウントでログイン

### 2-4. セットアッププロンプトを貼り付ける（最重要！）

このリポジトリに **`ANTIGRAVITY_PROMPT.md`** というファイルがあります。

1. そのファイルを開く
2. 「▼ ここからコピー ▼」〜「▲ ここまでコピー ▲」の間をすべてコピー
3. Antigravity のチャット欄に貼り付ける
4. その直後に「やりたいこと」を一言で書いて送信

これで Antigravity がこのシステムのことを全部理解した状態で会話できます。

---

## 3. このシステムをダウンロードする

### 方法 A：ZIP でダウンロード（簡単・おすすめ）

1. GitHub のページ上部にある緑色の「**Code**」ボタンをクリック
2. 「**Download ZIP**」をクリック
3. ダウンロードした ZIP ファイルをダブルクリックで解凍
4. 解凍されたフォルダを、わかりやすい場所（例：デスクトップ・書類フォルダ）に移動

### 方法 B：Git でクローン（ターミナルが使える場合）

```bash
git clone https://github.com/[USERNAME]/classroom_automation.git
```

---

## 4. Python をインストールする

Python はこのシステムが動く「エンジン」です。

### Mac の場合

**ターミナルの開き方**：Spotlight（⌘+スペース）→「ターミナル」と入力 → Enter

```bash
# Homebrew（Macのパッケージ管理ツール）をインストール
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python をインストール
brew install python3
```

確認：
```bash
python3 --version
# → Python 3.xx.x と表示されればOK
```

### Windows の場合

**コマンドプロンプトの開き方**：スタートボタン右クリック →「ターミナル」または「コマンドプロンプト」

1. [https://www.python.org/downloads/](https://www.python.org/downloads/) を開く
2. 「**Download Python 3.xx.x**」をクリック
3. インストーラーを実行
4. ⚠️ **「Add Python to PATH」に必ずチェックを入れる**
5. 「Install Now」をクリック

確認：
```cmd
python --version
# → Python 3.xx.x と表示されればOK
```

---

## 5. 必要なパッケージをインストールする

ダウンロードしたフォルダをターミナル（またはコマンドプロンプト）で開きます。

**フォルダへの移動方法：**
- Mac：ターミナルにフォルダをドラッグ＆ドロップすると自動でパスが入力される  
- Windows：フォルダを開いてアドレスバーに `cmd` と入力して Enter

### Mac

```bash
# 仮想環境を作成（初回のみ）
python3 -m venv venv

# 仮想環境を有効化
source venv/bin/activate

# パッケージをインストール
pip install google-auth google-auth-oauthlib google-auth-httplib2 \
            google-api-python-client python-dotenv google-genai PyMuPDF Pillow
```

### Windows

```cmd
:: 仮想環境を作成（初回のみ）
python -m venv venv

:: 仮想環境を有効化
venv\Scripts\activate

:: パッケージをインストール
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv google-genai PyMuPDF Pillow
```

> 💡 **エラーが出たら：** エラーをコピーして Antigravity に貼り付け「どうすればいいですか？」と聞けば OK

---

## 6. 設定ファイル（.env）を作る

`.env.example` をコピーして `.env` を作ります。

### Mac
```bash
cp .env.example .env
```

### Windows
```cmd
copy .env.example .env
```

作成した `.env` ファイルをテキストエディタで開いて、各項目を埋めていきます。

### 各設定項目の取得方法

#### `GEMINI_API_KEY`（Gemini APIキー）
1. [https://aistudio.google.com](https://aistudio.google.com) を開く
2. 「**Get API key**」→「**Create API key**」をクリック
3. 表示されたキーをコピーして貼り付ける

#### `TARGET_CALENDAR_ID`（カレンダーID）
1. [https://calendar.google.com](https://calendar.google.com) を開く
2. 左サイドバーの対象カレンダーの「⋮」→「設定と共有」
3. 下にスクロール→「**カレンダーの統合**」欄の「カレンダーID」をコピー

#### `MEET_URL`（Google MeetのURL）
1. [https://meet.google.com](https://meet.google.com) を開く
2. 「新しいミーティング」→「**後で使用するミーティングを作成**」
3. 表示された URL をコピー

#### `TEACHER_NAME`（担当者名）
Classroom に投稿されるメッセージに使われる名前を入力します。  
例：`TEACHER_NAME="山田 花子"`

#### `NOTIFY_MINUTES_BEFORE`（投稿タイミング）
授業開始の何分前に投稿するかを数字で入力します。  
例：`NOTIFY_MINUTES_BEFORE=60`（1時間前）、`NOTIFY_MINUTES_BEFORE=30`（30分前）

---

## 7. Google Cloud の認証情報を取得する

Googleカレンダー・Classroomにアクセスする「許可証」を作ります。

1. [https://console.cloud.google.com](https://console.cloud.google.com) を開く
2. 上部「プロジェクト選択」→「**新しいプロジェクト**」→ 好きな名前で作成（例：`juku-automation`）
3. 左メニュー「**APIとサービス**」→「**ライブラリ**」
4. 以下を1つずつ検索して「**有効にする**」：
   - `Google Calendar API`
   - `Google Classroom API`
   - `Google Drive API`
5. 「**APIとサービス**」→「**OAuth 同意画面**」
   - User Type：「**外部**」→「作成」
   - アプリ名（例：塾自動化）とメールを入力→「保存して次へ」を繰り返す
   - 「**テストユーザー**」に自分の Google アドレスを追加
6. 「**APIとサービス**」→「**認証情報**」→「**認証情報を作成**」→「**OAuthクライアントID**」
7. アプリケーションの種類：「**デスクトップアプリ**」→「作成」
8. 「**JSONをダウンロード**」をクリック
9. ダウンロードしたファイルを `classroom_automation` フォルダに移動して **`credentials.json`** に名前変更

---

## 8. 初回認証を行う

初回だけ必要な手順です。ブラウザが自動で開きます。

### Mac
```bash
source venv/bin/activate
python3 auth.py
```

### Windows
```cmd
venv\Scripts\activate
python auth.py
```

**ブラウザで：**
1. 塾の Google アカウントでログイン
2. 「このアプリは確認されていません」→「詳細」→「（アプリ名）に移動」をクリック  
   ※自分で作ったアプリなので安全です
3. 「**許可**」をクリック

成功すると `token.json` が自動生成されます。次回以降は自動ログインされます。

---

## 9. 生徒の設定をする

`students/` フォルダに生徒ごとのフォルダを作り、`settings.json` を置きます。

> ⚠️ **フォルダ名 = Googleカレンダーの予定タイトルに含まれる名前**  
> 例：予定タイトルが「田中 太郎 授業」なら、フォルダ名を `田中 太郎` にする

### 手順

1. `students/サンプル生徒/` フォルダをコピーして生徒名に変更
2. 中の `settings.json` を開いて `course_id` を書き換える

### `course_id` の調べ方

**Mac**  
```bash
source venv/bin/activate
python3 test_api.py
```

**Windows**  
```cmd
venv\Scripts\activate
python test_api.py
```

Classroom にあるコース一覧と ID が表示されます。対応する ID をコピーしてください。

### settings.json の中身

```json
{
    "course_id": "ここに上で調べたIDを貼り付け",
    "grade_prefix": "2年",
    "is_active": true
}
```

`"is_active": false` にすると、その生徒への投稿を一時停止できます。

---

## 10. 起動する

### Mac：`システムの起動.command` をダブルクリック

初回はセキュリティ確認が出ます：  
`システムの起動.command` を**右クリック**→「**開く**」→「**開く**」をクリック

### Windows：`システムの起動.bat` をダブルクリック

初回は自動でパッケージのインストールも行います（少し時間がかかります）。

### 正常に動いている場合の表示例

```
=== Classroom Meetリンク自動予約システム ===
✅ Google APIの認証に成功しました。

👨‍🎓 生徒: 田中 太郎 の処理を開始します。

📅 授業日時: 2026-04-15 18:00
🏫 Classroomへ予約投稿を設定中...
  - お知らせ（Meetリンク込み）を 17:00 に予約しました

🎉 04/15 分の予約投稿が完了しました！
```

---

## 11. 設定のカスタマイズ早見表

`.env` ファイルを編集するだけでカスタマイズできます。

| やりたいこと | 設定する変数 | 例 |
|------------|------------|-----|
| 投稿者名を変える | `TEACHER_NAME` | `"山田 花子"` |
| 投稿を30分前にする | `NOTIFY_MINUTES_BEFORE` | `30` |
| 投稿を2時間前にする | `NOTIFY_MINUTES_BEFORE` | `120` |
| Meetリンクを変える | `MEET_URL` | `"https://meet.google.com/xxx-xxxx-xxx"` |
| メッセージ文面を変える | → Antigravity に「メッセージを〇〇に変えて」と言う | - |

---

## 12. よくあるエラーと対処法

**❌ `ModuleNotFoundError: No module named 'xxx'`**  
→ パッケージが足りていません  
→ Mac: `pip install ...` / Windows: `pip install ...`（ステップ5参照）

**❌ `FileNotFoundError: credentials.json`**  
→ Google Cloud からダウンロードしたファイルが正しい場所にありません  
→ `classroom_automation` フォルダ直下に `credentials.json` という名前で置く

**❌ `.envの設定が不足しています`**  
→ `.env` ファイルが作られていないか、`TARGET_CALENDAR_ID` が未設定です  
→ ステップ6を確認する

**❌ 認証ブラウザが開かない**  
→ Mac: `python3 auth.py` / Windows: `python auth.py` を直接実行

**❌ `向こう1週間の授業予定が見つかりませんでした`**  
→ カレンダーの予定タイトルに生徒のフォルダ名が含まれているか確認  
→ フォルダ名：`田中 太郎` / 予定タイトル：`田中 太郎 授業` ← OK

> 💡 **どんなエラーも Antigravity に貼り付ければ解決策を教えてくれます。**  
> `ANTIGRAVITY_PROMPT.md` を最初に貼り付けるのを忘れずに！

---

*Python + Google APIs + Gemini API で構築*
