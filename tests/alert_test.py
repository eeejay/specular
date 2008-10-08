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
    base_url = "http://test.cita.uiuc.edu/"
    path = "/aria/alert/view_inline.php?title=Alert%20Example%201:%20Number%20Guessing%20Game&ginc=includes/alert1_inline.inc&gcss=css/alert1_class.css&gjs=../js/globals.js,../js/widgets_inline.js,js/alert1_class.js"
    def runTest(self):
        sel = self.selenium
        result = sel.get_accessible_match('<accessible role="alert">'
                                          '  <accessible name="Make a guess"/>'
                                          '</accessible>')
        self.failUnless(result)
    
#if __name__ == "__main__":
#    unittest.main()
