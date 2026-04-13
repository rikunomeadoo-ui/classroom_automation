# 📚 授業自動通知システム

Google カレンダーの授業予定を自動で読み取り、授業開始前に生徒の Google Classroom へ **Meet リンクを自動投稿**するシステムです。

---

## 📋 目次

1. [このシステムでできること](#1-このシステムでできること)
2. [まず最初に：Antigravity を使えるようにする](#2-まず最初にantigravity-を使えるようにする)
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
- 📢 **Classroom へ自動投稿**：授業開始前（デフォルト1時間前）に Meet リンク付きのお知らせを予約投稿
- ⚙️ **柔軟な設定**：`.env` ファイルを編集するだけで投稿タイミング・担当者名・Meet URL を変更可能

---

## 2. まず最初に：Antigravity を使えるようにする

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

### 2-3. ログインする

1. 左サイドバーの Antigravity アイコンをクリック
2. 「**Sign in with Google**」をクリック → ブラウザが開く
3. Google アカウントでログイン

### 2-4. モデルを選ぶ

右下のモデル選択ボタンから変更できます。**迷ったら Claude Sonnet 4.6 を選んでください。**

| モデル名 | 特徴 |
|---------|------|
| **Claude Sonnet 4.6（おすすめ）** | 速い・賢い・コードが得意 |
| Claude Opus 4.6 | 最高精度。複雑な改造向け |
| Gemini 3.1 Pro | Googleモデル。 |

### 2-5. セットアッププロンプトを貼り付ける（重要！）

**`ANTIGRAVITY_PROMPT.md`** ファイルを開いて：

1. 「▼ ここからコピー ▼」〜「▲ ここまでコピー ▲」を**まるごとコピー**
2. Antigravity のチャット欄に貼り付けて送信

→ Antigravity が自動で「何分前に通知？」「MeetのURL？」「メッセージ文面は？」と聞いてきます。  
答えるだけでセットアップが進みます。

---

## 3. このシステムをダウンロードする

1. GitHub ページ上部の緑色「**Code**」ボタンをクリック
2. 「**Download ZIP**」をクリック
3. ダウンロードした ZIP をダブルクリックで解凍
4. 解凍されたフォルダをわかりやすい場所（例：デスクトップ・書類）に移動

---

## 4. Python をインストールする

Python はこのシステムが動く「エンジン」です。

### Mac

ターミナルを開いて（Spotlight で「ターミナル」と検索）実行：

```bash
# Homebrew をインストール
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python をインストール
brew install python3

# 確認
python3 --version
```

### Windows

1. [https://www.python.org/downloads/](https://www.python.org/downloads/) を開く
2. 「Download Python 3.x.x」をクリック
3. **⚠️「Add Python to PATH」に必ずチェック**を入れてインストール

コマンドプロンプトで確認：
```cmd
python --version
```

---

## 5. 必要なパッケージをインストールする

ダウンロードしたフォルダをターミナルで開きます。

> **フォルダをターミナルで開く方法**  
> - Mac：フォルダをターミナルウィンドウにドラッグ＆ドロップ  
> - Windows：フォルダを開いてアドレスバーに `cmd` と入力して Enter

### Mac

```bash
# 仮想環境を作成（初回のみ）
python3 -m venv venv

# 仮想環境を有効化
source venv/bin/activate

# パッケージをインストール
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv
```

### Windows

```cmd
:: 仮想環境を作成（初回のみ）
python -m venv venv

:: 仮想環境を有効化
venv\Scripts\activate

:: パッケージをインストール
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv
```

> 💡 エラーが出たら Antigravity にコピペして相談してください。

---

## 6. 設定ファイル（.env）を作る

`.env.example` をコピーして `.env` を作り、各項目を入力します。

### コピー方法

**Mac**  
```bash
cp .env.example .env
```

**Windows**  
```cmd
copy .env.example .env
```

> ⚠️ **`.env` は絶対に人に見せたり共有したりしないでください。** APIキーが入ります。

### 各設定項目の取得方法

#### `TARGET_CALENDAR_ID`（カレンダーID）
1. [Google カレンダー](https://calendar.google.com) を開く
2. 左サイドバーの対象カレンダーの「⋮」→「設定と共有」
3. 「**カレンダーの統合**」欄の「カレンダーID」をコピー

#### `MEET_URL`（Google Meet URL）
1. [meet.google.com](https://meet.google.com) →「新しいミーティング」→「後で使用するミーティングを作成」
2. 表示された URL をコピー

#### `TEACHER_NAME`・`NOTIFY_MINUTES_BEFORE`
Antigravity のセットアッププロンプトを使えば、答えるだけで設定方法を教えてもらえます。

---

## 7. Google Cloud の認証情報を取得する

GoogleカレンダーやClassroomにアクセスするための「許可証」を作ります。

1. [Google Cloud Console](https://console.cloud.google.com) を開く
2. 「**新しいプロジェクト**」で作成（例：`juku-automation`）
3. 「APIとサービス」→「ライブラリ」から以下を有効化：
   - `Google Calendar API`
   - `Google Classroom API`
4. 「**OAuth 同意画面**」→ User Type「外部」→ 作成  
   → アプリ名・メールを入力して「保存して次へ」を繰り返す  
   → 「テストユーザー」に自分のアドレスを追加
5. 「**認証情報**」→「OAuthクライアントID」→「デスクトップアプリ」で作成
6. 「**JSONをダウンロード**」→フォルダに移動して **`credentials.json`** に名前変更

---

## 8. 初回認証を行う

**Mac**
```bash
source venv/bin/activate
python3 auth.py
```

**Windows**
```cmd
venv\Scripts\activate
python auth.py
```

ブラウザが開いたら：
1. 塾の Google アカウントでログイン
2. 「このアプリは確認されていません」→「詳細」→「安全でないページへ移動」  
   ※自分で作ったアプリです
3. 「**許可**」をクリック

→ `token.json` が自動生成されます。次回以降は自動ログインされます。

---

## 9. 生徒の設定をする

> ⚠️ **重要：** `students/` フォルダ内の**フォルダ名**と、Googleカレンダーの**予定タイトルに含まれる名前**が一致している必要があります。  
> 例：フォルダ名 `田中 太郎` → カレンダー予定タイトル「田中 太郎 授業」

1. `students/サンプル生徒/` フォルダをコピーして、生徒名（例：`田中 太郎`）に変更
2. 中の `settings.json` を開いて `course_id` を書き換える

### `course_id` の調べ方

**Mac**  
```bash
source venv/bin/activate && python3 test_api.py
```

**Windows**  
```cmd
venv\Scripts\activate && python test_api.py
```

Classroom のコース一覧と ID が表示されるので、対応するものをコピーしてください。

### settings.json の中身

```json
{
    "course_id": "ここに調べたIDを貼り付け",
    "is_active": true
}
```

`"is_active": false` にすると一時停止できます。

---

## 10. 起動する

| OS | 方法 |
|----|------|
| **Mac** | `システムの起動.command` をダブルクリック |
| **Windows** | `システムの起動.bat` をダブルクリック（初回は自動でパッケージインストール） |

> **Mac で初回セキュリティ警告が出た場合：**  
> `システムの起動.command` を**右クリック** → 「開く」→「開く」

### 正常動作時の表示例

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

`.env` ファイルを編集するだけで変更できます。

| やりたいこと | 変数名 | 例 |
|------------|--------|----|
| 投稿者名を変える | `TEACHER_NAME` | `"山田 花子"` |
| 1時間前 → 30分前 | `NOTIFY_MINUTES_BEFORE` | `30` |
| 2時間前にしたい | `NOTIFY_MINUTES_BEFORE` | `120` |
| Meetのリンクを変える | `MEET_URL` | `"https://meet.google.com/xxx-xxxx-xxx"` |

メッセージ文面を変えたい場合は → Antigravity に「`main.py` のメッセージを〇〇に変えて」と伝えてください。

---

## 12. よくあるエラーと対処法

**❌ `ModuleNotFoundError`**  
→ ステップ5のインストールを再実行する

**❌ `FileNotFoundError: credentials.json`**  
→ Google Cloud からダウンロードしたファイルを `classroom_automation` フォルダ直下に `credentials.json` という名前で置く

**❌ `.envの設定が不足しています`**  
→ `.env` ファイルが作られていないか `TARGET_CALENDAR_ID` が未入力

**❌ `向こう1週間の授業予定が見つかりませんでした`**  
→ カレンダーの予定タイトルに生徒フォルダ名が含まれているか確認

> 💡 どんなエラーも Antigravity に貼れば解決策を教えてくれます。  
> **`ANTIGRAVITY_PROMPT.md` を最初に貼るのを忘れずに。**

---

*Python + Google Calendar API + Google Classroom API*
