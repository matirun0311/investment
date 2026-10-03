# 週刊・はじめての株式投資

株式投資の初学者向けに、**毎週月曜 7:00（JST）に1本ずつ** 記事を配信する静的サイトです（Jekyll + GitHub Pages）。

## しくみ

- 記事は `_posts/` に、公開したい日付（毎週月曜）をつけて置いておきます。
- `_config.yml` の `future: false` により、公開日前の記事はサイトに出ません。
- GitHub Actions（`.github/workflows/pages.yml`）が **毎週月曜 7:00 JST** にサイトを再ビルドし、その日付になった記事が自動で公開されます。
- 読者は RSS フィード（`/feed.xml`）で購読できます。メールで届けたい場合は、Buttondown や follow.it などの「RSS→メール配信」サービスにフィードURLを登録してください。

つまり、記事を何週分か先まで書き溜めて push しておけば、あとは自動で週1回配信されます。

## 初期設定（1回だけ）

1. このブランチを `main` にマージする
2. GitHub のリポジトリ設定 → **Settings → Pages → Build and deployment → Source** を「**GitHub Actions**」にする
3. Actions タブから「Build and publish weekly articles」を手動実行（Run workflow）して公開を確認する

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
| `.github/workflows/pages.yml` | 週次ビルド・公開のワークフロー |
