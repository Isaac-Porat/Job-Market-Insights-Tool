import time
import pandas as pd
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scroll_down_entire_page(driver: WebDriver, timeout: int):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    time.sleep(timeout)

def scrape_indeed_jobs(position: str, location: str, page_count: int):
    base_url = f"https://www.indeed.com/jobs?q={position}&l={location}"

    options = Options()
    # options.add_argument("headless=new")

    driver = WebDriver(options=options)

    driver.get(base_url)

    wait = WebDriverWait(driver, 10)

    # waiting for the page to load
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "job_seen_beacon")))

    scroll_down_entire_page(driver, 3) # 3 second timeout after page scroll

    posts = driver.find_elements(By.class_name, "job_seen_beacon")

    a_tags = posts.find_elements(By.TAG_NAME, "a")

    for element in a_tags:
        href = element.get_attribute("href")
        print(href)

    time.sleep(1)

    driver.quit()

def main():
    position = "softwareenginner"
    page_count = 1

    data = scrape_indeed_jobs(position, "boston", page_count)

    # df = pd.DataFrame(data, columns=["title", "citation", "description", "url"])
    # df.to_csv(f"{query}.csv", index=False)

if __name__ == "__main__":
    main()