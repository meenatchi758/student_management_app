from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# DB INIT
def init_db():
    conn = sqlite3.connect('students.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        course TEXT NOT NULL
    )''')
    conn.close()

init_db()

# HOME - List students
@app.route('/')
def index():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template('index.html', students=students)

# ADD STUDENT
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']

        conn = sqlite3.connect('students.db')
        conn.execute("INSERT INTO students (name, email, course) VALUES (?, ?, ?)", (name, email, course))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_student.html')

# EDIT STUDENT
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        cursor.execute("UPDATE students SET name=?, email=?, course=? WHERE id=?", (name, email, course, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()
    conn.close()
    return render_template('edit_student.html', student=student)

# DELETE STUDENT
@app.route('/delete/<int:id>')
def delete_student(id):
    conn = sqlite3.connect('students.db')
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
