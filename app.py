from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import requests
import os
import boto3
from boto3.dynamodb.conditions import Key
import jwt
import sys

app = Flask(__name__)
cognito_client = boto3.client('cognito-idp', region_name='us-west-1')
dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
userTable = dynamodb.Table('users')

jobsTable = dynamodb.Table('job_postings')
response = jobsTable.scan()
jobs_data = response['Items']

applicationsTable = dynamodb.Table('applications')


@app.route('/')
def login():  
    return render_template('index.html', public_ip=publicIP)

@app.route('/search', methods=['GET', 'POST'])
def search():
    locs = set([item['job_location'] for item in jobs_data])

    keyword = request.form.get('keyword') if request.method == 'POST' else request.args.get('keyword')
    location = request.form.get('location') if request.method == 'POST' else request.args.get('location')


    filtered_jobs = []

    if request.method == 'GET': 
        filtered_jobs = jobs_data
    else:
        if location != "Location":
            print("DEBUG ONE")
            if keyword:
                for job in jobs_data:
                    if keyword.lower() in job['job_title'].lower() or keyword.lower() in job['job_description'].lower():
                        if job['job_location'] == location:
                            filtered_jobs.append(job)
            else:
                for job in jobs_data:
                    if job['job_location'] == location:
                        filtered_jobs.append(job)
        elif keyword and location == "Location":
            if keyword:
                for job in jobs_data:
                    if keyword.lower() in job['job_title'].lower() or keyword.lower() in job['job_description'].lower():
                        filtered_jobs.append(job)

        else:
            filtered_jobs = jobs_data

    return render_template('job-list.html', jobs=filtered_jobs, locs = locs)

@app.route('/user-profile')
def user(): 
    return render_template('user-profile.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/user') 
def user_profile():
    authorization_code = request.args.get('code')
    print(authorization_code)
    redirect_url = 'https://' + publicIP + '/user'
    print(redirect_url)

    if authorization_code:
        access_token_url = f'https://jobsearch.auth.us-west-1.amazoncognito.com/oauth2/token'
        query_parms = {
            'grant_type': 'authorization_code',
            'client_id': '7jtg9vv6jrc03a1clorb2s4d4r',
            'redirect_uri': redirect_url,
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
                    if attribute['Name'] == 'email':
                        email = attribute['Value']
                    if attribute['Name'] == 'birthdate':
                        birthdate = attribute['Value']

            print(email)
            db_response = userTable.get_item(Key={'email':email})
            if 'Item' in db_response:
                if 'email' in db_response['Item']:
                    user_email = db_response['Item']['email']
                    print(user_email)
                    if user_email:
                        if user_email == email:
                            return redirect('/search')

            return render_template('user-registration.html', user=name, email=email, dob=birthdate)
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

@app.route('/register', methods=['POST'])
def user_registeration():
    print(request.form.values)
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    birth_date = request.form.get('dob')
    address_line_1 = request.form.get('address_line_1')
    address_line_2 = request.form.get('address_line_2')
    postcode = request.form.get('postcode')
    country = request.form.get('country')
    state = request.form.get('state')
    education = request.form.get('education')
    experience = request.form.get('experience')
    skills = request.form.get('skills')
    recruiter = request.form.get('recruiter')
    website = request.form.get('website')
    github_link = request.form.get('github_link')

    db_response = userTable.put_item(
        Item={
            'full_name': str(full_name),
            'email': str(email),
            'phone': str(phone),
            'birth_date': str(birth_date),
            'address_line_1': str(address_line_1),
            'address_line_2': str(address_line_2),
            'postcode': str(postcode),
            'country': str(country),
            'state': str(state),
            'education': str(education),
            'experience': str(experience),
            'skills': str(skills),
            'recruiter': bool(recruiter),
            'website': str(website),
            'github_link': str(github_link)
        })
    print(db_response)
    return redirect('/search')

@app.route('/jobs/<job_id>') 
def job_details(job_id):
    response = jobsTable.query(
        KeyConditionExpression=Key('job_id').eq(job_id)
    )
    job = response.get('Items', [None])[0]
    if job:
        return render_template('job-details.html', job=job)
    else:
        return "Job not found", 404
    
@app.route('/apply/<job_id>') 
def apply(job_id):
    response = jobsTable.query(
        KeyConditionExpression=Key('job_id').eq(job_id)
    )
    job = response.get('Items', [None])[0]
    if job:
        return render_template('apply.html', job=job)
    else:
        return "Job not found", 404
    
@app.route('/post-job') 
def post_job():
    return render_template('post-job.html')
    
@app.route('/submitapp/<job_id>', methods=['POST'])
def submit_application(job_id):
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    phone = request.form.get('phone')

    application = {
        'job_id': job_id,
        'full_name': full_name,
        'email': email,
        'phone': phone,
    }

    applicationsTable.put_item(Item = application)

    return render_template('thankyou.html')

@app.route('/createjob', methods=['POST'])
def create_job():
    
    job_title = request.form['job_title']
    job_description = request.form['job_description']
    min_salary = int(request.form['min_salary'])
    max_salary = int(request.form['max_salary'])
    job_location = request.form['job_location']
    company_name = request.form['company_name']
    company_url = request.form['company_url']
    job_posted_on = request.form['job_posted_on']
    
    job_id = len(jobs_data) + 1
    
    new_job = {
        "job_id": str(job_id),
        "job_title": job_title,
        "job_description": job_description,
        "min_salary": min_salary,
        "max_salary": max_salary,
        "job_url": "/apply/{}".format(job_id),
        "job_location": job_location,
        "company_name": company_name,
        "company_url": company_url,
        "job_posted_on": job_posted_on
    }
    
    jobsTable.put_item(Item=new_job)
    
    return render_template('posted.html', job_id = str(job_id))

if __name__ == '__main__':
    publicIP = sys.argv[1]
    publicIP = publicIP.strip()
    print(publicIP)
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 9001)), ssl_context='adhoc')
    # app.run(debug=True)