from selenium import selenium
import unittest, time, re
from sys import platform


WINDOWS_HOST = "11.0.0.2"
LINUX_HOST = "localhost"

class RadioTest(object):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = \
            selenium(self.host, 4444, self.command, 
                     "http://test.cita.uiuc.edu/")
        #self.selenium.set_speed(1000)
        self.selenium.start()
        self.selenium.set_timeout(30000)

    def test_radio_button(self):
        sel = self.selenium
        sel.open("/aria/radio/view_inline.php?title=Radio%20Example%201&ginc=includes/radio1_inline.inc&gcss=css/radio1_inline.css&gjs=../js/globals.js,../js/widgets_inline.js,js/radio1_inline.js")
        sel.click("r3")
        success = False
        for i in xrange(10):
            e = sel.get_accessible_event_match(
                '<event type="object-state-changed">'
                '<source><accessible role="radio button"/>'
                '</source></event>', 0)
            if 'notfound' not in e:
                success = True
                break
            print 'retrying', i
        self.failUnless(
            success, 
            'Did not recieve a state-changed event after radio button toggle')
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

class LinuxFirefox3RadioTest(RadioTest, unittest.TestCase):
    host = LINUX_HOST
    command = "*chrome /usr/lib/firefox-3.0.1/firefox"

class WindowsFirefox3RadioTest(RadioTest, unittest.TestCase):
    host = WINDOWS_HOST
    command = "*chrome"

class WindowsSafariRadioTest(RadioTest, unittest.TestCase):
    host = WINDOWS_HOST
    command = "*safari C:\Documents and Settings\Eitan\Desktop\webkit-nightly\Safari.exe"

if __name__ == "__main__":
    unittest.main()
