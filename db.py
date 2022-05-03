import sqlite3

import click
# gは、リクエストごとに一意のオブジェクト
# 例えば、同じリクエストでget_dbが2回呼ばれた場合、
# 2回DBへの接続を作成するのではなく、1回目の接続がgに保存されて再利用する
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        # DBへの接続を確立する
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # dictのように動作する行を返すようにDBに指示する。
        # これにより、名前で列にアクセスできる
        g.db.row_factory = sqlite3.Row

    return g.db

# アプリで使用するためにアプリインスタンスに登録する必要がある
def close_db(e=None):
    db = g.pop('db', None)

    # DBに接続されている場合
    if db is not None:
        # DB接続を閉じる
        db.close()

def init_db():
    # DBに接続する関数を呼び出す
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# @click.commandは、ターミナルで実行するコマンドを定義する
# init_db関数を実行するinit-dbというコマンドを定義している
@click.command('init-db')
@with_appcontext

# アプリで使用するためにアプリインスタンスに登録する必要がある
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

# この関数をアプリインスタンス(__init__)で呼び出す
def init_app(app):
    app.teardown_appcontext(close_db)
    # flaskコマンドで実行できる新しいコマンドを追加する
    app.cli.add_command(init_db_command)
