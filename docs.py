__author__ = 'Artiom'

""" Contains 'helper' classes for managing search.Documents.
BaseDocumentManager provides some common utilities.
"""

import collections
import copy
import datetime
import logging
import re
import string
import urllib
from datetime import datetime
from base_handler import *

from config import *

from google.appengine.api import search
from google.appengine.ext import ndb

from random import randint
from random import uniform

class DeleteDocsPageHandler(BaseHandler):
    def get(self):
        BaseDocumentManager.delete_all_in_index(INDEX_NAME)
        self.redirect('/')


class BaseDocumentManager():
    """Abstract class. Provides helper methods to manage search.Documents."""

    @classmethod
    def create_document(cls, params):
        """ Creates doc for specific mechanic """
        # ALEXK split the location into pair of coordinates and create the geopoint
        # TODO make more proper handling of the undefined location (maybe block in GUI or not add to the document)
        businessLatitude = float(43.6519186) # this is a temporry solution since such case must be blocked in GUI
        businessLongitude = float(-79.3824024)

        if 'geo_lat' and 'geo_long' in params:#Artiom K. check if the key exists
            if params['geo_lat'] == "" or params['geo_lat'] == "undefined":
                logging.info("location as not defined as search criteria, setting to Toronto")
                businessLatitude = float(
                    43.6519186) # this is a temporry solution since such case must be blocked in GUI
                businessLongitude = float(-79.3824024)
            else:
                #coordinatesPair = tuple(params['location'].split(','))
                #businessLatitude = float(coordinatesPair[0].strip('(').strip(')'))
                #businessLongitude = float(coordinatesPair[1].strip('(').strip(')'))
                businessLatitude = float(params['geo_lat'])
                businessLongitude = float(params['geo_long'])
        geopoint = search.GeoPoint(businessLatitude, businessLongitude)

        #construct the address from the separated fields
        address = params['street'] + ", " + params['city'] + ", " + params['pcode']
        brands=''

        if params['brands'] == []:
            brands=''
        else:
            for brand in params['brands']:
                brands += brand + ','

        if params['num_reviews']=="":
            logging.info("number of reviews is not defined")
            num_reviews_var = random.randint(0, 100)        #random numbers for testing purposes
        else:
            num_reviews_var = int(params['num_reviews'])

        if params['avg_rating']=="":
            logging.info("average rating is not defined")
            avg_rating_var=round(random.uniform(1, 10), 2)           #random numbers for testing purposes
        else:
            avg_rating_var=float(params['avg_rating'])

        document = search.Document(
            fields=[search.TextField(name='pid', value=params['pid']),
                    search.TextField(name='name', value=params['name']),
                    search.TextField(name='address', value=address),
                    search.TextField(name='street', value=params['street']),
                    search.TextField(name='city', value=params['city']),
                    search.TextField(name='province', value=params['province']),
                    search.TextField(name='pcode', value=params['pcode']),
                    search.TextField(name='website', value=params['website']),
                    search.GeoField(name='location', value=geopoint),
                    #search.GeoField(name='geo_lat', value=params['geo_lat']),
                    #search.GeoField(name='geo_long', value=params['geo_long']),
                    #search.TextField(name='phones', value=params['phones']),
                    #search.TextField(name='categories', value=params['categories']),
                    search.TextField(name='brands', value=brands),
                    search.DateField(name='date', value=datetime.now().date()),
                    search.NumberField(name='num_reviews', value=num_reviews_var),
                    search.NumberField(name='avg_rating', value=avg_rating_var)
            ])

        try:
            search.Index(name=INDEX_NAME).put(document)
        except search.Error:
            logging.exception('Put failed')

        #for debug purpose only
        for index in search.get_indexes(fetch_schema=True):
            logging.info("index %s", index.name)
            logging.info("schema: %s", index.schema)
            #for debug purpose only


    @classmethod
    def delete_all_in_index(cls, index_name=INDEX_NAME):
        """Delete all the docs in the given index."""
        doc_index = search.Index(name=index_name)

        while True:
            # Get a list of documents populating only the doc_id field and extract the ids.
            document_ids = [document.doc_id
                            for document in doc_index.get_range(ids_only=True)]
            if not document_ids:
                logging.info("no docs found")
                break
                # Delete the documents for the given ids from the Index.
            logging.info("Deleting entries")
            doc_index.delete(document_ids)

            # def search_docs(self, index_name, query_str):
            #     try:
            #         results = search.Index(name=_INDEX_NAME).search(query_string)
            #         for scored_document in results:
            #         # process scored_document
            #
            #         except search.Error:
            #         logging.exception('Search failed')


    @classmethod
    def search_query(cls, query_string):
        results = None
        try:
            results = search.Index(name=INDEX_NAME).search(query_string)
            # for scored_document in results:
            #     # process scored_document
        except search.Error:
            logging.exception('Search failed')
        return results


    @classmethod
    def find_documents(cls, query_string, coordinates_to_search, limit, cursor):
        try:
            # Nathan Philip Square (addr., lat, long)
            # 100 Queen St W, Toronto, ON
            # 43.6519186
            # -79.3824024
            #TODO: Alex need to get location geo points
            # exampleLat = float(43.6519186)
            # exampleLon = float(-79.3824024)
            #loc_expr = 'distance(location, geopoint(%s, %s))' % (exampleLat, exampleLon)
            loc_expr = 'distance(location, geopoint%s)' % (coordinates_to_search)

            #expression='name',
            sort1 = search.SortExpression(
                expression=loc_expr,
                direction=search.SortExpression.ASCENDING,
                default_value=0)
            sort2 = search.SortExpression(
                expression='avg_rating',
                direction=search.SortExpression.DESCENDING,
                default_value=0)
            sort3 = search.SortExpression(
                expression='num_reviews',
                direction=search.SortExpression.DESCENDING,
                default_value=0)

            # Sort up to 1000 matching results by subject in descending order
            sort = search.SortOptions(expressions=[sort1, sort2, sort3], limit=1000)

            # Set query options
            sort_options = search.QueryOptions(
                limit=limit,# the number of results to return
                cursor=cursor,
                sort_options=sort,
                returned_fields=['name', 'address', 'location', 'pid', 'brands', 'phones','num_reviews','avg_rating'],
                snippeted_fields=['content'])

            #ALEXK added location example here, remove if all works
            # query = "distance(store_location, geopoint(-33.857, 151.215)) < 4500"
            #query_distance = ' distance(location, geopoint(%s, %s))<20000' % (exampleLat, exampleLon)
            query_distance = ' distance(location, geopoint%s)<20000' % coordinates_to_search
            query_string += query_distance
            logging.error(query_string)
            query = search.Query(query_string=query_string, options=sort_options)
            #query = search.Query(query_string=query_string, options=options)


            # query = search.Query(query_string=query_string, options=options)

            index = search.Index(name=INDEX_NAME)

            # Execute the query
            return index.search(query)
        except search.Error:
            logging.exception('Search failed')
        return None


def build_suggestions(self, str):
    """ Takes a sentence and returns the set of all possible prefixes for each word.
        For instance "hello world" becomes "h he hel hell hello w wo wor worl world" """
    suggestions = []
    for word in str.split():
        prefix = ""
        for letter in word:
            prefix += letter
            suggestions.append(prefix)
    return ' '.join(suggestions)

    # # Example use
    # document = search.Document(
    #     fields=[search.TextField(name='name', value=object_name),
    #             search.TextField(name='suggest', value=build_suggestions(object_name))])
