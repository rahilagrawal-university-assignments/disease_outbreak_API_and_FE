from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(Text, nullable=False)
    eventId = Column(Integer, ForeignKey("event.id"), nullable=False)


class Report(Base):
    __tablename__ = "report"
    id = Column(String(16), primary_key=True, autoincrement=False)
    disease = Column(Text)
    syndrome = Column(Text)
    articleId = Column(Integer, ForeignKey("article.id"), nullable=False)


class Event(Base):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Text)
    date = Column(Text)
    numAffected = Column(Integer)
    reportId = Column(String(16), ForeignKey("report.id"), nullable=False)


class Article(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Text)
    datePub = Column(Text)
    headline = Column(Text)
    mainText = Column(Text)


engine = create_engine('sqlite:///database/newPromedDB')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)

###########################################
'''
First insert into article table:
insert into article (url, datePub, headline, mainText) values ("xxx", "xxx", "xxx", "xxx")
replace xxx with values or leave as empty string

next get the id of the row that with just inserted into article table:
select * from article; and remeber the article_id for next insertion

Now insert into report table:
insert into report (id, disease, syndrome, articleId) values ("xxx", "xxx", "xxx", articleId from previous part)
btw the id u enter to report is the 16 char id from promed

Now remember the id that was entered into the previous id field (as that is the report id)

Now insert into event table:
insert into event (type, date, numAffected, reportId) values ("xxx", "xxx", "xxx", report id from previous part)

Now get the id of the event that was just inserted:
select * from event; and look for row that was inserted and remember its id

Now insert into location table:
insert into location (country, eventId) values ("xxx", event id from previous part)


'''
