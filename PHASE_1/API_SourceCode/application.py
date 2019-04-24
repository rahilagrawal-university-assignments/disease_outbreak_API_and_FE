from flask import Flask, request
from flask_restplus import Api, Resource, fields, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB_make import Location, Report, Event, Article
import datetime

# Setup App

app = Flask(__name__)
app.config['ERROR_404_HELP'] = False
api = Api(app)
disease = api.namespace('disease', description='Disease Services')

engine = create_engine('sqlite:///database/newPromedDB')
DBSession = sessionmaker(bind=engine)
session = DBSession()

# API Models

location_details = api.model('location_details', {
    "country": fields.String(),
    "location": fields.String()
})

report_event = api.model('report_event', {
    "type": fields.String(),
    "date": fields.DateTime(),
    "location": fields.List(fields.Nested(location_details)),
    "number_affected": fields.Integer()
})

report_details = api.model('report_details', {
    "disease": fields.List(fields.String()),
    "syndrome": fields.List(fields.String()),
    "reported_events": fields.List(fields.Nested(report_event)),
    "comment": fields.String()
})

article_details = api.model('article_details', {
    "url": fields.String(),
    "date_of_publication": fields.DateTime(),
    "headline": fields.String(),
    "main_text": fields.String(),
    "reports": fields.List(fields.Nested(report_details))
})


# Helper Functions
def fillEventJson(event):
    eventJson = {}
    eventJson["type"] = event.type
    eventJson["date"] = event.date
    eventJson["number_affected"] = event.numAffected
    return eventJson


def fillReportJson(report):
    reportJson = {}
    reportJson["disease"] = [report.disease]
    reportJson["syndrome"] = [report.syndrome]
    reportJson["articleId"] = report.articleId
    return reportJson


def fillArticleJson(article):
    articleJson = {}
    articleJson["url"] = article.url
    articleJson["date_of_publication"] = article.datePub
    articleJson["headline"] = article.headline
    articleJson["main_text"] = article.mainText
    return articleJson


def fillLocationJson(eventId):
    location = session.query(Location).filter_by(eventId=eventId).first()
    locationJson = {}
    locationJson['country'] = location.country
    locationJson['location'] = ""
    return locationJson

def getArticleArray(articleJsonDict, reportJsonDict, eventJsonDict):
    articleArray = []
    for articleId, articleJson in articleJsonDict.items():
        reportsArray = []
        for reportId in list(reportJsonDict):
            if articleId == reportJsonDict[reportId]["articleId"]:
                del reportJsonDict[reportId]["articleId"]
                eventsArray = []
                for eventId in list(eventJsonDict):
                    if reportId == eventJsonDict[eventId]["reportId"]:
                        del eventJsonDict[eventId]["reportId"]
                        eventsArray.append(eventJsonDict[eventId])
                        del eventJsonDict[eventId]
                reportJsonDict[reportId]["reported_events"] = eventsArray
                reportJsonDict[reportId]["comment"] = "null"

                reportsArray.append(reportJsonDict[reportId])
                del reportJsonDict[reportId]
        articleJson["reports"] = reportsArray
        articleArray.append(articleJson)
    return articleArray

def processDate(date):
    if date is None:
        return date
    date = date.split("-")
    date = list(map(int, date))
    date = datetime.date(date[0], date[1], date[2])
    return date


def getDateTime(dateTime):
    return f'{dateTime}Txx:xx:xx'


def get_request_json():
    """Get the request body as a JSON object."""
    j = request.json
    if not j:
        abort(400, "Expected a JSON object. Make sure you've set the 'Content-Type' header to 'application/json'.")
    return j


def get_request_arg(arg, type=str, required=False, default=None):
    """Get the value of arg from request.args, converted it using `type`.

    - If arg is provided but could not be parsed by `type`, then a 400 error is thrown.
    - If requires is True and the arg is not provided, then a 400 error is thrown.
    - If required is False and the arg is not provided, then default is returned.
    """
    if arg not in request.args:
        if required:
            abort(400, "Expected '{}' query parameter".format(arg))
        else:
            return default
    else:
        try:
            return type(request.args[arg])
        except:
            abort(400, "Query parameter '{}' malformed".format(arg))


def getArticlesInDateRange(articles, start_date, end_date):
    if start_date is None and end_date is None:
        articles = articles
    elif start_date is None:
        for article in articles:
            article_datetime = processDate(article["date_of_publication"])
            if article_datetime > end_date:
                articles.remove(article)
    elif end_date is None:
        for article in articles:
            article_datetime = processDate(article["date_of_publication"])
            if article_datetime < start_date:
                articles.remove(article)
    else:
        for article in articles:
            article_datetime = processDate(article["date_of_publication"])
            if not (start_date <= article_datetime <= end_date):
                articles.remove(article)
    for article in articles:
        article["date_of_publication"] = getDateTime(article["date_of_publication"])
    return articles


# Filter Functions

