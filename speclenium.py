#!/usr/bin/env python
#
# Speclenium
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


import speclenium
import os, os.path
import sys
import subprocess
from time import sleep
from optparse import OptionParser

def run_selenium(jar_file):
    if not jar_file:
        try:
            script_dir = os.path.dirname(__file__) or '.'
        except NameError:
            # This could be one of those py2exe entry-points.
            script_dir = os.path.dirname(sys.executable)
        try:
            jar_file = filter(
                lambda x: x.startswith('selenium-server') and \
                    x.endswith('.jar'), os.listdir(script_dir))[0]
        except IndexError:
            return False
        jar_file = os.path.join(script_dir, jar_file)
    try:
        extra_args = os.environ['SELENIUM_ARGS'].split(' ')
    except KeyError:
        extra_args = []
    s = subprocess.Popen(['java', '-jar', jar_file] + extra_args)
    sleep(1)
    return s.poll() != 1
    

if __name__ == '__main__':
    usage = "Usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("--no-selenium", dest="no_selenium", default=False,
                      action="store_true", help="don't launch selenium-rc")
    parser.add_option("-S", "--selenium-jar", dest="selenium_jar",
                      help="selenium-rc jar file to launch")

    options, args = parser.parse_args()

    if not options.no_selenium:
        if not run_selenium(options.selenium_jar):
            print 'Could not launch Selenium-RC. Start Selenium-RC seperately'
    speclenium.main()
