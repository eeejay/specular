from speclenium_client import SpecleniumClient as speclenium_client

class TestCommon(object):
    '''Do common setup and teardown tasks.'''
    expected_revision = None
    fail_on_revision = False
    broken = False

    def setUp(self):
        self.verificationErrors = []
        self.speclenium_client = speclenium_client(self.host, 4444, self.command, self.base_url)
        self.speclenium_client.start()
        self.speclenium_client.set_timeout(30000)
        self.speclenium_client.open(self.path)
        self._check_revision()
        self.speclenium_client.window_maximize()

    def _check_revision(self):
        if self.expected_revision is None: return
        rev_string = self.speclenium_client.get_text("//*[@id=\"revision\"]")
        try:
            rev_num = int(rev_string[11:-2])
        except:
            rev_num = -1
        if rev_num != self.expected_revision:
            if self.fail_on_revision:
                self.fail("Wrong revision in target web page."
                          " Got %s, expected %s" % \
                              (rev_num, self.expected_revision))
            else:
                print 'WARNING: (%s) Wrong revision in target web page' \
                    ' Got %s, expected %s.' % \
                    (self.__class__.__name__, rev_num, self.expected_revision)
        
    def tearDown(self):
        self.speclenium_client.stop()
        self.assertEqual([], self.verificationErrors)
        #self.failUnless([] == self.verificationErrors)
