import get_data_from_db
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index ():
    data = get_data_from_db.get_data()
    return render_template('index.html', jobListing=data)

if __name__ == '__main__':
    app.run(debug=True)