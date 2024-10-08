import ManageDB
import likedinScraper
from flask import Flask, render_template, request,jsonify, redirect, url_for
from dictionary import city_mapping
app = Flask(__name__)




@app.route('/')
def main_page():
    return render_template('mainpage.html')

    # @app.route('/jobs', methods=['GET'])
    # def get_all_jobs():
    #     data = ManageDB.get_ALL_data_DB("LinkedInDB")
    #     job_listings = [
    #         {
    #             'id': job[0],
    #             'company_name': job[3],
    #             'job_title': job[2],
    #             'city': job[4],
    #             'applicants': job[6],
    #             'time_posted': job[5],
    #             'link': job[7]
    #         }
    #         for job in data
    #     ]
    #     return render_template('index.html', jobListing=job_listings, city_mapping=city_mapping)

@app.route('/jobs', methods=['GET'])
def index():
    keyword = request.args.get('keyword')
    location = request.args.get('location')
    if keyword or location:
        result = ManageDB.searchDB("LinkedInDB", keyword, location)
        if result:
            job_listing  = [
                {
                    'id': job[0],
                    'company_name': job[3],
                    'job_title': job[2],
                    'city': job[4],
                    'applicants': job[6],
                    'time_posted': job[5],
                    'link': job[7]
                }
                for job in result
            ]
            return  render_template('index.html', jobListing=job_listing,city_mapping=city_mapping)
        
        if likedinScraper.linkedin_scraper(keyword, location):
            result = ManageDB.searchDB("LinkedInDB", keyword, location)
            job_listing  = [
                {
                    'id': job[0],
                    'company_name': job[3],
                    'job_title': job[2],
                    'city': job[4],
                    'applicants': job[6],
                    'time_posted': job[5],
                    'link': job[7]
                }
                for job in result
            ]
            return  render_template('index.html', jobListing=job_listing,city_mapping=city_mapping)
        return jsonify({"message": "No results found"}), 404
    
    


if __name__ == '__main__':
    app.run(debug=True)