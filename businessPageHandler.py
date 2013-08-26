__author__ = 'Artiom'

import logging

from base_handler import *
from docs import *
from config import *
from business_db import *

#This class is handling all the Mechanic representation requests
class BusinessPageHandler(BaseHandler):
    def get(self, pid):
        logging.error("pid is ++++++++++ %s" % pid)
        pid = pid.replace('/', '')
        logging.error("pid is ++++++++++ %s" % pid)

        business = Business.get_business_by_id(pid)
        logging.error("name is ++++++++++ %s" % business.name)

        if business:
            self.render("shop_details.html", business=business)
        #else:
        #    self.render("cant_find_page.html")