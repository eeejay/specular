from twisted.internet import gtk2reactor
gtk2reactor.install()
from twisted.internet import reactor
from twisted.web import xmlrpc, server
from subtree import XmlStringTree, XmlAccessibleTree
from events import events_map
import pyatspi
import gobject

class SpecServe(xmlrpc.XMLRPC):
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

    def xmlrpc_start(self):
        print 'start!'
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
                pyatspi.Registry.deregisterEventListener(
                    self._get_win, 'window:activate')

    def _event_cb(self, event):
        self._event_list.append(str(event.type))
        print event

    def xmlrpc_dump_events(self):
        elist = self._event_list[:]
        self._event_list = []
        print elist
        return elist

    def xmlrpc_flush_event_cache(self):
        self._event_list = []
        return True

    def xmlrpc_start_event_cache(self):
        if not self._registered_global_listener:
            for key in pyatspi.EVENT_TREE.keys():
                pyatspi.Registry.registerEventListener(self._event_cache_cb, key)
        self._registered_global_listener = True
        return True

    def xmlrpc_stop_event_cache(self):
        if self._registered_global_listener:
            for key in pyatspi.EVENT_TREE.keys():
                pyatspi.Registry.deregisterEventListener(self._event_cache_cb, key)
        self._registered_global_listener = False
        return True

    def _event_cache_cb(self, event):
        try:
            source = XmlAccessibleTree(event.source).toxml()
        except:
            source = ''
        self._event_list.append((str(event.type), source))
        
    def xmlrpc_check_for_event(self, etype, esource, start_at=0):
        print 'check', etype, esource
        esource_tree = XmlStringTree(esource)
        i = start_at
        if start_at != 0:
            event_list = self._event_list[start_at:]
        else:
            event_list = self._event_list
        for et, source in event_list:
            print events_map[etype], et
            if et.startswith(events_map[etype]):
#                print source
                if XmlStringTree(source).compareNode(esource_tree):
                    return i
            i += 1
        return -1
                                
    def xmlrpc_get_doc_tree(self):
        try:
            tree = self._find_root_doc(self._top_frame)
        except LookupError:
            return ''
        return XmlAccessibleTree(tree).toxml()

    def xmlrpc_start_wait(self, etype, timeout):
        self._last_waited = None
        self._last_waited_source = None
        gobject.timeout_add(timeout, self._wait_timeout, etype)
        pyatspi.Registry.registerEventListener(
            self._wait_event_cb, events_map[etype])
        return True

    def _wait_timeout(self, etype):
        pyatspi.Registry.deregisterEventListener(
            self._wait_event_cb, events_map[etype])
        self._last_waited = -1

    def _wait_event_cb(self, event):
        self._last_waited = event
        self._last_waited_source = XmlAccessibleTree(event.source)
                
    def xmlrpc_poll_wait(self):
        if self._last_waited == -1:
            return -1
        if self._last_waited is not None:
            return 1
        return 0

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

    def xmlrpc_echo(self, x):
        """Return all passed args."""
        return x

    def xmlrpc_add(self, a, b):
        """Return sum of arguments."""
        return a + b
def top():
    print 'heelo'
    return True

if __name__ == '__main__':
#    import gobject
#    gobject.timeout_add(1000, top)
    r = SpecServe()
    reactor.listenTCP(7080, server.Site(r))
    reactor.run()
