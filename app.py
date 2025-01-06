from flask import Flask, render_template, request, jsonify, send_file
from io import BytesIO
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import pickle
import csv
import os

app = Flask(__name__)


def data_save(data):
    os.makedirs('data', exist_ok=True)
    with open('data/job_data.pickle', 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


def data_load():
    try:
        with open('data/job_data.pickle', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []


def is_relevant(api_key, sys_mission, desc):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": sys_mission},
            {"role": "user", "content": desc}
        ],
        temperature=1,
        max_tokens=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    res = 0
    try:
        res = int(response.choices[0].message.content)
    except ValueError as e:
        print(e)
    return res


def job_list(api_key, sys_mission, keywords, limit, forbidden_levels):
    explored_ids = data_load()
    jobs = []

    for keyword in keywords:
        for page in range(limit):
            url = f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keyword}&geoId=101620260&trk=public_jobs_jobs-search-bar_search-submit&start={page * 25}'
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                job_listings = soup.find_all('div', {'class': 'job-search-card'})
                for job in job_listings:
                    j = {
                        'Title': job.find('h3', {'class': 'base-search-card__title'}).text.strip(),
                        'Company': job.find('a', {'class': 'hidden-nested-link'}).text.strip(),
                        'Location': job.find('span', {'class': 'job-search-card__location'}).text.strip(),
                        'Href': job.find('a', class_='base-card__full-link')['href']
                    }
                    id_num = job["data-entity-urn"].split("urn:li:jobPosting:")[1].strip()
                    if id_num in explored_ids:
                        print("Job was already explored")
                        continue
                    explored_ids.append(id_num)
                    level, description = job_details(id_num)
                    if level in forbidden_levels:
                        print("Job level is forbidden")
                        continue
                    if not is_relevant(api_key, sys_mission, description):
                        print("Job no relevant")
                        continue
                    print(f"Job added: {j}")
                    jobs.append(j)
            else:
                print("Failed to fetch job listings.")
    data_save(explored_ids)
    return jobs


def job_details(id_num):
    url = f'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{id_num}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        level = soup.find('span', {'class': 'description__job-criteria-text'}).text.strip()
        desc = soup.find('div', {'class': 'show-more-less-html__markup'}).text.strip()
        return level, desc
    else:
        print("Failed to fetch job details.")
        return "Director", "Description"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        api_key = request.form['api_key']
        keywords = request.form.getlist('keywords')
        description = request.form['description']

        # Get selected job levels
        selected_levels = request.form.getlist('job_levels')

        # Create forbidden levels based on what was NOT selected
        all_levels = ['Internship', 'Entry level', 'Mid-Senior level', 'Director', 'Executive']
        forbidden_levels = [level for level in all_levels if level not in selected_levels]

        mission = (
            "You will be provided with a job description from LinkedIn and your goal is to determine if it's applicable "
            "by returning 0 (not applicable) or 1 (applicable), do not return anything else. A job is applicable if it match"
            "the following criteria:\n")
        sys_mission = mission + description + ("\nOnce again, you are only allowed to answer only with one character: "
                                               "0 or 1.")

        # Fetch the job listings based on the user inputs
        results = job_list(api_key, sys_mission, keywords, limit=6, forbidden_levels=forbidden_levels)
        return render_template('index.html', results=results)

    return render_template('index.html', results=[])


if __name__ == '__main__':
    app.run(debug=True)