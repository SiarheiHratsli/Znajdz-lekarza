from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from datetime import datetime, timedelta 

from config import *
from db.models.models import *
from functools import wraps
from flask_mail import Mail, Message

from collections import OrderedDict
from datetime import datetime, timedelta, time
import openai

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(get_config())
db.init_app(app)
mail = Mail(app)

def get_serializer():
    return URLSafeTimedSerializer(app.config['SECRET_KEY'])

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Musisz być zalogowany, aby uzyskać dostęp do tej strony.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            s = get_serializer()
            token = s.dumps(user.id, salt='password-reset')
            reset_url = url_for('reset_password', token=token, _external=True)
            body = f"Aby zresetować hasło kliknij w link:\n{reset_url}\n\nJeśli to nie Ty, zignoruj tę wiadomość."
            msg = Message(subject="Reset hasła", recipients=[email], body=body)
            try:
                mail.send(msg)
                flash('Wysłaliśmy e-mail z linkiem do zresetowania hasła.', 'info')
            except Exception as e:
                flash('Błąd przy wysyłaniu e-maila: ' + str(e), 'danger')
        else:
            flash('Jeśli podany e-mail istnieje, wyślemy na niego instrukcję resetu.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    s = get_serializer()
    try:
        user_id = s.loads(token, salt='password-reset', max_age=600) # ważny przez 10 minut
    except SignatureExpired:
        flash('Link do resetowania hasła wygasł.', 'danger')
        return redirect(url_for('reset_password_request'))
    except BadSignature:
        flash('Nieprawidłowy link do resetowania hasła.', 'danger')
        return redirect(url_for('reset_password_request'))

    user = User.query.get(user_id)
    if not user:
        flash('Użytkownik nie istnieje.', 'danger')
        return redirect(url_for('reset_password_request'))

    if request.method == 'POST':
        password = request.form['password']
        password2 = request.form['password2']
        if password != password2:
            flash('Hasła się nie zgadzają.', 'danger')
            return redirect(request.url)
        user.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        db.session.commit()
        flash('Hasło zostało zmienione. Możesz się zalogować.', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html')

@app.route('/')
def main():
    cities = City.query.all()
    specializations = Specialization.query.all()
    return render_template('main.html', cities=cities, specializations=specializations)


@app.route('/search', methods=['GET'])
def search():
    visit_type = request.args.get('visit_type', '')
    city_district = request.args.get('city_district', '')
    specialization = request.args.get('specialization', '')
    sort = request.args.get('sort', 'best')

    query = Doctor.query
    if visit_type:
        query = query.filter_by(visit_type=visit_type)
    if city_district:
        query = query.filter_by(city_id=city_district)
    if specialization:
        query = query.filter_by(specialization_id=specialization)

    if sort == "soonest":
        query = query.order_by(Doctor.rating.desc())
    elif sort == "rating":
        query = query.order_by(Doctor.rating.desc())
    elif sort == "name":
        query = query.order_by(Doctor.last_name.asc())
    else:
        query = query.order_by(Doctor.rating.desc())

    doctors = query.all()

    for doctor in doctors:
        doctor.appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
        doctor.available_terms = get_available_terms_for_doctor(doctor)

    cities = City.query.all()
    specializations = Specialization.query.all()

    return render_template(
        'search.html',
        doctors=doctors,
        cities=cities,
        specializations=specializations
    )


@app.template_filter('group_terms_by_day')
def group_terms_by_day(terms):
    """
    Grupuje terminy według dni (format DD.MM)
    """
    result = {}
    for term in terms:
        day = term['datetime'].strftime("%d.%m")
        if day not in result:
            result[day] = []
        result[day].append(term)
    return result


def get_available_terms_for_doctor(doctor, days_ahead=7):
    """
    Funkcja generuje terminy dla lekarza i oznacza zajęte na podstawie bazy danych.
    """
    today = datetime.today()
    terms = []
    for day in range(days_ahead):
        date = today + timedelta(days=day)
        for hour in range(8, 17):
            term_datetime = datetime.combine(date, time(hour, 0))
            is_taken = any(
                appointment.appointment_date.date() == term_datetime.date() and
                appointment.appointment_date.hour == term_datetime.hour and
                appointment.status != 'cancelled'
                for appointment in doctor.appointments
            )
            terms.append({
                'datetime': term_datetime,
                'is_taken': is_taken
            })
    return terms



 
@app.route('/lekarze')
def doctors():
    doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=doctors)

@app.route('/specializations')
def specializations():
    specializations = Specialization.query.all()
    return render_template('specializations.html', specializations=specializations)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Dziękujemy za kontakt! Odpowiemy najszybciej jak to możliwe.', 'success')
        return redirect(url_for('contact'))
    return render_template('send_email.html')

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
        )
        db.session.add(new_user)
        db.session.commit()

        s = get_serializer()
        token = s.dumps(new_user.id, salt='email-confirm')
        confirm_url = url_for('confirm_email', token=token, _external=True)
        body = f"Aby potwierdzić adres e-mail, kliknij w link:\n{confirm_url}\n\nJeśli to nie Ty, zignoruj tę wiadomość."
        msg = Message(subject="Potwierdzenie rejestracji", recipients=[email], body=body)
        try:
            mail.send(msg)
            flash('Rejestracja zakończona sukcesem! Sprawdź pocztę i potwierdź adres e-mail.', 'success')
        except Exception as e:
            flash('Błąd przy wysyłaniu maila potwierdzającego: ' + str(e), 'danger')
        return redirect(url_for('login'))

    
    max_birth_date = (datetime.utcnow() - timedelta(days=365 * 18)).strftime('%Y-%m-%d')
    return render_template("register.html", max_birth_date=max_birth_date)


