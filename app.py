import json
import datetime
import urllib

from flask import Flask, render_template, jsonify, flash, request

app = Flask(__name__)

def load(thing):
    return json.loads(urllib.request.urlopen(thing).read())

def load_bypass(thing):
    req = urllib.request.Request(thing,headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urllib.request.urlopen(req).read()
    return json.loads(webpage)

def suntimeparse(s):
    l = s.split("T")
    s = l[1]
    s = str((int(s[:2]) - 5) % 12) + s[2:]
    l = s.split("+")
    s = l[0]
    return s

#key_loc = load("http://homer.stuy.edu/~jtung/sd_keys/p01.json")
with open("keys.json") as json_file:
    key_loc = json.load(json_file)

@app.route('/')
def hello_world():
    my_dict = key_loc

    # location

    requrl = "https://ipapi.co/json/"
    try:
        d = load(requrl)
        lon = d["longitude"]
        lat = d["latitude"]
        currcity = d["city"]
        currreg = d["region"]
        currcoun = d["country_name"]

        locationinfo = {"currcity":currcity, "currreg":currreg, "currcoun": currcoun}
    except:
        lon = 0
        lat = 0
        locationinfo = None

    # holidays

    requrl = "https://www.calendarindex.com/api/v1/holidays/json?"
    data = {}
    data["country"] = "US"
    data["year"] = "2018"
    data["state"] = "NY"
    data["api_key"] = my_dict["calendarindex"]

    requrl += urllib.parse.urlencode(data)

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

    requrl += urllib.parse.urlencode(data)

    try:
        d = load(requrl)
        newsarticles = []
        for i in range(10):
            newsarticles.append([d["articles"][i]["url"], d["articles"][i]["title"].split(" - ")[0]])
    except:
        newsarticles = None

    # weather

    requrl = "https://api.darksky.net/forecast/" + my_dict["darksky"] + "/" + str(lat) + "," + str(lon)

    try:
        d = load(requrl)
        weatheralerts = []
        if "alerts" in d.keys():
            for alert in d["alerts"]:
                weatheralerts.append([alert["title"], alert["uri"]])
        currentweather = d["minutely"]["summary"]
        currtemp = d["currently"]["temperature"]
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

    requrl += urllib.parse.urlencode(data)

    try:
        d = load(requrl)
        srisetoday = suntimeparse(d["results"]["sunrise"])
        ssettoday = suntimeparse(d["results"]["sunset"])
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

    requrl += urllib.parse.urlencode(data)

    try:
        d = load(requrl)
        srisetmw = suntimeparse(d["results"]["sunrise"])
        ssettmw = suntimeparse(d["results"]["sunset"])
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
    requrl += urllib.parse.urlencode(data)
    try:
        d = load(requrl)
        nasaimg = d["url"]
    except:
        nasaimg = None

    # poems

    requrl = "https://www.poemist.com/api/v1/randompoems"
    try:
        d.load(requrl)

        poem = {"title":poem["title"], "poet":poem["poet"]["name"], "poem":poem["content"]}
    except:
        poem = None

    # place all api data into a dict

    d = {}
    d["currtime"] = str(datetime.datetime.now().time())[:9]
    d["locationinfo"] = locationinfo
    d["holidays"] = holidays
    d["newsarticles"] = newsarticles
    if weatheralerts != []:
        d["weatheralerts"] = weatheralerts
    d["currentweather"] = currentweather
    d["currenttemp"] = currtemp
    d["weekweather"] = weekweather
    d["srisetoday"] = srisetoday
    d["ssettoday"] = ssettoday
    d["srisetmw"] = srisetmw
    d["ssettmw"] = ssettmw
    d["nasaimg"] = nasaimg
    d["poem"] = poem

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

    ss = ss[0].upper() + ss[1:]

    return render_template("horoscope.html", dctnary=d, sign=ss)

@app.route("/sunsign")
def ssselect():
    return render_template("sunsign.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
