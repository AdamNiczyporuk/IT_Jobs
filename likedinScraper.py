import requests 
from bs4 import BeautifulSoup
import random 
import pandas as pd 

tittle = "RPA"
location="Poland"

url="https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=RPA&location=Poland&start=25"


response = requests.get(url)
list_data = response.text

list_soup= BeautifulSoup(list_data, 'html.parser')
page_jobs= list_soup.find_all("li")

id_list =[]

for job in page_jobs: 
    base_card_div =job.find("div",{"class": "base-card"})
    job_id= base_card_div.get("data-entity-urn").split(":")[3]
    print(job_id)
    id_list.append(job_id)

job_list = []
for job_id in id_list:
    job_url=f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
    job_response = requests.get(job_url)
    # print(job_response.status_code)
    job_soup = BeautifulSoup(job_response.text,"html.parser")
    job_post= {}
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
    
    
print(job_list)



