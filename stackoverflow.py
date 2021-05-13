import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python&sort=p"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(html):
    title = html.find("h2").find("a")["title"]
    company = html.find("h3").find("span").get_text(strip=True)
    location = (
        html.find("h3").find("span", {"class": "fc-black-500"}).get_text(strip=True)
    )
    link = html.find("h2").find("a")["href"]
    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://stackoverflow.com{link}",
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(1, last_page + 1):
        page = 1
        result = requests.get(f"{URL}&pg={page}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "grid--cell fl1"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
