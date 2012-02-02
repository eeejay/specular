# Speclenium Tree Test
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

expect_subtree = """\
<accessible role="regexp:outline|tree" state="regexp:.*focusable.*">
  <accessible/>
  <accessible name="Veggies" role="regexp:list|outline item" state="regexp:.*expanded.*"/>
  <accessible role="regexp:grouping|panel">
    <accessible/>
    <accessible name="Green" role="regexp:list|outline item" state="regexp:.*expanded.*"/>
    <accessible role="regexp:grouping|panel">
      <accessible name="Asparagus" role="regexp:list|outline item" 
                  state="regexp:^((?!expanded|expandable).)*$"/>
      <accessible name="Kale" role="regexp:list|outline item" 
                  state="regexp:^((?!expanded|expandable).)*$"/>
    </accessible>
  </accessible>
</accessible>"""

class TreeTest(TestCommon, unittest.TestCase):
    '''WAI-ARIA Tree Test
    Tests tree widgets. Specifically state changed events for 
    expanded/collapsed.'''
    base_url = "http://codetalks.org/"
    path = "/source/widgets/tree/tree.html"
    _failed_asserts = []

    def _wait_for_expanded(self, expanded):
        if expanded:
            state_regex = 'regexp:.*expanded.*'
        else:
            state_regex = 'regexp:^((?!expanded).)*$'

        event_query = '<event type="object-state-changed"><source>' \
            '<accessible name="Leafy" ' \
            'role="regexp:list|outline item" state="%s"/>' \
            '</source></event>' % state_regex

        got_events = self.speclenium_client.wait_accessible_events([event_query])

        try:
            self.failUnless(
                got_events != [], 
                'Did not get a state-change event for expand/collapse')
        except AssertionError, e:
            print '\n\n'.join(self.speclenium_client.dump_accessible_event_cache())
            self._failed_asserts.append(e)
            return None
        else:
            return got_events[0]


    def _wait_for_focus_change(self, name):
        event_query = '<event type="object-focus"><source><accessible role="regexp:list|outline item" name="%s"/></source></event>' % name
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

    def runTest(self):
        sel = self.speclenium_client

        found_subtree = self.speclenium_client.get_accessible_match(expect_subtree)
        
        try:
            self.failUnless(found_subtree, 
                            'Did not find proper subtree')
        except AssertionError, e:
            self._failed_asserts.append(e)

        sel.click("//div[@id='greenGroup']/div[1]/span")
        self._wait_for_focus_change('Asparagus')
        sel.click("//div[@id='greenGroup']/div[3]/img")
        self._wait_for_expanded(False)
        sel.click("//div[@id='greenGroup']/div[3]/img")
        self._wait_for_expanded(True)


        self.failUnless(
            self._failed_asserts == [],
            'Failed assertions:\n%s' \
                % '\n'.join(map(str, self._failed_asserts)))
    

#if __name__ == "__main__":
#    unittest.main()
