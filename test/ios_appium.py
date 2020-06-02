#coding=utf-8
from appium import webdriver
from appium.webdriver.extensions.android.nativekey import AndroidKey
from selenium.webdriver.support.ui import WebDriverWait



desired_caps = {
            'platformName': 'ios',  # 被测手机是安卓
            'deviceName': 'iPhone XR',  # 设备名，安卓手机可以随意填写
            'app': 'com.qinlin.ahaschool',  # 启动APP Package名称
            'platformVersion': '13.3.1',  # 手机安卓版本
            'automationName': 'XCUITest',
            'udid':'00008020-000961C634D1002E'
        }
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(8)






