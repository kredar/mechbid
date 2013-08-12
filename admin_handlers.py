__author__ = 'Art(i|y)om'

#!/usr/bin/env python
#

""" Contains the admin request handlers for the app (those that require
administrative access).
"""

import csv
import logging
import os
import urllib
import uuid
import json

from base_handler import BaseHandler
from docs import *
from business_db import *
from pprint import pprint

from google.appengine.api import users
from google.appengine.ext.deferred import defer
from google.appengine.ext import ndb
from google.appengine.api import search

car_brands = ["Acura","Aston Martin","Audi","Bentley","BMW","Buick","Cadillac","Chevrolet","Chrysler","Dodge","Ferrari","Fiat","Ford","GMC","Honda","Hyundai","Infiniti","Jaguar","Jeep","Kia","Lamborghini","Land Rover","Lexus","Lincoln","Lotus","Maserati","Maybach","Mazda","Mercedes-Benz","MINI","Mitsubishi","Nissan","Porsche","Ram","Rolls-Royce","Scion","smart","Subaru","Suzuki","Toyota","Volkswagen","Volvo"]

def reinitAll(sample_data=True):
    """
    Deletes all product entities and documents, essentially resetting the app
    state, then loads in static sample data if requested. Hardwired for the
    expected product types in the sample data.
    (Re)loads store location data from stores.py as well.
    This function is intended to be run 'offline' (e.g., via a Task Queue task).
    As an extension to this functionality, the channel ID could be used to notify
    when done."""

    # delete all the product and review entities
    review_keys = models.Review.query().fetch(keys_only=True)
    ndb.delete_multi(review_keys)
    prod_keys = models.Product.query().fetch(keys_only=True)
    ndb.delete_multi(prod_keys)
    # delete all the associated product documents in the doc and
    # store indexes
    docs.Product.deleteAllInProductIndex()
    docs.Store.deleteAllInIndex()
    # load in sample data if indicated
    if sample_data:
        logging.info('Loading product sample data')
        # Load from csv sample files.
        # The following are hardwired to the format of the sample data files
        # for the two example product types ('books' and 'hd televisions')-- see
        # categories.py
        datafile = os.path.join('data', config.SAMPLE_DATA_BOOKS)
        # books
        reader = csv.DictReader(
            open(datafile, 'r'),
            ['pid', 'name', 'category', 'price',
             'publisher', 'title', 'pages', 'author',
             'description', 'isbn'])
        importData(reader)
        datafile = os.path.join('data', config.SAMPLE_DATA_TVS)
        # tvs
        reader = csv.DictReader(
            open(datafile, 'r'),
            ['pid', 'name', 'category', 'price',
             'size', 'brand', 'tv_type',
             'description'])
        importData(reader)

        # next create docs from store location info
        loadStoreLocationData()

    logging.info('Re-initialization complete.')


def loadStoreLocationData():
    # create documents from store location info
    # currently logs but otherwise swallows search errors.
    slocs = stores.stores
    for s in slocs:
        logging.info("s: %s", s)
        geopoint = search.GeoPoint(s[3][0], s[3][1])
        fields = [search.TextField(name=docs.Store.STORE_NAME, value=s[1]),
                  search.TextField(name=docs.Store.STORE_ADDRESS, value=s[2]),
                  search.GeoField(name=docs.Store.STORE_LOCATION, value=geopoint)
        ]
        d = search.Document(doc_id=s[0], fields=fields)
        try:
            add_result = search.Index(config.STORE_INDEX_NAME).put(d)
        except search.Error:
            logging.exception("Error adding document:")


def importData():
    """Import via the csv reader iterator using the specified batch size as set in
    the config file.  We want to ensure the batch is not too large-- we allow 100
    rows/products max per batch."""
    # MAX_BATCH_SIZE = 100
    # rows = []
    # # index in batches
    # # ensure the batch size in the config file is not over the max or < 1.
    # batchsize = utils.intClamp(config.IMPORT_BATCH_SIZE, 1, MAX_BATCH_SIZE)
    # logging.debug('batchsize: %s', batchsize)
    # for row in reader:
    #     if len(rows) == batchsize:
    #         docs.Product.buildProductBatch(rows)
    #         rows = [row]
    #     else:
    #         rows.append(row)
    # if rows:
    #     docs.Product.buildProductBatch(rows)
    datafile = os.path.join('input_data', '')
    with open(datafile) as data_file:
        data = json.load(data_file)

    return data
    #self.write(pprint(data))
    #print json.load("/input_data/1")


def OpenJson(file_name, dir_name):

    datafile = os.path.join(dir_name, file_name)
    with open(datafile) as data_file:
        data = json.load(data_file)

    return data


def GetFileList(dir_name):

    file_list = os.listdir(dir_name)
    return file_list


