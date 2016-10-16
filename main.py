#!/usr/bin/env python
import os
import jinja2
import webapp2
import random


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

secret = random.randint(0,100)

class MainHandler(BaseHandler):

    def get(self):
        city = cities[secret]
        return self.render_template("index.html", params={"picture" : city.picture, "country" : city.country})

    def post(self):
        capital = self.request.get("capital")
        city = cities[secret]
        if capital == city.name:
            return self.write("You have it.")

        else:
            return self.write("Sorry, it's wrong")

class City(object):
    def __init__(self, name, country, picture):
        self.name = name
        self.country = country
        self.picture = picture

cities = [City(name="Vienna""Berlin", country="Austria""Germany", picture="http://www.mpnpokertour.com/wp-content/uploads/2015/08/Slider-Vienna.png""http://polpix.sueddeutsche.com/bild/1.1406949.1355282590/560x315/berlin-staedtetipps-szkorrespondenten.jpg")]

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
