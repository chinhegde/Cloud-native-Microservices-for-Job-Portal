import pandas as pd

def dataCleaning_multipleFiles(job_file, company_file, salary_file, out_file):
    #job_df = pd.DataFrame
    #company_df = pd.DataFrame
    #salary_df = pd.DataFrame

    #if not job_file:
    job_df = pd.read_csv(job_file, header=0)
    #print(job_df.columns)
    
    #if company_file != '':
    company_df = pd.read_csv(company_file, header=0)

    #if salary_file != '':
    salary_df = pd.read_csv(salary_file, header=0)
    #print(len(salary_df))
    #print(salary_df.columns)

    if 'max_salary' in job_df.columns and 'max_salary' in salary_df.columns:
        job_df = job_df.drop('max_salary', axis=1)

    if 'med_salary' in job_df.columns and 'med_salary' in salary_df.columns:
        job_df = job_df.drop('med_salary', axis=1)

    if 'min_salary' in job_df.columns and 'min_salary' in salary_df.columns:
        job_df = job_df.drop('min_salary', axis=1)

    if 'pay_period' in job_df.columns and 'pay_period' in salary_df.columns:
        job_df = job_df.drop('pay_period', axis=1)

    if 'currency' in job_df.columns and 'currency' in salary_df.columns:
        job_df = job_df.drop('currency', axis=1)


    company_name = []
    min_salary = []
    max_salary = []
    med_salary = []
    pay_period = []
    currency = []
    for index, row in job_df.iterrows():
        #print(row)
        if 'job_id' in job_df.columns:
            job_id = row['job_id']
        #print(job_id)
        if company_file != "" and 'company_id' in job_df.columns and 'company_id' in company_df.columns and 'name' in company_df.columns:
            company_id = row['company_id']
            company_row = company_df.loc[company_df['company_id'] == company_id]
            if 'name' in company_df.columns and not company_row['name'].empty:
                company_name.append(company_row['name'].values[0])
            else:
                    company_name.append(' ')

        if salary_file != "":
            if 'job_id' in salary_df.columns:
                salary_row = salary_df.loc[salary_df['job_id'] == job_id]
                #print(salary_row)

                if 'min_salary' in salary_df.columns and not salary_row['min_salary'].empty:
                    min_salary.append(salary_row['min_salary'].values[0])
                else:
                    min_salary.append(' ')

                if 'max_salary' in salary_df.columns and not salary_row['max_salary'].empty:
                    max_salary.append(salary_row['max_salary'].values[0])
                else:
                    max_salary.append(' ')

                if 'med_salary' in salary_df.columns and not salary_row['med_salary'].empty:
                    med_salary.append(salary_row['med_salary'].values[0])
                else:
                    med_salary.append(' ')

                if 'pay_period' in salary_df.columns and not salary_row['pay_period'].empty:
                    pay_period.append(salary_row['pay_period'].values[0])
                else:
                    pay_period.append(' ')

                if 'currency' in salary_df.columns and not salary_row['currency'].empty:
                    currency.append(salary_row['currency'].values[0])
                else:
                    currency.append(' ')

    print(len(job_df))
    print(len(company_name))
    print(len(min_salary))
    print(len(max_salary))
    print(len(pay_period))
    print(len(currency))
    job_df['company_name'] = company_name
    job_df['min_salary'] = min_salary
    job_df['max_salary'] = max_salary
    job_df['med_salary'] = med_salary
    job_df['pay_period'] = pay_period
    job_df['currency'] = currency


    if 'job_id' in job_df.columns:
        job_df = job_df.drop('job_id', axis=1)

    if 'title' in job_df.columns:
        job_df = job_df.rename(columns={'title': 'job_title'})

    if 'description' in job_df.columns:
        job_df = job_df.rename(columns={'description': 'job_description'})

    if 'location' in job_df.columns:
        job_df = job_df.rename(columns={'location': 'job_location'})

    if 'job_posting_url' in job_df.columns:
        job_df = job_df.rename(columns={'job_posting_url': 'job_url'})

    if 'application_url' in job_df.columns:
        job_df = job_df.rename(columns={'application_url': 'company_website'})

    job_df.to_csv(out_file, encoding='utf-8', index=False)

