from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('office.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            role TEXT NOT NULL,
            salary REAL NOT NULL,
            status TEXT DEFAULT 'Active'
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('office.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*) FROM employees")
    total_emp = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(salary) FROM employees")
    total_salary = cursor.fetchone()[0] or 0
    
    conn.close()
    return render_template('index.html', employees=employees, total_emp=total_emp, total_salary=total_salary)

@app.route('/add', methods=['POST'])
def add_employee():
    name = request.form['name']
    email = request.form['email']
    department = request.form['department']
    role = request.form['role']
    salary = request.form['salary']

    conn = sqlite3.connect('office.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO employees (name, email, department, role, salary) VALUES (?, ?, ?, ?, ?)",
                       (name, email, department, role, salary))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_employee(id):
    conn = sqlite3.connect('office.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
