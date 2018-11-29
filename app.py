import json
import random
import datetime

from urllib import request, parse, error

from flask import Flask, render_template

app = Flask(__name__)

def load(thing):
    return json.loads(request.urlopen(thing).read())

key_loc = "http://homer.stuy.edu/~jtung/sd_keys/p01.json"

@app.route('/')
def hello_world():
    my_dict = load(key_loc)

    # time/date

    # requrl = "https://www.calendarindex.com/api/v1/holidays/json?"
    # data = {}
    # data["country"] = "US"
    # data["year"] = "2018"
    # data["state"] = "NY"
    # data["api_key"] = my_dict["calendarindex"]

    # requrl += parse.urlencode(data)

    # d = load(requrl)

    # print(d)

    # news

    requrl = "https://newsapi.org/v2/top-headlines?"
    data = {}
    data["country"] = "us"
    data["apiKey"] = my_dict["newsapi"]

    requrl += parse.urlencode(data)

    d = load(requrl)

    newsarticles = []
    for i in range(10):
        newsarticles.append([d["articles"][i]["url"], d["articles"][i]["title"], d["articles"][i]["content"]])

    # location

    requrl = "https://ipapi.co/json/"
    d = load(requrl)
    lon = d["longitude"]
    lat = d["latitude"]

    # weather

    requrl = "https://api.darksky.net/forecast/" + my_dict["darksky"] + "/" + str(lat) + "," + str(lon)
    d = load(requrl)

    weatheralerts = []
    if "alerts" in d.keys():
    	for alert in d["alerts"]:
    		weatheralerts.append([alert["title"], alert["uri"]])
    currentweather = d["minutely"]["summary"]
    weekweather = d["daily"]["summary"]

    # sunrise/sunset (today)

    requrl = "https://api.sunrise-sunset.org/json?"
    data = {}
    data["lat"] = lat
    data["lng"] = lon
    data["date"] = datetime.date.today()
    data["formatted"] = 0

    requrl += parse.urlencode(data)

    d = load(requrl)

    srisetoday = d["results"]["sunrise"]
    ssettoday = d["results"]["sunset"]

    # sunrise/sunset (tomorrow)

    requrl = "https://api.sunrise-sunset.org/json?"
    data = {}
    data["lat"] = lat
    data["lng"] = lon
    data["date"] = datetime.date.today() + datetime.timedelta(days=1)
    data["formatted"] = 0

    requrl += parse.urlencode(data)

    d = load(requrl)

    srisetmw = d["results"]["sunrise"]
    ssettmw = d["results"]["sunset"]

    return render_template("index.html",title="project almanac")

if __name__ == "__main__":
    app.debug = True
    app.run()

