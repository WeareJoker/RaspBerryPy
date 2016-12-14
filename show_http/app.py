from flask import Flask, render_template, request, session
from flask import abort
from flask import redirect
from flask import url_for

from analysis.plugins import table_list, db_session

import show_http.login_manager

login_manager = show_http.login_manager
login_check = login_manager.user_required


def make_app():
    tmp_app = Flask(__name__)

    tmp_app.config['SECRET_KEY'] = 'development_key'
    tmp_app.config['ADMIN_ID'] = 'admin'
    tmp_app.config['ADMIN_PW'] = 'admin'

    return tmp_app


app = make_app()


@app.before_first_request
def pre_setting():
    session['login'] = False


@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/login', methods=['GET', 'POST'])
@login_check(False)
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        data = request.form

        if data['id'] == 'admin' and data['password'] == 'admin':
            login_manager.login_user()

        else:
            abort(401)

        return redirect(url_for('index'))


@app.route('/logout', methods=['GET', 'POST'])
@login_check(True)
def logout():
    login_manager.logout_user()
    return redirect(url_for('index'))


def get_table_columns(table):
    return [_ for _ in dir(table) if not _.startswith("_") and _ not in ['metadata', 'id']]


@app.route('/show')
@app.route('/show/<string:table_name>')
@login_check(True)
def show(table_name=None):
    if table_name is None:
        return render_template('show_db.html',
                               table_list=table_list)
    else:
        for table in table_list:
            if table.__tablename__ == table_name:
                return render_template('show_table.html',
                                       table=table,
                                       columns=get_table_columns(table),
                                       data=db_session.query(table).all())
        else:
            return render_template('show_db.html')


@app.errorhandler(401)
def go_login(_):
    return redirect(url_for('login'))


def main():
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    main()
