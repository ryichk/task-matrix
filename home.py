from flask import (
    Blueprint, render_template
)

bp = Blueprint('home', __name__)

# route()デコレータを使用して、関数をトリガーするURLを指定している
# デコレータは、呼び出した時に実行できる関数を定義できる。＠がついているのがデコレータ
@bp.route('/')
def index():
    hello = 'Hello World.'
    return render_template('index.html', hello=hello)
