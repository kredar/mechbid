__author__ = 'Artiom'
"""Contains all the handlers for the main application"""


from base_handler import *


class SignUpHandler(BaseHandler):
    def get(self):
        self.render("signup.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        email = self.request.get('email')


        u = User.register(username, password, email)
        u.put()
        self.login(u)
        self.redirect('/')
