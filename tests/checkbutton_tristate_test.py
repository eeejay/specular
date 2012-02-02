# Speclenium Checkbox Tristate Test
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

class CheckboxTristateTest(TestCommon, unittest.TestCase):
    '''WAI-ARIA Checkbox Tristate Test
    Tests to see if the correct state change events are emited when checkboxes
    are toggled. And that the there is partial state.'''
    base_url = "http://codetalks.org/"
    path = "/source/widgets/checkbox/checkbox-tristate.html"
    expected_revision = 120

    def _wait_for_checked(self, checked, name="regexp:.*"):
        if checked:
            state_regex = 'regexp:.*checked.*'
        elif checked is None:
            state_regex = 'regexp:.*(indeterminate|mixed).*'
        else:
            state_regex = 'regexp:^((?!checked|indeterminate|mixed).)*$'

        event_query = '<event type="object-state-changed"><source><accessible role="check box" name="%s" state="%s"/></source></event>' % (name, state_regex)
        got_events = self.speclenium_client.wait_accessible_events([event_query])

        self.failUnless(got_events != [])
        return got_events[0]

    def runTest(self):
        sel = self.speclenium_client
        sel.click("//span[@id='remove-to-clear']/img")
        self._wait_for_checked(False,'regexp:.*removeAttribute.*')
        sel.click("//span[@id='remove-to-clear']/img")
        self._wait_for_checked(None,'regexp:.*removeAttribute.*')
        sel.click("//span[@id='remove-to-clear']/img")
        self._wait_for_checked(True,'regexp:.*removeAttribute.*')
        sel.click("//span[@id='set-false-to-clear']/img")
        self._wait_for_checked(False, 'regexp:.*setAttribute.*')
        sel.click("//span[@id='set-false-to-clear']/img")
        self._wait_for_checked(None, 'regexp:.*setAttribute.*')
        sel.click("//span[@id='set-false-to-clear']/img")
        self._wait_for_checked(True, 'regexp:.*setAttribute.*')    

#if __name__ == "__main__":
#    unittest.main()
