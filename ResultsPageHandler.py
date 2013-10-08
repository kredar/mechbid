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

        logging.error("str_to_search is %s" % str_to_search)

        #TODO: ARTIOM K. - need to take care of the location decomposition
        #the above code is not clear, so putting some checks
        coordinates_to_search = self.request.get('coordinatesForSearch')

        if not coordinates_to_search:
            coordinates_to_search = "(43.3333, -79.9999)"

        logging.error("coordinates_to_search is: %s" % coordinates_to_search)

        results = BaseDocumentManager.find_documents(str_to_search, coordinates_to_search, 20, search.Cursor())
        if results:
            self.render("results.html", results=results)
        else:
            self.redirect("/")