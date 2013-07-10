__author__ = 'Artiom'
#!/usr/bin/env python
#

"""Defines the routing for the app's admin request handlers
(those that require administrative access)."""

from admin_handlers import *

import webapp2

application = webapp2.WSGIApplication(
    [
        ('/admin/manage', AdminHandler),
        ('/admin/import_mech_data', ImportMechData),
        ('/admin/add_business', CreateBusinessHandler),
        ('/admin/delete_mech', DeleteMechHandler)
    ],
    debug=True)

