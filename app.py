from flask import Flask, render_template, request
import urllib2, json

app = Flask(__name__)

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
        info["iconURL"] = "../static/" + d[counter]["iconUrl"]
        info["message"] = d[counter]["message"]
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
    return render_template('index.html', group = group, display = display)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
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
    return render_template('profile.html', group = group, display = display)

if __name__ == '__main__':
    app.debug = True
    app.run()
