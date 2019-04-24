from flask import Flask, redirect, render_template, request, url_for
from server import app
import requests
import json


outbreak_list = []

with open("country.json") as file:
    country_data = json.loads(file.read())

for c in country_data: 
    c["coord"]["lat"] = (c["north"]+c["south"])/2
    c["coord"]["long"] = (c["east"]+c["west"])/2

@app.route('/', methods=["GET", "POST"])
def index():
    global outbreak_list
    if request.method == "POST":
        location = request.form["location"]
        disease = request.form["disease"]
        startDate = request.form["startDate"]
        endDate = request.form["endDate"]
        if not location and not disease:
            return render_template("index.html", fail=1)
        return redirect(url_for('search', location=location, disease=disease, startDate=startDate, endDate=endDate)) 
    
    if request.args.get('fail'):
        fail = request.args.get('fail')
        return render_template("index.html", fail=2)

    outbreak_list = []
    return render_template("index.html")

@app.route('/search', methods=["GET", "POST"])
def search():
    global outbreak_list
    if request.method == "POST":
        pass
    
    startDate = request.args.get("startDate")
    if startDate == '':
        startDate = '2013-06-03'

    endDate = request.args.get("endDate")
    if endDate == '':
        endDate = '2019-04-09'

    url = 'http://epi.ioxel.com/api/search?start_date='+startDate+'T00%3A00%3A00&end_date='+endDate+'T00%3A00%3A00&keyterms='+request.args.get("disease")+'&location='+request.args.get("location")
    if outbreak_list == []:
        r = requests.get(url)
        outbreak_list = json.loads(r.text)
        try:
            if outbreak_list == [] or outbreak_list['error']:
                return redirect(url_for('index', fail=2))
        except:
            pass
        
    infected = 0
    death = 0
    hosp = 0
    recovered = 0
    
    mapList = country_data
    for m in mapList:
        m["affected"] = 0
    for outbreak in outbreak_list:
        for report in outbreak['reports']:
            for event in report['reported_events']:
                if event['type'] == "presence" or event['type'] == "infected":
                    infected += 1
                elif event['type'] == "death":
                    death += 1
                elif event['type'] == "hospitalised":
                    hosp += 1
                elif event['type'] == "recovered":
                    recovered += 1
                for location in event['location']:
                    for m in mapList:
                        if m["geonameId"] == location["geonames-id"] and event["number_affected"] is not None:
                            if event["number_affected"] >= 100000:
                                m["affected"] = m["affected"] + 100
                            else:
                                m["affected"] = m["affected"] + event["number_affected"]

    print(infected, death, hosp, recovered)

    return render_template("search2.html", outbreak_list = outbreak_list, location= request.args.get("location"), disease= request.args.get("disease"), endDate=request.args.get("endDate"), infected=infected, death=death, hosp=hosp, recovered=recovered, mapList=mapList)

@app.route('/news', methods=["GET", "POST"])
def news():
    # /v2/top-headlines ??
    url = ('https://newsapi.org/v2/everything?'+"pageSize=35&q=disease&")
    if(request.args.get("disease")):
        url = url + request.args.get("disease") + "&"
    if(request.args.get("location")):
        url = url + request.args.get("location") + "&"

    # THE CURRENT GOOGLE PLAN REQUIRES START DATE TO BE ONLY A MONTH BEFORE CURR DATE
    # if(request.args.get("startDate")):
    #     url = url + "from=" + request.args.get("startDate") + "&"
    if(request.args.get("endDate")):
        url = url + "to=" + request.args.get("endDate") + "&"
    url = url + 'apiKey=b90fe99d9349421ca66159209d0e73db'

    response = requests.get(url)
    google_news = json.loads(response.text)
    google_news = google_news['articles']

    return render_template("news.html", google_news=google_news)  


@app.route('/details', methods=["GET", "POST"])
def details():
    typeEvent = ""
    if request.args.get('type') == "infected" or request.args.get('type') == "presence":
        typeEvent = "Infected"
    elif request.args.get('type') == "death":
        typeEvent = "Death"
    elif request.args.get('type') == "hospitalised":
        typeEvent = "Hospitalised"
    elif request.args.get('type') == "recovered":
        typeEvent = "Recovered"

    flag = False
    if request.args.get('type') == "infected":
        flag = True
    
    new_list = []
    for outbreak in outbreak_list:
        for report in outbreak['reports']:
            for event in report['reported_events']:
                if flag:
                    if event['type'] == request.args.get('type') or event['type'] == "presence":
                        alreadyIn = False
                        for i in new_list:
                            if i['headline'] == outbreak['headline']:
                                alreadyIn = True
                                break
                        if not alreadyIn:
                            new_list.append(outbreak)
                else:
                    if event['type'] == request.args.get('type'):
                        alreadyIn = False
                        for i in new_list:
                            if i['headline'] == outbreak['headline']:
                                alreadyIn = True
                                break
                        if not alreadyIn:
                            new_list.append(outbreak)

    return render_template("details.html", type=typeEvent, outbreak_list=new_list)  


@app.route('/table', methods=["GET", "POST"])
def table():  
    global outbreak_list
    return render_template("table.html", outbreak_list=outbreak_list)  




# @app.route('/map', methods=["GET", "POST"])
# def map():

#      return render_template("map.html")  


