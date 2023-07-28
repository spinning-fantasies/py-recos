from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Configuration for SQLite database
DB_NAME = "activities.db"

# Create the database and tables using schema.sql if it doesn't exist
if not os.path.exists(DB_NAME):
    with sqlite3.connect(DB_NAME) as conn:
        with open('schema.sql') as f:
            conn.executescript(f.read())

@app.route('/')
def index():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activities")
        activities = cursor.fetchall()

        cursor.execute("SELECT * FROM locations")
        locations = cursor.fetchall()

    return render_template('index.html', activities=activities, locations=locations)


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


if __name__ == '__main__':
    app.run(debug=True)
