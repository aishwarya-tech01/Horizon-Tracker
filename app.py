from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    # Added 'date_applied' to track time for your 7-day alerts
    conn.execute('''CREATE TABLE IF NOT EXISTS applications 
                    (id INTEGER PRIMARY KEY, company TEXT, title TEXT, status TEXT, date_applied DATE)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = get_db()
    jobs = conn.execute('SELECT * FROM applications').fetchall()
    conn.close()
    return render_template('index.html', jobs=jobs)

@app.route('/add', methods=['POST'])
def add():
    company = request.form['company']
    title = request.form['title']
    conn = get_db()
    # Using CURRENT_DATE to track when you added it
    conn.execute('INSERT INTO applications (company, title, status, date_applied) VALUES (?, ?, ?, CURRENT_DATE)', 
                 (company, title, 'Applied'))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/update/<int:id>')
def update(id):
    conn = get_db()
    conn.execute('UPDATE applications SET status = "Interviewing" WHERE id = ?', (id,))
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