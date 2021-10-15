from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")


# create route that renders index.html template and finds documents from mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    destination_data = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("index.html", mars_scrape=destination_data)

@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars_data
    mars_data = scrape_mars.scrape()
    mongo.db.mars_data.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
