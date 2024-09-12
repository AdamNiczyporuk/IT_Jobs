import ManageDB
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index ():
    data = ManageDB.get_dataDB("LinkedInDB")
    return render_template('index.html', jobListing=data)

if __name__ == '__main__':
    app.run(debug=True)