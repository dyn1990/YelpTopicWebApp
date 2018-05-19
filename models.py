from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

import geocoder
import urllib3
import json


db = SQLAlchemy()


# model for the reviews
class Reviews(db.Model):
  __tablename__ = 'db_reviews'
  index = db.Column(db.BigInteger, primary_key = True)
  business_id = db.Column(db.String(100))
  review_id = db.Column(db.String(100))
  date = db.Column(db.TIMESTAMP(100))
  text = db.Column(db.String(20000))
  stars = db.Column(db.Integer)
  name = db.Column(db.String(100))
  topics = db.Column(db.String(100))


class TopicClass(db.Model):
  __tablename__ = 'db_topics'
  topic_num = db.Column(db.Integer, primary_key = True)
  topics = db.Column(db.String(100))

  def __init__(self, topic_num, topics):
    self.topic_num = topic_num
    self.topics = topics