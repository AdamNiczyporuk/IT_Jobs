import requests 
from bs4 import BeautifulSoup
import pandas as pd 
import time
import random
import re 
import proxy
import ManageDB as db
# import agents as ag


def extract_number(text):
    match= re.search(r"\d+", text)
    if match:
        return int(match.group())
    return None

def likedIn_numOffert_scraper(url): 
    response = requests.get(url)
    text_page= response.text
    parse_data = BeautifulSoup(text_page, 'html.parser')
    num_offerts= parse_data.find("span", {"class": "results-context-header__job-count"})
    print(num_offerts)
    if num_offerts is None:
        likedIn_numOffert_scraper(url)
    else:
        return num_offerts.text

def linkedin_scraper(tittle="RPA", location="Poland"):
    
    num_page = 0
    list_page_jobs = []
    id_list =[]
    job_list = []
    Checking=0 
    time_sleep=1
    index =0 
    
    all_offerts= likedIn_numOffert_scraper(f"https://www.linkedin.com/jobs/search?keywords={tittle}&location={location}&pageNum=0&position=1")
    while all_offerts is None:
        all_offerts= likedIn_numOffert_scraper(f"https://www.linkedin.com/jobs/search?keywords={tittle}&location={location}&pageNum=0&position=1")
        print(all_offerts)
        
    all_offerts = all_offerts.replace(',', '')
    all_offerts= all_offerts.replace('+', '')
    
    all_offerts =int(all_offerts)
    
    if all_offerts%25 == 0:
        how_pages= all_offerts//25
        print(how_pages)
    else:
        how_pages= all_offerts//25 +1
        print(how_pages)
    
    if how_pages>10:
        how_pages=10
        
    
    while num_page <= how_pages*25:
        print(f"Page {num_page}")
        url=f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={tittle}&location={location}&start={num_page}"
        # headers = {'User-Agent': ag.get_random_agent()}
        response = proxy.make_request_proxy(url)
        list_page_jobs.append(response.text)
        num_page += 25
        
    
    for list_data in list_page_jobs:
        list_data= BeautifulSoup(list_data, 'html.parser')
        page_jobs= list_data.find_all("li")
        
        for job in page_jobs: 
            base_card_div =job.find("div",{"class": "base-card"})
            if base_card_div is not None:
                job_id= base_card_div.get("data-entity-urn").split(":")[3]
                # print(job_id)
                id_list.append(job_id)
                index +=1
            else:
                continue
    
    for job_id in id_list:
        job_url=f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
        
        while True:
            # headers = {'User-Agent': ag.get_random_agent()}
            job_response =  proxy.make_request_proxy(job_url)
            print(job_response.status_code)
            
            if job_response.status_code == 200:
                Checking=0
                break
            
            if  job_response.status_code == 429:
                time_sleep = random.uniform(1, 10)
                print(f"Coun Check {Checking} this {job_id} time sleep {time_sleep}")
                time.sleep(time_sleep)
                Checking +=1
                
        job_soup = BeautifulSoup(job_response.text,"html.parser")
        
        # WRITING TO FILE TO DEBUG
        # with open("job_soup.txt", "a", encoding="utf-8") as file:
        #     file.write(str(job_soup)+"\n")
        
        job_post= {}
        
        job_post["job_link"] = f"https://www.linkedin.com/jobs/search?keywords={tittle}&location={location}&pageNum=0&position=28&currentJobId={job_id}"
        job_post["job_id"] = job_id
        
        try:
            job_post["city"] = job_soup.find("span", {"class":"topcard__flavor topcard__flavor--bullet"}).text.strip()
        except:
             job_post["city"] = None
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
                # print(job_post["num_applicatns"])
            else:
                num_applicants_figcaption = job_soup.find("figcaption", {"class": "num-applicants__caption"})
                if num_applicants_figcaption and num_applicants_figcaption.text.strip():
                    job_post["num_applicatns"] = extract_number(num_applicants_figcaption.text.strip()) 
                    # print(job_post["num_applicatns"])
                else:
                    job_post["num_applicatns"] = None
        except Exception as e:
            print("Error:", e)
            job_post["num_applicatns"] = None
        
        job_list.append(job_post)
        
    db.saveToDBLikedin(job_list,"LinkedInDB")        
    


    
    # Writting Data to Excel  
    # job_df = pd.DataFrame(job_list)
    # job_df.to_csv("linkedin_jobs.csv",index=False)
    print(index)
    return job_list




        