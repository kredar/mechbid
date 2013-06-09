__author__ = 'Artiom'

import logging

from google.appengine.ext import ndb
from google.appengine.api import memcache


class Mechanic(ndb.Model):
    """Model for Mechanics. A Mechanic entity will be built for each garage,
  and have an associated search.Document. The product entity does not include
  all of the fields in its corresponding indexed product document, only 'core'
  fields."""

    doc_id = ndb.StringProperty()
    name = ndb.StringProperty(required=True)
    #location = ndb.GeoPtProperty()
    address = ndb.TextProperty()
    description = ndb.TextProperty()
    active = ndb.IntegerProperty()


    @classmethod
    def create(cls, params, doc_id):
        """Create a new mechanic entity from a subset of the given params dict
        values, and the given doc_id."""
        mech = cls(
            id=params['pid'], name=params['name'],
            description=params['description'],
            address=params['address'],
            doc_id=doc_id)
        mech.put()
        return mech


    @classmethod
    def get_mech_by_id(cls, id):
        return Mechanic.get_by_id(id)


