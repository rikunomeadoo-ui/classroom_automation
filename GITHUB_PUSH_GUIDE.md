# 🚀 GitHubへのプッシュ手順（1回だけ必要）

ローカルのコードは準備完了しています。  
以下の手順でGitHubに公開してください。

---

## Step 1: GitHubでリポジトリを作成する

1. [https://github.com](https://github.com) にログイン（アカウントがない場合はSign up）
2. 右上の「**＋**」アイコン → **「New repository」** をクリック
3. 以下を設定：
   - **Repository name**: `classroom_automation`
   - **Description**: `Google Classroomへの授業通知を自動化するシステム`（任意）
   - **Visibility**: ⚠️ **Private**（同僚だけに共有したいので必ずPrivateに）
   - 「Add a README file」「Add .gitignore」は**チェックしない**
4. 緑の「**Create repository**」ボタンをクリック

---

## Step 2: ターミナルでリモートリポジトリを登録してpushする

リポジトリ作成後、画面に表示されるHTTPS URLをコピーしてください。  
（例：`https://github.com/あなたのID/classroom_automation.git`）

ターミナルで以下を実行（URLは自分のものに変更）：

```bash
cd /Users/oohatariku/Downloads/塾講/classroom_automation

git remote add origin https://github.com/あなたのID/classroom_automation.git

git branch -M main

git push -u origin main
```

GitHubのログイン画面が出た場合は、GitHubのユーザー名とパスワードを入力してください。  
（パスワードは「Personal access token」を使う必要がある場合があります）

---

## Step 3: 同僚を招待する

1. GitHubのリポジトリページを開く
2. 「**Settings**」タブ → 「**Collaborators**」をクリック
3. 「**Add people**」をクリック
4. 同僚のGitHubアカウントのユーザー名またはメールアドレスを入力して招待

招待を受けた同僚は、メールのリンクから承認してREADME.mdの手順に従ってセットアップできます。

---

## ⚠️ 絶対にpushしてはいけないもの

以下のファイルは `.gitignore` で自動除外されています：
- `.env`（APIキー）
- `credentials.json`（OAuthシークレット）
- `token.json`（ログイン情報）
- `students/実名フォルダ/`（生徒の個人情報）
- `venv/`（Pythonパッケージ）
- `参考書/`（PDF）

`git status` を実行して、これらが「Changes to be committed」に**含まれていないこと**を確認してからpushしてください。

```bash
git status
# → "nothing to commit" または上記ファイルが含まれていなければOK
```

---

*コマンドの実行に失敗したり、エラーが出た場合はAntigravityに相談してください。*
