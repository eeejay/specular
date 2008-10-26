# Speclenium Test harness
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
#
# The Initial Developer of the Original Code is Eitan Isaacson.
# Portions created by the Initial Developer are Copyright (C) 2008
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Original Author: Eitan Isaacson (eitan@ascender.com)
#
# Alternatively, the contents of this file may be used under the terms of
# either of the GNU General Public License Version 2 or later (the "GPL"),
# or the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.

import os, os.path, sys
import unittest, new
from ConfigParser import ConfigParser

_testsdir = os.path.dirname(__file__)
sys.path.insert(0, _testsdir)

_test_modules = \
    map(lambda x: x[:-3],
        filter(lambda x: x.endswith('_test.py') and not x.startswith("."), 
               os.listdir(_testsdir)))

base_tests = {}
for mod in _test_modules:
    m = __import__(mod)
    for key, value in m.__dict__.items():
        if key.endswith('Test') and \
                issubclass(value, unittest.TestCase):
            base_tests[key] = value

def build_test_suite(config_file,
                     browsers=None, 
                     tests=base_tests.keys(),
                     base_url=None):
    cfg_parser = ConfigParser()
    cfg_parser.read(config_file)
    if not browsers:
        browsers = cfg_parser.sections()
    full_suite = unittest.TestSuite()
    for browser in browsers:
        class_dict = {'host': cfg_parser.get(browser, 'host'), 
                      'command' : cfg_parser.get(browser, 'command')}
        if base_url:
            class_dict['base_url'] = base_url
        suite = unittest.TestSuite()
        for test_name in tests:
            c = new.classobj(
                browser+test_name, (base_tests[test_name],), class_dict)
            suite.addTest(c())
        full_suite.addTest(suite)
    return full_suite
