# coding=utf-8
import unittest
import os
from random import randint
from appium import webdriver
from time import sleep

class SimpleIOSTests(unittest.TestCase):
    def setUp(self):
        # set up appium
        # app = os.path.abspath('/Users/sunny/Desktop/TestApp.app')
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',
            desired_capabilities={
                'app':'com.qinlin.ahaschool',
                'platformName': 'iOS',
                'platformVersion': '13.3.1',
                'deviceName': 'iPhone XR',
                'automationName': 'XCUITest',
                'udid': '00008020-000961C634D1002E'
            })

    def testsend(self):
        self.driver.find_element_by_accessibility_id("IntegerA").send_keys("186****1761"),
        self.driver.find_element_by_accessibility_id("IntegerB").send_keys("wsg123")
        sleep(3)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(SimpleIOSTests("testsend"))
    unittest.TextTestRunner(verbosity=2).run(suite)

