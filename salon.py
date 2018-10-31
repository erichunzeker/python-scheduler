import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from models import db, Stylist, Patron

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
def home():
    return render_template('patron.html')


@app.route('/owner')
def owner_page():
    stylists = Stylist.query.order_by(Stylist.id.desc()).all()
    return render_template('owner.html', stylists=stylists)


@app.route('/add_stylist', methods=['POST'])
def add_stylist():
    if not session.get('logged_in'):
        abort(401)
    if not session.get('username') == 'owner':
        abort(401)
    new = Stylist(request.form['name'], request.form['password'])
    db.session.add(new)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('owner_page'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        patrons = Patron.query.all()
        stylists = Stylist.query.all()
        for patron in patrons:
            if request.form['name'] == patron.name and request.form['password'] == patron.password:
                session['logged_in'] = True
                session['username'] = request.form['name']
                flash('You were logged in')
                return redirect(url_for('home'))
        for stylist in stylists:
            if request.form['name'] == stylist.name and request.form['password'] == stylist.password:
                session['logged_in'] = True
                session['username'] = request.form['name']
                flash('You were logged in')
                return redirect(url_for('owner_page'))
        if request.form['name'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['username'] = request.form['name']
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('owner_page'))
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        new = Patron(request.form['name'], request.form['password'])
        db.session.add(new)
        db.session.commit()
        flash('New patron was successfully added')
        return redirect(url_for('owner_page'))
    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('owner_page'))


if __name__ == "__main__":
    app.run()
