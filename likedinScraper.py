import requests 
from bs4 import BeautifulSoup
import random 
import pandas as pd 

tittle = "RPA"
location="Poland"

url="https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=RPA&location=Poland&start=25"


response = requests.get(url)

job_id = "3823863310"
job_url=f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
job_response = requests.get(job_url)

list_data = response.text

list_soup= BeautifulSoup(list_data, 'html.parser')