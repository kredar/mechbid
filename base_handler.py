__author__ = 'Artiom'

""" The base request handler class.
"""


import webapp2
from tools import *


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render(self, template, **kw):
        self.write(render_str(template, **kw))

