from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

#setup flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#mars_app is the name of our mongo database
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#setup flask routes
#flask routes bind url to function
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()  #mars is the name of the collection 
   return render_template("index.html", mars=mars)

#new webpage which will display the scrapped data on the click of a button 
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars  #variable that points to our db
   mars_data = scraping.scrape_all()  #variable to hold newly scraped data
   mars.update({}, mars_data, upsert=True)  #update db using new data
   return redirect('/', code=302)

#tell flask application to run
if __name__ == "__main__":
   app.debug = True
   app.run()