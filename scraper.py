from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Import scraping tasks
from linkedin import scrape_linkedin

# Setup chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=2560,1440")

# Setup webdriver service
webdriver_service = Service("./chromedriver")

# Choose Chrome Browser
browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# Setup sites config
sites = {
    "LINKEDIN": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=San%20Francisco%20Bay%20Area&locationId=&geoId=90000084&f_TPR=r604800&f_JT=F&f_E=2&position=1&pageNum=0",
    "INDEED": "",
    "GLASSDOOR": ""
}

# Scrape sites
for site in sites:
    if site == "LINKEDIN":
        scrape_linkedin(browser, sites[site])
    if site == "INDEED":
        pass
    if site == "GLASSDOOR":
        pass
