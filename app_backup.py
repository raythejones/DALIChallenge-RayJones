from flask import Flask, render_template, request
import urllib2, json

app = Flask(__name__)

def findLoc(lat, long):
    data = "https://api.opencagedata.com/geocode/v1/json?q=" + lat + "+" + long + "&key=3bca35db76e64e53bbb8d1f69af6fb7a&q=52.51627%2C13.37769&pretty=1"
    u = urllib2.urlopen(data)
    d = json.loads(u.read())
    results = d["results"]
    if (len(results) > 0):
        country = results[0]["components"]["country"]
        if (country == "USA"):
            components = results[0]["components"]["state"] + ", " + country
        else:
            components = country
    else:
        components = "can't find location?"
    return components


@app.route('/', methods=['GET', 'POST'])
def root():
    data = "https://raw.githubusercontent.com/dali-lab/mappy/gh-pages/members.json"
    u = urllib2.urlopen(data)
    d = json.loads(u.read())
    display = {}
    pdict = {}
    counter = 0
    while(len(d) > counter):
        person = d[counter]["name"]
        info = {}
        info["url"] = d[counter]["url"]
        info["termsOn"] = d[counter]["terms_on"][0]
        info["iconURL"] = "../static/" + d[counter]["iconUrl"]
        info["message"] = d[counter]["message"]
        info["hometown"] = findLoc(str(d[counter]["lat_long"][0]),str(d[counter]["lat_long"][1]))
        if (len(d[counter]["project"]) > 0):
            info["project"] = d[counter]["project"][0]
        else:
            info["project"] = "n/a"
        pdict[person] = info
        counter +=1
    if (request.method =="POST"):
        group = ":" + request.form["term"]
        if (request.form["term"] == "all"):
            display = pdict
            group = " : all"
        else:
            for person in pdict:
                if (pdict[person]["termsOn"] == request.form["term"]):
                    display[person] = pdict[person]
    else:
        display = pdict
        group = " : all"
    return render_template('home1.html', group = group, display = display)



if __name__ == '__main__':
    app.debug = True
    app.run()
