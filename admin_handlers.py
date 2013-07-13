__author__ = 'Artiom'

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
from mech_db import *
from pprint import pprint

from google.appengine.api import users
from google.appengine.ext.deferred import defer
from google.appengine.ext import ndb
from google.appengine.api import search


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
    datafile = os.path.join('input_data', '1')
    with open(datafile) as data_file:
        data = json.load(data_file)

    return data
    #self.write(pprint(data))
    #print json.load("/input_data/1")


class AdminHandler(BaseHandler):
    """Displays the admin page with all the admin options"""
    def get(self):
        self.render("admin.html")


class ImportMechData(BaseHandler):
    # TODO implement ImportMechData class
    # @BaseHandler.logged_in
    def get(self):
        self.write("Under construction")
        #self.write(importData())


class DeleteMechHandler(BaseHandler):
    """Remove mech entity with the given pid,
    including reviews and its associated indexed document."""

    def get(self):
        self.write("Under construction")


class CreateMechHandler(BaseHandler):
    """Handler to create a new mech account with all the properties: this constitutes both a mech entity
    and its associated indexed document."""

    def get(self):
        self.render("index.html")

    def post(self):
        name = self.request.get('name')
        description = self.request.get('description')
        address = self.request.get('address')



        params = {
            'pid': uuid.uuid4().hex, # auto-generate default UID
            'name': name,
            'description': description,
            'location': '',
            'address': address}

        BaseDocumentManager.create_document(name=name, description=description, address=address)

        Mechanic.create(params, params['pid'])



        self.redirect('/admin/manage')

