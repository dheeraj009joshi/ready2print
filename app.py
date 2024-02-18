from flask import Flask, render_template, redirect,request, session,flash,url_for
from flask_login import login_required

app = Flask(__name__)
app.secret_key = 'Dheeraj@2006'
users = {
    'dheeraj@gmail.com': {'username': 'dheeraj@gmail.com', 'password': 'dheeraj@gmail.com'},
    'user2': {'username': 'user2', 'password': 'password2'}
}


@app.route('/')
def index():
    return render_template('home/index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username,password)
        if username in users and users[username]['password'] == password:
            session['username'] = username
            print(session)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('home/sign-in.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            flash('Username already taken. Please choose a different one.', 'error')
        else:
            users[username] = {'username': username, 'password': password}
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('home/sign-up.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
