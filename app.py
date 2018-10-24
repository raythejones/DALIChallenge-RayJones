from flask import Flask, render_template, request
import urllib2, json, web
import ast

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def root():
    data = "https://raw.githubusercontent.com/dali-lab/mappy/gh-pages/members.json"
    u = urllib2.urlopen(data)
    d = json.loads(u.read())
    print(d)
    display = {}
    pdict = {}
    counter = 0
    while(len(d) > counter):
        person = d[counter]["name"]
        info = {}
        info["name"] = d[counter]["name"]  
        info["url"] = d[counter]["url"]
        info["termsOn"] = d[counter]["terms_on"][0]
        info["iconURL"] = "../static/" + d[counter]["iconUrl"]
        info["message"] = d[counter]["message"]
        pdict[person] = info
        counter +=1
    display = pdict
    return render_template('index.html', display = display, title = 'hey')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    data = "https://raw.githubusercontent.com/dali-lab/mappy/gh-pages/members.json"
    u = urllib2.urlopen(data)
    d = json.loads(u.read())
    print(d)
    pdict = {}
    counter = 0
    while(len(d) > counter):
        person = d[counter]["name"]
        info = {}
        info["name"] = d[counter]["name"]  
        info["url"] = d[counter]["url"]
        info["termsOn"] = d[counter]["terms_on"][0]
        info["iconURL"] = "../static/" + d[counter]["iconUrl"]
        info["message"] = d[counter]["message"]
        if (len(d[counter]["project"]) > 0):
            info["project"] = d[counter]["project"][0]
        else:
            info["project"] = "None Right Now!"        
        pdict[person] = info
        counter +=1
    display = pdict
    if (request.method == 'POST'):
        aPerson = request.form["theSubmit"]
        print(aPerson)

    thePerson = ast.literal_eval(aPerson)

    return render_template('profile.html', thePerson = thePerson)

'''
    while(len(d) > counter):
        person = d[counter]["name"]
        info = {}
        info["name"] = d[counter]["name"]  
        info["url"] = d[counter]["url"]
        info["termsOn"] = d[counter]["terms_on"][0]
        info["iconURL"] = "../static/" + d[counter]["iconUrl"]
        info["message"] = d[counter]["message"]
        if (len(d[counter]["project"]) > 0):
            info["project"] = d[counter]["project"][0]
        else:
            info["project"] = "None Right Now!"
        pdict[person] = info
        counter +=1
        
        display = pdict         

        '''



if __name__ == '__main__':
    app.debug = True
    app.run()

