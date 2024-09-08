import config_data as config
import ManageDB 
import scraper
# import website


def main():
    # scrapeData = scraper.scrape()
    #ManageDB.create_tableDB()
    ManageDB.create_tableDB("LinkedInDB")
    # website.app.run(debug=True)
    
if __name__ == '__main__':
    main()