
import likedinScraper as ls
import datetime
import pymysql
import config_data
import schedule
import time 

def saveToDBLikedin(data,nameDB):
   try:
        connection  = pymysql.connect(
            host='127.0.0.1',
            user=config_data.user,
            password=config_data.password,
            database=nameDB,
            port= 3306
        )
        cursor = connection .cursor()
        
        
        InserQuery = """INSERT INTO LinkedInJobs (job_id,job_title, company_name,City, time_posted, job_link,num_applicatns, formatted_dataTime) VALUES (%s,%s,%s,%s,%s, %s, %s, %s)"""
        delete_query="""DELETE FROM LinkedInJobs"""
        
        cursor.execute(delete_query)
        
        for job in data:
            job_id = job.get('job_id')
            job_title = job.get('job_title')
            Company_name = job.get('company_name')
            city = job.get('city').split(",")[0]
            time_posted = job.get('time_posted')
            job_link = job.get('job_link')
            num_applicatns= job.get('num_applicatns')
           
            dataTime=datetime.datetime.now()
            formatted_dataTime = dataTime.strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute(InserQuery, (job_id,job_title, Company_name,city, time_posted, job_link,num_applicatns, formatted_dataTime))
        
        connection.commit()
        
        
   except pymysql.MySQLError as error:
        print(f"Error: {error}")
        
        
   finally:
       if connection: 
           cursor.close()
           connection.close()
           print("Połączenie zostało zamknięte.")


def job():
    data = ls.linkedin_scraper()
    if data: 
        print("Data is not empty")
        saveToDBLikedin(data,"LinkedInDB")
        print("Data has been saved to DB")
        
schedule.every().hours.do(job)

if __name__=="__main__":
    while True:
        schedule.run_pending()