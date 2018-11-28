import json
import random

from urllib import request, parse, error

from flask import Flask, render_template

app = Flask(__name__)

def load(thing):
    return json.loads(request.urlopen(thing).read())

key_loc = "http://homer.stuy.edu/~jtung/sd_keys/p01.json"

@app.route('/')
def hello_world():
    my_dict = load(key_loc)
    print(my_dict)

    # time/date

    #requrl = "https://www.calendarindex.com/api/v1/holidays/json?country=US&year=2018&state=NY&api_key="
    #requrl += my_dict["calendarindex"]

    #print(requrl)

    #d = load(requrl)

    # news

    requrl = "https://newsapi.org/v2/top-headlines?"
    data = {}
    data["country"] = "us"
    data["apiKey"] = my_dict["newsapi"]

    requrl += parse.urlencode(data)

    d = load(requrl)
    print(d)

    newsarticles = []
    for i in range(d["totalResults"] - 1):
        print(i)
        newsarticles.append([d["articles"][i]["url"], d["articles"][i]["title"]])

    print(newsarticles)

    return render_template("index.html",title="project almanac")

if __name__ == "__main__":
    app.debug = True
    app.run()

