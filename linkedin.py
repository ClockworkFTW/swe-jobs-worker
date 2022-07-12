from selenium.webdriver.common.by import By
import dateparser
import datetime
import time

from db import session, Job

def scrape_linkedin(browser, url):

    # Load page
    browser.get(url)

    # Get job count
    job_count = browser.find_element(By.CLASS_NAME, "results-context-header__job-count").get_attribute("textContent").strip()
    job_count = job_count.replace("+", "")
    job_count = job_count.replace(",", "")

    # Get page count
    page_count = int(int(job_count)/25)

    print(f"Found {page_count} pages\n")

    # Load jobs
    for i in range(page_count):

        print(f"Loading page {i + 1}/{page_count}...\n")
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        try:
            browser.find_element(By.CLASS_NAME, "infinite-scroller__show-more-button--visible").click()
            time.sleep(2)

        except:
            pass
            time.sleep(2)

    # Scrape jobs
    jobs = browser.find_element(By.CLASS_NAME, "jobs-search__results-list").find_elements(By.TAG_NAME, "li")
    print(f"Found {len(jobs)} jobs\n")

    success_count = 0

    for i in range(len(jobs)):
        
        try:
            
            print(f"Scraping job {i + 1}/{len(jobs)}...")

            # Load job details
            jobs[i].click()
            time.sleep(2)

            # Scrape job details
            link = browser.find_element(By.XPATH, "/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/a").get_attribute("href")
            date = browser.find_element(By.XPATH, "/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[2]/span").get_attribute("textContent")
            title = browser.find_element(By.XPATH, "/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/a/h2").get_attribute("textContent")
            company = browser.find_element(By.XPATH, "/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[1]/span[1]/a").get_attribute("textContent")
            location = browser.find_element(By.XPATH, "/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[1]/span[2]").get_attribute("textContent")
            description = browser.find_element(By.XPATH, "/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/div").get_attribute("innerHTML")

            try:

                job = Job(
                    id=int(link.split("?")[0][-10:]),
                    link=link.split("?")[0],
                    title=title.strip(),
                    company=company.strip(),
                    location=location.strip(),
                    description=description.strip(),
                    date=dateparser.parse(date.strip()),
                    createdAt=datetime.datetime.now(),
                    updatedAt=datetime.datetime.now(),
                )

                session.add(job)
                session.commit()

                success_count = success_count + 1
                print("Success\n")

            except:
                
                session.rollback()
                print("Error: postgres\n")

        except: 
            
            print("Error: selenium\n")
        
    print (f"{success_count}/{len(jobs)} jobs scrapped successfully!")