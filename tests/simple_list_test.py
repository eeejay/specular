# Speclenium Simple List Test
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

class SimpleListTest(TestCommon, unittest.TestCase):
    '''WAI-ARIA Simple List Test
    Tests to see if static divs with "list" and "listitem" roles are exposed
    correctly'''
    base_url = "http://codetalks.org/"
    path = "/source/enhanced-html-forms/list.html"
    expected_revision = 71

    def runTest(self):
        sel = self.selenium
        # "embedded component" is here just to have this test pass in Linux.
        match = sel.get_accessible_match("""
  <accessible role="list">
    <accessible name="dog" role="list item"/>
    <accessible name="cat" role="list item"/>
    <accessible name="sparrow" role="list item"/>
    <accessible name="wolf!"/>
  </accessible>
""")
        self.assertNotEqual(
            match,  '', 'No accessible with "application" role.')
