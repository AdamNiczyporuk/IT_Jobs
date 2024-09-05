import ManageDB
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index ():
    data = ManageDB.get_data()
    return render_template('index.html', jobListing=data)

