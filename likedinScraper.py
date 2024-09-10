import requests 
from bs4 import BeautifulSoup
import pandas as pd 
import time
import random
import re 

def extract_number(text):
    match= re.search(r"\d+", text)
    if match:
        return int(match.group())
    return None

def likedIn_numOffert_scraper(url): 
    response= requests.get(url)
    text_page= response.text
    parse_data = BeautifulSoup(text_page, 'html.parser')
    num_offerts= parse_data.find("span", {"class": "results-context-header__job-count"}).text
    return num_offerts

def linkedin_scraper(tittle="RPA", location="Poland", how_pages=0):
    
    num_page = 0
    list_page_jobs = []
    id_list =[]
    job_list = []
    Checking=0 
    time_sleep=1
    all_offerts= likedIn_numOffert_scraper(f"https://www.linkedin.com/jobs/search?keywords={tittle}&location={location}&trk=public_jobs_jobs-search-bar_search-submit&pageNum=0&position=1")
    
   
    
    while num_page <= how_pages*25:
        url=f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={tittle}&location={location}&start={num_page}"
        response = requests.get(url)
        list_page_jobs.append(response.text)
        num_page += 25
        
    print(len(list_page_jobs))
    for list_data in list_page_jobs:
        list_data= BeautifulSoup(list_data, 'html.parser')
        page_jobs= list_data.find_all("li")
        
        for job in page_jobs: 
            base_card_div =job.find("div",{"class": "base-card"})
            job_id= base_card_div.get("data-entity-urn").split(":")[3]
            print(job_id)
            id_list.append(job_id)
    
    for job_id in id_list:
        job_url=f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
        
        while True:
            job_response = requests.get(job_url)
            print(job_response.status_code)
            
            if job_response.status_code == 200:
                Checking=0
                break
            
            if  job_response.status_code == 429:
                time_sleep = random.uniform(1, 5)
                print(f"Coun Check {Checking} this {job_id} time sleep {time_sleep}")
                time.sleep(time_sleep)
                Checking +=1
                
        job_soup = BeautifulSoup(job_response.text,"html.parser")
        
        # WRITING TO FILE TO DEBUG
        # with open("job_soup.txt", "a", encoding="utf-8") as file:
        #     file.write(str(job_soup)+"\n")
        
        job_post= {}
        
        job_post["job_link"] = job_url
        job_post["job_id"] = job_id
        try:   
            job_post["job_title"] = job_soup.find("h2", {"class":"top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title"}).text.strip()
        except:  
            job_post["job_title"] = None
        try:
            job_post["company_name"] = job_soup.find("a", {"class":"topcard__org-name-link topcard__flavor--black-link"}).text.strip()
        except:
            job_post["company_name"]  = None
        try:           
            job_post["time_posted"] = job_soup.find("span", {"class":"posted-time-ago__text topcard__flavor--metadata"}).text.strip()
        except:
            job_post["time_posted"]  = None
        try:
            num_applicants_span = job_soup.find("span", {"class": "num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet"})
            if num_applicants_span and num_applicants_span.text.strip():
                job_post["num_applicatns"] = extract_number(num_applicants_span.text.strip())
                print(job_post["num_applicatns"])
            else:
                num_applicants_figcaption = job_soup.find("figcaption", {"class": "num-applicants__caption"})
                if num_applicants_figcaption and num_applicants_figcaption.text.strip():
                    job_post["num_applicatns"] = extract_number(num_applicants_figcaption.text.strip()) 
                    print(job_post["num_applicatns"])
                else:
                    job_post["num_applicatns"] = None
        except Exception as e:
            print("Error:", e)
            job_post["num_applicatns"] = None
        
        job_list.append(job_post)
            
           


    # print(BeautifulSoup(list_data, 'html.parser'))

    job_df = pd.DataFrame(job_list)
    job_df.to_csv("linkedin_jobs.csv",index=False)
  
    return job_list



print(likedIn_numOffert_scraper("https://www.linkedin.com/jobs/search?keywords=RPA&location=Poland&trk=public_jobs_jobs-search-bar_search-submit&pageNum=0&position=1"))
# linkedin_scraper()
        