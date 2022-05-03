# タスク・マトリックス アプリケーション

## 環境

### OS

macOS Monterey v12.2.1

### チップ

Apple M1

### プログラミング言語

[python v3.9.1](https://www.python.org/downloads/release/python-391/)

#### ライブラリ

- [Flask v2.1.2](https://flask.palletsprojects.com/en/2.1.x/)
- [sqlite-web v0.4.0](https://github.com/coleifer/sqlite-web)
- [pytest v7.1.2](https://docs.pytest.org/en/7.1.x/)
- [coverage v6.3.2](https://coverage.readthedocs.io/en/6.3.2/#quick-start)

その他、依存しているライブラリなどは`requirements.txt`を参照してください。

[venvについて](https://qiita.com/fiftystorm36/items/b2fd47cf32c7694adc2e)

### VSCode拡張機能

- [EditorConfig for VS Code](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig)
- [Trailing Spaces](https://marketplace.visualstudio.com/items?itemName=shardulm94.trailing-spaces)
- [Highlight Trailing White Spaces](https://marketplace.visualstudio.com/items?itemName=ybaumes.highlight-trailing-white-spaces)
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
- [HTML CSS Support](https://marketplace.visualstudio.com/items?itemName=ecmel.vscode-html-css)
- [Auto Close Tag](https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-close-tag)
- [Tabnine AI Autocomplete for JavaScript, Python, ..etc](https://marketplace.visualstudio.com/items?itemName=TabNine.tabnine-vscode)

## 環境構築

ターミナルで実行してください。

```sh
git clone git@github.com:ryichk/task-matrix.git
cd task-matrix
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
export FLASK_ENV=development
```

### DB作成

```sh
python -m flask init-db
```

### Flaskサーバ起動

```sh
python -m flask run
```

[127.0.0.1:5000](http://127.0.0.1:5000/)へアクセス

### DB GUIクライアント・サーバ起動

```sh
sqlite_web ./instance/app.sqlite
```

### ユニットテスト実行

```sh
python -m pytest
```

#### テストのコードカバレッジ測定

```sh
coverage run -m pytest
```

## Gitブランチ運用方法

- 本体ブランチ：main
- 検証環境ブランチ：staging
- 作業ブランチ：feature/branch-name
- バグ修正ブランチ：fix/branch-name

### コミットテンプレートの設定

```sh
git config commit.template ./.commit_template
```
