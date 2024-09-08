import pymysql
import config_data
import  scraper
import datetime

def get_dataDB ():
    connection  = pymysql.connect(
            host='127.0.0.1',
            user=config_data.user,
            password=config_data.password,
            database='mydatabase',
            port= 3306
        )
    try:
        cursor = connection .cursor()
        query="SELECT * FROM mydatabase.JobListing"
        cursor.execute(query)   
        result = cursor.fetchall()
        print(f"Retrieved {len(result)} records")
        return result
    except pymysql.MySQLError as error:
        print(f"Error: {error}")
        return []
    finally:
        cursor.close()
        connection.close()
 






#function to Create Database table
def create_tableDB(nameDB):

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
                Company_name VARCHAR(255),
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

def saveToDB(data,nameDB):
   try:
        connection  = pymysql.connect(
            host='127.0.0.1',
            user=config_data.user,
            password=config_data.password,
            database=nameDB,
            port= 3306
        )
        cursor = connection .cursor()
        
        
        InserQuery = """INSERT INTO LinkedInJobs (job_id,job_title, Company_name, time_posted, job_link,num_applicatns, formatted_dataTime) VALUES (%s,%s,%s,%s, %s, %s, %s)"""
        SelectQuery="""SELECT COUNT(*) From LinkedInJobs WHERE job_id=%s"""
        
        
        for job in data:
            job_id = job.get('job_id')
            job_title = job.get('job_title')
            Company_name = job.get('company_name')
            time_posted = job.get('time_posted')
            job_link = job.get('job_link')
            num_applicatns= job.get('num_applicatns')
           
            dataTime=datetime.datetime.now()
            formatted_dataTime = dataTime.strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute(SelectQuery, (job_id,))
            result = cursor.fetchone()
            
            if result[0] == 0:
                cursor.execute(InserQuery, (job_id,job_title, Company_name, time_posted, job_link,num_applicatns, formatted_dataTime))
        
        connection.commit()
        
        
   except pymysql.MySQLError as error:
        print(f"Error: {error}")
        
        
   finally:
       if connection: 
           cursor.close()
           connection.close()
           print("Połączenie zostało zamknięte.")
