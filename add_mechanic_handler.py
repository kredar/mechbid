__author__ = 'Artiom'

import logging
import uuid

from base_handler import *
from mech_db import *
from docs import *
from google.appengine.api import search


class AddMechanicHandler(BaseHandler):

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



        self.redirect('/')



