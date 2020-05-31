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
        self.driver.implicitly_wait(15)

    # 登录
    def login(self, egnum, num, model, *args):
        if self.really == '成功':
            if model == "1":
                try:
                    self.appium_start()
                    self.login_start1(num, egnum)
                except:
                    self.error_information(egnum)
            elif model == "2":
                try:
                    self.appium_start()
                    self.login_start2(num, egnum)
                except:
                    self.error_information(egnum)
            else:
                try:
                    self.appium_start()
                    self.login_start3()
                except:
                    self.error_information(egnum)
            self.userid = domysql().select_db('user_id', num)
            print(self.userid)
        else:
            pass
        self.fu_information(egnum)

    # model-1清缓存登录
    def login_start1(self, num, egnum, *args):
        """
        三种情况
        1完全退出-清除数据：有引导界面，选择性别和老用户登录
        2正常登录：直接进入输入手机号界面
        3不需要登录：全部pass
        :param num:
        :param args:
        :return:
        """
        try:
            # 弹框，是否始终允许
            self.driver.find_element_by_xpath('//*[@text="始终允许"]').click()
            # 选择已有账户登录
            self.driver.find_element_by_xpath('//*[@text="已有账户登录"]').click()
            self.model = '登录模式1-清缓存'
        except:
            pass
        try:
            num = int(num)
            # 输入手机号
            input_num = self.driver.find_element_by_id('com.qinlin.ahaschool:id/et_phone_input')
            input_num.click()
            input_num.send_keys(num)
            # 获取验证码
            self.driver.find_element_by_id('tv_login_phone_input_verification_code').click()
            # 点击验证码输入框
            input_code = self.driver.find_element_by_id('et_verification_code_input')
            input_code.click()
            time.sleep(3)
            code = domysql().select_db('code', num)
            code = int(code)
            input_code.send_keys(code)
        except:
            pass
        try:
            # 登录之后，同意弹框
            self.driver.find_element_by_id('android:id/button1').click()
            print('同意弹框')
        except:
            self.error_information(egnum)
        print(self.model)

    # model-2正常登录
    def login_start2(self, num, egnum, *args):
        try:
            self.driver.find_element_by_xpath('//*[@text="开启新版本"]').click()
        except:
            pass
        try:
            num = int(num)
            # 输入手机号
            input_num = self.driver.find_element_by_id('com.qinlin.ahaschool:id/et_phone_input')
            input_num.click()
            input_num.send_keys(num)
            # 获取验证码
            self.driver.find_element_by_id('tv_login_phone_input_verification_code').click()
            # 点击验证码输入框
            input_code = self.driver.find_element_by_id('et_verification_code_input')
            input_code.click()
            time.sleep(3)
            code = domysql().select_db('code', num)
            code = int(code)
            input_code.send_keys(code)
            self.model = '登录模式2-常规登录'
        except:
            self.error_information(egnum)
        # 18134727
        print(self.model)

    # model-3免登录
    def login_start3(self):
        try:
            self.driver.find_element_by_xpath('//*[@text="开启新版本"]').click()
        except:
            pass
        self.model = '登录模式3-免登录'
        print(self.model)

    # 开始输入
    def start(self, num, eg, *args):
        # 用例编号
        self.num = num
        # 错误序号
        self.error_num = ''
        # 用例描述
        self.eg = eg
        # 初始实际结果
        self.really = '成功'
        # 生成时间
        self.nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 结束输出
    def end(self, *args):
        list = [self.num, self.nowtime, self.eg, self.really, self.error_num]
        print(list)
        a = save_excel()
        a.save_excel_w(list)
        self.clean_all()

    # 清除数据
    def clean_all(self):
        self.num = ''
        self.error_num = ''
        self.nowtime = ''
        self.eg = ''
        self.really = ''
        domysql().delete_clean_all(self.userid)

    # 保存日志
    def write(self, message, *args):
        self.terminal.write(message)
        self.log.write(message)

    # 日志
    def flush(self, *args):
        pass

    # 等待时间
    def imp_time2(self, num):
        self.nowtime2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("{}---{}".format(num, self.nowtime2))

    # 异常信息
    def error_information(self, egnum):
        self.really = '异常'
        self.error_num = '{}-{}'.format(self.num, egnum)
        self.driver.get_screenshot_as_file(
            '../Screenshot/Error/{}-{}-{}.png'.format(self.num, egnum, self.nowtime))

    # 方法实际执行结果
    def fu_information(self, egnum):
        print("{}-{}:  {}".format(self.num, egnum, self.really))
        return self.really

    # 弹框验证
    def toast(self, egnum, toast_message, *args):
        """
        :param egnum: 错误序号
        :param toast_message: 弹框期望信息
        :param args:
        :return:
        """
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
        self.fu_information(egnum)
        return self.really

    # 数据库取值校验
    def data_checkout(self, egnum, select, ex_temp, *args):
        """
        :param egnum: 错误序号
        :param select:数据字段
        :param ex_temp:期望值
        :param args:
        :return:
        """
        if self.really == '成功':
            try:
                temp = domysql().select_db(select, self.userid)
                if temp == ex_temp:
                    self.really = '成功'
                else:
                    self.really = '失败'
            except:
                self.error_information(egnum)
        else:
            pass
        self.fu_information(egnum)
        return self.really

    # 数据库时间校验
    def data_checkout_date(self, egnum, select, ex_temp, *args):
        """
        :param egnum: 错误序号
        :param select: 数据字段
        :param ex_temp: 期望值
        :param args:
        :return:
        """
        if self.really == '成功':
            try:
                temp = domysql().select_db(select, self.userid)
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
                self.error_information(egnum)
        else:
            pass
        self.fu_information(egnum)
        return self.really

    # 数据库清除课程
    def date_delete_group(self, egnum, *args):
        if self.really == '成功':
            try:
                temp = domysql()
                temp.delete_db_group(self.userid)
                self.really = '成功'
            except:
                self.error_information(egnum)
        else:
            pass
        self.fu_information(egnum)
        return self.really

    # 页面元素校验xpath（两个元素）
    def find_element_xpath(self, egnum, element1, element2, *args):
        if self.really == '成功':
            try:
                self.driver.find_element_by_xpath(element1)
                self.driver.find_element_by_xpath(element2)
                self.really = '成功'
            except:
                self.error_information(egnum)
        else:
            pass
        self.fu_information(egnum)
        return self.really

    # 页面元素校验id（所有元素）
    def find_elements_id(self, egnum, id, *args):
        if self.really == '成功':
            try:
                list = self.driver.find_elements_by_id(id)
                if len(list) > 0:
                    self.really = '成功'
            except:
                self.error_information(egnum)
        else:
            pass
        self.fu_information(egnum)
        return self.really

    # xpath点击
    def fc_xpath_click(self, egnum, xp, *args):
        if self.really == '成功':
            try:
                temp = self.driver.find_element_by_xpath(xp)
                temp.click()
            except:
                self.error_information(egnum)
        else:
            pass
        self.fu_information(egnum)
        return self.really

    # id点击
    def fc_id_click(self, egnum, id, *args):
        if self.really == '成功':
            try:
                self.driver.find_element_by_id(id).click()
            except:
                self.error_information(egnum)
        else:
            pass
        self.fu_information(egnum)
        return self.really

    # xpath输入
    def fc_xpath_input(self, egnum, xp, value, *args):
        if self.really == '成功':
            try:
                input = self.driver.find_element_by_xpath(xp)
                input.click()
                input.clear()
                input.send_keys(value)
            except:
                self.error_information(egnum)
        else:
            pass
        self.fu_information(egnum)
        return self.really

    # id输入
    def fc_id_input(self, egnum, id, value, *args):
        if self.really == '成功':
            try:
                input = self.driver.find_element_by_id(id)
                input.click()
                input.clear()
                input.send_keys(value)
            except:
                self.error_information(egnum)
        else:
            pass
        self.fu_information(egnum)
        return self.really

    # id输入（键盘）
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
                self.error_information(egnum)
        else:
            pass
        self.fu_information(egnum)
        return self.really


# 日志输出
sys.stdout = test('../Log/log/text.log', sys.stdout)
sys.stderr = test('../Log/a.log_file', sys.stderr)
