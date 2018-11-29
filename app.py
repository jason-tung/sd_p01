
import json
import random

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

    return render_template("test.html",hello = nasad["url"])

if __name__ == "__main__":
    app.debug = True
    app.run()


