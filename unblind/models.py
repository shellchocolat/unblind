# models.py

from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    user_uid = db.Column(db.String(100), unique=True)
    user_name = db.Column(db.String(100), unique=True)
    user_hash = db.Column(db.String(100))

class XSS(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    xss_uid = db.Column(db.String(100), unique=True)
    xss_created_at = db.Column(db.String(100))
    xss_value = db.Column(db.String(100))
    xss_ip_from = db.Column(db.String(255))
    xss_stage_1 = db.Column(db.Boolean)
    xss_stage_2 = db.Column(db.Boolean)
    cookie = db.Column(db.String(1000))
    user_agent = db.Column(db.String(1000))
    platform = db.Column(db.String(100))
    screen_resolution = db.Column(db.String(100))
    browser_size = db.Column(db.String(100))
    url = db.Column(db.String(255))

class Interact(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    agent_uid = db.Column(db.String(100), unique=True)
    agent_cmd = db.Column(db.String(10000))
    agent_response = db.Column(db.String(10000))