from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/full_info")

@app.route("/")
def index():

    full_info = mongo.db.full_info.find_one()
    return render_template("index.html", full_info=full_info)


@app.route("/scrape")
def scrape():

    full_info = mongo.db.full_info
    mars_data = scrape_mars.scrape()
    full_info.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)