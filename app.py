import json
import datetime
import urllib

from flask import Flask, render_template, jsonify, flash, request

from util import apiretrieve

app = Flask(__name__)

def load(thing):
    return json.loads(urllib.request.urlopen(thing).read())

def load_bypass(thing):
    req = urllib.request.Request(thing,headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urllib.request.urlopen(req).read()
    return json.loads(webpage)

@app.route('/')
def hello_world():
    d = apiretrieve.maincontent()

    return render_template("index.html",title="project almanac", dctnary=d)

@app.route('/horoscope')
def dayweekmonth():
    ss = request.args['sunsign']
    dict = apiretrieve.horoscope(ss)

    return render_template("horoscope.html", title=dict["title"], dctnary=dict["dict"], sign=(ss[0].upper() + ss[1:]))

@app.route("/sunsign")
def ssselect():
    return render_template("sunsign.html", title="select sunsign")


if __name__ == "__main__":
    app.debug = True
    app.run()
