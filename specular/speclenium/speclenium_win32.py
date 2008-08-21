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

from twisted.internet import win32eventreactor
win32eventreactor.install()
from twisted.internet import reactor
from twisted.web import xmlrpc, server
from specular.specular_event import events_map
import pyia
from speclenium_base import SpecleniumBase

class Speclenium(SpecleniumBase):
    """An example object to be published."""
    def __init__(self):
        SpecleniumBase.__init__(self)

    def xmlrpc_start(self, browser_start_cmd):
        SpecleniumBase.xmlrpc_start(self, browser_start_cmd)
        print 'starty, yo!'
        self._top_frame = None
        self._target_pid = -1
        self._window_id = -1
        pyia.Registry.registerEventListener(
            self._get_win, pyia.EVENT_OBJECT_NAMECHANGE)
        return True

    def _get_win(self, event):
        if event.source != None:
            if self._target_pid == -1 and \
                    'Selenium Remote Control' in (event.source.accName(0) or ''):
                self._target_pid = pyia.getAccessibleThreadProcessID(event.source)[0]
                self._window_id = event.hwnd
            elif pyia.getAccessibleThreadProcessID(event.source)[0] == self._target_pid and \
                    self._window_id != event.hwnd:
                pyia.Registry.deregisterEventListener(
                    self._get_win, pyia.EVENT_OBJECT_NAMECHANGE)
                self._top_frame = event.source
                print 'TOP FRAME', event.source

    def xmlrpc_start_event_cache(self):
        if not self._registered_global_listener:
            for value in events_map.values():
                pyia.Registry.registerEventListener(self._event_cache_cb, value)
        self._registered_global_listener = True
        return True

    def xmlrpc_stop_event_cache(self):
        if self._registered_global_listener:
            for value in events_map.values():
                pyia.Registry.deregisterEventListener(self._event_cache_cb, value)
        self._registered_global_listener = False
        return True

    def _find_root_doc(self, window_acc):
        print '_find_root_doc'
        agent_id = self._get_agent()
        print 'agent', self.AGENTS[agent_id]
        rv = None
        if agent_id == self.AGENT_MOZILLA:
            # Firefox
            pred = lambda x: x.accRole(0) == pyia.ROLE_SYSTEM_DOCUMENT and \
                not x.accState(0) & pyia.STATE_SYSTEM_INVISIBLE
            rv = pyia.findDescendant(window_acc, pred)
        elif agent_id == self.AGENT_IE:
            # IE
            pred = lambda x: x.accRole(0) == pyia.ROLE_SYSTEM_PANE and \
                x.accParent.accRole(0) == pyia.ROLE_SYSTEM_CLIENT and \
                x.accParent.accParent.accRole(0) == pyia.ROLE_SYSTEM_CLIENT
            rv = pyia.findDescendant(window_acc, pred)
        elif agent_id == self.AGENT_WEBKIT:
            # Webkit
            print 'Webkit!'
            rv = window_acc[3][0][3][0][3]
        print 'Root doc:', rv
        return rv

