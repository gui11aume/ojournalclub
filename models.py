#! -*- coding:utf-8 -*-
import setup_django_version

from google.appengine.ext import db
from google.appengine.api import users

class UserInfo (db.Model):
   """Model for users of ojournalclub."""
   user = db.UserProperty()
   display_name = db.StringProperty()
   creationdate = db.DateTimeProperty(auto_now_add=True)
   misc = db.BlobProperty()

class UserContent (db.Model):
   """Model for comments and crocodoc iframes."""
   author = db.UserProperty()
   display_name = db.StringProperty()
   content = db.TextProperty()
   is_crocodoc_iframe = db.BooleanProperty(default=False)
   pubdate = db.DateTimeProperty(auto_now_add=True)

def thread_key(thread_id):
   return db.Key.from_path('thread', thread_id)
