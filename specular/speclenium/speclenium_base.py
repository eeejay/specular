from twisted.web import xmlrpc, server
from xml.dom.minidom import parseString
from specular.specular_accessible import \
    specular_accessible_from_accessible, specular_accessible_from_string
from specular.specular_event import \
    specular_event_from_event, specular_event_from_string

class SpecleniumBase(xmlrpc.XMLRPC):
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
        # Capture target frame here.
        self.xmlrpc_start_event_cache()
        print browser_start_cmd

    def xmlrpc_flush_event_cache(self):
        self._event_list = []
        return True

    def xmlrpc_start_event_cache(self):
        raise NotImplementedError

    def xmlrpc_stop_event_cache(self):
        raise NotImplementedError

    def _event_cache_cb(self, event):
        e = specular_event_from_event(event)
        self._event_list.append(e)
        
    def xmlrpc_get_accessible_event_match(self, event, start_at):
        spec_event = specular_event_from_string(event)

        i = start_at
        if start_at != 0:
            event_list = self._event_list[start_at:]
        else:
            event_list = self._event_list

        for e in event_list:
            if e.match(spec_event):
                e.documentElement.setAttribute('index', str(i))
                return e.toxml()
            i += 1
        return '<notfound index="%s"/>' % i

    def xmlrpc_doc_accessible_diff(self, other_doc):
        return "Not implemented yet"
                                
    def xmlrpc_get_accessible_doc(self):
        try:
            tree = self._find_root_doc(self._top_frame)
        except:
            return ''
        return specular_accessible_from_accessible(tree).toxml()
    
    def xmlrpc_get_accessible_match(self, acc_node):
        try:
            tree = self._find_root_doc(self._top_frame)
        except:
            return ''
        doc_tree = specular_accessible_from_accessible(tree)

        found = doc_tree.find_subtree(
            specular_accessible_from_string(acc_node))
        if found:
            return found.toxml()
        else:
            return ''

    def _find_root_doc(self, window_acc):
        raise NotImplementedError

    def _get_agent(self):
        raise NotImplementedError

