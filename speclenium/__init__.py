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

__version__   = "0.0.8"
__copyright__ = "Copyright (c) 2008 Eitan Isaacson"
__license__   = "MPL 1.1/GPL 2.0/LGPL 2.1"

from sys import platform
import os, os.path
import sys
import subprocess
from time import sleep

if platform == 'win32':
    from speclenium_win32 import Speclenium
else:
    from speclenium_atspi import Speclenium


def main(use_existing_selenium, selenium_jar, port=4117):
    from twisted.internet import reactor
    from twisted.web import server
 
    if use_existing_selenium and not run_selenium(selenium_jar):
        print 'Could not launch Selenium Server. Start Selenium Server separately (run with --help for options)'
        return

    run_selenium(selenium_jar)
       
    spec_server = Speclenium()
    try:
        reac = reactor;
        reac.listenTCP(port, server.Site(spec_server))
        reac.run()
    finally:
        # TODO: Proper exception handling.
        # TODO: Shutdown automatically when Selenium Server is shutdown separately. 
        spec_server.shutdown()
        print '==> Speclenium Server stopped'

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
    


