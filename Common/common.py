# coding=utf-8
from appium import webdriver
import yaml
# from appium.webdriver.extensions.android.nativekey import AndroidKey
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

    """
    appium初始化
    start
    end
    """

    # appium初始化
    def appium_start(self, devices_name, *args):
        try:
            with open('../Main/config.yaml', 'r')as file:
                data = yaml.load(file, Loader=yaml.FullLoader)
                if devices_name == 'huawei_nova3i':
                    i = 0
                elif devices_name == 'huawei_Honor7A':
                    i = 1
                else:
                    pass
                self.desired_caps = {
                    'udid': data[i]['udid'],
                    'platformName': data[i]['platformName'],  # 被测手机是安卓
                    'platformVersion': data[i]['platformVersion'],  # 手机安卓版本
                    'deviceName': data[i]['deviceName'],  # 设备名，安卓手机可以随意填写
                    'appPackage': data[i]['appPackage'],  # 启动APP Package名称
                    'appActivity': data[i]['appActivity'],  # 启动Activity名称
                    'unicodeKeyboard': data[i]['unicodeKeyboard'],  # 使用自带输入法，输入中文时填True
                    'resetKeyboard': data[i]['resetKeyboard'],  # 执行完程序恢复原来输入法
                    'noReset': data[i]['noReset'],  # 不要重置App
                    'newCommandTimeout': 6000,  # 超时断开
                    'automationName': 'UiAutomator2'
                }
                self.driver = webdriver.Remote('http://' + str(data[i]['ip']) + ':' + str(data[i]['port']) + '/wd/hub',
                                               self.desired_caps)
                self.driver.implicitly_wait(data[i]['wait_time'])
        except:
            self.error_information(egnum=2)
        self.fu_information(egnum=2)

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

    """
    登录选择
    login
    login_start1
    login_start2
    login_start3
    login_choose
    """

    # 登录
    def login(self, egnum, num, model, *args):
        num = self.int_num(num)
        model = str(self.int_num(model))
        if self.really == '成功':
            if model == "1":
                try:
                    self.login_start1(num, egnum)
                except:
                    self.error_information(egnum)
            elif model == "2":
                try:
                    self.login_start2(num, egnum)
                except:
                    self.error_information(egnum)
            else:
                try:
                    self.login_start3()
                except:
                    self.error_information(egnum)
            self.userid = domysql().select_db('user_id', num)
            self.print_text('账户UserID', self.userid)
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
            # num = int(num)
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
            self.error_information(egnum)
        print(self.model)

    # model-2正常登录
    def login_start2(self, num, egnum, *args):
        try:
            # num = int(num)
            # print(num)
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
        print(self.model)

    # model-3免登录
    def login_start3(self):
        self.model = '登录模式3-免登录'
        print(self.model)

    # 国外手机号
    def login_choose(self, egnum, num, choose_click, choose, quhao, *args):
        try:
            num = self.int_num(num)
            quhao = self.int_num(quhao)
            self.driver.find_element_by_id('tv_phone_input_country_code').click()
            input = self.driver.find_element_by_id('et_select_country_code_search_header_text')
            input.click()
            input.clear()
            input.send_keys(choose)
            self.driver.keyevent(66)
            self.driver.find_element_by_xpath(choose_click).click()
            input_num = self.driver.find_element_by_id('et_phone_input')
            input_num.click()
            input_num.send_keys(num)
            num = "{}{}".format(quhao, str(num))
            num = int(num)
            print(type(num))
            print(num)
            # 获取验证
            self.driver.find_element_by_id('tv_login_phone_input_verification_code').click()
            # 点击验证码输入框
            input_code = self.driver.find_element_by_id('et_verification_code_input')
            input_code.click()
            print(1)
            time.sleep(3)
            print(2)
            code = domysql().select_db('code', num)
            time.sleep(3)
            print(3)
            code = int(code)
            print(code)
            input_code.send_keys(code)
            self.model = '登录模式2-常规登录'
        except:
            self.error_information(egnum)
        self.fu_information(egnum)

    """
    appium 方法
    fc_xpath_click
    fc_id_click
    fc_xpath_input
    fc_id_input
    fc_classname_click
    """

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

    # class name点击
    def fc_classname_click(self, egnum, classname, *args):
        if self.really == '成功':
            try:
                temp = self.driver.find_element_by_class_name(classname)
                temp.click()
            except:
                self.error_information(egnum)
        else:
            pass
        self.fu_information(egnum)
        return self.really

    # 弹窗点击
    def toast_click(self, egnum, xp, *args):
        try:
            self.driver.find_element_by_xpath(xp).click()
        except:
            self.error_information(egnum)
        self.fu_information(egnum)

    """
    键盘操作
    fc_id_input_keyboard
    back
    swipeUp
    swipeDown
    swipeLeft
    swipeRight
    """

    # id输入（键盘）
    def fc_id_input_keyboard(self, egnum, id, value, *args):
        if self.really == '成功':
            try:
                input = self.driver.find_element_by_id(id)
                input.click()
                input.clear()
                input.send_keys(value)
                self.driver.keyevent(66)
                # self.driver.press_keycode(66)
            except:
                self.error_information(egnum)
        else:
            pass
        self.fu_information(egnum)
        return self.really

        # 键盘回退键

    # 后退
    def back(self, *args):
        # time.sleep(3)
        self.driver.keyevent(4)
        # self.driver.press_keycode(4)

    # 上划
    def swipeUp(self, egnum, n, *args):
        n = self.int_num(n)
        size = self.driver.get_window_size()
        width = size['width']
        height = size['height']
        x1 = width * 0.5
        y1 = height * 0.9
        y2 = height * 0.25
        print("滑动前")
        for i in range(n):
            print("第%d次滑屏" % i)
            time.sleep(3)
            self.driver.swipe(x1, y1, x1, y2)

    # 下划
    def swipeDown(self, egnum, n, *args):
        n = self.int_num(n)
        size = self.driver.get_window_size()
        width = size['width']
        height = size['height']
        x1 = width * 0.5
        y1 = height * 0.25
        y2 = height * 0.9
        print("滑动前")
        for i in range(n):
            print("第%d次滑屏" % i)
            time.sleep(3)
            self.driver.swipe(x1, y1, x1, y2)

    # 左划
    def swipeLeft(self, egnum, n, *args):
        n = self.int_num(n)
        size = self.driver.get_window_size()
        width = size['width']
        height = size['height']
        x1 = width * 0.8
        x2 = width * 0.2
        y1 = height * 0.5
        print("滑动前")
        for i in range(n):
            print("第%d次滑屏" % i)
            time.sleep(3)
            self.driver.swipe(x1, y1, x2, y1)

    # 右划
    def swipeRight(self, egnum, n, *args):
        n = self.int_num(n)
        size = self.driver.get_window_size()
        width = size['width']
        height = size['height']
        x1 = width * 0.2
        x2 = width * 0.8
        y1 = height * 0.5
        print("滑动前")
        for i in range(n):
            print("第%d次滑屏" % i)
            time.sleep(3)
            self.driver.swipe(x1, y1, x2, y1)

    """
    校验
    """

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
                    self.really = '异常'
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
                self.print_text('过期时间', d1)
                self.print_text('当前时间', d2)
                self.print_text('有效时间', day)
                ex_temp = int(ex_temp)
                if day > ex_temp:
                    self.really = '成功'
                else:
                    self.really = '异常'
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

    # 页面全部元素校验
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

    """
    特殊用例单独方法
    """

    # 微信登录
    def fc_weixing(self, egnum, *args):
        if self.really == '成功':
            try:
                # input = self.driver.find_element_by_id(id)
                # input.click()
                # input.clear()
                # input.send_keys(value)
                self.driver.keyevent(8)
                self.driver.keyevent(12)
                self.driver.keyevent(15)
                self.driver.keyevent(15)
                self.driver.keyevent(8)
                self.driver.keyevent(8)

                # self.driver.press_keycode(66)
            except:
                self.error_information(egnum)
        else:
            pass
        self.fu_information(egnum)
        return self.really

    # 支付宝登录
    def fc_zhifubao(self, egnum, *args):
        if self.really == '成功':
            try:
                # input = self.driver.find_element_by_id(id)
                # input.click()
                # input.clear()
                # input.send_keys(value)
                self.driver.keyevent(7)
                self.driver.keyevent(15)
                self.driver.keyevent(8)
                self.driver.keyevent(14)
                self.driver.keyevent(9)
                self.driver.keyevent(13)

                # self.driver.press_keycode(66)
            except:
                self.error_information(egnum)
        else:
            pass
        self.fu_information(egnum)
        return self.really

    """
    方法流程
    """

    # 清除数据
    def clean_all(self):
        self.num = ''
        self.error_num = ''
        self.nowtime = ''
        self.eg = ''
        self.really = ''
        domysql().delete_clean_all(self.userid)

    # 浮点数转整型
    def int_num(self, num):
        a = type(num)
        b = str(a)
        if b == "<class 'float'>":
            num = int(num)
        else:
            pass
        return num

    # log文本打印
    def print_text(self, text, value):
        print("{}:{}".format(text, value))

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

    # time3
    def time_wite(self, *args):
        time.sleep(3)


# 日志输出
sys.stdout = test('../Log/log/text.log', sys.stdout)
sys.stderr = test('../Log/a.log_file', sys.stderr)