def diseaseByLocation(location, start_date, end_date):
    locations = session.query(Location).filter_by(country=location).all()
    if locations is None:
        abort(404, 'Locaton does not exist')

    locationJsonDict = {}
    for locationElm in locations:
        locationJson = {}
        locationJson['country'] = locationElm.country
        locationJson['location'] = ""
        locationJson['eventId'] = locationElm.eventId
        locationJsonDict[locationElm.id] = locationJson

    eventJsonDict = {}
    events = []
    for id, locationElm in locationJsonDict.items():
        queryResults = session.query(Event).filter_by(id=locationElm['eventId']).all()
        events.extend(queryResults)

    for event in events:
        eventJson = fillEventJson(event)
        locationArray = []
        for id in list(locationJsonDict):
            if event.id == locationJsonDict[id]["eventId"]:
                del locationJsonDict[id]["eventId"]
                locationArray.append(locationJsonDict[id])
                del locationJsonDict[id]
        eventJson["location"] = locationArray
        eventJson["reportId"] = event.reportId
        eventJsonDict[event.id] = eventJson

    reportJsonDict = {}
    for id in eventJsonDict:
        report = session.query(Report).filter_by(id=eventJsonDict[id]["reportId"]).first()
        if report is None:
            continue
        reportJson = fillReportJson(report)
        reportJsonDict[report.id] = reportJson

    articleJsonDict = {}
    for id in reportJsonDict:
        article = session.query(Article).filter_by(id=reportJsonDict[id]["articleId"]).first()
        if article is None:
            continue
        articleJson = fillArticleJson(article)
        articleJsonDict[article.id] = articleJson


    return getArticlesInDateRange(getArticleArray(articleJsonDict, reportJsonDict, eventJsonDict), start_date, end_date)


def diseaseByName(disease, start_date, end_date):
    reports = session.query(Report).filter_by(disease=disease).all()
    if reports is None:
        abort(404, 'Disease does not exist')

    reportJsonDict = {}
    for report in reports:
        events = session.query(Event).filter_by(reportId=report.id).all()
        eventJsonArray = []
        for event in events:
            eventJson = fillEventJson(event)
            locationJson = fillLocationJson(event.id)
            eventJson["location"] = [locationJson]
            eventJsonArray.append(eventJson)
        reportJson = fillReportJson(report)
        reportJson["reported_events"] = eventJsonArray
        reportJson["comment"] = "null"
        reportJsonDict[report.id] = reportJson

    articleJsonDict = {}
    for id in reportJsonDict:
        article = session.query(Article).filter_by(id=reportJsonDict[id]["articleId"]).first()
        if article is None:
            continue
        articleJson = fillArticleJson(article)
        articleJsonDict[article.id] = articleJson

    articleArray = []
    for articleId, articleJson in articleJsonDict.items():
        reportsArray = []
        for reportId in list(reportJsonDict):
            if articleId == reportJsonDict[reportId]["articleId"]:
                del reportJsonDict[reportId]["articleId"]
                reportsArray.append(reportJsonDict[reportId])
                del reportJsonDict[reportId]
        articleJson["reports"] = reportsArray
        articleArray.append(articleJson)

    return getArticlesInDateRange(articleArray, start_date, end_date)


def diseaseByLocationAndName(location, disease, start_date, end_date):
    reports = session.query(Report).filter_by(disease=disease).all()
    if reports is None:
        abort(404, 'Disease does not exist')

    reportJsonDict = {}
    for report in reports:
        events = session.query(Event).filter_by(reportId=report.id).all()
        eventJsonArray = []
        for event in events:
            eventJson = fillEventJson(event)
            locationJson = fillLocationJson(event.id)
            eventJson["location"] = [locationJson]
            if locationJson["country"] == location:
                eventJsonArray.append(eventJson)
        reportJson = fillReportJson(report)
        reportJson["reported_events"] = eventJsonArray
        reportJson["comment"] = "null"
        if len(eventJsonArray) > 0:
            reportJsonDict[report.id] = reportJson

    articleJsonDict = {}
    for id in reportJsonDict:
        article = session.query(Article).filter_by(id=reportJsonDict[id]["articleId"]).first()
        if article is None:
            continue
        articleJson = fillArticleJson(article)
        articleJsonDict[article.id] = articleJson

    articleArray = []
    for articleId, articleJson in articleJsonDict.items():
        reportsArray = []
        for reportId in list(reportJsonDict):
            if articleId == reportJsonDict[reportId]["articleId"]:
                del reportJsonDict[reportId]["articleId"]
                reportsArray.append(reportJsonDict[reportId])
                del reportJsonDict[reportId]
        articleJson["reports"] = reportsArray
        articleArray.append(articleJson)

    return getArticlesInDateRange(articleArray, start_date, end_date)

# API Endpoint

@disease.route('/', strict_slashes=False)
class Disease(Resource):

    @disease.response(200, 'Success', article_details)
    @disease.response(400, 'Malformed Request')
    @disease.response(404, 'Disease Not Found')
    @disease.param('disease', 'name of the disease you want information about')
    @disease.param('location', 'name of location where disease or outbreaks occurred')
    @disease.param('start_date', 'Start date for filtering search in YYY-MM-DD Eg: 2018-01-01')
    @disease.param('end_date', 'End date for filtering search in YYYY-MM-DD Eg: 2018-02-27')
    @disease.doc(description='''
        Lets you fetch information in one of the following ways:
        1. Name of the Disease - Returns information about given disease in the given location (if selected, otherwise all locations are included)
        2. Location - Returns information for given location and disease (if selected, otherwise all diseases are shown).
        3. Date From - Returns information for occurrences after the supplied date
        4. Date To - Returns information for occurrences before the supplied date
    ''')
    def get(self):
        disease_name = get_request_arg('disease', str)
        location = get_request_arg('location', str)
        start_date = processDate(get_request_arg('start_date', str))
        end_date = processDate(get_request_arg('end_date', str))
        if start_date is not None and end_date is not None and start_date > end_date:
            abort(404, 'Invalid Date Range - Start Date is after End Date')
        if disease_name is None and location is None:
            abort(404, 'Disease and Location cannot both be empty. Please input at least one')
        if disease_name is None:
            return diseaseByLocation(location, start_date, end_date)
        if location is None:
            return diseaseByName(disease_name, start_date, end_date)
        return diseaseByLocationAndName(location, disease_name, start_date, end_date)


if __name__ == "__main__":
    app.run()
