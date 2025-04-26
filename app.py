from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='proj',
        unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock'
    )
    return conn


@app.route('/')
def main():
    # Połączenie z bazą danych
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Pobranie miast
    cursor.execute("SELECT * FROM cities")
    cities = cursor.fetchall()

    # Pobranie specjalizacji
    cursor.execute("SELECT * FROM specializations")
    specializations = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('main.html', cities=cities, specializations=specializations)


@app.route('/search', methods=['GET', 'POST'])
def search():
    # Pobieranie danych z formularza
    visit_type = request.args.get('visit_type', '')
    city_district = request.args.get('city_district', '')
    specialization = request.args.get('specialization', '')

    # Łączenie z bazą danych
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Tworzenie zapytania w zależności od wybranych opcji
    query = "SELECT * FROM doctors WHERE 1=1"
    params = []

    if visit_type:
        query += " AND visit_type = %s"
        params.append(visit_type)

    if city_district:
        query += " AND city_id = %s"
        params.append(city_district)

    if specialization:
        query += " AND specialization_id = %s"
        params.append(specialization)

    cursor.execute(query, params)
    doctors = cursor.fetchall()

    query = "SELECT name FROM specializations where id = %s"

    cursor.execute(query, (specialization,))
    specialization = cursor.fetchone()

    query = "SELECT name FROM cities where id = %s"

    cursor.execute(query, (city_district,))
    city_district = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('search.html', doctors=doctors, city_district=city_district, specialization=specialization)


@app.route('/register', methods=['GET'])
def register():
    return render_template("register.html")

@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")

@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    return render_template("reserve.html")


if __name__ == '__main__':
    app.run(port=5005)