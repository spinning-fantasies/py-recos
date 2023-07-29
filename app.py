from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mail import Mail, Message
import requests
import sqlite3
import os
from dotenv import load_dotenv

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")  # Replace with a secure secret key

# Configuration for Flask-Mail
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = 25  # Use the appropriate port for your mail server
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = 'g'

mail = Mail(app)

# Configuration for SQLite database
DB_NAME = "activities.db"

# Create the database and tables using schema.sql if it doesn't exist
if not os.path.exists(DB_NAME):
    with sqlite3.connect(DB_NAME) as conn:
        with open('schema.sql') as f:
            conn.executescript(f.read())

@app.route('/')
def index():
    location_id = request.args.get('location', None)  # Get the location ID from query parameters

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        # Fetch the locations for the location selector
        cursor.execute("SELECT * FROM locations")
        locations = cursor.fetchall()

        # Fetch activities filtered by the selected location (if provided)
        if location_id is not None:
            cursor.execute("SELECT * FROM activities WHERE is_deleted = 0 AND location_id = ?", (location_id,))
        else:
            cursor.execute("SELECT * FROM activities WHERE is_deleted = 0")

        activities = cursor.fetchall()

    return render_template('index.html', activities=activities, locations=locations, location_id=int(location_id))

@app.route('/activity/add', methods=['GET', 'POST'])
def add_activity():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        date = request.form['date']
        time = request.form['time']
        location_id = request.form['location']

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO activities (name, description, date, time, location_id) VALUES (?, ?, ?, ?, ?)",
                           (name, description, date, time, location_id))
            conn.commit()

        return redirect(url_for('index'))

    # Fetch locations to display in the form
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM locations")
        locations = cursor.fetchall()

    return render_template('add_activity.html', locations=locations)

@app.route('/activity/edit/<int:activity_id>', methods=['GET', 'POST'])
def edit_activity(activity_id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        date = request.form['date']
        time = request.form['time']
        location_id = request.form['location']

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE activities SET name=?, description=?, date=?, time=?, location_id=? WHERE id=?",
                           (name, description, date, time, location_id, activity_id))
            conn.commit()

        return redirect(url_for('index'))

    # Fetch the activity to display in the form for editing
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activities WHERE id=?", (activity_id,))
        activity = cursor.fetchone()

        cursor.execute("SELECT * FROM locations")
        locations = cursor.fetchall()

    return render_template('edit_activity.html', activity=activity, locations=locations)

@app.route('/activity/delete/<int:id>')
def delete_activity(id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE activities SET is_deleted = 1 WHERE id = ?", (id,))
        conn.commit()

    return redirect(url_for('index'))

@app.route('/send_email')
def send_email():
    location_id = request.args.get('location', None)  # Get the location ID from query parameters

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        # Fetch the locations for the location selector
        cursor.execute("SELECT * FROM locations")
        locations = cursor.fetchall()

        # Fetch activities filtered by the selected location (if provided)
        if location_id is not None:
            cursor.execute("SELECT * FROM activities WHERE is_deleted = 0 AND location_id = ?", (location_id,))
        else:
            cursor.execute("SELECT * FROM activities WHERE is_deleted = 0")

        activities = cursor.fetchall()

    recipient = 'mate@e.email'  
    subject = activities[0][1]
    body = activities[0][2]

    message = Message(subject=subject, recipients=[recipient], body=body)

    try:
        mail.send(message)
        flash('Email sent successfully!', 'success')
    except Exception as e:
        flash(f'Failed to send email. Error: {str(e)}', 'danger')

    return redirect(url_for('index'))

@app.route('/send_sms')
def send_sms():
    # URL of the external web service you want to call
    url = 'https://smsapi.free-mobile.fr/sendmsg?user=18347461&pass=hOVpAGJQu71fHN&msg=Hello%20World%20!'  # Replace this with the actual API URL

    # Make the GET request to the external API
    response = requests.get(url)

    if response.status_code == 200:  # Successful GET request
        data = response.json()
        return jsonify(data)  # Return the JSON response as a Flask JSON response
    else:
        return jsonify({'message': 'Failed to fetch data from the external API.'}), 500


if __name__ == '__main__':
    app.run(debug=True)
