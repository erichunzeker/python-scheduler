from flask_sqlalchemy import SQLAlchemy

# note this should only be created once per project
# to define models in multiple files, put this in one file, and import db into each model, as we import it in flaskr.py
db = SQLAlchemy()


class Patron(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    #appointments = db.relationship('Appointment', backref='patron', lazy='dynamic')

    def __init__(self, name, password):
        self.name = name
        self.password = password
        #self.appointments = appointments

    def __repr__(self):
        return '<Patron {}>'.format(self.id)


class Stylist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    #appointments = db.relationship('Appointment', backref='stylist', lazy='dynamic')

    def __init__(self, name, password):
        self.name = name
        self.password = password
        #self.appointments = appointments

    def __repr__(self):
        return '<Stylist {}>'.format(self.id)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Integer, nullable=False)
    stylist_id = db.Column(db.Integer, db.ForeignKey('stylist.id'))
    patron_id = db.Column(db.Integer, db.ForeignKey('patron.id'))
