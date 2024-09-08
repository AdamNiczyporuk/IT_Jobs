import requests 
from bs4 import BeautifulSoup
import pandas as pd 


def linkedin_scraper(tittle="RPA", location="Poland", num_page= 0):
    

        url=f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={tittle}&location={location}&start={num_page}"
        response = requests.get(url)
        # if response.status_code != 200:
        #     print(f"Nie udało się pobrać strony: {response.status_code}")
        #     break 
        
        num_page += 25
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
            
            job_df = pd.DataFrame(job_list)
            job_df.to_csv("linkedin_jobs.csv")
            
        return job_list
    




        