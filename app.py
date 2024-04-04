from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json

app = Flask(__name__)

with open('jobs.json', 'r') as jobs_file:
    jobs_data = json.load(jobs_file)
    print(jobs_data.keys())

# @app.route('/')
# def login(): 
#     return render_template('index.html')

@app.route('/')
def search(): 
    return render_template('job-list.html', jobs = jobs_data['jobs'])

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/user') 
def user_profile():
    return f'Welcome, user!'

@app.route('/jobs/<int:job_id>') 
def job_details(job_id):
    job = next((job for job in jobs_data['jobs'] if job['job_id'] == job_id), None)
    if job:
        return render_template('job-details.html', job=job)
    else:
        return "Job not found", 404

if __name__ == '__main__':
    app.run(debug=True)