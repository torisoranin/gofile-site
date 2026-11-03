# Gofile × X 公開版

## 使い方
1. Gofile の共有URL `https://gofile.io/d/AbC12345` から `AbC12345` を取得。
2. GitHubにこのフォルダのファイルをアップロード（`.env` やトークンは絶対にアップしない）。
3. Vercel の Add New > Project から GitHub リポジトリをImportしDeploy。
4. Vercel > Project > Settings > Environment Variables に下記を登録してRedeploy。
    - `GOFILE_FOLDER_ID` : フォルダID
    - `GOFILE_API_TOKEN` : 自分のAPIトークン（秘密）
    - `SITE_TITLE` : Xプレビューとサイトのタイトル
    - `SITE_DESCRIPTION` : Xプレビューの説明
    - `SITE_IMAGE_URL` : Xプレビュー用の**誰でもアクセスできるHTTPS画像URL**。例: `https://your-project.vercel.app/thumbnail.jpg`
5. XでVercel公開URLをシェア。

### Xサムネ画像を変更
`static/thumbnail.jpg` というファイルを設置して `SITE_IMAGE_URL` を `https://あなたの公開ドメイン/static/thumbnail.jpg` に設定。画像は1200×630pxが使いやすい。変更後は再デプロイが必要。X側でプレビューがキャッシュされる場合あり。

### 動画別サムネ変更
`thumbnails.json` に `"ファイル名.mp4": "https://あなたのドメイン/画像.jpg"` の形で追加。例を削除して使用。ファイルIDをキーにしてもよい。画像を `static/` に置いた場合は `"/static/画像.jpg"` と指定可能。

### ローカル検証
`pip install -r requirements.txt` → 環境変数を設定 → `python app.py` → `http://127.0.0.1:8765`

### 注意
- Gofile公式APIの `/contents/{contentId}` はPremiumが必要な場合があります。APIで `error-notPremium` が出る場合この方法では自動連携できません。
- APIトークンをHTML・JavaScript・GitHub公開リポジトリに入れないこと。
- 公開フォルダの動画等は著作権・肖像権・本人の同意を確認して公開すること。
- 一覧は上限1000件です。1000件以上はページネーション実装が必要。
- ファイル別リンクは保護のためデフォルトで元のGofile共有フォルダへ誘導します（直リンクは付与しません）。
- 実APIのユーザートークン接続テストは行っていません。
