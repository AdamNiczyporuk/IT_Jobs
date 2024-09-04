import pymysql
from scraper  import scraped_data
import config_data 

#function to Create Database table
def create_table():

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

create_table()