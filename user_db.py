__author__ = 'Artiom'

"""Contains user db and associated functions"""


import os
import re
import random
import hashlib
import hmac

import logging
import time
import urllib

from string import letters
from time import gmtime, strftime

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.api import mail
#from google.appengine.ext import blobstore
from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext.webapp import blobstore_handlers

from config import *


def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(SECRET, val).hexdigest())


def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val


def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)


def users_key(group='default'):
    """

    :param group:
    :return:
    """
    return ndb.Key('users', group)


def valid_username(username):
    return username and USER_RE.match(username)


def valid_password(password):
    return password and PASS_RE.match(password)


def valid_email(email):
    return not email or EMAIL_RE.match(email)


class User(ndb.Model):
    # TODO move User model to ndb
    name = ndb.StringProperty(required=True)
    pw_hash = ndb.StringProperty(required=True)
    email = ndb.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent=users_key(),
                    name=name,
                    pw_hash=pw_hash,
                    email=email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u

    @classmethod
    def add_user(cls, username, password, email):
        u = User.register(username, password, email)
        u.put()


