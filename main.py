#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Sporocilo



template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

class SendMessageHandler(BaseHandler):
    def post(self):
        user_name = self.request.get("user_name")
        user_email = self.request.get("user_email")
        user_message = self.request.get("user_message")

        message = Sporocilo(ime = user_name, email = user_email, sporocilo= user_message)
        message.put()
        return self.render_template("message-sent.html")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/message-sent', SendMessageHandler),
], debug=True)
