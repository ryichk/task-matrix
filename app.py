import os
from flask import Flask

# ファクトリ関数といって一番最初に実行される関数
# アプリの心臓部分
def create_app(test_config=None):
    # __name__にはフォルダ名(app)が代入されている。
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # データを安全に保つために使用される
        # サービス公開時に別のランダム値で上書きする必要がある
        SECRET_KEY='dev',
        # SQLiteというDBのファイルが保存されるパス
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )

    if test_config is None:
        # インスタンスフォルダ内のconfig.pyから取得した値で設定を上書きする
        # インスタンスフォルダというのは、GitHubに公開したくない設定情報を管理する場所 (パスワードやAPIキーなど)
        app.config.from_pyfile('config.py', silent=True)

    # テスト用設定がある場合 (テスト実行時)
    else:
        # テスト用の設定を読み込む
        app.config.from_mapping(test_config)

    try:
        # インスタンスフォルダがあるかどうか確認する
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # db.pyに記載した機能をアプリで使えるように読み込んでいる
    import db
    db.init_app(app)

    # home.pyに記載した機能をアプリで使えるように読み込んでいる
    import home
    app.register_blueprint(home.bp)
    # エンドポイント名をURLに関連付ける
    app.add_url_rule('/', endpoint='index')

    # auth.pyに記載した機能をアプリで使えるように読み込んでいる
    import auth
    app.register_blueprint(auth.bp)

    return app
