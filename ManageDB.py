import pymysql
import config_data
import  scraper
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
def create_tableDB():

    try:
        connection  = pymysql.connect(
            host='127.0.0.1',
            user=config_data.user,
            password=config_data.password,
            database='mydatabase',
            port= 3306
        )
        cursor = connection .cursor()
        createTableQuery = """
                CREATE TABLE IF NOT EXISTS JobListing (
                id INT AUTO_INCREMENT PRIMARY KEY,
                job_title VARCHAR(255),
                job_link VARCHAR(255),
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

def saveToDB(data):
   try:
        connection  = pymysql.connect(
            host='127.0.0.1',
            user=config_data.user,
            password=config_data.password,
            database='mydatabase',
            port= 3306
        )
        cursor = connection .cursor()
        
        InserQuery = """INSERT INTO JobListing (job_title, job_link, site, type, formatted_dataTime) VALUES (%s, %s, %s, %s, %s)"""
        for job, link, site, type_, formatted_dataTime in data:
            cursor.execute(InserQuery, (job, link, site, type_, formatted_dataTime))
        
        connection.commit()
        
        
   except pymysql.MySQLError as error:
        print(f"Error: {error}")
        
        
   finally:
       if connection: 
           cursor.close()
           connection.close()
           print("Połączenie zostało zamknięte.")
data = scraper.scrape()
