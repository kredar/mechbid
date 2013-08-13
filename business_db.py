__author__ = 'Art(i|y)om'

import logging

from google.appengine.ext import ndb
from google.appengine.api import memcache

car_brands = ["Acura","Aston Martin","Audi","Bentley","BMW","Buick","Cadillac","Chevrolet","Chrysler","Dodge","Ferrari","Fiat","Ford","GMC","Honda","Hyundai","Infiniti","Jaguar","Jeep","Kia","Lamborghini","Land Rover","Lexus","Lincoln","Lotus","Maserati","Maybach","Mazda","Mercedes-Benz","MINI","Mitsubishi","Nissan","Porsche","Ram","Rolls-Royce","Scion","smart","Subaru","Suzuki","Toyota","Volkswagen","Volvo"]


class Address(ndb.Model):
    street = ndb.StringProperty()
    city = ndb.StringProperty()
    province = ndb.StringProperty()
    country = ndb.StringProperty()
    postalCode = ndb.StringProperty()


class Phone(ndb.Model):
    type = ndb.StringProperty()
    number = ndb.StringProperty()

class Business(ndb.Model):
    id = ndb.StringProperty()
    name = ndb.StringProperty(required = True)
    address = ndb.StructuredProperty(Address, required = True)
    phones = ndb.StructuredProperty(Phone, repeated = True)
    email = ndb.StringProperty()
    website = ndb.StringProperty()
    geoLocation = ndb.GeoPtProperty(required = True)
    workingHours = ndb.StringProperty(repeated = True)
    languagesSpoken = ndb.StringProperty(repeated = True)
    brandsServiced = ndb.StringProperty(repeated = True)
    categories = ndb.StringProperty(repeated = True)
    services = ndb.StringProperty(repeated = True)
    paymentMethod = ndb.StringProperty(repeated = True)
    rating = ndb.IntegerProperty()
    dateAdded = ndb.DateTimeProperty(auto_now_add = True)
    active = ndb.BooleanProperty()

    @classmethod
    def create(cls, params, doc_id):
        """Create a new business entity from a subset of the given params dict
        values, and the given doc_id."""

        if params['brands'] == 'ALL':
            brands = car_brands
        else:
            brands = params['brands']

        phones = []
        for phone in params['phones']:
                new_phone = Phone(type=phone['type'], number=phone['number'])
                phones.append(new_phone)

        try:
            business = cls(
                id = params['pid'],
                name = params['name'],
                address = Address(street=params['street'], city=params['city'], province=params['province'], country='Canada', postalCode=params['pcode']),
                phones = phones,
                email = params['email'],
                website = params['website'],
                geoLocation =  ndb.GeoPt(params['geo_lat'], params['geo_long']),
                workingHours = params['open_hours'],
                languagesSpoken = params['lang_spk'],
                brandsServiced = brands,
                categories = params['categories'],
                services = params['products_services'],
                paymentMethod = params['pay_methods'],
                active = bool(1))
        except:
            return 'null'

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

