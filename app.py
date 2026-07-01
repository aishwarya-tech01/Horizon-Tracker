from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    # Stores salary as integer for calculations
    conn.execute('''CREATE TABLE IF NOT EXISTS applications 
                    (id INTEGER PRIMARY KEY, company TEXT, title TEXT, status TEXT, date_applied DATE, salary INTEGER)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = get_db()
    jobs = conn.execute('SELECT * FROM applications').fetchall()
    # Logic to sum up only 'Offered' salaries
    total_offered = sum(job['salary'] for job in jobs if job['status'] == 'Offered' and job['salary'])
    conn.close()
    return render_template('index.html', jobs=jobs, total_offered=total_offered)

@app.route('/add', methods=['POST'])
def add():
    company = request.form['company']
    title = request.form['title']
    salary = request.form.get('salary', 0)
    conn = get_db()
    conn.execute('INSERT INTO applications (company, title, status, date_applied, salary) VALUES (?, ?, ?, CURRENT_DATE, ?)', 
                 (company, title, 'Applied', salary))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/update/<int:id>/<string:status>')
def update(id, status):
    conn = get_db()
    conn.execute('UPDATE applications SET status = ? WHERE id = ?', (status, id))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute('DELETE FROM applications WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)