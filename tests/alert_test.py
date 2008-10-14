# Speclenium Alert Test
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

import unittest, time, re
from sys import platform
from common import TestCommon
from time import sleep

class AlertTest(TestCommon, unittest.TestCase):
    '''WAI-ARIA Alert Test
    Tests to see if an accessible with an 'alert' role is in the document'''
    base_url = "http://codetalks.org/"
    path = "/source/widgets/alert/alert.html"

    def _wait_for_alert_show(self, focus):
        events = [
            '<event type="object-add">'
            '<source><accessible role="alert"/>'
            '</source></event>', 
            '<event type="system-alert">'
            '<source><accessible role="alert"/>'
            '</source></event>']

        if focus:
            events.append('<event type="object-focus">'
                          '<source><accessible role="alert"/>'
                          '</source></event>')
        
        got_events = self.selenium.wait_accessible_events(events)
        self.failUnless(len(got_events) == len(events), 
                        'Expected:\n%s\nGot:\n%s\n' % ('\n'.join(events),
                                                       '\n'.join(got_events)))

    def _assert_no_alert_showing(self):
        self.assertEqual(
            self.selenium.get_accessible_match(
                '<accessible role="alert" state="regexp:^((?!invisible).)*$" />'), '')
        
        
    def _assert_alert_showing(self):
        self.assertNotEqual(
            self.selenium.get_accessible_match(
                '<accessible role="alert" state="regexp:^((?!invisible).)*$" />'), '')
        

    def runTest(self):
        sel = self.selenium
        self._assert_no_alert_showing()
        sel.click("//button[@onclick='createRemoveAlert(FOCUS_TEXT, true);']")
        self._wait_for_alert_show(True)
        self._assert_alert_showing()
        sel.click("//a[@onclick='createRemoveAlert();']")
        self._assert_no_alert_showing()
        sel.click("//button[@onclick='createRemoveAlert(NOFOCUS_TEXT, false);']")
        self._wait_for_alert_show(False)
        self._assert_alert_showing()
        sel.click("//a[@onclick='createRemoveAlert();']")
        self._assert_no_alert_showing()
        sel.click("//button[@onclick=\"toggleAlert('alertVis', true);\"]")
#        self._wait_for_alert_show(True)
        self._assert_alert_showing()
        a = sel.get_accessible_doc()
        sel.click("link=close")
        self._assert_no_alert_showing()
        sel.click("//button[@onclick=\"toggleAlert('alertVis');\"]")
        self._wait_for_alert_show(False)
        self._assert_alert_showing()
        sel.click("link=close")
        self._assert_no_alert_showing()
        sel.click("//button[@onclick=\"toggleAlert('alertDisp', true);\"]")
#        self._wait_for_alert_show(True)
        self._assert_alert_showing()
        sel.click("//div[@id='alertDisp']/div/a")
        self._assert_no_alert_showing()
        sel.click("//button[@onclick=\"toggleAlert('alertDisp');\"]")
        self._wait_for_alert_show(False)
        self._assert_alert_showing()
        sel.click("//div[@id='alertDisp']/div/a")
        self._assert_no_alert_showing()
        #self.failUnless(result)
    
#if __name__ == "__main__":
#    unittest.main()
