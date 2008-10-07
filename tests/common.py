from selenium import selenium

class TestCommon:
    '''Do common setup and teardown tasks.'''
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium(self.host, 4444, self.command, self.base_url)
        self.selenium.start()
        self.selenium.set_timeout(30000)
        self.selenium.open(self.path)
        self.selenium.window_maximize()
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)
        #self.failUnless([] == self.verificationErrors)
