from xmlrpclib import ServerProxy
from selenium import selenium
from speculum.subtree import XmlStringTree, XmlAccessibleTree
from time import sleep

POLL_INTERVAL = 500

class speclenium(selenium):
    def __init__(self, host, port, browserStartCommand, browserURL, speculum_host='localhost', speculum_port=7080):
        selenium.__init__(self, host, port, browserStartCommand, browserURL)
        self._speculum = ServerProxy('http://%s:%s' % \
                                         (speculum_host, speculum_port))
    
    def start(self):
        self._speculum.start()
        sleep(0.5)
        selenium.start(self)
        self._speculum.start_event_cache()

    def stop(self):
        selenium.stop(self)
        self._speculum.stop_event_cache()
        self._speculum.flush_event_cache()

    def do_command(self, verb, args):
        self._speculum.flush_event_cache()
        return selenium.do_command(self, verb, args)

    def get_doc_tree(self):
        return self._speculum.get_doc_tree()

    def wait_for_acc_event(self, etype, esource='<accessible/>', timeout=3000):
        place_in_cache = -1
        for i in xrange(int(timeout/POLL_INTERVAL)):
            print 'checking', i, etype, esource
            place_in_cache = self._speculum.check_for_event(etype, esource)
            if place_in_cache != -1:
                break
            sleep(POLL_INTERVAL/1000.0)
        if place_in_cache == -1:
            raise AssertionError("Timeout")

    def is_subtree_present(self, tree, search_tree=None):
        if search_tree:
            other_tree = XmlStringTree(search_tree)
        else:
            other_tree = XmlStringTree(self._speculum.get_doc_tree())
        return other_tree.find_subtree(XmlStringTree(tree))
    
