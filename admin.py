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
        ('/admin/create_product', CreateProductHandler),
        ('/admin/delete_product', DeleteProductHandler)
    ],
    debug=True)

