__author__ = 'Art(i|y)om'

import logging

from google.appengine.ext import ndb
from google.appengine.api import memcache




class Address(ndb.Model):
    street = ndb.StringProperty()
    city = ndb.StringProperty()
    province = ndb.StringProperty()
    country = ndb.StringProperty()
    postalCode = ndb.StringProperty()


class Phone(ndb.Model):
    type = ndb.StringProperty(choices = ["phone","fax","cell"])
    number = ndb.StringProperty()


class WorkingHours(ndb.Model):
    day = ndb.StringProperty(choices = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
    from_hour = ndb.TimeProperty()
    to_hour = ndb.TimeProperty()



class Business(ndb.Model):
    id = ndb.IntegerProperty()
    name = ndb.StringProperty(required=True)
    addresses = ndb.StructuredProperty(Address, required=True)
    phones = ndb.StructuredProperty(Phone, repeated = True)
    email = ndb.StringProperty()
    website = ndb.StringProperty()
    geoLocation = ndb.GeoPtProperty(required=True)
    workingHours = ndb.StructuredProperty(WorkingHours, repeated = True)
    languagesSpoken = ndb.StringProperty(repeated = True)
    brandsServiced = ndb.StringProperty(repeated = True)
    categories = ndb.StringProperty(repeated = True)
    services = ndb.StringProperty(repeated = True) #TBD
    paymentMethod = ndb.StringProperty(repeated = True)
    rating = ndb.IntegerProperty()
    dateAdded = ndb.DateTimeProperty(auto_now_add = True)
    active = ndb.BooleanProperty()

    @classmethod
    def create(cls, params, doc_id):
        """Create a new business entity from a subset of the given params dict
        values, and the given doc_id."""

        business = cls(
            id=params['pid'],
            name=params['name'])

        business.put()

        return business

    @classmethod
    def get_business_by_id(cls, id):
        return Business.get_by_id(id)



class Review(ndb.Model):
    business = ndb.KeyProperty(kind = Business)
    reviewText= ndb.StringProperty()
    mark = ndb.IntegerProperty(choices = [1,2,3,4,5])
    dateTimeAdded =  ndb.DateTimeProperty(auto_now_add = True)
    #user =  TBD

