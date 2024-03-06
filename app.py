from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json

app = Flask(__name__)

with open('jobs.json', 'r') as jobs_file:
    jobs_data = json.load(jobs_file)

# with open('users.json', 'r') as users_file:
#     users_data = json.load(users_file)

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template('job-list.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/user')
def user_profile():
    return f'Welcome, user!'

@app.route('/login', methods=['POST'])
def process_login():
    email = request.form['email']
    password = request.form['pswd']

    return redirect(url_for('user_profile'))

@app.route('/signup', methods=['POST'])
def process_signup():
    user_id = request.form['txt']
    email = request.form['email']
    password = request.form['pswd']
    return email
    # Store user data in the database (replace this with actual storage logic)
    # users_db[user_id] = {'email': email, 'password': password}

    # Redirect to the user's profile page upon successful registration
    return redirect(url_for('user_profile', user_id=user_id))

if __name__ == '__main__':
    app.run(debug=True)