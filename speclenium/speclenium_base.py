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

from twisted.web import xmlrpc, server
from xml.dom.minidom import parseString
from specular.specular_accessible import \
    specular_accessible_from_accessible, specular_accessible_from_string
from specular.specular_event import \
    specular_event_from_event, specular_event_from_string, events_map

class SpecleniumBase(xmlrpc.XMLRPC):
    AGENTS = ['Mozilla', 'Internet Explorer', 'Webkit', 'Opera', 'Chrome', 'Unknown']
    AGENT_MOZILLA = 0
    AGENT_IE = 1
    AGENT_SAFARI = 2
    AGENT_OPERA = 3
    AGENT_CHROME = 4
    AGENT_UNKNOWN = -1
    """An example object to be published."""
    def __init__(self):
        xmlrpc.XMLRPC.__init__(self)
        self._event_list = []
        self._registered_global_listener = False
        self._store_events = False

    def shutdown(self):
        pass

    def xmlrpc_start(self, browser_start_cmd, store_events):
        # Capture target frame here.
        self._store_events = store_events
        self._stored_event_list = []
        self.xmlrpc_start_event_cache()
        self._browser_start_cmd = browser_start_cmd

    def xmlrpc_flush_event_cache(self):
        if self._store_events:
            self._stored_event_list += self._event_list
        self._event_list = []
        return True

    def xmlrpc_start_event_cache(self):
        raise NotImplementedError

    def xmlrpc_stop_event_cache(self):
        raise NotImplementedError

    def xmlrpc_get_stored_events(self):
        events = self._stored_event_list + self._event_list
        return map(str, events)

    def _event_cache_cb(self, event):
        if self._is_in_frame(event):
            e = specular_event_from_event(event)
            self._event_list.append(e)
        
    def xmlrpc_get_accessible_event_match(self, event, start_at):
        spec_event = specular_event_from_string(event.encode('utf-8'))
        if events_map[spec_event.type] == 'not supported on platform':
            spec_event.documentElement.setAttribute(
                'supportedOnPlatform', u'false')
            return spec_event.toxml()

        i = start_at
        if start_at != 0:
            event_list = self._event_list[start_at:]
        else:
            event_list = self._event_list

        for e in event_list:
            if e.match(spec_event):
                e.documentElement.setAttribute('index', unicode(i))
                return e.toxml()
            i += 1
        return '<notfound index="%s"/>' % i

    def xmlrpc_dump_accessible_event_cache(self):
        return [n.toxml() for n in self._event_list]

    def xmlrpc_get_accessible_doc(self):
        if not self._top_frame:
            print 'ERROR: Did not get top accessible frame'
            return ''
        
        tree = self._find_root_doc(self._top_frame)
        if tree:
            xml_tree = specular_accessible_from_accessible(tree).documentElement.toxml()
        else:
            print 'no xml_tree'
            xml_tree = ''
        return xml_tree

    def xmlrpc_get_accessible_match(self, acc_node):
        if not self._top_frame:
            print 'ERROR: Did not get top accessible frame'
            return ''

        tree = self._find_root_doc(self._top_frame)
        doc_tree = specular_accessible_from_accessible(tree)
        
        found = doc_tree.find_subtree(
            specular_accessible_from_string(acc_node))
        if found:
            return found.toxml()
        else:
            return ''

    def _is_in_frame(self, event):
        raise NotImplementedError        

    def _find_root_doc(self, window_acc):
        raise NotImplementedError

    def _get_agent(self):
        if 'firefox' in self._browser_start_cmd:
            return self.AGENT_MOZILLA
        if 'explore' in self._browser_start_cmd:
            return self.AGENT_IE
        if 'safari' in self._browser_start_cmd:
            return self.AGENT_SAFARI
        if 'opera' in self._browser_start_cmd:
            return self.AGENT_OPERA
        if 'chrome' in self._browser_start_cmd:
			return self.AGENT_CHROME
        return self.AGENT_UNKNOWN
