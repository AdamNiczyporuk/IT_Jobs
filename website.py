import ManageDB
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/jobs', methods=['POST'])
def search():
    data =request.json
    keyword = data['keyword']
    loctaion = data['location']
    
    result = ManageDB.get_ALL_data_DB("LinkedInDB", keyword, location)
    
 
def index ():
    data = ManageDB.get_ALL_data_DB("LinkedInDB")
    return render_template('index.html', jobListing=data)

@app.route('/')
def main_page():
    return render_template('mainpage.html')

if __name__ == '__main__':
    app.run(debug=True)