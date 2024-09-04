import pymysql
import config_data

def get_data ():
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
 


    