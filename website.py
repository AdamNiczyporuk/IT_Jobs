import ManageDB
import likedinScraper
from flask import Flask, render_template, request,jsonify, redirect, url_for
app = Flask(__name__)



# @app.route('/jobs', methods=['GET'])
# def index():
#     keyword = request.args.get('keyword')
#     location = request.args.get('location')
#     if keyword or location:
#         result = ManageDB.searchDB("LinkedInDB", keyword, location)
#         if result:
#             return  render_template('index.html', jobListing=result)
        
#         if likedinScraper.linkedin_scraper(keyword, location):
#             result = ManageDB.searchDB("LinkedInDB", keyword, location)
#             return render_template('index.html', jobListing=result)
#         return jsonify({"message": "No results found"}), 404


@app.route('/')
def index ():
    data = ManageDB.get_ALL_data_DB("LinkedInDB")
    return render_template('index.html', jobListing=data)

# @app.route('/')
# def main_page():
#     return render_template('mainpage.html')

if __name__ == '__main__':
    app.run(debug=True)