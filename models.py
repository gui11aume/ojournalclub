#! -*- coding:utf-8 -*-
import setup_django_version

from google.appengine.ext import db
from google.appengine.api import users

class UserComment(db.Model):
   author = db.UserProperty()
   content = db.StringProperty(multiline=True)
   date = db.DateTimeProperty(auto_now_add=True)

def thread_key(thread_id):
   return db.Key.from_path('thread', thread_id)
