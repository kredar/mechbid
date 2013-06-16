__author__ = 'Artiom'

""" The base request handler class.
"""


import webapp2
from tools import *
from user_db import *


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render(self, template, **kw):
        self.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        # params['user_name'] = self.get_current_username()
        # params['logged_in'] = self.userLogedIn()
        # params['logoutLink'] = self.logoutLink()
        # params['isUserAdmin'] = self.isUserAdmin()
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        #logging.error(str(user.key().id()))
        current_user = user.name
        # logging.error(str(user.key().id()))
        self.set_secure_cookie('user_id', str(user.key().id()))
        #self.set_secure_cookie('user_id', user.name)

    def logout(self):
        if self.user:
            self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))
        if self.user:
            self.current_user = User.by_id(int(uid)).name
        else:
            self.current_user = None

    def get_user_name(self):
        """Returns user_id from cookie"""
        if self.read_secure_cookie('user_id') != None:
            return self.read_secure_cookie('user_id')

    def userLoggedIn(self):
        if self.user or users.get_current_user():
            return True
        else:
            return False

    def get_current_username(self):
        if self.user:
            return self.user.name
        elif users.get_current_user():
            #logging.error("USER:  %s" %users.get_current_user().nickname() )
            return users.get_current_user().nickname()
        else:
            return None

    def logoutLink(self):
        if self.userType() == 0:
            return '/logout'
        else:
            return users.create_logout_url('/')

    def userType(self):
        if self.user:
            return 0
        else:
            return 1
    # def isUserAdmin(self):
    #
    #     """
    #     Checks if user is admin
    #
    #     :return: True - user is Admin, else return False
    #     """
    #     if self.userLogedIn():
    #         if self.userType() == 0:
    #             if self.user.name == ADMIN:
    #                 return True
    #             else:
    #                 return False
    #         elif self.userType() == 1:
    #             if users.is_current_user_admin():
    #                 return True
    #             else:
    #                 return False
    #     else:
    #         return None


