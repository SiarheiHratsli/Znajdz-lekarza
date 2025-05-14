from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from config import *
from db.models.models import *
from functools import wraps

app = Flask(__name__)
app.config.from_object(get_config())
db.init_app(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Musisz być zalogowany, aby uzyskać dostęp do tej strony.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def main():
    cities = City.query.all()
    specializations = Specialization.query.all()
    return render_template('main.html', cities=cities, specializations=specializations)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    visit_type = request.args.get('visit_type', '')
    city_district = request.args.get('city_district', '')
    specialization = request.args.get('specialization', '')

    query = Doctor.query
    if visit_type:
        query = query.filter_by(visit_type=visit_type)
    if city_district:
        query = query.filter_by(city_id=city_district)
    if specialization:
        query = query.filter_by(specialization_id=specialization)

    doctors = query.all()

    city = City.query.get(city_district)
    specialization = Specialization.query.get(specialization)

    return render_template(
        'search.html', doctors=doctors, city_district=city, specialization=specialization
***REMOVED***


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        flash('Jesteś już zalogowany.', 'info')
        return redirect(url_for('main'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password_confirmation = request.form['password_confirmation']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        birth_date = request.form['birth_date']

        if password != password_confirmation:
            flash('Hasła się nie zgadzają.', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Użytkownik z takim adresem e-mail już istnieje.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(
            email=email,
            password_hash=hashed_password,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            birth_date=birth_date
    ***REMOVED***
        db.session.add(new_user)
        db.session.commit()

        flash('Rejestracja zakończona sukcesem! Możesz się teraz zalogować.', 'success')
        return redirect(url_for('login'))

    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        flash('Jesteś już zalogowany.', 'info')
        return redirect(url_for('main'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            flash('Login successful.', 'success')
            resp = redirect(url_for('main'))
            resp.set_cookie('is_logged_in', 'true', max_age=3600)  # Ważne przez 4 godziny
            return resp
    ***REMOVED***
            flash('Invalid credentials.', 'danger')

    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'success')
    resp = redirect(url_for('main'))
    resp.delete_cookie('is_logged_in')
    return resp


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005)