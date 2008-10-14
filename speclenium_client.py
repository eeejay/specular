from selenium import selenium
from xmlrpclib import ServerProxy
import time
from xml.dom.minidom import parseString

class SpecleniumClient(selenium):
    SPECLENIUM_PORT = 4117
    def start(self):
        self._speclenium_server =  \
            ServerProxy('http://%s:%d' % (self.host, self.SPECLENIUM_PORT))
        self._speclenium_server.start(self.browserStartCommand)
        selenium.start(self)

    def do_command(self, verb, args):
        self._speclenium_server.flush_event_cache()
        return selenium.do_command(self, verb, args)

    def get_accessible_doc(self):
        return self._speclenium_server.get_accessible_doc()
    
    def get_accessible_match(self, match_criteria):
        return self._speclenium_server.get_accessible_match(match_criteria)

    def get_accessible_event_match(self, match_criteria, index):
        return self._speclenium_server.get_accessible_event_match(
            match_criteria, index)

    def wait_accessible_events(self, events, timeout=3000):
        returned_events = []
        index = 0
        cumulative_time = 0
        for event in events:
            while cumulative_time < timeout:
                e = parseString(self.get_accessible_event_match(event, index))
                if e.documentElement.tagName == 'event':
                    index = \
                        int(e.documentElement.getAttribute('index') or 0) + 1
                    returned_events.append(e.toxml())
                    break
                cumulative_time += 500
                time.sleep(0.5)

        return returned_events
