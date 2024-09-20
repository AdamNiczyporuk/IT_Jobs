import pymysql
import config_data
import  scraper
import datetime

def get_dataDB (nameDB):
    connection  = pymysql.connect(
            host='127.0.0.1',
            user=config_data.user,
            password=config_data.password,
            database='mydatabase',
            port= 3306
        )
    try:
        cursor = connection .cursor()
        query=f"SELECT * FROM {nameDB}.LinkedInJobs"
        cursor.execute(query)   
        result = cursor.fetchall()
        print(f"Retrieved {len(result)} records")
        return result
    except pymysql.MySQLError as error:
        print(f"Error: {error}")
        return []
    finally:
        cursor.close()

#function to Create Database table
def create_tableDBLikedIn(nameDB):

    try:
        connection  = pymysql.connect(
            host='127.0.0.1',
            user=config_data.user,
            password=config_data.password,
            database=nameDB,
            port= 3306
        )
        cursor = connection .cursor()
        createTableQuery = """
                CREATE TABLE IF NOT EXISTS LinkedInJobs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                job_id VARCHAR(255) UNIQUE,
                job_title VARCHAR(255),
                company_name VARCHAR(255),
                city VARCHAR(255),
                time_posted VARCHAR(255),
                num_applicatns VARCHAR(255),
                job_link VARCHAR(255) ,
                formatted_dataTime DATETIME );
                """
                
        cursor.execute(createTableQuery)
        print("Table createg GOOD")
    except pymysql.MySQLError as error:
        print(f"Error: {error}")
    
    finally: 
         if connection:
            cursor.close()
            connection.close()
            print("Połączenie zostało zamknięte.")

def create_tableDBScraper(nameDB):

    try:
        connection  = pymysql.connect(
            host='127.0.0.1',
            user=config_data.user,
            password=config_data.password,
            database=nameDB,
            port= 3306
        )
        cursor = connection .cursor()
        createTableQuery = """
                CREATE TABLE IF NOT EXISTS JobListing (
                id INT AUTO_INCREMENT PRIMARY KEY,
                job_title VARCHAR(255),
                job_link VARCHAR(255) ,
                site VARCHAR(255),
                type VARCHAR(255),
                formatted_dataTime DATETIME );
                """
                
        cursor.execute(createTableQuery)
        print("Table createg GOOD")
    except pymysql.MySQLError as error:
        print(f"Error: {error}")
    
    finally: 
         if connection:
            cursor.close()
            connection.close()
            print("Połączenie zostało zamknięte.")




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
        SelectQuery="""SELECT COUNT(*) From LinkedInJobs WHERE job_id=%s"""
        
        
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
            
            cursor.execute(SelectQuery, (job_id,))
            result = cursor.fetchone()
            
            if result[0] == 0:
                cursor.execute(InserQuery, (job_id,job_title, Company_name,city, time_posted, job_link,num_applicatns, formatted_dataTime))
        
        connection.commit()
        
        
   except pymysql.MySQLError as error:
        print(f"Error: {error}")
        
        
   finally:
       if connection: 
           cursor.close()
           connection.close()
           print("Połączenie zostało zamknięte.")


def saveToDBScraper(data,nameDB):
   try:
        connection  = pymysql.connect(
            host='127.0.0.1',
            user=config_data.user,
            password=config_data.password,
            database=nameDB,
            port= 3306
        )
        cursor = connection .cursor()
        
        
        InserQuery = """INSERT INTO JobListing (job_title,job_link,site,type,formatted_dataTime) VALUES (%s,%s,%s,%s,%s)"""
        SelectQuery="""SELECT COUNT(*) From JobListing WHERE job_link=%s"""
        
        
        for job in data:
            job_title = job.get('job')
            job_link = job.get('url')
            site = job.get('site')
            type = job.get('type')

            # Generowanie czasu wewnątrz pętli
            dataTime = datetime.datetime.now()
            formatted_dataTime = dataTime.strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(SelectQuery, (job_link,))
            result = cursor.fetchone()

            if result[0] == 0:
                cursor.execute(InserQuery, (job_title, job_link, site, type, formatted_dataTime))
            
        connection.commit()
        
        
   except pymysql.MySQLError as error:
        print(f"Error: {error}")
        
        
   finally:
       if connection: 
           cursor.close()
           connection.close()
           print("Połączenie zostało zamknięte.")
