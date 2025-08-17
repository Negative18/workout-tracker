from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3
from flask import send_from_directory

app = Flask(__name__)


# Route: View All Workouts
@app.route('/')
def index():
    conn = sqlite3.connect('workout.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS workouts 
                 (id INTEGER PRIMARY KEY, exercise TEXT, sets INTEGER, reps INTEGER, date TEXT)''')
    
    # 🚀 Check if the 'weight' column exists, if not, add it
    c.execute("PRAGMA table_info(workouts)")
    columns = [column[1] for column in c.fetchall()]
    
    if 'weight' not in columns:
        c.execute("ALTER TABLE workouts ADD COLUMN weight REAL")
    if 'unit' not in columns:
        c.execute("ALTER TABLE workouts ADD COLUMN unit TEXT")
    
    # Fetch all workouts
    c.execute('SELECT * FROM workouts')
    workouts = c.fetchall()
    conn.close()
    return render_template('index.html', workouts=workouts)


# Route: Add Workout
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        exercise = request.form['exercise']
        sets = request.form['sets']
        reps = request.form['reps']
        date = request.form['date']
        weight = request.form['weight']
        unit = request.form['unit']

        conn = sqlite3.connect('workout.db')
        c = conn.cursor()
        c.execute('INSERT INTO workouts (exercise, sets, reps, date, weight, unit) VALUES (?, ?, ?, ?, ?, ?)',
                  (exercise, sets, reps, date, weight, unit))
        conn.commit()
        conn.close()
        return redirect('/')
    
    return render_template('add.html')



# Route: Edit Workout
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('workout.db')
    conn.row_factory = sqlite3.Row  # ✅ This makes `workout` a dict-like object
    workout = conn.execute('SELECT * FROM workouts WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        exercise = request.form['exercise']
        date = request.form['date']
        sets = request.form['sets']
        reps = request.form['reps']
        weight = request.form['weight']
        unit = request.form['unit']

        conn.execute('''
            UPDATE workouts
            SET exercise = ?, date = ?, sets = ?, reps = ?, weight = ?, unit = ?
            WHERE id = ?
        ''', (exercise, date, sets, reps, weight, unit, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', workout=workout)




#Route: Delete Workout
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = sqlite3.connect('workout.db')
    c = conn.cursor()
    c.execute('DELETE FROM workouts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json', mimetype='application/manifest+json')


@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('static', 'service-worker.js')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)






