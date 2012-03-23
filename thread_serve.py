import setup_django_version

import cgi
import datetime
import urllib
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import models
import hard_html_serve

class ThreadServer(webapp.RequestHandler):
   def get(self, path):

      # Query all user comments for that page.
      try:
         #query = models.UserComment.all().ancestor(
         #   models.thread_key(path)).order('-date')
         query = models.UserComment.all()
         comments = query.fetch(10)
      except:
         comments = []

      template_vals = {
         'comments': comments,
         'path': path,
      }

      self.response.out.write(hard_html_serve.render_template('thread.html', template_vals))


class NewCommentPostHandler(webapp.RequestHandler):
   def post(self):
      path = self.request.get('path')

      # Instantiate comment.
      comment = models.UserComment(parent=models.thread_key(path))
      if users.get_current_user():
         comment.author = users.get_current_user()
      comment.content = self.request.get('content')
      comment.put()

      self.redirect('/threads/' + path)



app= webapp.WSGIApplication([
  ('/threads/newcomment', NewCommentPostHandler),
  ('/threads/(.*)', ThreadServer),
])

def main():
  run_wsgi_app(app)

if __name__ == '__main__':
  main()
