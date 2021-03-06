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
from MainPageHandler import *
from handlers import *
from ResultsPageHandler import *
from businessPageHandler import *

#Artiom K. Defines the pages our app is handling
app = webapp2.WSGIApplication(
    [('//?', MainPageHandler),
     ('/signup', SignUpHandler),
     ('/results' + RESULTS_RE, ResultsPageHandler),
     (BUSINESS_PID_RE, BusinessPageHandler)],

    debug=True)
