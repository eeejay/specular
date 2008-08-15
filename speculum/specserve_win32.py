from twisted.internet import win32eventreactor
win32eventreactor.install()
from twisted.internet import reactor
from twisted.web import xmlrpc, server
from subtree import XmlStringTree, XmlAccessibleTree
from events import events_map
import pyia
from specserve_base import SpecServeBase

class SpecServe(SpecServeBase):
    """An example object to be published."""
    def __init__(self):
        SpecServeBase.__init__(self)

    def xmlrpc_start(self):
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
        pred = lambda x: False
        if agent_id == self.AGENT_MOZILLA:
            # Firefox
            pred = lambda x: x.accRole(0) == pyia.ROLE_SYSTEM_DOCUMENT and \
                not x.accState(0) & pyia.STATE_SYSTEM_INVISIBLE
        elif agent_id == self.AGENT_IE:
            # IE
         pred = lambda x: x.accRole(0) == pyia.ROLE_SYSTEM_PANE and \
             x.accParent.accRole(0) == pyia.ROLE_SYSTEM_CLIENT and \
             x.accParent.accParent.accRole(0) == pyia.ROLE_SYSTEM_CLIENT
        elif agent_id == self.AGENT_WEBKIT:
            # Webkit
            pred = lambda x: False
        rv = pyia.findDescendant(window_acc, pred)
        print rv
        return rv

    def _get_agent(self):
        return self.AGENT_MOZILLA

