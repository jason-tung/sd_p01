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

    requrl = "https://newsapi.org/v2/top-headlines?"
    data = {}
    data["country"] = "us"
    data["apiKey"] = my_dict["newsapi"]

    requrl += parse.urlencode(data)

    try:
        d = load(requrl)
        newsarticles = []
        for i in range(10):
            newsarticles.append([d["articles"][i]["url"], d["articles"][i]["title"]])
    except:
        newsarticles = None
    print(newsarticles)
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

    # poems

    requrl = "https://www.poemist.com/api/v1/randompoems"
    try:
        d.load(requrl)

        poems = []
        for poem in d:
            poems.append({"title":poem["title"], "poet":poem["poet"]["name"], "poem":poem["content"]})
    except:
        poems = None

    # place all api data into a dict

    d = {}
    d["holidays"] = holidays
    d["newsarticles"] = newsarticles
    d["currentweather"] = currentweather
    d["weekweather"] = weekweather
    d["srisetoday"] = srisetoday
    d["ssettoday"] = ssettoday
    d["srisetmw"] = srisetmw
    d["ssettmw"] = ssettmw
    d["nasaimg"] = nasaimg
    d["poems"] = poems

    return render_template("index.html",title="project almanac", dctnary=d)



@app.route('/horoscope')
def dayweekmonth():
    d = {}
    ss = request.args['sunsign']

    requrl = "http://horoscope-api.herokuapp.com/horoscope/today/" + ss
    try:
        today = load(requrl)
    except:
        today = None

    d["today"] = today["horoscope"]
    requrl = "http://horoscope-api.herokuapp.com/horoscope/week/" + ss
    try:
        week = load(requrl)
    except:
        week = None

    d["week"] = week["horoscope"]
    requrl = "http://horoscope-api.herokuapp.com/horoscope/month/" + ss
    try:
        month = load(requrl)
    except:
        month = None

    d["month"] = month["horoscope"]
    requrl = "http://horoscope-api.herokuapp.com/horoscope/year/" + ss
    try:
        year = load(requrl)
    except:
        year = None

    d["year"] = year["horoscope"]


if __name__ == "__main__":
    app.debug = True
    app.run()
