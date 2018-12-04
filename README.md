# team azrael <img src="https://d1lss44hh2trtw.cloudfront.net/assets/article/2015/07/06/Azrael_Returns_feature.jpg" height="40">
Vincent Chi, Bill Ni, Jason Tung, Wei Wen Zhou

**[Devlog](https://github.com/jason-tung/sd_p01/blob/master/devlog.txt)**

## Project Almanac: A News-Almanac Hybrid

### Abstract:
Our website is designed to provide the user with information correlating certain locations (much like an almanac) but do so while also giving more “live” information like current news in the area, the weather, what time the sun will set on a given day, etc. We plan on presenting this in a newspaper format (like NYT) with horoscopes, poems, and maybe a crossword puzzle.

### How To Procure Your Own API Keys
Team azrael uses its own API keys to run the website (stored in an API on the stuy.edu servers), but if you so choose to get your own, the APIs are listed below with brief descriptions and websites to start on getting your own keys.

api | description
--- | ---
[calendar index](https://www.calendarindex.com/)  | Gives dates of holidays and observances
[sunrise-sunset](https://sunrise-sunset.org/api) | Provides time for sunrise, high noon, and sunset
[darksky](https://darksky.net/dev) | To get the past, current, and future weather at a location
[ipapi](https://ipapi.co/)  | To get the information about location based on ip address
[horoscope-api](https://github.com/tapaswenipathak/Horoscope-API) | To get the daily, weekly, monthly horoscope
[newsapi](https://newsapi.org/) | To get the news or anything
[poemist](https://poemist.github.io/poemist-apidoc/#misc-services) | Get a random poem
[nasa-api](https://api.nasa.gov/) | Used to fetch a picture of location based on long/lat

### Dependencies: 
Our dependencies, as listed in requirements.txt, are as follows:

dependency | version | origin | description
--- | --- | --- | ---
Click | 7.0 | Flask | unused
Flask | 1.0.2 | Flask |  microframework of choice
itsdangerous | 1.1.0 | Flask |  unused
Jinja2 | 2.10 | Flask |  templating language
MarkupSafe | 1.1.0 | Flask |  unused
Werkzeug | 0.14.1 | Flask |  unused
json | n/a | py3.7.1-stdlib |  converts json strings into python dictionaries and vice-versa
datetime | n/a | py3.7.1-stdlib | fetches current date and time
urllib | n/a | py3.7.1-stdlib |  fetches json data from urls
urllib.request | n/a | py3.7.1-stdlib |  fetches json data from urls


Install our dependencies with the follow command in the root directory of our repo:
```
pip3 install -r requirements.txt
```

### Instructions:
1. Clone the repo
** ssh **
```
git clone git@github.com:jason-tung/sd_p01.git
```

**https**
```
git clone https://github.com/jason-tung/sd_p01.git
```

2. (optional) make a virutal env
```
python3 -m venv <venv_name>
```

3. (optional) activate virtual env
```
. <path-to-venv>/bin/activate
```

4. enter the repo directory
```
cd <path-to-repo>
```

5. install requirements
```
pip3 install -r requirements.txt
```

6. run the app.py with python3
**python 2.7**
```
python app.py
```

**python 3.7**
```
python3 app.py
```
7. go to localhost 127.0.0.1:5000 on any browser
   http://127.0.0.1:5000/