'''
    if 'company_id' in job_df.columns:
        job_df = job_df.drop('company_id', axis=1)

    if 'formatted_work_type' in job_df.columns:
        job_df = job_df.drop('formatted_work_type', axis=1)

    if 'applies' in job_df.columns:
        job_df = job_df.drop('applies', axis=1)

    if 'original_listed_time' in job_df.columns:
        job_df = job_df.drop('original_listed_time', axis=1)

    if 'remote_allowed' in job_df.columns:
        job_df = job_df.drop('remote_allowed', axis=1)

    if 'views' in job_df.columns:
        job_df = job_df.drop('views', axis=1)

    if 'application_url' in job_df.columns:
        job_df = job_df.drop('application_url', axis=1)

    if 'application_type' in job_df.columns:
        job_df = job_df.drop('application_type', axis=1)

    if 'expiry' in job_df.columns:
        job_df = job_df.drop('expiry', axis=1)

    if 'closed_time' in job_df.columns:
        job_df = job_df.drop('closed_time', axis=1)

    if 'formatted_experience_level' in job_df.columns:
        job_df = job_df.drop('formatted_experience_level', axis=1)

    if 'skills_desc' in job_df.columns:
        job_df = job_df.drop('skills_desc', axis=1)

    if 'listed_time' in job_df.columns:
        job_df = job_df.drop('listed_time', axis=1)

    if 'posting_domain' in job_df.columns:
        job_df = job_df.drop('posting_domain', axis=1)

    if 'sponsored' in job_df.columns:
        job_df = job_df.drop('sponsored', axis=1)

    if 'work_type' in job_df.columns:
        job_df = job_df.drop('work_type', axis=1)

    if 'compensation_type' in job_df.columns:
        job_df = job_df.drop('compensation_type', axis=1)

    if 'scraped' in job_df.columns:
        job_df = job_df.drop('scraped', axis=1)
'''

#dataCleaning_multipleFiles('../Dataset/dataset_1/job_postings.csv', '../Dataset/dataset_1/company_details/companies.csv', '../Dataset/dataset_1/job_details/salaries.csv', '../Dataset/cleaned_datasets/cleaned_dataset_1.csv')


def dataCleaning_twoFiles(job_file, company_file, out_file):
    jobs_df = pd.read_csv(job_file, header=0)
    #print(jobs_df.columns)
    
    companies_df = pd.read_csv(company_file, header=0)
    #print(companies_df.columns)

    company_name = []
    for index, row in jobs_df.iterrows():
        #print(row)
        if company_file != "" and 'company_id' in jobs_df.columns and 'company_id' in companies_df.columns and 'name' in companies_df.columns:
            company_id = row['company_id']
            company_row = companies_df.loc[companies_df['company_id'] == company_id]

            if company_row.empty:
                jobs_df = jobs_df.drop(index)
                #jobs_df = jobs_df.reset_index(inplace=True)
            else:
                if 'name' in companies_df.columns and not company_row['name'].empty:
                    company_name.append(company_row['name'].values[0])
                else:
                        company_name.append(' ')

    jobs_df['company_name'] = company_name


    if 'job_id' in jobs_df.columns:
        jobs_df = jobs_df.drop('job_id', axis=1)

    if 'title' in jobs_df.columns:
        jobs_df = jobs_df.rename(columns={'title': 'job_title'})

    if 'description' in jobs_df.columns:
        jobs_df = jobs_df.rename(columns={'description': 'job_description'})

    if 'location' in jobs_df.columns:
        jobs_df = jobs_df.rename(columns={'location': 'job_location'})

    if 'job_posting_url' in jobs_df.columns:
        jobs_df = jobs_df.rename(columns={'job_posting_url': 'job_url'})

    if 'application_url' in jobs_df.columns:
        jobs_df = jobs_df.rename(columns={'application_url': 'company_website'})

    jobs_df.to_csv(out_file, encoding='utf-8', index=False)

