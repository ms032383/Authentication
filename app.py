from flask import Flask, render_template, request, redirect, url_for, flash, session

# App initialization
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Make sure this key is unique and secret

# Database (in-memory for simplicity)
data = [
    ["Alice", "password123"],
    ["Bob", "qwerty"],
    ["Charlie", "12345"],
    ["David", "pass123"],
    ["admin", "admin"],
]

# Helper function to check if user exists
def find_user(username):
    for user in data:
        if user[0] == username:
            return user
    return None

# Routes
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = find_user(username)
        
        if user and user[1] == password:
            flash('Login successful!', 'success')
            session['username'] = username
            return redirect(url_for('login'))
        else:
            flash('Invalid username or password. Please try again or register if you do not have an account.', 'danger')
            return redirect(url_for('home'))
        
    return render_template('index.html')

@app.route('/login')
def login():
    username = session.get('username')
    if username:
        return render_template('home.html', name=username)
    else:
        return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')  # Currently not used but can be stored
        password = request.form.get('password')
        user = find_user(username)
        
        if user:
            flash('Username already exists. Please choose a different username.', 'danger')
        else:
            data.append([username, password])
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('home'))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
