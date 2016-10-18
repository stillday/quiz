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

cities = [City (name="Vienna", country="Austria", picture="https://pixabay.com/static/uploads/photo/2016/04/15/22/08/town-hall-1332069_960_720.jpg"),
        City (name="Berlin", country="Germany", picture="hhttps://pixabay.com/static/uploads/photo/2015/10/15/09/03/berlin-989111_960_720.jpg"),
        City (name="Washington", country="USA", picture="https://pixabay.com/static/uploads/photo/2016/08/28/18/48/jefferson-memorial-1626580_960_720.jpg"),
        City (name="Sydney", country="Australia", picture="https://pixabay.com/static/uploads/photo/2014/06/06/09/36/sydney-363244_960_720.jpg"),
        City (name="London", country="UK", picture="https://pixabay.com/static/uploads/photo/2014/09/11/18/23/london-441853_960_720.jpg"),
        City (name="Cardiff", country="UK", picture="https://pixabay.com/static/uploads/photo/2013/03/02/01/51/mermaid-quay-89121_960_720.jpg"),
        City (name="Amsterdam", country="Netherlands", picture="https://pixabay.com/static/uploads/photo/2016/07/19/00/53/amsterdam-1527295_960_720.jpg"),
        City (name="Brussels", country="Belgium", picture="https://pixabay.com/static/uploads/photo/2016/01/13/17/02/belgium-1138448_960_720.jpg"),
        City (name="Den Haag", country="Netherlands", picture="https://pixabay.com/static/uploads/photo/2015/10/17/21/38/the-hague-993433_960_720.jpg"),
        City (name="Cologne", country="Germany", picture="https://pixabay.com/static/uploads/photo/2015/12/05/19/49/cologne-1078671_960_720.jpg"),
        City (name="Paris", country="France", picture="https://pixabay.com/static/uploads/photo/2013/04/11/19/46/louvre-102840_960_720.jpg"),
        City (name="Hamburg", country="Germany", picture="https://pixabay.com/static/uploads/photo/2014/07/09/22/24/harbour-city-388658_960_720.jpg"),
        City (name="Zürich", country="Switzerland", picture="https://pixabay.com/static/uploads/photo/2014/10/26/19/02/zurich-504252_960_720.jpg"),
        City (name="Copenhagen", country="Denmark", picture="https://pixabay.com/static/uploads/photo/2015/07/24/12/26/copenhagen-858271_960_720.jpg"),
        City (name="St Petersburg", country="Russia", picture="https://pixabay.com/static/uploads/photo/2015/11/08/21/54/st-petersburg-russia-1034319_960_720.jpg"),
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
