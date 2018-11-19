
import json
import random

import urllib.request

from flask import Flask, render_template

app = Flask(__name__)

def load(thing):
    return json.loads(urllib.request.urlopen(thing).read())

key_loc = "http://homer.stuy.edu/~jtung/sd_keys/p01.json"

@app.route('/')
def hello_world():
    my_dict = load(key_loc)
    for k,v in my_dict.items():
        print (k,v)
    return 0

if __name__ == "__main__":
    app.debug = True
    app.run()

