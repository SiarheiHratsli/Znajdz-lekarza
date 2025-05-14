from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum('M', 'F', 'Other'), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)

    @property
    def age(self):
        from datetime import date
        return date.today().year - self.birth_date.year - ((date.today().month, date.today().day) < (self.birth_date.month, self.birth_date.day))


class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)


class Specialization(db.Model):
    __tablename__ = 'specializations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)


class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    specialization_id = db.Column(db.Integer, db.ForeignKey('specializations.id'))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    visit_type = db.Column(db.Enum('gabinet', 'online'), nullable=False)
    address = db.Column(db.String(255))

    specialization = db.relationship('Specialization', backref='doctors')
    city = db.relationship('City', backref='doctors')