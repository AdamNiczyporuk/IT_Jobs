import ManageDB
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/jobs')
def index ():
    data = ManageDB.get_dataDB("LinkedInDB")
    return render_template('index.html', jobListing=data)

@app.route('/')
def main_page():
    return render_template('mainpage.html')

if __name__ == '__main__':
    app.run(debug=True)