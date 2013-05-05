__author__ = 'Artiom'

import logging

from google.appengine.ext import ndb
from google.appengine.api import memcache


class Mechanic(ndb.Model):
    name = ndb.StringProperty(required=True)
    location = ndb.GeoPtProperty()
    #address =