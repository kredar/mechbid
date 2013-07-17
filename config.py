__author__ = 'Artiom'

import re

""" Holds configuration settings.
"""


# the number of search results to display per page
DOC_LIMIT = 3
INDEX_NAME = "my_mechanic"

SECRET = "artiom"

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

