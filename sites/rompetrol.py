from scraper_peviitor import Scraper, Rules, loadingData
import uuid

#Cream o instanta a clasei Scraper
url = "https://careers.rompetrol.com/search/?q=&locationsearch=Romania"
scraper = Scraper(url)
rules = Rules(scraper)

#Obtinem numarul total de joburi
jobs = int(rules.getTag("span", {"class": "paginationLabel"}).find_all("b")[1].text)

#Cream o lista cu toate query-urile
queryList = [*range(0, jobs, 25)]

finaljobs = list()

#Iteram prin fiecare query
for query in queryList:
    #Setam url-ul paginii curente
    url = "https://careers.rompetrol.com/search/?q=&locationsearch=Romania&startrow=" + str(query)
    scraper.url = url

    #Luam toate joburile de pe pagina curenta
    jobs = rules.getTags("tr", {"class": "data-row"})

    #Iteram prin fiecare job
    for job in jobs:
        id = uuid.uuid4()
        job_title = job.find("a").text
        job_link = "https://careers.rompetrol.com" + job.find("a")["href"]
        company = "Rompetrol"
        country = "Romania"
        city = job.find("span", {"class": "jobLocation"}).text.split(",")[0].strip()
        print(job_title + " -> " + city)

        finaljobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": country,
            "city": city
        })

#Afisam numarul total de joburi
print("Total jobs: " + str(len(finaljobs)))

#Incarcam datele in baza de date
loadingData(finaljobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", "Rompetrol")