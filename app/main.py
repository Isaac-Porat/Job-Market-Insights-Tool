import time
import json
import os
from typing import List

import pandas as pd
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

CACHE_FILE = 'job_cache.json'

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)

def extract_vjk(url):
    vjk = url.split("vjk=")[1]
    return vjk

def scrape_indeed_jobs(position: str, location: str, page_count: int) -> List:
    base_url = f"https://www.indeed.com/jobs?q={position}&l={location}"

    options = Options()
    # options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = WebDriver(options=options)

    post_data = set()

    try:
        driver.get(base_url)

        cache = load_cache()

        wait = WebDriverWait(driver, 10)

        # waiting for url to load
        wait.until(EC.url_contains("vjk="))

        current_url = driver.current_url

        print(f"Scraping URL: {current_url}")

        vjk = extract_vjk(current_url)

        if vjk in cache:
            print(f"{vjk} found in cache, skipping url...")
            driver.quit()
            return cache[vjk]

        posts = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")

        for post in posts:
            a_tag = post.find_element(By.TAG_NAME, "a")

            href = a_tag.get_attribute("href")

            post_data.add(href)

    except Exception as e:
        print(f"Error scraping {base_url}: {e}")

    finally:
        driver.quit()

    cache[vjk] = list(post_data)
    save_cache(cache)

    return list(post_data)

def scrape_job_posts(url: str):

    options = Options()
    # options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = WebDriver(options=options)

    try:
        driver.get(url)
        print(f"Scraping URL: {url}")

        # wait = WebDriverWait(driver, 10)

        try:
            title = driver.find_element(By.TAG_NAME, "h1").text
        except NoSuchElementException:
            title = None

        try:
            company_name = driver.find_element(By.CLASS_NAME, "jobsearch-CompanyReview--heading")
            company_name = company_name.get_attribute("innerHTML")
        except NoSuchElementException:
            company_name = None

        try:
            location = driver.find_element(By.CLASS_NAME, "css-waniwe").text
        except NoSuchElementException:
            location = None

        try:
            salary = driver.find_element(By.CLASS_NAME, "css-19j1a75").text
        except NoSuchElementException:
            salary = None

        try:
            description = driver.find_element(By.ID, "jobDescriptionText").text
        except NoSuchElementException:
            description = None

    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return {}

    finally:
        driver.quit()

    return {
        "url": url,
        "title": title,
        "company_name": company_name,
        "location": location,
        "salary": salary,
        "description": description
    }


def main():
    position = "software+engineer"
    page_count = 1

    job_urls = scrape_indeed_jobs(position, "boston", page_count)

    post_data = []

    for url in job_urls:
        job_details = scrape_job_posts(url)
        post_data.append(job_details)

    df = pd.DataFrame(post_data)
    df.to_csv(f"{position.replace('+', '_')}.csv", index=False)

if __name__ == "__main__":
    main()