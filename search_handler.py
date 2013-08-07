__author__ = 'Artiom'


import logging

from base_handler import *
from docs import *
from config import *

_INDEX_NAME="my_mechanic"


class SearchHandler(BaseHandler):
    def get(self):
        self.render("search.html")

    def post(self):
        str_to_search = self.request.get('search')

        #str_to_search = "second"
        #logging.error("search ====================== %s " % str_to_search)
        # Set query options

        #query = search.Query(query_string=str_to_search, options=options)
        #results = search.Index(name=INDEX_NAME).search(str_to_search)
        results = BaseDocumentManager.find_documents(str_to_search, 20, search.Cursor())

        #self.write(results)
        if results:
            for doc in results:
                # logging.info("doc: %s ", doc)
                #search_str="ID="+doc.id+doc.field
                self.write("name %s <br>" % doc.field('name').value)
                self.write("doc ID= %s <br>" % doc.doc_id)
                self.write("doc = %s <br><br>" % doc)

        else:
            self.write("No Results")



    # def find_documents(self, query_string, limit, cursor):
    #
    #     try:
    #         subject_desc = search.SortExpression(
    #             expression='name',
    #             #direction=search.SortExpression.DESCENDING,
    #             direction=search.SortExpression.ASCENDING,
    #             default_value='')
    #
    #         # Sort up to 1000 matching results by subject in descending order
    #         sort = search.SortOptions(expressions=[subject_desc], limit=1000)
    #
    #         # Set query options
    #         options = search.QueryOptions(
    #             limit=limit,  # the number of results to return
    #             cursor=cursor,
    #             sort_options=sort,
    #             returned_fields=['name', 'address', 'description'],
    #             snippeted_fields=['content'])
    #
    #         query = search.Query(query_string=query_string, options=options)
    #
    #         index = search.Index(name=INDEX_NAME)
    #
    #         # Execute the query
    #         return index.search(query)
    #     except search.Error:
    #         logging.exception('Search failed')
    #     return None
    #
    # """ Takes a sentence and returns the set of all possible prefixes for each word.
    # For instance "hello world" becomes "h he hel hell hello w wo wor worl world" """
    # def build_suggestions(self, str):
    #     suggestions = []
    #     for word in str.split():
    #         prefix = ""
    #         for letter in word:
    #             prefix += letter
    #             suggestions.append(prefix)
    #     return ' '.join(suggestions)
    #
    # # # Example use
    # # document = search.Document(
    # #     fields=[search.TextField(name='name', value=object_name),
    # #             search.TextField(name='suggest', value=build_suggestions(object_name))])