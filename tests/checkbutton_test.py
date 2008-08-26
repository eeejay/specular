# Speclenium Checkbox Test
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
'''WAI-ARIA Checkbox Test
Tests to see if the correct state change events are emited when checkboxes
are toggled.'''

from selenium import selenium
import unittest, time, re
from sys import platform
import settings

class CheckboxTest(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = \
            selenium(settings.current_host, 4444, 
                     settings.current_command, 
                     "http://www.mozilla.org/")
        #self.selenium.set_speed(1000)
        self.selenium.start()
        self.selenium.set_timeout(30000)

    def runTest(self):
        sel = self.selenium
        sel.open("/access/dhtml/checkbox")
        sel.click("//div[2]/span/img")
        success = False
        for i in xrange(10):
            e = sel.get_accessible_event_match(
                '<event type="object-state-changed-checked">'
                '<source><accessible role="check box"/>'
                '</source></event>', 0)
            if 'notfound' not in e:
                success = True
                break
            print 'retrying', i
        self.failUnless(
            success, 
            'Did not recieve a state-changed event after check button toggle')
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

#if __name__ == "__main__":
#    unittest.main()