def ImportNewBusiness(file_name, dir_name):
        json_doc = OpenJson(file_name, dir_name)
        #parse json

        #website
        try:
            website = json_doc['products']['webUrl'][0]
        except:
            website='null'

        # categories
        categories = []
        try:
            for category in json_doc['categories']:
                categories.append(category['name'])
        except:
            categories=[]

        # phones
        phones = []
        try:
            for phone in json_doc['phones']:
                phone_dict = {'type': phone['type'], 'number': phone['dispNum']}
                phones.append(phone_dict)
        except:
            phones=[]

        # pay methods
        pay_methods = []
        try:
            for pmethod in json_doc['products']['profiles'][0]['keywords']['MthdPmt']:
                pay_methods.append(pmethod)
        except:
            pay_methods=[]

        # spoken languages
        lang_spk = []
        try:
            for lang in json_doc['products']['profiles'][0]['keywords']['LangSpk']:
                lang_spk.append(lang)
        except:
            lang_spk=[]

        # open hours
        open_hours = []
        try:
            for day in json_doc['products']['profiles'][0]['keywords']['OpenHrs']:
                open_hours.append(day)
        except:
            open_hours=[]

        # products and services
        products_services = []
        try:
            for prod_serv in json_doc['products']['profiles'][0]['keywords']['ProdServ']:
               products_services.append(prod_serv)
        except:
            products_services=[]

        # specials
        specials = []
        try:
            for special in json_doc['products']['profiles'][0]['keywords']['Special']:
                specials.append(special)
        except:
            specials=[]

        # brands
        brands = []
        try:
            for brand in json_doc['products']['profiles'][0]['keywords']['BrndCrrd']:
                brands.append(brand)
        except:
            brands='ALL'

        # teasers
        teasers = []
        try:
            for teaser in json_doc['products']['profiles'][0]['keywords']['Teaser']:
                teasers.append(teaser)
        except:
            teasers=[]

        #self.write(json.dumps(json_doc, sort_keys=True, indent=4))

        params = {
            'pid': uuid.uuid4().hex, # auto-generate default UID
            'name': json_doc['name'],
            'street':  json_doc['address']['street'],
            'city': json_doc['address']['city'],
            'pcode': json_doc['address']['pcode'],
            'province': json_doc['address']['prov'],
            'email': '',
            'website': website,
            'geo_lat': json_doc['geoCode']['latitude'],
            'geo_long': json_doc['geoCode']['longitude'],
            'categories': categories,
            'phones': phones,
            'pay_methods': pay_methods,
            'lang_spk': lang_spk,
            'open_hours': open_hours,
            'specials': specials,
            'brands': brands,
            'teasers': teasers,
            'products_services': products_services}

        #self.write(params['phones'][0]['type'])



        if Business.create(params, params['pid']) != 'null':
            BaseDocumentManager.create_document(params)
            return 'Business '+json_doc['name']+' successfully created'

        return 'ERROR creating '+json_doc['name']+' business!'


class AdminHandler(BaseHandler):
    """Displays the admin page with all the admin options"""
    def get(self):
        self.render("admin.html")


class ImportMechData(BaseHandler):

    # @BaseHandler.logged_in

    def get(self):
        file_list_to_import = GetFileList('input_data')

        for file in file_list_to_import:
             self.write(ImportNewBusiness(file, 'input_data'))
             self.write('<br>')


class DeleteMechHandler(BaseHandler):
    """Remove mech entity with the given pid,
    including reviews and its associated indexed document."""

    def get(self):
        self.write("Under construction")



class CreateBusinessHandler(BaseHandler):
    """Handler to create a new business account with all the properties: this constitutes both a mech entity
    and its associated indexed document."""

    #"Jenkins Test 2"
    def get(self):
        self.render("new_business.html", car_brands=car_brands)

    def post(self):

        phones = {}
        #Get all phones
        phone_num = 1

        while self.request.get('phone_number'+str(phone_num)) != '':
            phones['type'+str(phone_num)] = self.request.get('phone_type'+str(phone_num))
            phones['number'+str(phone_num)] = self.request.get('phone_number'+str(phone_num))
            phone_num += 1

        params = {
            'pid': uuid.uuid4().hex, # auto-generate default UID
            'name': self.request.get('name'),
            'street': self.request.get('street'),
            'city': self.request.get('city'),
            'pcode': self.request.get('pcode'),
            'province': self.request.get('province'),
            'phone_type': self.request.get('phone_type1'),
            'phone_number': self.request.get('phone_number1'),
            'email': self.request.get('email'),
            'website': self.request.get('website'),
            'location': self.request.get('location')}

        # BaseDocumentManager.create_document(name=name, description=description, address=address)
        BaseDocumentManager.create_document(params=params)
        #Business.create(params, params['pid'])

        self.redirect('/admin/manage')

        #testing  stuff here - pls ignore.
        #Artyom

        #self.response.write("<h3>"+phones['number1']+"</h3><br><h3>"+phones['type2']+"</h3>")



