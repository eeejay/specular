from selenium.selenium import selenium
from xmlrpclib import ServerProxy
import time
from xml.dom.minidom import parseString

class SpecleniumClient(selenium):
    SPECLENIUM_PORT = 4117
    def start(self, record_events=False):
        self._speclenium_client =  \
            ServerProxy('http://%s:%d' % (self.host, self.SPECLENIUM_PORT))
        self._speclenium_client.start(self.browserStartCommand, record_events)
        selenium.start(self)

    def do_command(self, verb, args):
        self._speclenium_client.flush_event_cache()
        return selenium.do_command(self, verb, args)

    def flush_accessible_event_cache(self):
        self._speclenium_client.flush_event_cache()

    def dump_accessible_event_cache(self):
        return self._speclenium_client.dump_accessible_event_cache()

    def get_accessible_doc(self):
        return self._speclenium_client.get_accessible_doc()

    def get_accessible_match(self, match_criteria):
        return self._speclenium_client.get_accessible_match(match_criteria)

    def get_stored_events(self):
        return self._speclenium_client.get_stored_events()

    def get_accessible_event_match(self, match_criteria, index):
        return self._speclenium_client.get_accessible_event_match(
            match_criteria, index)

    def wait_accessible_events(self, events, timeout=3000):
        returned_events = []
        index = 0
        cumulative_time = 0
        for event in events:
            while cumulative_time < timeout:
                m = self.get_accessible_event_match(event, index)
                e = parseString(m.encode('utf-8'))
                if e.documentElement.tagName == 'event':
                    index = \
                        int(e.documentElement.getAttribute('index') or 0) + 1
                    returned_events.append(e.toxml())
                    break
                cumulative_time += 500
                time.sleep(0.5)

        return returned_events
