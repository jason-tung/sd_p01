import json
import datetime

from urllib import request, parse, error
from urllib.request import Request, urlopen
from flask import Flask, render_template, jsonify, flash

app = Flask(__name__)

def load(thing):
    return json.loads(request.urlopen(thing).read())

def load_bypass(thing):
    req = Request(thing,headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    return json.loads(webpage)


key_loc = "http://homer.stuy.edu/~jtung/sd_keys/p01.json"

@app.route('/')
def hello_world():
    my_dict = load(key_loc)

    # time/date

    requrl = "https://www.calendarindex.com/api/v1/holidays/json?"
    data = {}
    data["country"] = "US"
    data["year"] = "2018"
    data["state"] = "NY"
    data["api_key"] = my_dict["calendarindex"]

    requrl += parse.urlencode(data)

    try:
        d = load_bypass(requrl)
        holidays = d["response"]["holidays"]
    except:
        holidays = None

    # news

    r equrl = "https://newsapi.org/v2/top-headlines?"
    data = {}
    data["country"] = "us"
    data["apiKey"] = my_dict["newsapi"]

    requrl += parse.urlencode(data)

    try:
        d = load(requrl)
        newsarticles = []
        for i in range(10):
            newsarticles.append([d["articles"][i]["url"], d["articles"][i]["title"], d["articles"][i]["content"]])
    except:
        newsarticles = None

    # location

    requrl = "https://ipapi.co/json/"
    try:
        d = load(requrl)
        lon = d["longitude"]
        lat = d["latitude"]
    except:
        lon = 0
        lat = 0

    # weather

    requrl = "https://api.darksky.net/forecast/" + my_dict["darksky"] + "/" + str(lat) + "," + str(lon)

    try:
        d = load(requrl)
        weatheralerts = []
        if "alerts" in d.keys():
            for alert in d["alerts"]:
                weatheralerts.append([alert["title"], alert["uri"]])
        currentweather = d["minutely"]["summary"]
        weekweather = d["daily"]["summary"]
    except:
        weatheralerts = None
        currentweather = None
        weekweather = None

    # sunrise/sunset (today)

    requrl = "https://api.sunrise-sunset.org/json?"
    data = {}
    data["lat"] = lat
    data["lng"] = lon
    data["date"] = datetime.date.today()
    data["formatted"] = 0

    requrl += parse.urlencode(data)

    try:
        d = load(requrl)
        srisetoday = d["results"]["sunrise"]
        ssettoday = d["results"]["sunset"]
    except:
        srisetoday = None
        ssettoday = None

    # sunrise/sunset (tomorrow)

    requrl = "https://api.sunrise-sunset.org/json?"
    data = {}
    data["lat"] = lat
    data["lng"] = lon
    data["date"] = datetime.date.today() + datetime.timedelta(days=1)
    data["formatted"] = 0

    requrl += parse.urlencode(data)

    try:
        d = load(requrl)
        srisetmw = d["results"]["sunrise"]
        ssettmw = d["results"]["sunset"]
    except:
        srisetmw = None
        ssettmw = None

    # nasa imaging

    requrl = "https://api.nasa.gov/planetary/earth/imagery/?"
    data = {}
    data["lon"] = lon
    data["lat"] = lat
    data["dim"] = "0.2"
    data["api_key"] = my_dict["nasa"]
    requrl += parse.urlencode(data)
    try:
        d = load(requrl)
        nasaimg = d["url"]
    except:
        nasaimg = None

    return render_template("index.html",title="project almanac")

    # poems
    #requrl = "https://www.poemist.com/api/v1/randompoems"
    #d.load(requrl)

    #title = d[1]["title"]
    #poet = d[1]["poet"]["name"]
    #content = d[1]["content"]

if __name__ == "__main__":
    app.debug = True
    app.run()
