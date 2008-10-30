# Speclenium List Box iFrame Test
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

class ListBoxIframeTest(TestCommon, unittest.TestCase):
    '''WAI-ARIA List Box iFrame Test
    Tests to see if we get the right events when traversing the list. 
    This tests potential "iFrame" mashups.'''
    base_url = "http://codetalks.org/"
    path = "/source/widgets/listbox/listbox-owner.html"
    expected_revision = 71
    _failed_asserts = []

    def _wait_for_focus_change(self, name, role="list item"):
        event_query = '<event type="object-focus"><source><accessible role="%s" name="%s"/></source></event>' % (role, name)
        got_events = self.selenium.wait_accessible_events([event_query])

        try:
            self.failUnless(got_events != [], 
                            'Did not get a focus event for "%s"' % name)
        except AssertionError, e:
            print '\n\n'.join(self.selenium.dump_accessible_event_cache())
            self._failed_asserts.append(e)
            return None
        else:
            return got_events[0]

    def runTest(self):
        sel = self.selenium
        sel.click("//*[@id=\"listbox1-1\"]")
        self._wait_for_focus_change('Green')
        sel.click("//*[@id=\"listbox1-2\"]")
        self._wait_for_focus_change('Orange')
        sel.click("//*[@id=\"listbox1-3\"]")
        self._wait_for_focus_change('Red')
        sel.click("//*[@id=\"listbox1-4\"]")
        self._wait_for_focus_change('Blue')
        sel.click("//*[@id=\"listbox1-5\"]")
        self._wait_for_focus_change('Violet')
        sel.click("//*[@id=\"listbox1-6\"]")
        self._wait_for_focus_change('Periwinkle')

        self.failUnless(
            self._failed_asserts == [],
            'Failed assertions:\n%s' \
                % '\n'.join(map(str, self._failed_asserts)))
    
