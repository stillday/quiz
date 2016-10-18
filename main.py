#!/usr/bin/env python
import os
import jinja2
import webapp2
import random
from google.appengine.ext import ndb



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
        city = cities[secret]
        return self.render_template("index.html", params={"picture" : city.picture, "country" : city.country})

    def post(self):
        global secret
        capital = self.request.get("capital")
        city = cities[secret]
        guess = Guess(expected = city.name,  actual = capital)
        guess.put()
        if capital == city.name:
            self.write("That's right :)")
            possibleSecrets = range(0, len(cities))
            random.shuffle(possibleSecrets)
            for possibleSecret in possibleSecrets:
                if possibleSecret != secret:
                    secret = possibleSecret
                    break
            city = cities[secret]
            self.render_template("index.html", params={"picture" : city.picture, "country" : city.country})
        else:
            self.write("Sorry, it's wrong")
            self.render_template("index.html", params={"picture": city.picture, "country": city.country})


class City(object):
    def __init__(self, name, country, picture):
        self.name = name
        self.country = country
        self.picture = picture

cities = [City (name="Vienna", country="Austria", picture="http://www.mpnpokertour.com/wp-content/uploads/2015/08/Slider-Vienna.png"),
        City (name="Berlin", country="Germany", picture="http://polpix.sueddeutsche.com/bild/1.1406949.1355282590/940x528/berlin-staedtetipps-szkorrespondenten.jpg")
          ]
secret = random.randint(0, len(cities) - 1)

class Guess(ndb.Model):
    expected = ndb.StringProperty()
    actual = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

class MessageListHandler(BaseHandler):
    def get(self):
        guesses = Guess.query().fetch()
        params = {"guesses": guesses}
        return self.render_template("guess.html", params=params)

class MessageDetailsHandler(BaseHandler):
    def get(self, guess_id):
        guess = Guess.get_by_id(int(guess_id))
        params = {"guess": guess}
        return self.render_template("guess_details.html", params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/guess', MessageListHandler),
    webapp2.Route('/guesses/<guess_id:\d+>', MessageDetailsHandler)
], debug=True)