@app.route('/confirm_email/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    s = get_serializer()
    try:
        user_id = s.loads(token, salt='email-confirm', max_age=3600*24)  # 24h ważność
    except SignatureExpired:
        flash('Link do potwierdzenia e-maila wygasł.', 'danger')
        return redirect(url_for('login'))
    except BadSignature:
        flash('Nieprawidłowy link do potwierdzenia e-maila.', 'danger')
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    if not user:
        flash('Użytkownik nie istnieje.', 'danger')
        return redirect(url_for('register'))

    if request.method == 'POST':
        if user.is_email_confirmed:
            flash('Adres e-mail już został potwierdzony.', 'info')
        else:
            user.is_email_confirmed = True
            db.session.commit()
            flash('Adres e-mail został potwierdzony! Możesz się zalogować.', 'success')
        return redirect(url_for('login'))

    return render_template('confirm_email.html', user=user)


@app.route('/resend_confirmation/<int:user_id>')
def resend_confirmation(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('Użytkownik nie istnieje.', 'danger')
        return redirect(url_for('login'))

    if user.is_email_confirmed:
        flash('Adres e-mail jest już potwierdzony.', 'info')
        return redirect(url_for('login'))

    s = get_serializer()
    token = s.dumps(user.id, salt='email-confirm')
    confirm_url = url_for('confirm_email', token=token, _external=True)
    body = f"Aby potwierdzić adres e-mail, kliknij w link:\n{confirm_url}\n\nJeśli to nie Ty, zignoruj tę wiadomość."
    msg = Message(subject="Potwierdzenie rejestracji", recipients=[user.email], body=body)
    try:
        mail.send(msg)
        flash('Ponownie wysłano e-mail z potwierdzeniem!', 'info')
    except Exception as e:
        flash('Błąd przy wysyłaniu maila potwierdzającego: ' + str(e), 'danger')
    return redirect(url_for('login'))


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
            if not user.is_email_confirmed:
                resend_url = url_for('resend_confirmation', user_id=user.id)
                flash(
                    f'Najpierw potwierdź adres e-mail, sprawdź skrzynkę pocztową. '
                    f'<a href="{resend_url}">Wyślij ponownie maila potwierdzającego</a>',
                    'warning'
                )
                return redirect(url_for('login'))
            session['user_id'] = user.id
        if user and check_password_hash(user.password_hash, password):
            flash('Login successful.', 'success')
            resp = redirect(url_for('main'))
            resp.set_cookie('is_logged_in', 'true', max_age=3600)  # Ważne przez 4 godziny
            return resp
        else:
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


openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({"error": "Brak wiadomości w żądaniu"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Jesteś pomocnym asystentem dla użytkowników serwisu znajdź-lekarza."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=150
        )

        response_message = response.choices[0].message.content
        return jsonify({"response": response_message})

    except openai.OpenAIError as e:
        return jsonify({"error": f"Błąd OpenAI: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": f"Wystąpił nieoczekiwany błąd: {str(e)}"}), 500


@app.route('/book_appointment', methods=['POST'])
@login_required
def book_appointment():
    """
    Endpoint do rezerwacji wizyty lekarskiej.
    Wymaga przesłania:
    - doctor_id: ID lekarza
    - appointment_date: data i godzina spotkania w formacie "YYYY-MM-DD HH:MM:SS"
    """
    try:
        doctor_id = request.form.get('doctor_id')
        appointment_date_str = request.form.get('appointment_date')
        notes = request.form.get('notes', '')

        # Walidacja danych
        if not doctor_id or not appointment_date_str:
            flash('Błąd: Brak wymaganych danych do rezerwacji wizyty.', 'danger')
            return redirect(request.referrer or url_for('search'))

        try:
            appointment_date = datetime.strptime(appointment_date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            flash('Błąd: Nieprawidłowy format daty i godziny.', 'danger')
            return redirect(request.referrer or url_for('search'))

        if appointment_date < datetime.now():
            flash('Błąd: Nie można zarezerwować terminu w przeszłości.', 'danger')
            return redirect(request.referrer or url_for('search'))

        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            flash('Błąd: Wybrany lekarz nie istnieje.', 'danger')
            return redirect(request.referrer or url_for('search'))

        existing_appointment = Appointment.query.filter_by(
            doctor_id=doctor_id,
            appointment_date=appointment_date
        ).first()

        if existing_appointment:
            flash('Błąd: Wybrany termin jest już zajęty. Proszę wybrać inny termin.', 'danger')
            return redirect(request.referrer or url_for('search'))

        new_appointment = Appointment(
            doctor_id=doctor_id,
            user_id=session['user_id'],
            appointment_date=appointment_date,
            status='pending',
            notes=notes
        )

        db.session.add(new_appointment)
        db.session.commit()

        flash(f'Wizyta została pomyślnie zarezerwowana na {appointment_date.strftime("%d.%m.%Y o %H:%M")}', 'success')

        return redirect(url_for('my_appointments'))

    except Exception as e:
        db.session.rollback()
        flash(f'Wystąpił błąd podczas rezerwacji wizyty: {str(e)}', 'danger')
        return redirect(request.referrer or url_for('search'))


@app.route('/my_appointments')
@login_required
def my_appointments():
    """
    Strona z listą wizyt użytkownika.
    Automatycznie aktualizuje statusy przeszłych wizyt.
    """
    now = datetime.now()

    past_appointments = Appointment.query.filter(
        Appointment.user_id == session['user_id'],
        Appointment.appointment_date < now,
        Appointment.status.in_(['pending', 'confirmed'])
    ).all()

    if past_appointments:
        for appointment in past_appointments:
            appointment.status = 'completed'

        db.session.commit()
        print(f"Zaktualizowano {len(past_appointments)} wizyt na status 'completed'")

    appointments = Appointment.query.filter_by(user_id=session['user_id']).order_by(Appointment.appointment_date).all()

    appointments_data = []
    for appointment in appointments:
        doctor = Doctor.query.get(appointment.doctor_id)
        appointment_data = {
            'id': appointment.id,
            'doctor_name': f"{doctor.first_name} {doctor.last_name}",
            'doctor_specialization': doctor.specialization.name if doctor.specialization else 'Brak specjalizacji',
            'appointment_date': appointment.appointment_date,
            'status': appointment.status,
            'notes': appointment.notes
        }
        appointments_data.append(appointment_data)

    return render_template('my_appointments.html', appointments=appointments_data, now=now)


@app.route('/cancel_appointment/<int:appointment_id>', methods=['POST'])
@login_required
def cancel_appointment(appointment_id):
    """
    Anulowanie wizyty.
    """
    appointment = Appointment.query.get(appointment_id)

    if not appointment or appointment.user_id != session['user_id']:
        flash('Nie masz uprawnień do anulowania tej wizyty lub wizyta nie istnieje.', 'danger')
        return redirect(url_for('my_appointments'))

    if appointment.appointment_date < datetime.now():
        flash('Nie można anulować wizyty, która już się odbyła.', 'danger')
        return redirect(url_for('my_appointments'))

    appointment.status = 'cancelled'
    db.session.commit()

    flash('Wizyta została anulowana.', 'success')
    return redirect(url_for('my_appointments'))


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Dziękujemy za kontakt! Odpowiemy najszybciej jak to możliwe.', 'success')
        return redirect(url_for('contact'))
    return render_template('send_email.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005)
