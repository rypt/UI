# coding=utf-8
from appium import webdriver
from appium.webdriver.extensions.android.nativekey import AndroidKey
from Tool.save_excel.save_excel import save_excel
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
from Tool.database.db import domysql
import sys


class test:
    def __init__(self, filename='../Log/default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'w')

    # 登录
    def login(self, egnum, num, *args):
        self.appium_start()
        self.login_start(num)

    # 弹窗/验证码/跳过
    def login_start(self, num, *args):
        try:
            iknow = self.driver.find_element_by_id('permission_allow_button')
            iknow.click()
            iknow = self.driver.find_element_by_id('tv_login_guide_edit_child_info_login')
            iknow.click()
            iknow = self.driver.find_element_by_id('com.qinlin.ahaschool:id/ll_skip_container')
            iknow.click()
        except:
            pass
        try:
            iknow = self.driver.find_element_by_id('com.qinlin.ahaschool:id/et_phone_input')
            if iknow:
                iknow.click()
                num = int(num)
                iknow.send_keys(num)
                iknow = self.driver.find_element_by_id('tv_login_phone_input_verification_code')
                iknow.click()
                iknow = self.driver.find_element_by_id('et_verification_code_input')
                iknow.click()
                time.sleep(3)
                code = domysql().select_db('code', num)
                code = int(code)
                iknow.send_keys(code)
        except:
            pass
        try:
            iknow = self.driver.find_element_by_id('android:id/button1')
            if iknow:
                iknow.click()
        except:
            pass

    # appium初始化
    def appium_start(self, *args):
        self.desired_caps = {
            'platformName': 'Android',  # 被测手机是安卓
            'platformVersion': '8.0.0',  # 手机安卓版本
            # 'Device Name':'ip:port',
            'deviceName': '192.168.11.180:5556',  # 设备名，安卓手机可以随意填写
            'appPackage': 'com.qinlin.ahaschool',  # 启动APP Package名称
            'appActivity': '.view.activity.LaunchActivity',  # 启动Activity名称
            'unicodeKeyboard': True,  # 使用自带输入法，输入中文时填True
            'resetKeyboard': True,  # 执行完程序恢复原来输入法
            'noReset': True,  # 不要重置App
            # 'skipServerInstallation': True,
            # 'skipDeviceInitialization': True,
            'newCommandTimeout': 6000,  # 超时断开
            'automationName': 'UiAutomator2'
        }
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        self.driver.implicitly_wait(8)

    # 开始输入
    def start(self, num, eg, *args):
        self.nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.num = num
        self.eg = eg
        self.really = '成功'
        self.error_num = ''

    # 结束输出
    def end(self, *args):
        num = self.num
        really = self.really
        nowtime = self.nowtime
        error_num = self.error_num
        eg = self.eg
        list = [nowtime, num, eg, really, error_num]
        print(list)
        a = save_excel()
        a.save_excel_w(list)
        self.num = ''
        self.really = ''
        self.error_num = ''

    # 保存日志
    def write(self, message, *args):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self, *args):
        pass

    # 等待时间
    def imp_time(self):
        self.driver.implicitly_wait(8)

    def error_information(self,egnum):
        self.really = '异常'
        self.error_num = '{}-{}'.format(self.num, egnum)
        self.driver.get_screenshot_as_file(
            '../Screenshot/Error/{}-{}-{}.png'.format(self.num, egnum,self.nowtime))


    def toast(self, egnum, toast_message, *args):
        if self.really == '成功':
            try:
                message = '//*[@text=\'{}\']'.format(toast_message)
                toast_element = WebDriverWait(self.driver, 5).until(lambda x: x.find_element_by_xpath(message))
                # toast_loc = ("xpath", ".//*[contains(@text,'{}')]".format(toast_message))
                # toast_element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(toast_loc))
                print('toast--{}'.format(toast_message))
                if toast_element.text == toast_message:
                    self.really = '成功'
                else:
                    self.really = '失败'
            except:
                self.error_information(egnum)
        else:
            pass
        print("{}-{}:  {}".format(self.num,egnum,self.really))


    def data_checkout(self, egnum, select, userid, ex_temp, *args):
        if self.really == '成功':
            try:
                for i in range(100):
                    temp = domysql().select_db(select, userid)
                    if temp == ex_temp:
                        self.really = '成功'
                    else:
                        self.really = '失败'
            except:
                self.really = '失败'
        else:
            pass
        print("{}-{}:  {}".format(self.num,egnum,self.really))


    def data_checkout_date(self, egnum, select, userid, ex_temp, *args):
        if self.really == '成功':
           try:
               temp = domysql().select_db(select, userid)
               d1 = datetime.datetime.strptime(temp, '%Y-%m-%d %H:%M:%S')
               d2 = self.nowtime
               d2 = datetime.datetime.strptime(d2, '%Y-%m-%d %H:%M:%S')
               day = (d1 - d2).days
               ex_temp = int(ex_temp)
               if day > ex_temp:
                   self.really = '成功'
               else:
                   self.really = '失败'
           except:
               self.really = '失败'
        else:
            pass
        print("{}-{}:  {}".format(self.num,egnum,self.really))


    def date_delete_group(self,egnum,userid,*args):
        if self.really == '成功':
            try:
                temp = domysql()
                temp.delete_db_group(userid)
                self.really = '成功'
            except:
                self.really = '失败'
        else:
            pass
        print("{}-{}:  {}".format(self.num,egnum,self.really))



    def find_element_xpath(self, egnum, element1, element2,*args):
        if self.really == '成功':
            try:
                self.driver.find_element_by_xpath(element1)
                self.driver.find_element_by_xpath(element2)
                self.really = '成功'
            except:
                self.really = '失败'
        else:
            pass
        print("{}-{}:  {}".format(self.num,egnum,self.really))


    def find_elements_id(self, egnum, id, *args):
        if self.really == '成功':
            try:
                list = self.driver.find_elements_by_id(id)
                if len(list) > 0:
                    self.really = '成功'
            except:
                self.really = '失败'
        else:
            pass
        print("{}-{}:  {}".format(self.num,egnum,self.really))


    # xpath点击
    def fc_xpath_click(self, egnum, xp, *args):
        if self.really == '成功':
            try:
                temp = self.driver.find_element_by_xpath(xp)
                temp.click()
            except:
                self.really = '异常'
                self.error_num = '{}-{}'.format(self.num, egnum)
                # self.driver.get_screenshot_as_file('../Screenshot/Error/{}-{}.png'.format(self.num,egnum))
                self.driver.get_screenshot_as_file(
                    '../Screenshot/Error/{}-{}-{}.png'.format(self.num, egnum, self.nowtime))

        else:
            pass
        print("{}-{}:  {}".format(self.num,egnum,self.really))

    # id点击
    def fc_id_click(self, egnum, id, *args):
        if self.really == '成功':
            try:
                self.driver.find_element_by_id(id).click()
            except:
                self.really = '异常'
                self.error_num = '{}-{}'.format(self.num, egnum)
                # self.driver.get_screenshot_as_file('../Screenshot/Error/{}-{}.png'.format(self.num, egnum))
                self.driver.get_screenshot_as_file(
                    '../Screenshot/Error/{}-{}-{}.png'.format(self.num, egnum, self.nowtime))
        else:
            pass
        print("{}-{}:  {}".format(self.num,egnum,self.really))


    # xpath输入
    def fc_xpath_input(self, egnum, xp, value, *args):
        if self.really == '成功':
            try:
                input = self.driver.find_element_by_xpath(xp)
                input.click()
                input.clear()
                input.send_keys(value)
            except:
                self.really = '异常'
                self.error_num = '{}-{}'.format(self.num, egnum)
                # self.driver.get_screenshot_as_file('../Screenshot/Error/{}-{}.png'.format(self.num, egnum))
                self.driver.get_screenshot_as_file(
                    '../Screenshot/Error/{}-{}-{}.png'.format(self.num, egnum, self.nowtime))
        else:
            pass
        print("{}-{}:  {}".format(self.num,egnum,self.really))


    # id输入
    def fc_id_input(self, egnum, id, value, *args):
        if self.really == '成功':
            try:
                input = self.driver.find_element_by_id(id)
                input.click()
                input.clear()
                input.send_keys(value)
            except:
                self.really = '异常'
                self.error_num = '{}-{}'.format(self.num, egnum)
                # self.driver.get_screenshot_as_file('../Screenshot/Error/{}-{}.png'.format(self.num,egnum))
                self.driver.get_screenshot_as_file(
                    '../Screenshot/Error/{}-{}-{}.png'.format(self.num, egnum, self.nowtime))
        else:
            pass
        print("{}-{}:  {}".format(self.num,egnum,self.really))


    def fc_id_input_keyboard(self, egnum, id, value, *args):
        if self.really == '成功':
            try:
                input = self.driver.find_element_by_id(id)
                input.click()
                input.clear()
                input.send_keys(value)
                self.driver.keyevent(66)
                self.driver.press_keycode(66)
            except:
                self.really = '异常'
                self.error_num = '{}-{}'.format(self.num, egnum)
                # self.driver.get_screenshot_as_file('../Screenshot/Error/{}-{}.png'.format(self.num,egnum))
                self.driver.get_screenshot_as_file(
                    '../Screenshot/Error/{}-{}-{}.png'.format(self.num, egnum, self.nowtime))
        else:
            pass
        print("{}-{}:  {}".format(self.num,egnum,self.really))


sys.stdout = test('../Log/log/text.log', sys.stdout)
sys.stderr = test('../Log/a.log_file', sys.stderr)
