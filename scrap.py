import requests
from bs4 import BeautifulSoup

def github_scraper():
    URL = f"https://github.com/SMeydan?tab=repositories"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    repositories = soup.findAll('a', attrs={'itemprop':'name codeRepository'})

    for repo in repositories:
        name = repo.get_text().strip()
        link = f"https://github.com{repo['href']}"
        print(f"Name: {name}, Link: {link}")

github_scraper()  # replace 'username' with the GitHub username