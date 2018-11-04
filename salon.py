import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from datetime import date, time, datetime

from models import db, Stylist, Patron, Appointment

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
    return render_template('home.html')


@app.route('/patron/<name>')
def patron_page(name):
    stylists = Stylist.query.order_by(Stylist.id.desc()).all()
    patron = Patron.query.filter(Patron.name == name).first()
    return render_template('patron.html', stylists=stylists, name=name, patron=patron)


@app.route('/owner')
def owner_page():
    if not session.get('username') == 'owner':
        abort(401)

    stylists = Stylist.query.order_by(Stylist.id.desc()).all()
    return render_template('owner.html', stylists=stylists)


@app.route('/stylist/<name>')
def stylist_page(name):
    stylist = Stylist.query.filter(Stylist.name == name).first()
    return render_template('stylist.html', name=name, stylist=stylist)


@app.route('/add_stylist', methods=['POST'])
def add_stylist():
    if not session.get('logged_in'):
        abort(401)
    if not session.get('username') == 'owner':
        abort(401)
    new = Stylist(request.form['name'], request.form['password'])

    a = Appointment(date.today(), new.id, -1)

    new.appointments.append(a)
    db.session.add(new)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('owner_page'))


@app.routh('/requestappointment', methods=['GET', 'POST'])
def request_appointment(patron_name, stylist_name):
    return render_template('appointment.html', patron=patron_name, stylist=stylist_name)


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
                return redirect(url_for('patron_page', name=patron.name))
        for stylist in stylists:
            if request.form['name'] == stylist.name and request.form['password'] == stylist.password:
                session['logged_in'] = True
                session['username'] = request.form['name']
                flash('You were logged in')
                return redirect(url_for('stylist_page', name=stylist.name))
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
        return redirect(url_for('home'))
    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run()
