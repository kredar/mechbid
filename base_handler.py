__author__ = 'Artiom'

import webapp2
from tools import *


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        #params['user_name'] = self.get_current_username()
        #params['logged_in'] = self.userLogedIn()
        #params['logoutLink'] = self.logoutLink()
        #params['isUserAdmin'] = self.isUserAdmin()
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(render_str(template, **kw))

