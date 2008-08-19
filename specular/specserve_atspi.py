from twisted.internet import gtk2reactor
gtk2reactor.install()
from twisted.internet import reactor
from twisted.web import xmlrpc, server
from events import events_map
import pyatspi
import gobject
from specserve_base import SpecServeBase

class SpecServe(SpecServeBase):
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
        SpecServeBase.xmlrpc_start(self, browser_start_cmd)
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

