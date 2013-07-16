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

from config import *

from google.appengine.api import search
from google.appengine.ext import ndb


class BaseDocumentManager():
    """Abstract class. Provides helper methods to manage search.Documents."""

    @classmethod
    def create_document(cls, params):
    #name, description, address):

        """ Creates doc for specific mechanic """
        document = search.Document(
            fields=[search.TextField(name='name', value=params['name']),
                    search.TextField(name='description', value=params['description']),
                    search.TextField(name='address', value=params['address']),
                    search.DateField(name='date', value=datetime.now().date())])


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
    def delete_all_in_index(cls, index_name):
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
    def find_documents(cls, query_string, limit, cursor):
        try:
            subject_desc = search.SortExpression(
                expression='name',
                #direction=search.SortExpression.DESCENDING,
                direction=search.SortExpression.ASCENDING,
                default_value='')


            # Sort up to 1000 matching results by subject in descending order
            sort = search.SortOptions(expressions=[subject_desc], limit=1000)

            # Set query options
            options = search.QueryOptions(
                limit=limit, # the number of results to return
                cursor=cursor,
                sort_options=sort,
                returned_fields=['name', 'address', 'description'],
                snippeted_fields=['content'])

            query = search.Query(query_string=query_string, options=options)

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
