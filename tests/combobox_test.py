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

class ComboboxEditTest(TestCommon, unittest.TestCase):
    '''WAI-ARIA Checkbox Tristate Test
    Tests to see if the correct state change events are emited when checkboxes
    are toggled. And that the there is partial state.'''
    base_url = "http://codetalks.org/"
    path = "/source/widgets/combobox/combo-editable.html"
    expected_revision = 71
    _failed_asserts = []

    def _wait_for_focus_change(self, 
                               name, role="list item", value="regexp:.*"):
        event_query = '<event type="object-focus"><source><accessible role="%s" name="%s" value="%s"/></source></event>' % (role, name, value)
        got_events = self.speclenium_client.wait_accessible_events([event_query])

        try:
            self.failUnless(got_events != [], 
                            'Did not get a focus event for "%s"' % name)
        except AssertionError, e:
            print '\n\n'.join(self.speclenium_client.dump_accessible_event_cache())
            self._failed_asserts.append(e)
            return None
        else:
            return got_events[0]

    def _wait_for_combobox_show(self):
        events = [
            '<event type="object-add">'
            '<source><accessible role="list"/>'
            '</source></event>',
            '<event type="object-focus">'
            '<source><accessible name="cool" role="list item"/>'
            '</source></event>']

        
        got_events = self.speclenium_client.wait_accessible_events(events)
        try:
            self.failUnless(len(got_events) == len(events), 
                            'Did not get the right events for combo box show\n'
                            'Expected:\n%s\nGot:\n%s\n' % (
                    '\n'.join(events),
                    '\n'.join(got_events)))
        except AssertionError, e:
            print '\n\n'.join(self.speclenium_client.dump_accessible_event_cache())
            self._failed_asserts.append(e)


    def runTest(self):
        sel = self.speclenium_client
        sel.type("cat", "cool")
        sel.key_down("cat", "\\13")
        self._wait_for_combobox_show()
        sel.key_down('//*[@id="combo"]', "\\38")
        self._wait_for_focus_change('catholic')        
        sel.key_down('//*[@id="combo"]', "\\38")
        self._wait_for_focus_change('cathedral')        
        sel.key_down('//*[@id="combo"]', "\\38")
        self._wait_for_focus_change('caterpillar')        
        sel.key_down('xpath=/html/body/div/div/div[7]', "\\13")
        self._wait_for_focus_change(
            'regexp:Editable Combo:.*', 
            'regexp:(entry|editable text)', 
            'caterpillar')        
        
        self.failUnless(
            self._failed_asserts == [],
            'Failed assertions:\n%s' \
                % '\n'.join(map(str, self._failed_asserts)))
    
#if __name__ == "__main__":
#    unittest.main()
