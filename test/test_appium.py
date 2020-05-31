#coding=utf-8
from appium import webdriver
from appium.webdriver.extensions.android.nativekey import AndroidKey
from selenium.webdriver.support.ui import WebDriverWait


print('2')
desired_caps = {
            'platformName': 'Android',  # 被测手机是安卓
            'platformVersion': '8.0.0',  # 手机安卓版本
            'deviceName': '192.168.11.180:5556',  # 设备名，安卓手机可以随意填写
            'appPackage': 'com.qinlin.ahaschool',  # 启动APP Package名称
            'appActivity': '.view.activity.LaunchActivity',  # 启动Activity名称
            'unicodeKeyboard': True,  # 使用自带输入法，输入中文时填True
            'resetKeyboard': True,  # 执行完程序恢复原来输入法
            'noReset': True,  # 不要重置App
            'newCommandTimeout': 3000,  # 超时断开
            'automationName': 'UiAutomator2'
        }
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(8)
driver.find_element_by_id('ll_home_campuses_search_filter_search').click()
a=driver.find_element_by_id('et_course_search')
a.click()
a.send_keys('我是你')
# driver.press_keycode(84)
driver.press_keycode(AndroidKey.ENTER)
a=driver.find_elements_by_id('iv_course_list_pic')
print(type(a))
print(a)
# driver.find_element_by_xpath('//*[@text="请填写年龄"]').click()
# a=driver.find_element_by_id('et_edit_child_profile_name')
# print('22')
# driver.find_element_by_xpath('//*[@text="我"]').click()
# driver.find_element_by_id('iv_child_avatar').click()
# a=driver.find_element_by_id('et_edit_child_profile_name')
# a.click()
# a.clear()
# a.send_keys('我是cc')
# driver.find_element_by_xpath('//*[@text="孩子生日"]').click()
# driver.find_element_by_xpath('//*[@text="30"]').click()
# driver.find_element_by_xpath('//*[@text="确定"]').click()
# driver.find_element_by_xpath('//*[@text="孩子性别"]').click()
# driver.find_element_by_xpath('//*[@text="女"]').click()
# driver.find_element_by_xpath('//*[@text="保存"]').click()
# toast_message = "保存成功"
# message ='//*[@text=\'{}\']'.format(toast_message)
# toast_element = WebDriverWait(driver,5).until(lambda x:x.find_element_by_xpath(message))
# print(toast_element.text)






