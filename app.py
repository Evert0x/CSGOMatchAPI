import requests
import datetime
from bs4 import BeautifulSoup
import json
import pytz
from flask import request, jsonify
from flask import Flask
app = Flask(__name__)

def scrape(stars):
    rt = []

    data = requests.get("https://www.hltv.org/matches?star=%s" % stars).content
    soup = BeautifulSoup(data)
    matches = soup.findAll("div", {"class": "upcoming-match"})

    for mt in matches:
        match = {}
        teams = mt.findAll("div", {"class": "team"})
        if len(teams) != 2:
            continue
        match["team1"] = teams[0].text
        match["team2"] = teams[1].text

        time = mt.find("div", {"class": "time"})
        match["timestamp"] = int(time["data-unix"][:-3])

        amsterdam = pytz.timezone('Europe/Amsterdam')
        date = datetime.datetime.fromtimestamp(match["timestamp"], tz=amsterdam)
        match["datetime"] = date.isoformat()

        stars = mt.findAll("i", {"class": "fa-star"})
        match["stars"] = len(stars)

        map = mt.find("div", {"class": "map-text"})
        match["maps"] = map.text
        rt.append(match)
    return rt


@app.route("/")
def meme():
    return "You are a SIMP!"

@app.route("/csgay")
def parse():
    stars = request.args.get('stars', 0)
    data = scrape(stars)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host=settings.APP_HOST, port=settings.APP_PORT, debug=settings.APP_DEBUG)
