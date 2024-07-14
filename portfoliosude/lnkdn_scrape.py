from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import requests
import os
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
def scrape_linkedin():
    chrome_driver_path = 'C:\\Users\\suden\\Downloads\\chromedriver-win32\\chromedriver-win32\\chromedriver.exe'
    chrome_options = Options()
    
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    profile_url = 'https://www.linkedin.com/in/sudenur-meydan/'

    driver.get(profile_url)
    time.sleep(5)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Scrape Experience Section
    experience_section = soup.find_all('section', {'class': 'core-section-container'})
    experiences = []

    for section in experience_section:
        if 'experience' in section.get('class', []):
            print("Experience Section Found")
            experience_list = section.find_all('li', {'class': 'profile-section-card'})
            for experience in experience_list:
                job_title = experience.find('h3').get_text(strip=True) if experience.find('h3') else 'N/A'
                dates = experience.find('span', {'class': 'date-range'}).get_text(strip=True) if experience.find('span', {'class': 'date-range'}) else 'N/A'
                company_url = experience.find('a')['href']
                company = (company_url.split('company/')[1].split('?')[0].replace('-',' ')).capitalize() if 'company' in company_url else 'N/A'

                experiences.append({
                    'job_title': job_title,
                    'company_url': company,
                    'dates': dates
                })

    for exp in experiences:
        print(f"Job Title: {exp['job_title']}, Company URL: {exp['company_url']}, Dates: {exp['dates']}")

    # Scrape Education Section
    education_section = soup.find_all('section', {'class': 'education-section'})
    education_list = []

    for section in education_section:
        print("Education Section Found")
        edu_list = section.find_all('li', {'class': 'profile-section-card'})
        for edu in edu_list:
            school_name = edu.find('h3').get_text(strip=True) if edu.find('h3') else 'N/A'
            degree = edu.find('span', {'class': 'degree-name'}).get_text(strip=True) if edu.find('span', {'class': 'degree-name'}) else 'N/A'
            field_of_study = edu.find('span', {'class': 'field-of-study'}).get_text(strip=True) if edu.find('span', {'class': 'field-of-study'}) else 'N/A'
            dates = edu.find('span', {'class': 'date-range'}).get_text(strip=True) if edu.find('span', {'class': 'date-range'}) else 'N/A'

            education_list.append({
                'school_name': school_name,
                'degree': degree,
                'field_of_study': field_of_study,
                'dates': dates
            })

    for edu in education_list:
        print(f"School Name: {edu['school_name']}, Degree: {edu['degree']}, Field of Study: {edu['field_of_study']}, Dates: {edu['dates']}")

    driver.quit()
    return experiences, education_list

def get_github_profile():
    username = "SMeydan"
    url = f"https://api.github.com/users/{username}"

    response = requests.get(url)
    if response.status_code == 200:
        profile_data = response.json()
        print(f"Name: {profile_data['name']}")
        print(f"Company: {profile_data['company']}")
        print(f"Location: {profile_data['location']}")
        print(f"Bio: {profile_data['bio']}")
        print(f"Public Repos: {profile_data['public_repos']}")
        print(f"Followers: {profile_data['followers']}")
        print(f"Following: {profile_data['following']}")
    else:
        print(f"Failed to retrieve profile: {response.status_code}")

    url = f"https://api.github.com/users/{username}/repos"

    response = requests.get(url)
    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            print(f"Repo Name: {repo['name']}")
            print(f"Repo URL: {repo['html_url']}")
            print(f"Description: {repo['description']}")
            print(f"Stars: {repo['stargazers_count']}")
            print(f"Forks: {repo['forks_count']}")
            print()
    else:
        print(f"Failed to retrieve repositories: {response.status_code}")

    return profile_data, repos

def get_google_drive_files():

    CLIENT_SECRET_FILE = 'portfoliosude\secret.json'
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    REDIRECT_URI = 'http://localhost:8080/'

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            flow.redirect_uri = REDIRECT_URI
            creds = flow.run_local_server(port=8080)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(f"{item['name']} ({item['id']})")