dataCleaning_twoFiles('../Dataset/dataset_9/job_postings.csv', '../Dataset/dataset_9/companies.csv', '../Dataset/cleaned_datasets/cleaned_dataset_9.csv')



def dataCleaning_singleFile(job_file, out_file):
    job_df = pd.read_csv(job_file, header=0)

    if 'jod_id' in job_df.columns:
        job_df = job_df.drop('job_id', axis=1)

    if 'company' in job_df.columns:
        job_df = job_df.rename(columns={'company': 'company_name'})

    if 'Company' in job_df.columns:
        job_df = job_df.rename(columns={'Company': 'company_name'})

    if 'Company Name' in job_df.columns:
        job_df = job_df.rename(columns={'Company Name': 'company_name'})

    if 'title' in job_df.columns:
        job_df = job_df.rename(columns={'title': 'job_title'})

    if 'Title' in job_df.columns:
        job_df = job_df.rename(columns={'Title': 'job_title'})

    if 'job' in job_df.columns:
        job_df = job_df.rename(columns={'job': 'job_title'})

    if 'Job Title' in job_df.columns:
        job_df = job_df.rename(columns={'Job Title': 'job_title'})

    if 'description' in job_df.columns:
        job_df = job_df.rename(columns={'description': 'job_description'})

    if 'Job Description' in job_df.columns:
        job_df = job_df.rename(columns={'Job Description': 'job_description'})

    if 'JobDescription' in job_df.columns:
        job_df = job_df.rename(columns={'JobDescription': 'job_description'})

    if 'job_details' in job_df.columns:
        job_df = job_df.rename(columns={'job_details': 'job_description'})

    if 'location' in job_df.columns:
        job_df = job_df.rename(columns={'location': 'job_location'})

    if 'Location' in job_df.columns:
        job_df = job_df.rename(columns={'Location': 'job_location'})

    if 'post_url' in job_df.columns:
        job_df = job_df.rename(columns={'post_url': 'job_url'})

    if 'hiring_person_link' in job_df.columns:
        job_df = job_df.rename(columns={'hiring_person_link': 'job_url'})

    if 'Apply Url' in job_df.columns:
        job_df = job_df.rename(columns={'Apply Url': 'job_url'})

    if 'sal_high' in job_df.columns:
        job_df = job_df.rename(columns={'sal_high': 'max_salary'})

    if 'sal_low' in job_df.columns:
        job_df = job_df.rename(columns={'sal_low': 'min_salary'})

    if 'Salary' in job_df.columns:
        job_df = job_df.rename(columns={'Salary': 'salary'})

    if 'avg_salary' in job_df.columns:
        job_df = job_df.rename(columns={'avg_salary': 'med_salary'})

    job_df.to_csv(out_file, encoding='utf-8', index=False)



#dataCleaning_singleFile('../Dataset/dataset_2/jobs.csv', '../Dataset/cleaned_datasets/cleaned_dataset_2.csv')
#dataCleaning_singleFile('../Dataset/dataset_3/marketing_sample_for_trulia_com-real_estate__20190901_20191031__30k_data.csv', '../Dataset/cleaned_datasets/cleaned_dataset_3.csv')
#dataCleaning_singleFile('../Dataset/dataset_5/data job posts.csv', '../Dataset/cleaned_datasets/cleaned_dataset_5.csv')
#dataCleaning_singleFile('../Dataset/dataset_7/linkdin_Job_data.csv', '../Dataset/cleaned_datasets/cleaned_dataset_7.csv')
#dataCleaning_singleFile('../Dataset/dataset_8/Cleaned_DS_Jobs.csv', '../Dataset/cleaned_datasets/cleaned_dataset_8.csv')
#dataCleaning_singleFile('../Dataset/dataset_10/data job posts.csv', '../Dataset/cleaned_datasets/cleaned_dataset_10.csv')