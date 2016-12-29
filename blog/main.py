import webapp2
import jinja2
import os
import re

from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), 
    autoescape=True)


class BlogPost(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    time_added = db.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        recent_postings = BlogPost.all().order('-time_added')
        blog = jinja_env.get_template('blog.html')
        self.response.write(blog.render(recent_postings=recent_postings))


class PostPage(webapp2.RequestHandler):
    def get(self):
        form = jinja_env.get_template('newentry.html')
        self.response.write(form.render())

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            post = BlogPost(subject=subject, content=content)
            post_key = post.put()
            post_id = str(post_key.id())

            self.redirect('/blog/' + post_id)

        else:
            error = "Must include subject and content"
            form = jinja_env.get_template('newentry.html')
            self.response.write(form.render(error=error))


class BlogEntry(webapp2.RequestHandler):
    def get(self, post_id):
        key = db.Key.from_path('BlogPost', int(post_id))
        post = db.get(key)

        if not post:
            self.error(404)
            return

        blog = jinja_env.get_template('permalink.html')
        self.response.write(blog.render(post=post))


app = webapp2.WSGIApplication([
    ('/blog', MainPage),
    ('/blog/newpost', PostPage),
    ('/blog/(\w+)', BlogEntry)
    ], debug=True)
