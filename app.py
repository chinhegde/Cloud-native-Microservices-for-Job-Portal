from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import requests
import os
import boto3
import jwt

app = Flask(__name__)
cognito_client = boto3.client('cognito-idp', region_name='us-west-1')

with open('jobs.json', 'r') as jobs_file:
    jobs_data = json.load(jobs_file)
    print(jobs_data.keys())

@app.route('/')
def login():  
    return render_template('index.html')

@app.route('/search')
def search(): 
    return render_template('job-list.html', jobs = jobs_data['jobs'])

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/user') 
def user_profile():
    authorization_code = request.args.get('code')
    print(authorization_code)

    if authorization_code:
        access_token_url = f'https://jobsearch.auth.us-west-1.amazoncognito.com/oauth2/token'
        query_parms = {
            'grant_type': 'authorization_code',
            'client_id': '7jtg9vv6jrc03a1clorb2s4d4r',
            'redirect_uri': 'http://localhost:9001/user',
            'scope': 'aws.cognito.signin.user.admin',
            'code': authorization_code
        }
        response = requests.post(access_token_url, data=query_parms)
        if response.status_code == 200:
            access_token = response.json().get('access_token')
            '''
            decoded_token = decode_access_token(access_token)
            if decoded_token:
                print("Decoded Token:")
                print(decoded_token)
            else:
                print("Failed to decode token.")
            '''
            user_info = get_user_info(access_token)
            if user_info:
                for attribute in user_info:
                    if attribute['Name'] == 'name':
                        name = attribute['Value']
            return ('Welcome ' + name)
        else:
            return 'Failed to exchange authorization code for access token'
    else:
        return 'Authorization code not found in query parameters'

def decode_access_token(access_token):
    try:
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})
        return decoded_token
    except jwt.DecodeError as e:
        print("Error decoding token:", e)
        return None

def get_user_info(access_token):
    try:
        response = cognito_client.get_user(AccessToken=access_token)
        print(response['UserAttributes'])
        return response['UserAttributes']
    except Exception as e:
        print("Error:", e)
        return None

@app.route('/jobs/<int:job_id>') 
def job_details(job_id):
    job = next((job for job in jobs_data['jobs'] if job['job_id'] == job_id), None)
    if job:
        return render_template('job-details.html', job=job)
    else:
        return "Job not found", 404

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 9001)))