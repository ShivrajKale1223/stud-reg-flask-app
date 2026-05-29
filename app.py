from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database configuration
db_config = {
    "host": "localhost",
    "user": "flaskuser",
    "password": "Flask@1234",
    "database": "student_db"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    name    = request.form['name']
    email   = request.form['email']
    phone   = request.form['phone']
    course  = request.form['course']
    address = request.form['address']
    contact = request.form.get('contact', '')

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, email, phone, course, address, contact) VALUES (%s,%s,%s,%s,%s,%s)",
            (name, email, phone, course, address, contact)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash("Student registered successfully!", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")

    return redirect(url_for('index'))

@app.route('/students')
def students():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('students.html', students=data)

    
if __name__ == '__main__':
    app.run(debug=True)

