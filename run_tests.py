#!/usr/bin/env python
#
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
import tests
from ConfigParser import ConfigParser

test_dir = os.path.join(os.path.dirname(__file__), 'tests')

sys.path.insert(0, test_dir)

def list_tests():
    print 'Available tests:'
    test_names = tests.base_tests.keys()
    test_names.sort()
    for tname in test_names:
        tclass = tests.base_tests[tname]
        try:
            short_desc = tclass.__doc__.split('\n')[0]
        except:
            short_desc = ''
        if tclass.broken:
            short_desc += ' (BROKEN)'
        print ' %s%s%s' % (tname, ' '*(25-len(tname)), short_desc)

def main(cfg_file, matrix_args, gui):
    global test_suite
    test_suite = tests.build_test_suite(cfg_file, **matrix_args)
    if gui:
        import unittestgui
        unittestgui.main('__main__.test_suite')
    else:
        unittest.TextTestRunner().run(test_suite)

if __name__ == '__main__':
    from optparse import OptionParser

    usage = "Usage: %prog [options] tests"
    parser = OptionParser(usage)
    parser.add_option("--list-tests", dest="list_tests",
                      action="store_true", help="list available tests")
    parser.add_option("--list-agents", dest="list_agents",
                      action="store_true", help="list available user agents")
    parser.add_option("--include-broken", dest="include_broken",
                      action="store_true", default=False,
                      help="include broken tests in suite")
    parser.add_option("-B", "--browsers", dest="browsers",
                      help="comma seperated list of browsers")
    parser.add_option("-g", "--gui", dest="gui",
                      action="store_true", help="run tests in gui")
    parser.add_option("-U", "--base-url", dest="base_url",
                      default="http://codetalks.org/",
                      action="store", help="base url for all tests.")
    parser.add_option("-c", "--config", dest="cfg_file",
                      action="store", help="config file", 
                      default="settings.ini")

    (options, args) = parser.parse_args()
    if options.list_tests:
        list_tests()
    elif options.list_agents:
        cfg = ConfigParser()
        cfg.read(options.cfg_file)
        print 'Available user agents:'
        for section in cfg.sections():
            print ' %s' % section
    else:
        matrix_args = {'base_url':options.base_url, 
                       'include_broken':options.include_broken}
        if args != []:
            matrix_args['tests'] = args
        if options.browsers:
            matrix_args['browsers'] = options.browsers.split(',')
        main(options.cfg_file, matrix_args, options.gui)
