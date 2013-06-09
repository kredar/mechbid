#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# test submit
#
import webapp2
from base_handler import *
from add_mechanic_handler import *
from search_handler import *


class MainHandler(BaseHandler):
    def get(self):
        #self.response.write('Hello world!')
        self.response.write(" <a href=\"add_mechanic\" > Add mechanic</a>"
                            "<br>"
                            " <a href=\"search\" > Search</a>")


app = webapp2.WSGIApplication(
    [('/add_mechanic', AddMechanicHandler),
     ('/search', SearchHandler),
     ('/', MainHandler)

    ],
    debug=True)
