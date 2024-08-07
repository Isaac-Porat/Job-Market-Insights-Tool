import time
import pandas as pd
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_indeed_jobs(position: str, location: str, page_count: int):
    base_url = f"https://www.indeed.com/jobs?q={position}&l={location}"

    options = Options()
    # options.add_argument("headless=new")

    driver = WebDriver(options=options)

    driver.get(base_url)

    wait = WebDriverWait(driver, 10)

    # waiting for the page to load
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "job_seen_beacon")))

    post_data = set()

    posts = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")

    for post in posts:
        a_tag = post.find_element(By.TAG_NAME, "a")

        href = a_tag.get_attribute("href")

        post_data.add(href)

    driver.quit()

    print(len(post_data))
    print(post_data)

def main():
    position = "softwareenginner"
    page_count = 1

    data = scrape_indeed_jobs(position, "boston", page_count)

    # df = pd.DataFrame(data, columns=["title", "citation", "description", "url"])
    # df.to_csv(f"{query}.csv", index=False)

if __name__ == "__main__":
    main()