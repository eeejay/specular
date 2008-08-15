from twisted.web import xmlrpc, server
from subtree import XmlStringTree, XmlAccessibleTree
from events import events_map

class SpecServeBase(xmlrpc.XMLRPC):
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
        # Capture target frame here.
        raise NotImplementedError

    def xmlrpc_flush_event_cache(self):
        self._event_list = []
        return True

    def xmlrpc_start_event_cache(self):
        raise NotImplementedError

    def xmlrpc_stop_event_cache(self):
        raise NotImplementedError

    def _event_cache_cb(self, event):
        try:
            source = XmlAccessibleTree(event.source).toxml()
        except:
            source = ''
        if type(event.type) == int:
            et = event.type
        else:
            et = str(event.type)
        self._event_list.append((et, source))
        
    def xmlrpc_check_for_event(self, etype, esource, start_at=0):
        esource_tree = XmlStringTree(esource)
        i = start_at
        if start_at != 0:
            event_list = self._event_list[start_at:]
        else:
            event_list = self._event_list
        for et, source in event_list:
            if type(et) == str:
                compare = et.startswith(events_map[etype])
            else:
                compare = et == events_map[etype]
            print et, etype, compare
            if compare:
                if XmlStringTree(source).compareNode(esource_tree):
                    return i
            i += 1
        return -1
                                
    def xmlrpc_get_doc_tree(self):
        if self._top_frame is None: return ''
        try:
            tree = self._find_root_doc(self._top_frame)
        except LookupError:
            return ''
        return XmlAccessibleTree(tree).toxml()

    def _find_root_doc(self, window_acc):
        raise NotImplementedError

    def _get_agent(self):
        raise NotImplementedError

