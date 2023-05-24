from flask import Flask, render_template, request, redirect, url_for
from werkzeug.local import Local
import sqlite3

# Create a Flask web application
app = Flask(__name__)

# Create a thread-local object to store the connection and cursor
local = Local()

# Function to get the database connection for the current thread
def get_db():
    if not hasattr(local, 'connection'):
        local.connection = sqlite3.connect('example.db')
    return local.connection

# Function to get the database cursor for the current thread
def get_cursor():
    if not hasattr(local, 'cursor'):
        local.cursor = get_db().cursor()
    return local.cursor

# Create a table if it doesn't exist
def create_table():
    cursor = get_cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    age INTEGER)''')

# Route for the home page
@app.route('/')
def home():
    cursor = get_cursor()
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()
    return render_template('index.html', records=records)

# Route for inserting a new student record
@app.route('/insert', methods=['POST'])
def insert():
    name = request.form['name']
    age = request.form['age']
    cursor = get_cursor()
    cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", (name, age))
    get_db().commit()
    return redirect(url_for('home'))

# Close the database connection at the end of the request
@app.teardown_appcontext
def close_connection(exception):
    connection = getattr(local, 'connection', None)
    if connection is not None:
        connection.close()
        local.connection = None
        local.cursor = None

# Start the Flask application
if __name__ == '__main__':
    create_table()
    app.run(debug=True)
