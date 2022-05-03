import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

# Blueprintは、テンプレートのHTMLやそれに紐づく処理を整理するためのクラス
# url_prefixはこのファイルに定義されているURLの前に付加される
bp = Blueprint('auth', __name__, url_prefix='/auth')

# /auth/registerというURLとユーザ登録画面を紐付ける
@bp.route('/register', methods=('GET', 'POST'))
def register():
    # ユーザがフォームを送信したらユーザ登録処理が走る
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # バリデーション処理
        # ユーザ名とPasswordは必須項目だからからの場合はエラーを表示する
        if not username:
            error = 'ユーザ名は必須です。'
        elif not password:
            error = 'Passwordは必須です。'

        # エラーがなければDBに登録する
        if error is None:
            # 例外処理
            try:
                # DBにユーザを登録するSQLを実行する
                db.execute(
                    # ?はユーザが入力した値を安全に処理するため
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    # セキュリティの観点からパスワードを暗号化してからDBに保存する
                    (username, generate_password_hash(password)),
                )
                # DBの変更を保存する
                db.commit()

            # ユーザ名が既に登録されている場合はエラーを表示する
            except db.IntegrityError:
                error = f"{username}は既に登録されているため別のユーザ名にしてください。"

            else:
                # ユーザをDBに保存した後、セッションにユーザIDを保存する
                user = db.execute(
                    'SELECT * FROM user WHERE username = ?', (username,)
                ).fetchone()
                session['user_id'] = user['id']
                # ホーム画面にリダイレクトする
                return redirect(url_for("index"))

        # エラーがある場合は、画面に表示するエラーメッセージを格納する
        flash(error)

    # ユーザ登録画面が表示する
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    # ユーザがフォームを送信したらログイン処理が走る
    if  request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        # DBからユーザを取得するSQLを実行する（ユーザ名で検索）
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        # DBにユーザが送信したユーザ名がない場合
        if user is None:
            error = 'ユーザ名が正しくありません。'
        elif not check_password_hash(user['password'], password):
            error = 'passwordが正しくありません。'

        if error is None:
            # sessionはユーザを識別するためのデータを保持する変数
            # 一度セッションをクリアする（前にログインしていた情報などが残っているかもしれないため）
            session.clear()
            # セッションで送ったデータはブラウザのCookieの保存される
            # そのためログインしているユーザを識別できる
            session['user_id'] = user['id']
            # ホーム画面へリダイレクト
            return redirect(url_for('index'))

        flash(error)

    # 普通にアクセスした場合はログイン画面を表示する
    return render_template('auth/login.html')

# アクセスされたURLに関係なく、事前に実行される関数を定義
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    # ユーザIDがセッションに保存されているか確認
    if user_id is None:
        g.user = None

    else:
        # ユーザIDがセッションにある場合、ユーザのデータをDBから取得
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    # セッションをクリアして、セッションからユーザIDを削除する
    session.clear()
    # ホーム画面にログイン画面にリダイレクト
    return redirect(url_for('auth.login'))

# ログインが必要な画面でこの関数を呼び出す
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # ユーザがログインしていない場合
        if g.user is None:
            # ログイン画面へリダイレクトする
            return redirect(url_for('auth.login'))

        # ログインしている場合は、アクセスした画面を表示する
        return view(**kwargs)

    return wrapped_view
