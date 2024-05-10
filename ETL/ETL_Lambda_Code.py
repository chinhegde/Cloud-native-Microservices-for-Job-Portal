import json
import boto3
import pandas as pd
from datetime import date, timedelta, datetime
import random
import io
import csv
import mysql.connector as mysql

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
jobPostingsTable = dynamodb.Table('job_postings')

def lambda_handler(event, context):
    # TODO implement
    #print(event)
    bucket = event['Records'][0]['s3']['bucket']['name']
    file = event['Records'][0]['s3']['object']['key']
    #print(bucket, ' - ', file)
    '''
    response = s3.get_object(Bucket=bucket, Key=file)
    print(response)

    df = pd.read_csv(response['Body'].read())
    print(df.size)
    print(df.shape)
    print(df.head())
    
    response = s3.head_object(Bucket=bucket, Key=file)
    file_size = response['ContentLength']
    offset = 0
    chunk_size=1024 * 1024
    
    while offset < file_size:
        end = min(offset + chunk_size, file_size)
        chunk = s3.get_object(Bucket=bucket, Key=file, Range=f'bytes={offset}-{end-1}')['Body']
        chunk_data = chunk.read().decode('utf-8')
        
        if offset == 0:
            df = pd.read_csv(StringIO(chunk_data))
        else:
            chunk_df = pd.read_csv(StringIO(chunk_data))
            df = df.append(chunk_df, ignore_index=True)
            
        offset = end
    '''
    
    rowList = []
    response = s3.get_object(Bucket=bucket, Key=file)
    #print(response)
    stream_wrapper = io.TextIOWrapper(response['Body'], encoding='utf-8')
    csv_reader = csv.reader(stream_wrapper)
    headers = next(csv_reader)
    dict_reader = csv.DictReader(stream_wrapper, fieldnames=headers)
    
    for row in dict_reader:
        #print(row)
        rowList.append(row)
        
    df = pd.DataFrame(rowList, columns=headers)
    
    #print(df.shape)
    #print(df.head())
    
    # Synthesize job posted date and expiry date
    start_date = date(2024, 4, 15)
    end_date = date(2024, 6, 30)
    delta = end_date - start_date
    
    today = date.today()
    currentDate = today.strftime("%m%d%y")
    time = datetime.now()
    currentTime = time.strftime("%H%M%S")
    id = 0

    jobID = []
    posted_date = []
    expire_date = []
    max_salary = []
    min_salary = []
    company_website = []
    job_url = []
        
    for index, row in df.iterrows():
        start_random_number = random.randint(1, delta.days-16)
        end_random_number = random.randint(start_random_number+15, delta.days+1)
        posted_date.append(start_date + timedelta(days=start_random_number))
        expire_date.append(start_date + timedelta(days=end_random_number))
        id = id + 1
        jobID.append(str(currentDate) + str(currentTime) + str(id))
        
        if 'max_salary' not in df.columns and 'salary' in df.columns:
            max_salary.append(row['salary'])
        elif 'max_salary' not in df.columns and 'salary' not in df.columns:
            max_salary.append(' ')
        if 'min_salary' not in df.columns and 'salary' in df.columns:
            min_salary.append(row['salary'])
        elif 'min_salary' not in df.columns and 'salary' not in df.columns:
            min_salary.append(' ')

        if 'company_website' not in df.columns:
            company_website.append(' ')
            
        if 'job_url' not in df.columns:
            job_url.append(' ')
            

    df['job_id'] = jobID
    df['job_posted_date'] = posted_date
    df['job_expiration_date'] = expire_date
    
    if 'company_website' not in df.columns:
        df['company_website'] = company_website
        
    if 'job_url' not in df.columns:
        df['job_url'] = job_url
    
    if 'max_salary' not in df.columns:
        df['max_salary'] = max_salary
    if 'min_salary' not in df.columns:
        df['min_salary'] = min_salary
            
    
    df = df[['job_id'] + [col for col in df.columns if col != 'job_id']]
    df['max_salary'] = df['max_salary'].fillna(' ')
    df['min_salary'] = df['min_salary'].fillna(' ')
    df['company_website'] = df['company_website'].fillna(' ')
    df['job_url'] = df['job_url'].fillna(' ')
    df['job_description'] = df['job_description'].fillna(' ')
    #pd.set_option('max_columns', None)
    #print(df.shape)
    #print(df.head())
    
    for index, row in df.iterrows():
        print(row['job_id'])
        db_response = jobPostingsTable.put_item(
            Item={
                'job_id': str(row['job_id']),
                'job_title': str(row['job_title']),
                'job_description': str(row['job_description']),
                'max_salary': str(row['max_salary']),
                'min_salary': str(row['min_salary']),
                'job_location': str(row['job_location']),
                'job_url': str(row['job_url']),
                'company_name': str(row['company_name']),
                'company_website': str(row['company_website']),
                'job_posted_date': str(row['job_posted_date']),
                'job_expiration_date': str(row['job_expiration_date'])
            })
            
    print("Loaded to table")
    
    '''
    connection=mysql.connect (host="jobpostdb.cfukwk80s47c.us-west-1.rds.amazonaws.com", user="admin", password="admin123", database="JobPostingsDB")
    cursor=connection.cursor()
    query = "insert into JobPostingsTable(job_id, job_title, job_description, salary, job_location, job_url, company_name, company_website, job_posted_date, job_expiry_date) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, df.values.tolist())
    connection.commit()
    connection.close()
    '''
    
    return {
        'statusCode': 200,
        'body': json.dumps('ETL completed!')
    }
