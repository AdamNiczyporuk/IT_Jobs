import requests 
from bs4 import BeautifulSoup
import pandas as pd 
import time

def linkedin_scraper(tittle="RPA", location="Poland", how_pages=3):
    
    num_page = 0
    list_page_jobs = []
    id_list =[]
    job_list = []
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
        job_response = requests.get(job_url)
        print(job_response.status_code)
        if job_response ==429: 
            print("To many requests")
            time.sleep(10)
            continue
        
        job_soup = BeautifulSoup(job_response.text,"html.parser")
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
            job_post["num_applicatns"] = job_soup.find("span", {"class":"num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet"}).text.strip()
        except:   
            job_post["num_applicatns"]  = None
        job_list.append(job_post)
            
           


    # print(BeautifulSoup(list_data, 'html.parser'))

    job_df = pd.DataFrame(job_list)
    job_df.to_csv("linkedin_jobs.csv")
  
    return job_list




linkedin_scraper()
        