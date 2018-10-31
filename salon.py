import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from models import db, Stylist

app = Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='owner',
    PASSWORD='pass',

    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.root_path, 'salon.db')
))
app.config.from_envvar('SALON_SETTINGS', silent=True)

db.init_app(app)


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    db.drop_all()
    db.create_all()
    print('Initialized the database.')


@app.route('/')
def owner_page():
    stylists = Stylist.query.order_by(Stylist.id.desc()).all()
    return render_template('owner.html', stylists=stylists, name=app.config['USERNAME'])


@app.route('/add', methods=['POST'])
def add_stylist():
    if not session.get('logged_in'):
        abort(401)
    new = Stylist(request.form['name'])
    db.session.add(new)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('owner_page'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('owner_page'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('owner_page'))


if __name__ == "__main__":
    app.run()
