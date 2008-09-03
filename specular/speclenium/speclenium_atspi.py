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

from twisted.internet import glib2reactor
glib2reactor.install()
from twisted.internet import reactor
from twisted.web import xmlrpc, server
import pyatspi
import gobject
from speclenium_base import SpecleniumBase
from specular.specular_event import events_map

class Speclenium(SpecleniumBase):
    AGENTS = ['Mozilla', 'Internet Explorer', 'Webkit', 'Unknown']
    AGENT_MOZILLA = 0
    AGENT_IE = 1
    AGENT_WEBKIT = 2
    AGENT_UNKNOWN = -1
    """An example object to be published."""
    def __init__(self):
        xmlrpc.XMLRPC.__init__(self)
        self._event_list = []
        self._registered_global_listener = False

    def xmlrpc_start(self, browser_start_cmd):
        SpecleniumBase.xmlrpc_start(self, browser_start_cmd)
        self._top_frame = None
        pyatspi.Registry.registerEventListener(
            self._get_win, 'window:activate')
        return True

    def _get_win(self, event):
        if not len(event.host_application) == 2:
            return
        frames = [f for f in event.host_application]
        if 'Selenium Remote Control' not in ' '.join([f.name for f in frames]):
            return
        for frame in frames:
            if 'Selenium Remote Control' not in frame.name:
                self._top_frame = frame
                print 'TOP FRAME:', frame
                pyatspi.Registry.deregisterEventListener(
                    self._get_win, 'window:activate')

    def xmlrpc_start_event_cache(self):
        if not self._registered_global_listener:
            for value in events_map.values():
                pyatspi.Registry.registerEventListener(self._event_cache_cb, value)
        self._registered_global_listener = True
        return True

    def xmlrpc_stop_event_cache(self):
        if self._registered_global_listener:
            for value in events_map.values():
                pyatspi.Registry.deregisterEventListener(self._event_cache_cb, value)
        self._registered_global_listener = False
        return True

    def _find_root_doc(self, window_acc):
        agent_id = self._get_agent()
        pred = lambda x: False
        if agent_id == self.AGENT_MOZILLA:
            # Firefox
            pred = lambda x: x.getRole() == pyatspi.ROLE_DOCUMENT_FRAME and \
                x.getState().contains(pyatspi.STATE_SHOWING)
        return pyatspi.findDescendant(window_acc, pred)

    def _get_agent(self):
        return self.AGENT_MOZILLA

