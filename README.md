# 週刊・はじめての株式投資

株式投資の初学者向けに、**毎週月曜 7:00（JST）に1本ずつ** 記事を配信する静的サイトです（Jekyll + GitHub Pages）。

## しくみ

- 記事は `_posts/` に、公開したい日付（毎週月曜）をつけて置いておきます。
- `_config.yml` の `future: false` により、公開日前の記事はサイトに出ません。
- GitHub Actions（`.github/workflows/pages.yml`）が **毎週月曜 7:00 JST** にサイトを再ビルドし、その日付になった記事が自動で公開されます。
- 同じタイミングで、その日の記事が **自分の Gmail 宛てにメールで届きます**（`scripts/send_email.py`）。
- RSS フィード（`/feed.xml`）でも購読できます。

つまり、記事を何週分か先まで書き溜めて push しておけば、あとは自動で週1回配信されます。

## 初期設定（1回だけ）

1. このブランチを `main` にマージする
2. GitHub のリポジトリ設定 → **Settings → Pages → Build and deployment → Source** を「**GitHub Actions**」にする
3. Actions タブから「Build and publish weekly articles」を手動実行（Run workflow）して公開を確認する

### メール配信の設定

1. Google アカウントで **2段階認証** を有効にし、[アプリパスワード](https://myaccount.google.com/apppasswords) を作成する（16文字）
2. GitHub の **Settings → Secrets and variables → Actions → New repository secret** で次の2つを登録する
   - `GMAIL_ADDRESS`：自分の Gmail アドレス（送信元・宛先の両方に使われます）
   - `GMAIL_APP_PASSWORD`：1 で作ったアプリパスワード
3. Actions タブで「Run workflow」→ **send_latest にチェック** して実行すると、公開済みの最新記事が届きます（送信テスト）

Secret が未設定の間は、メール送信だけがスキップされます（サイトの公開は通常どおり行われます）。

## 記事の追加

```sh
python3 scripts/new_article.py three-ways-to-profit
```

最新記事の翌週月曜の日付で、カリキュラム（`curriculum.md`）の次の週のテーマが入った下書きが `_posts/` に作られます。本文を書いて push してください。書き方の型は `templates/article-template.md` を参照。

## ローカルでの確認

```sh
bundle install
bundle exec jekyll serve --future   # 未来日付の記事も含めて表示
```

## 構成

| パス | 内容 |
|---|---|
| `_posts/` | 記事（第1〜4週は作成済み：2026/10/5〜10/26 公開） |
| `curriculum.md` | 52週分のカリキュラム |
| `about.md` | サイトの目的と免責事項 |
| `templates/article-template.md` | 記事テンプレート |
| `scripts/new_article.py` | 次の週の記事の下書きを作るスクリプト |
| `scripts/send_email.py` | 公開日を迎えた記事を Gmail で送るスクリプト |
| `.github/workflows/pages.yml` | 週次ビルド・公開・メール送信のワークフロー |
