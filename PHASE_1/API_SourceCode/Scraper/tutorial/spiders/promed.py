#!/usr/bin/env python3

#!/usr/local/lib/python3.7/

import scrapy
# Importing Regular Expressions
import re 

# pip install spacy
# python -m spacy download en_core_web_sm
# import spacy
import os

import json


import sqlite3
from sqlite3 import Error


# nlp = spacy.load('en_core_web_sm')

disease_list = []
location_list = []


class QuotesSpider(scrapy.Spider):
    name = "promed"
    def start_requests(self):
        urls = [
            'https://www.promedmail.org/ajax/getPosts.php?edate=&return_map=true&feed_id=1&seltype=latest',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        

    def parse(self, response):
        # page = response.url.split("/")[-2]
        
        # filename = '%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)


        with open('disease_list.json','r') as f:
            data = json.load(f)
            for p in data:
                disease_list.append(p['name'])

        with open('country_list.json','r') as f:
            data = json.load(f)
            for p in data:
                location_list.append(p['name'])

        links = []
        for quote in response.css('a'):
            link = quote.xpath('@id').get()
            yield {
                'id': quote.xpath('@id').get(),
            }
            link = 'http://www.promedmail.org/ajax/getPost.php?alert_id='+ re.sub("([^0123456789])", "" , link)
            links.append(link)
            #response.css('a').xpath('@id').getall()
        for l in links:
            yield scrapy.Request(url=l, callback=self.parselinks, headers={"Referer": "http://www.promedmail.org/post/"+re.sub("([^0123456789])", "" , link)})

    def parselinks(self, response):
        page = response.url.split("=")[-1]
        #  DEBUGGING - REMOVE
        # filename = 'weblinks/id%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        filename = 'weblinks/id%s.txt' % page



        # Removing useless html tags
        diseaseString = re.sub('<', '', re.sub('(.*)>', '', re.sub('<', '<\n', response.text)))
        diseaseString = re.sub('\n\n\n', '' ,diseaseString)

        # VARIABLES WE USE TO INSERTIN TO DB
        dbArchiveNnum = ''
        dbSubject = ''
        dbDisease = 'Unknown'
        dbLocation = []
        dbPubDate = ''
        dbBodyText = []

        # doc = nlp(diseaseString)
        # for ent in doc.ents:
        #     print(ent.text, ent.label_)

        with open(filename, 'w') as f:
            f.write(diseaseString)
        with open(filename) as f:
            line = ' '
            while(line):
                line = f.readline()
                if (line.find('Archive Number') >= 0):
                    dbArchiveNnum = f.readline().strip()
                elif(line.find('Subject') >= 0):
                    dbSubject = str(f.readline().strip())
                    for disease in disease_list:
                        if (dbSubject.find(disease) >= 0):
                            dbDisease = disease
                elif(line.find('Published Date') >= 0):
                    dbPubDate = f.readline().strip()
                elif(line.find('http:\/\/www.isid.org') >= 0):
                    while(line):
                        line = f.readline()
                        if(line.find('communicated by') >= 0):
                            break
                        if(line.find('Communicated by') >= 0):
                            break
                        dbBodyText.append(line)
                else:
                    for location in location_list:
                        if (line.find(location) >= 0):
                            dbLocation.append(location)
                

        dbBodyText = ''.join(dbBodyText)
        if os.path.exists(filename):
            os.remove(filename)
        else:
            self.log("The file does not exist")
        conn = sqlite3.connect('../database/newPromedDB')
        url = 'http://www.promedmail.org/post/' + page
        c = conn.cursor()

        # First insert into article table:
        # insert into article (url, datePub, headline, mainText) values ("xxx", "xxx", "xxx", "xxx")
        # replace xxx with values or leave as empty string
        c.execute('INSERT INTO article (url, datePub, headline, mainText) VALUES (?,?,?,?)',(url ,dbPubDate, dbSubject, dbBodyText))        
        # next get the id of the row that with just inserted into article table:
        # select * from article; and remeber the article_id for next insertion        c.execute('INSERT INTO article VALUES (NULL,?,?,?,?)', (url ,dbPubDate, dbSubject, dbBodyText))
        conn.commit()

        c.execute('SELECT id FROM article WHERE url = ?', (url,))
        conn.commit()

        article_id = c.fetchone()
        article_id = article_id[0]
        # Now insert into report table:
        # insert into report (id, disease, syndrome, articleId) values ("xxx", "xxx", "xxx", articleId from previous part)
        c.execute('INSERT INTO report VALUES (?,?,?,?)', (page , dbDisease, '', article_id))
        conn.commit()

        c.execute('INSERT INTO event (type, date, numAffected, reportId) VALUES (?,?,?,?)', ('' ,dbPubDate, 1 , page))
        conn.commit()

        c.execute('SELECT id FROM event WHERE reportId=?', (page,))
        conn.commit()

        eventid = c.fetchone()
        eventid = eventid[0]

        for l in dbLocation:
            c.execute('INSERT INTO location (country,eventId) VALUES (?,?)',(l, eventid))
            conn.commit()

        c.close()
        conn.close()
        print(page + ' - ' + dbArchiveNnum + ' - '+ dbSubject + ' - ' + dbPubDate)
        # print(' '.join(dbBodyText)) 