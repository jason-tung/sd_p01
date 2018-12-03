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
Click | 7.0 | Flask | tbd
Flask | 1.0.2 | Flask |  tbd
itsdangerous | 1.1.0 | Flask |  tbd
Jinja2 | 2.10 | Flask |  tbd
MarkupSafe | 1.1.0 | Flask |  tbd
Werkzeug | 0.14.1 | Flask |  tbd
json | n/a | python standard lib |  tbd
datetime | n/a | python standard lib |  tbd
urllib | n/a | python standard lib |  tbd
urllib.request | n/a | python standard lib |  tbd


Install our dependencies with the follow command in the root directory of our repo:
```
pip install -r requirements.txt
```

### Instructions:


Include clear instructions on how to run your project. (Including how to procure API keys, with hyperlinks...)
Assume your audience is cloning your repo and running from localhost.
List dependencies
...as well as how to install/procure them,
and a brief explanation of what each one does / how your app utilizes it.
