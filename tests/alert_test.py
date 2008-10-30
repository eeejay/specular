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
    _failed_asserts = []
    expected_revision = 72
    broken = True

    def _wait_for_alert_show(self, subtest ,focus):
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
        try:
            self.failUnless(len(got_events) == len(events), 
                            'Did not get the right events for "%s"\n'
                            'Expected:\n%s\nGot:\n%s\n' % (subtest,
                                                           '\n'.join(events),
                                                           '\n'.join(got_events)))
        except AssertionError, e:
            print '-'*80
            print '\n'.join(self.selenium.dump_accessible_event_cache())
            print '-'*80
            self._failed_asserts.append(e)

    def _assert_no_alert_showing(self, subtest):
        try:
            self.assertEqual(
                self.selenium.get_accessible_match(
                    '<accessible role="alert" state="regexp:.*focusable.*" />'), 
                '', 'Found unexpected focusable "alert" accessible in "%s" test' % subtest)
        except AssertionError, e:
            self._failed_asserts.append(e)
        
        
    def _assert_alert_showing(self, subtest):
        try:
            self.assertNotEqual(
                self.selenium.get_accessible_match(
                    '<accessible role="alert" state="regexp:.*focusable.*" />'), 
                '', 
                'Failed to find focusable "alert" accessible in "%s" test' % subtest)
        except AssertionError, e:
            self._failed_asserts.append(e)
        

    def runTest(self):
        sel = self.selenium
        self._assert_no_alert_showing('')

        # Create and Focus
        subtest = 'Create and Focus'
        sel.click("//button[@onclick='createRemoveAlert(FOCUS_TEXT, true);']")
        self._wait_for_alert_show(subtest, True)
        self._assert_alert_showing(subtest)
        sel.click("//a[@onclick='createRemoveAlert();']")
        self._assert_no_alert_showing(subtest)

        # Create - no Focus
        subtest = 'Create - no Focus'
        sel.click("//button[@onclick='createRemoveAlert(NOFOCUS_TEXT, false);']")
        self._wait_for_alert_show(subtest, False)
        self._assert_alert_showing(subtest)
        sel.click("//a[@onclick='createRemoveAlert();']")
        self._assert_no_alert_showing(subtest)

        # Show (via visibility style) and Focus
        subtest = 'Show (via visibility style) and Focus'
        sel.click("//button[@onclick=\"toggleAlert('alertVis', true);\"]")
        self._wait_for_alert_show(subtest, True)
        self._assert_alert_showing(subtest)
        sel.click("link=close")
        self._assert_no_alert_showing(subtest)


        # Show (via visibility style) - no Focus
        subtest = 'Show (via visibility style) - no Focus'
        sel.click("//button[@onclick=\"toggleAlert('alertVis');\"]")
        self._wait_for_alert_show(subtest, False)
        self._assert_alert_showing(subtest)
        sel.click("link=close")
        self._assert_no_alert_showing(subtest)

        # Show (via display style) and Focus
        subtest = 'Show (via display style) and Focus'
        sel.click("//button[@onclick=\"toggleAlert('alertDisp', true);\"]")
        self._wait_for_alert_show(subtest, True)
        self._assert_alert_showing(subtest)
        sel.click("//div[@id='alertDisp']/div/a")
        self._assert_no_alert_showing(subtest)

        # Show (via display style) - no Focus
        subtest = 'Show (via display style) - no Focus'
        sel.click("//button[@onclick=\"toggleAlert('alertDisp');\"]")
        self._wait_for_alert_show(subtest, False)
        self._assert_alert_showing(subtest)
        sel.click("//div[@id='alertDisp']/div/a")
        self._assert_no_alert_showing(subtest)

        # Fail if we had any assertion failures.
        self.failUnless(
            self._failed_asserts == [],
            'Failed assertions:\n%s' \
                % '\n'.join(map(str, self._failed_asserts)))
    
#if __name__ == "__main__":
#    unittest.main()
