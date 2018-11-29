import json
import random
import datetime

from urllib import request, parse, error

from flask import Flask, render_template, jsonify

app = Flask(__name__)

def load(thing):
    return json.loads(request.urlopen(thing).read())

key_loc = "http://homer.stuy.edu/~jtung/sd_keys/p01.json"

@app.route('/')
def hello_world():
    my_dict = load(key_loc)
    #for k,v in my_dict.items():
        #print (k,v)
    #ip api here
    ipd = load("https://ipapi.co/json")

    #nasa imaging here
    url = "https://api.nasa.gov/planetary/earth/imagery/?"
    data = {}
    data["lon"] = str(ipd["longitude"])
    data["lat"] = str(ipd["latitude"])
    data["dim"] = "0.2"
    data["cloud_score"] = "True"
    data["api_key"] = my_dict["nasa"]
    url+=parse.urlencode(data)
    nasad = load(url)
    print(url)
    """
    return render_template("test.html",hello = nasad["url"])
    """

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

    return render_template("index.html",title="project almanac")\


    #requrl = "https://www.poemist.com/api/v1/randompoems"
    #d.load(requrl)

    #title = d[02]["title"]
    #poet = d[02]["poet"]["name"]
    #content = d[02]["content"]

if __name__ == "__main__":
    app.debug = True
    app.run()


