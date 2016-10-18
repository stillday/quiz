#!/usr/bin/env python
#-*- Coding: utf-8 -*-
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

cities = [City (name="Vienna", country="Austria", picture="https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Wien_Rathaus_hochaufl%C3%B6send.jpg/1280px-Wien_Rathaus_hochaufl%C3%B6send.jpg"),
        City (name="Berlin", country="Germany", picture="https://upload.wikimedia.org/wikipedia/commons/7/74/Berlin_Brandenburger_Tor_Nacht.jpg"),
        City (name="Washington", country="USA", picture="https://upload.wikimedia.org/wikipedia/commons/c/c5/IMG_2259_-_Washington_DC_-_US_Capitol.JPG"),
        City (name="Sydney", country="Australia", picture="https://upload.wikimedia.org/wikipedia/commons/9/91/Sydney_opera_house_2010.jpg"),
        City (name="London", country="UK", picture="https://upload.wikimedia.org/wikipedia/commons/8/8b/London_Eye_Night_Shot.JPG"),
        City (name="Cardiff", country="UK", picture="https://upload.wikimedia.org/wikipedia/commons/f/f3/Cardiff_Hafen.JPG"),
        City (name="Amsterdam", country="Netherlands", picture="https://upload.wikimedia.org/wikipedia/commons/5/54/Amsterdam_Keizersgracht_Leidsegracht_001.JPG"),
        City (name="Brussels", country="Belgium", picture="https://upload.wikimedia.org/wikipedia/de/f/fb/Bruessel-GrandPlace-NO-Seite-Links-20060905.JPG"),
        City (name="Den Haag", country="Netherlands", picture="https://upload.wikimedia.org/wikipedia/commons/3/3d/Den_Haag_Binnenhof.jpg"),
        City (name="Cologne", country="Germany", picture="https://upload.wikimedia.org/wikipedia/commons/0/07/K%C3%B6lner_Rhein.jpg"),
        City (name="Paris", country="France", picture="https://c2.staticflickr.com/8/7003/6672156239_01bde2b717_b.jpg"),
        City (name="Hamburg", country="Germany", picture="https://c4.staticflickr.com/6/5640/23170282419_4011d76eb6_b.jpg"),
        City (name="Zurich", country="Switzerland", picture="https://upload.wikimedia.org/wikipedia/commons/7/76/Z%C3%BCrich.jpg"),
        City (name="Copenhagen", country="Denmark", picture="https://upload.wikimedia.org/wikipedia/commons/d/d5/Nyhavn,_Copenhagen.jpg"),
        City (name="St Petersburg", country="Russia", picture="https://upload.wikimedia.org/wikipedia/commons/5/56/Sankt-Petersburg_Eremitage_by_night.JPG"),
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
