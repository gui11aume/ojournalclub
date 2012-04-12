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

def user_is_admin(user):
   return user.email() == 'guillaume@thegrandlocus.com'

def thread_is_open(path):
   return path in (
                     'how-to-use-the-open-journal-club',
                     'do-histone-modifications-affect-TF-binding',
                  )

class ThreadServer(webapp.RequestHandler):
   def get(self, path):

      if not thread_is_open(path):
         self.response.out.write(
            hard_html_serve.render_template('404.html')
         )
         return

      user = users.get_current_user()
      if not user:
         # User not logged in... Back to square 1.
         self.redirect("/")
         return

      # Check if user is known.
      if models.UserInfo.get_by_key_name(user.user_id()) is None:
         self.redirect("/signin.html")
         return

      # Query all user comments for that page.
      query = models.UserContent.all().ancestor(
          models.thread_key(path)).order('pubdate')
      contents = query.fetch(100)

      template_vals = {
         'page_title': path,
         'usercontents': contents,
         'path': path,
         'user_is_admin': user_is_admin(user),
      }

      self.response.out.write(
          hard_html_serve.render_template(path, template_vals)
      )


class NewContentPostHandler(webapp.RequestHandler):
   def post(self):

      user = users.get_current_user()
      user_info = models.UserInfo.get_by_key_name(user.user_id())
      if not user or user_info is None:
         self.redirect("/")

      path = self.request.get('path')

      # Instantiate content.
      content = models.UserContent(parent=models.thread_key(path))
      content.author = user
      content.display_name = user_info.display_name
      content.content = self.request.get('content')

      is_crocodoc_iframe = self.request.get('crocodoc', False)
      if is_crocodoc_iframe:
         if user_is_admin(user):
            content.is_crocodoc_iframe = True
         else:
            # Cheating??
            self.redirect("/")

      # Save and reload.
      content.put()
      self.redirect('/threads/' + path)

class NewUserPostHandler(webapp.RequestHandler):
   def post(self):

      user = users.get_current_user()
      if not user:
         self.redirect("/")

      # Instantiate user.
      try:
         newuser = models.UserInfo(key_name=user.user_id())
         newuser.user = user
         newuser.display_name = self.request.get('display_name')
         newuser.put()
      except:
         self.redirect("/signin-error.html")

      self.redirect("/signin-successful.html")
      return


app= webapp.WSGIApplication([
  ('/newuser', NewUserPostHandler),
  ('/threads/newusercontent', NewContentPostHandler),
  ('/threads/(.*)', ThreadServer),
])

def main():
  run_wsgi_app(app)

if __name__ == '__main__':
  main()
