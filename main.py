import config_data as config
import ManageDB as db
import scraper
import likedinScraper as LkScrap
import website
import proxy


def main():
    # scrapeData = scraper.scrape()
    # print(scrapeData)
    # db.create_tableDBScraper("mydatabase")
    # db.saveToDBScraper(scrapeData,"mydatabase")
    # db.create_tableDB("LinkedInDB")
    # proxy.start_tor()
    # Data = LkScrap.linkedin_scraper()

    # # print(Data)
    # db.saveToDBLikedin(Data,"LinkedInDB")
    # print(db.get_dataDB("LinkedInDB"))
    website.app.run(debug=True)
    
if __name__ == '__main__':
    main()