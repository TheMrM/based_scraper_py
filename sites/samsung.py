from scraper_peviitor import Scraper, Rules, loadingData, ScraperSelenium
from selenium.webdriver.common.by import By

import time
import uuid
import os


#Folosim ScraperSelenium dewoarece nu putem accesa paginatia prin BeautifulSoup
scraper = ScraperSelenium("https://sec.wd3.myworkdayjobs.com/Samsung_Careers?q=Romania")
scraper.get()

time.sleep(5)

#Cautam butonul de acceptare a cookie-urilor si il apasam
cookieBtn = scraper.find_element(By.CLASS_NAME, "css-yih7c7")
scraper.click(cookieBtn)

#Cautam numarul total de joburi si il impartim la 20 pentru a afla numarul de pagini
jobs = scraper.find_element(By.CLASS_NAME, "css-12psxof").text.split(" ")[0]

totalJobs = [*range(0, int(jobs), 20)]

finalJobs = list()

#Parcurgem fiecare pagina si extragem joburile
for page in range(len(totalJobs)):
    if page != 0:
        nextPage = scraper.find_element(By.CLASS_NAME, "css-1xuojeq")
        scraper.driver.execute_script("arguments[0].scrollIntoView();", nextPage)
        scraper.click(nextPage)
        time.sleep(3)

    doom = scraper.getDom()
    pageScraper = Scraper()
    pageScraper.soup = doom
    rules = Rules(pageScraper)

    jobs = rules.getTags("li", {"class": "css-1q2dra3"})
    for job in jobs:
        id = uuid.uuid4()
        job_title = job.find("a").text
        job_link = "https://sec.wd3.myworkdayjobs.com" + job.find("a")["href"]
        company = "Samsung"
        country = "Romania"
        city = "Romania"
        print(job_title + " -> " + city)

        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": country,
            "city": city,
        })

    time.sleep(3)

#Afisam numarul de joburi
print("Total jobs: " + str(len(finalJobs)))

#Incarcam joburile in baza de date
apikey = os.environ.get("apikey")
loadingData(finalJobs, apikey, "Samsung")