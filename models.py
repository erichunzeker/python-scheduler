from flask_sqlalchemy import SQLAlchemy

# note this should only be created once per project
# to define models in multiple files, put this in one file, and import db into each model, as we import it in flaskr.py
db = SQLAlchemy()


class Patron(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    appointments = db.relationship('Appointment', cascade='all, delete-orphan', backref='patron', lazy='dynamic')
    stylist_id = db.Column(db.Integer, db.ForeignKey("stylist.id"))

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return '<Patron {}>'.format(self.id)


class Stylist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    appointments = db.relationship('Appointment', cascade='all, delete-orphan', backref='stylist', lazy='dynamic')
    patron = db.relationship("Patron", backref="stylist", lazy="select", uselist=False)

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return '<Stylist {}>'.format(self.id)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    stylist_id = db.Column(db.Integer, db.ForeignKey('stylist.id'))
    patron_id = db.Column(db.Integer, db.ForeignKey('patron.id'))

    def __init__(self, date, stylist_id, patron_id):
        self.date = date
        self.stylist_id = stylist_id
        self.patron_id = patron_id
