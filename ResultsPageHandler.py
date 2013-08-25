__author__ = 'Artiom'

import logging

from base_handler import *
from docs import *
from config import *

_INDEX_NAME = "my_mechanic"

#This class is handling all the search requests
class ResultsPageHandler(BaseHandler):
    def get(self, query):
        url_get = self.request.GET
        logging.error("Current URL is %s" % url_get)
        logging.error("query is %s" % query)
        matchObj = re.match(r'/(.*)-near-(.*?)$', query, re.M | re.I)
        if matchObj:
            str_to_search = matchObj.group(1)
            location = matchObj.group(2)

        str_to_search = str_to_search.replace('-', ' ')


        results = BaseDocumentManager.find_documents(str_to_search, 20, search.Cursor())

        self.render("results.html", results=results)