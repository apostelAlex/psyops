from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import random, os

app = Flask(__name__)
app.secret_key = "secret"

def get_login_db_connection():
    conn = sqlite3.connect('users_login.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_images(n:int)-> tuple[list]:
    num_emotions = 6
    base_path = "static/images/"
    result_vals = []
    result_paths = []
    listed_dirs = [os.listdir(x) for x in [os.path.join(base_path, str(y)) for y in range(num_emotions)]]
    for _ in range(n):
        val = random.randint(0,num_emotions-1)
        result_vals.append(val+1)
        result_paths.append(os.path.join("images", str(val), listed_dirs[val][random.randint(0,len(listed_dirs[val]))]))
    return (result_paths, result_vals)

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/game')
def game():
    num_pics = 5
    images_paths, correct_buttons = get_images(num_pics)
    images = [url_for("static", filename=x) for x in images_paths]
    delay = request.args.get('delay', default=1, type=int)
    return render_template('game.html', images=images, correct_buttons=correct_buttons, delay=delay)

@app.route('/submit_results', methods=['POST'])
def submit_results():
    data = request.get_json()
    total_images = len(data['results'])
    correct_responses = sum(data['results'])
    accuracy = (correct_responses / total_images) * 100
    return jsonify(accuracy=accuracy)

@app.route('/result')
def result():
    accuracy = request.args.get('accuracy', default=0, type=float)
    return f"Deine Genauigkeit ist {accuracy:.2f}%"

@app.route('/start_game')
def start_game():
    if 'user_id' in session:
        return redirect(url_for('game'))
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_login_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = get_login_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        except sqlite3.IntegrityError:
            return render_template('register_failed.html')
        
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)