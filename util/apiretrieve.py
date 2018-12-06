import json
import datetime
import urllib

def load(thing):
    return json.loads(urllib.request.urlopen(thing).read())

def load_bypass(thing):
    req = urllib.request.Request(thing,headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urllib.request.urlopen(req).read()
    return json.loads(webpage)

def horoscope(ss):
    d = {}

    requrl = "http://horoscope-api.herokuapp.com/horoscope/today/" + ss
    try:
        today = load(requrl)
        d["today"] = today["horoscope"]
    except:
        today = None

    requrl = "http://horoscope-api.herokuapp.com/horoscope/week/" + ss
    try:
        week = load(requrl)
        d["week"] = week["horoscope"]
    except:
        week = None

    requrl = "http://horoscope-api.herokuapp.com/horoscope/month/" + ss
    try:
        month = load(requrl)
        d["month"] = month["horoscope"]
    except:
        month = None

    requrl = "http://horoscope-api.herokuapp.com/horoscope/year/" + ss
    try:
        year = load(requrl)
        d["year"] = year["horoscope"]
    except:
        year = None

    ss = ss[0].upper() + ss[1:]

    t = ss + " horoscope"

    return {"title":t, "dict":d, "sign":ss}

def suntimeparse(s):
    l = s.split("T")
    s = l[1]
    s = str((int(s[:2]) - 5) % 12) + s[2:]
    l = s.split("+")
    s = l[0]
    return s

def maincontent():
    with open("keys.json") as json_file:
        key_loc = json.load(json_file)
    my_dict = key_loc

    # location

    requrl = "https://ipapi.co/json/"
    try:
        d = load(requrl)
        lon = d["longitude"]
        lat = d["latitude"]
        currcity = d["city"]
        currreg = d["region"]
        regid = d["region_code"]
        currcoun = d["country_name"]
        counid = d["country"]

        locationinfo = {"currcity":currcity, "currreg":currreg, "currcoun": currcoun}
    except:
        lon = 0
        lat = 0
        locationinfo = None

    # holidays

    requrl = "https://www.calendarindex.com/api/v1/holidays/json?"
    data = {}
    data["country"] = counid
    data["year"] = datetime.datetime.today().year
    data["state"] = regid
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
    data["country"] = counid
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
        d.load_bypass(requrl)

        poem = {"title":d[0]["title"], "poet":d[0]["poet"]["name"], "poem":d[0]["content"]}
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

    return d
