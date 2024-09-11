import config_data as config
import ManageDB as db
import scraper
import likedinScraper as LkScrap
import website


def main():
    # scrapeData = scraper.scrape()
    # print(scrapeData)
    # db.create_tableDB("LinkedInDB")
    Data = LkScrap.linkedin_scraper()
    # print(Data)
    db.saveToDB(Data,"LinkedInDB")
    # website.app.run(debug=True)
    
if __name__ == '__main__':
    main()