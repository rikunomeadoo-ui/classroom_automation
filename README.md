# 📚 授業自動通知システム セットアップガイド

**このシステムでできること：**
- Googleカレンダーの授業予定を自動で読み取り、授業開始前に生徒のGoogle Classroomへ自動でMeetリンクを投稿する

---

## 📋 目次

1. [必要なもの（事前準備）](#1-必要なもの事前準備)
2. [ステップ1：Antigravity（AI）を使えるようにする](#ステップ1antigravityaiを使えるようにする)
3. [ステップ2：このシステムをダウンロードする（GitHub）](#ステップ2このシステムをダウンロードするgithub)
4. [ステップ3：Pythonの環境を構築する](#ステップ3pythonの環境を構築する)
5. [ステップ4：APIキーを取得・設定する](#ステップ4apiキーを取得設定する)
6. [ステップ5：Google認証を行う](#ステップ5google認証を行う)
7. [ステップ6：生徒の設定をする](#ステップ6生徒の設定をする)
8. [ステップ7：実際に動かす](#ステップ7実際に動かす)
9. [設定のカスタマイズ（投稿タイミング・担当者名など）](#設定のカスタマイズ)
10. [よくあるエラーと対処法](#よくあるエラーと対処法)
11. [Antigravityに何を任せるか](#antigravityに何を任せるか)

---

## 1. 必要なもの（事前準備）

- **Mac** （このガイドはMac向けです）
- **Googleアカウント**（塾の法人アカウントが望ましい）
- **Google Classroom** で生徒のクラスが作成済みであること
- **Googleカレンダー** で生徒の授業予定が登録済みであること
- **Antigravity** （AIコーディングアシスタント）※インストール手順は次のステップで説明

---

## ステップ1：Antigravity（AI）を使えるようにする

AntigravityはAIがあなたの代わりにコードを書いてくれるツールです。  
一度設定すれば、このシステムの使い方や改造についてAIに日本語で質問できます。

### 1-1. VS Code（コードエディタ）をインストールする

1. [https://code.visualstudio.com](https://code.visualstudio.com) を開く
2. 「Download for Mac」ボタンをクリック
3. ダウンロードしたファイルをApplicationsフォルダへドラッグ＆ドロップ
4. VS Codeを起動する

### 1-2. AntigravityをVS Codeに追加する

1. VS Codeの左サイドバーにある「Extensions（拡張機能）」のアイコン（4つのブロックのマーク）をクリック
2. 検索欄に `Antigravity` と入力
3. 表示された「Antigravity」をクリックして「Install」を押す
4. インストール後、左サイドバーにAntigravityのアイコンが追加される

### 1-3. Antigravityにログインする

1. サイドバーのAntigravityアイコンをクリック
2. 「Sign in with Google」をクリックしてGoogleアカウントでログイン

> **💡 Antigravityで使うべきAIモデル**  
> Antigravityには複数のAIモデルが選べます。このシステムのセットアップや質問には **Claude Sonnet** または **Gemini 2.5 Pro** が特におすすめです。賢くて日本語の理解も正確です。


---

## ステップ2：このシステムをダウンロードする（GitHub）

GitHubはコードを共有・管理するためのサービスです。  
難しく考えず「コードのダウンロード場所」だと思ってください。

### 2-1. GitHubアカウントを作る（持っていない場合）

1. [https://github.com](https://github.com) を開く
2. 「Sign up」をクリックしてアカウントを作成する
3. メールアドレスとパスワードを設定する

### 2-2. このリポジトリをダウンロードする

1. 共有されたGitHubのURLを開く（例：`https://github.com/xxxx/classroom_automation`）
2. 緑色の「Code」ボタンをクリック
3. 「Download ZIP」をクリック
4. ダウンロードしたZIPを展開（ダブルクリック）する
5. 展開されたフォルダを**わかりやすい場所**（Documentsフォルダなど）に移動する

> **📌 もしくはGit（上級者向け）でCloneする場合：**
> ```bash
> git clone https://github.com/xxxx/classroom_automation.git
> ```

---

## ステップ3：Pythonの環境を構築する

Pythonはこのシステムが動く「エンジン」です。

### 3-1. Homebrewをインストールする（Mac必須ツール）

ターミナルを開いて（Spotlight検索で「ターミナル」と入力）、以下をコピー・貼り付けして実行：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 3-2. Pythonをインストールする

```bash
brew install python3
```

### 3-3. 仮想環境を作ってパッケージをインストールする

1. ターミナルで、ダウンロードしたフォルダに移動する：
   ```bash
   cd /Users/あなたのユーザー名/Documents/classroom_automation
   ```
   （フォルダをターミナルにドラッグ＆ドロップしてもOK）

2. 仮想環境を作成：
   ```bash
   python3 -m venv venv
   ```

3. 仮想環境を有効化：
   ```bash
   source venv/bin/activate
   ```

4. 必要なパッケージをインストール：
   ```bash
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv google-genai PyMuPDF Pillow
   ```

> **💡 Antigravityに任せられること：**  
> このステップがうまくいかない場合は、エラーメッセージをコピーしてAntigravityに  
> 「このエラーが出ました。どうすれば直せますか？」と質問すればOKです。

---

## ステップ4：APIキーを取得・設定する

### 4-1. 設定ファイルを作る

フォルダの中にある `.env.example` ファイルをコピーして、`.env` という名前に変更します。

**ターミナルで：**
```bash
cp .env.example .env
```

または、Finderで `.env.example` を右クリック→「複製」→ファイル名を `.env` に変更。

> ⚠️ **`.env` ファイルは絶対に人に共有しないでください。**  
> APIキーなどの秘密情報が入ります。

### 4-2. Gemini APIキーを取得する

GeminiはGoogleのAIです。参考書のPDF解析に使います（無料枠あり）。

1. [https://aistudio.google.com](https://aistudio.google.com) を開く
2. 右上の「Get API key」をクリック
3. 「Create API key」をクリック
4. 表示されたAPIキーをコピー
5. `.env` ファイルを開いて、`GEMINI_API_KEY=` の後に貼り付ける：
   ```
   GEMINI_API_KEY="AIzaSy...（取得したキー）"
   ```

### 4-3. Google Cloud Projectを作成してOAuth認証情報を取得する

Googleカレンダー・Classroomと連携するための許可証です。

1. [https://console.cloud.google.com](https://console.cloud.google.com) を開く
2. 上部の「プロジェクト選択」→「新しいプロジェクト」で好きな名前（例：`juku-automation`）で作成
3. 左メニューから「APIとサービス」→「ライブラリ」を開く
4. 以下のAPIを1つずつ検索して「有効にする」：
   - `Google Calendar API`
   - `Google Classroom API`
   - `Google Drive API`
5. 「APIとサービス」→「OAuth 同意画面」を開く
   - User Type：「外部」を選択→「作成」
   - アプリ名（例：塾自動化）・メールアドレスを入力→「保存して次へ」を押し続ける
   - 「テストユーザー」に自分のGoogleアドレスを追加する
6. 「APIとサービス」→「認証情報」を開く
7. 「認証情報を作成」→「OAuthクライアントID」をクリック
8. アプリケーションの種類：「デスクトップアプリ」を選択→「作成」
9. 「JSONをダウンロード」をクリック
10. ダウンロードしたファイルを `classroom_automation` フォルダに移動し、**`credentials.json`** という名前に変更する

### 4-4. カレンダーIDを設定する

1. [https://calendar.google.com](https://calendar.google.com) を開く
2. 左サイドバーの対象カレンダーの「⋮」→「設定と共有」をクリック
3. 下にスクロールして「カレンダーの統合」欄にある**「カレンダーID」**をコピー
4. `.env` ファイルの `TARGET_CALENDAR_ID=` の後に貼り付ける

### 4-5. Google Meet URLを設定する

1. [https://meet.google.com](https://meet.google.com) で「新しいミーティング」→「後で使用するミーティングを作成」
2. 表示されたURLをコピー
3. `.env` ファイルの `MEET_URL=` の後に貼り付ける

---

## ステップ5：Google認証を行う

初回だけ必要な手順です。

```bash
# フォルダに移動して仮想環境を有効化
cd /Users/あなたのユーザー名/Documents/classroom_automation
source venv/bin/activate

# 認証を実行
python3 auth.py
```

ブラウザが自動で開いてGoogleのログイン画面が表示されます：

1. 塾のGoogleアカウントでログイン
2. 「このアプリは確認されていません」という警告が出たら「詳細」→「安全でないページへ移動」をクリック  
   ※自分で作ったアプリなので安全です
3. 要求されている権限を確認して「許可」をクリック

認証が成功すると `token.json` というファイルが自動で生成されます。  
これで次回以降は自動でログインされます。

---

## ステップ6：生徒の設定をする

`students/` フォルダの中に、**生徒の名前のフォルダ**を作成します。  
フォルダの名前と、Googleカレンダーの授業予定タイトルに含まれる生徒名が一致している必要があります。

### 6-1. 生徒フォルダを作成する

例：「田中 太郎」という生徒の場合

```
students/
  田中 太郎/
    settings.json
```

### 6-2. settings.jsonを作成する

`students/サンプル生徒/settings.json` を参考に、生徒ごとのフォルダに `settings.json` を作成します：

```json
{
    "course_id": "ここにClassroomのコースIDを入れる",
    "grade_prefix": "2年",
    "is_active": true
}
```

**`course_id` の調べ方：**

```bash
python3 test_api.py
```

を実行すると、Classroom上のコース一覧とIDが表示されます。対応するIDをコピーしてください。

### 6-3. 生徒を一時的に無効化する場合

`"is_active": false` に変更すると、その生徒への自動投稿がスキップされます。

---

## ステップ7：実際に動かす

設定が完了したら、システムを起動します。

**方法①：ダブルクリックで起動（最も簡単）**

`システムの起動.command` ファイルをダブルクリックすると自動で動きます。

初回はMacのセキュリティ確認が出る場合があります：
- Finder で `システムの起動.command` を右クリック→「開く」→「開く」をクリック

**方法②：ターミナルから起動**

```bash
cd /Users/あなたのユーザー名/Documents/classroom_automation
source venv/bin/activate
python3 main.py
```

**正常に動いている場合の表示例：**
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

## 設定のカスタマイズ

`.env` ファイルを編集することで、動作をカスタマイズできます。

| 設定項目 | 変数名 | 例 | 説明 |
|---------|--------|-----|------|
| 担当者名 | `TEACHER_NAME` | `"山田 花子"` | Classroomに投稿されるメッセージの担当者名 |
| 通知タイミング | `NOTIFY_MINUTES_BEFORE` | `60` | 授業開始の何分前に投稿するか（60=1時間前） |
| Meet URL | `MEET_URL` | `"https://meet.google.com/..."` | 使用するGoogle MeetのURL |
| カレンダーID | `TARGET_CALENDAR_ID` | `"xxxx@group.calendar.google.com"` | 授業予定が入っているカレンダーのID |

**例：授業30分前に通知したい場合**

`.env` ファイルを開いて：
```
NOTIFY_MINUTES_BEFORE=30
```

---

## よくあるエラーと対処法

**❌ `ModuleNotFoundError: No module named 'xxx'`**  
→ パッケージが足りていません。以下を実行：
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv google-genai PyMuPDF Pillow
```

**❌ `FileNotFoundError: credentials.json`**  
→ Google Cloudからダウンロードした認証情報ファイルが正しい場所にありません。  
`classroom_automation` フォルダ直下に `credentials.json` という名前で置いてください。

**❌ `❌ .envの設定が不足しています`**  
→ `.env` ファイルが作成されていないか、`TARGET_CALENDAR_ID` が設定されていません。  
ステップ4の手順を確認してください。

**❌ ブラウザで認証画面が開かない**  
→ ターミナルで `python3 auth.py` を直接実行してみてください。

**❌ `向こう1週間の授業予定が見つかりませんでした`**  
→ Googleカレンダーの予定タイトルに生徒のフォルダ名が含まれているか確認してください。  
例：フォルダ名が `田中 太郎` なら、予定タイトルは `田中 太郎 授業` のようにしてください。

---

## Antigravityに何を任せるか

このシステムはAntigravityと一緒に使うことを想定しています。  
以下のことはAntigravityに任せてしまいましょう（日本語でOK）：

✅ **任せてOK**
- エラーが出たときの解決（エラーをコピペして「これどういう意味？」と聞く）
- 新しい機能の追加（例：「LINEにも通知を送りたい」）
- メッセージ文面の変更
- 生徒設定の追加方法の確認
- コードの意味の説明

❌ **Antigravityに見せてはいけないもの**
- `.env` ファイルの内容（APIキーが含まれる）
- `credentials.json`（本物のOAuthシークレット）
- `token.json`（ログイン情報）

---

## 📞 困ったときは

1. エラーメッセージをAntigravityにコピペして相談
2. このREADMEの「よくあるエラー」を確認
3. Googleの各サービスのヘルプページを確認

---

*このシステムはPython + Google APIs + Gemini APIで構築されています。*
