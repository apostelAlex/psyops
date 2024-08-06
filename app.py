from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_game')
def start_game():
    # Hier kann man die Logik für den Start des Spiels einfügen
    print("Game Started!")
    return redirect(url_for('home'))

@app.route('/login')
def login():
    # Hier kann man die Logik für die Anmeldung einfügen
    print("Login clicked!")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
