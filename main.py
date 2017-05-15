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


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

    def post(self):
        params = {"sporocilo": "Oh, ok then :("}
        return self.render_template("index.html", params=params)


class LotoHandler(BaseHandler):
    def get(self):
        stevilke = random.sample(range(1, 40), 7)
        params = {"loto_numbers": stevilke}
        return self.render_template("lotto.html", params=params)

    def post(self):
        stevilke = random.sample(range(1, 40), 7)
        params = {"sporocilo2": "Really? I thought they were pretty good.",
                  "loto_numbers": stevilke}
        params2 = {"sporocilo3": "You're welcome!"}

        if self.request.method == 'POST' and 'new_numbers' in self.request.POST:
            return self.render_template("lotto.html", params=params)
        if self.request.method == 'POST' and 'thanks' in self.request.POST:
            return self.render_template("lotto.html", params=params2)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/lotto', LotoHandler),
], debug=True)

