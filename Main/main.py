# from Common.common import *
from Common.common4 import *
from Tool.parser.parser_excel import *


class Scheduler:

    def __init__(self):
        self.kdt = test()

    def start_run(self):
        self.parser = ReadExcel().read_excel(self.path)
        for line in self.parser:
            keyword = line[2]
            print("------------------------------------")
            print(keyword)
            a = line[1]
            b = line[3:]
            a = int(a)
            tmp = [a, ]
            for i in b:
                tmp.append(i)
            params = tmp
            print(params)
            if hasattr(self.kdt, keyword):
                if keyword == 'appium_start':
                    params = self.device_name
                    getattr(self.kdt, keyword)(params)
                else:
                    self.really = getattr(self.kdt, keyword)(*params)
                n = 2
                if self.really == '异常' or self.really == '错误':
                    for i in range(self.try_num):
                        if self.really == '异常' or self.really == '错误':
                            print("第{}次重试".format(n))
                            n += 1
                            self.really = getattr(self.kdt, keyword)(*params)
                            print(self.really)
                        else:
                            pass
                else:
                    pass
            else:
                print('fu_error')

    def choose(self, devices_name):
        with open('config.yaml', 'r')as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            if devices_name == 'huawei_nova3i':
                i = 0
            elif devices_name == 'huawei_Honor7A':
                i = 1
            else:
                pass
            self.device_name = data[i]['name']
            self.try_num = data[i]['try_num']
            self.path = data[i]['casepath']


if __name__ == '__main__':
    a = Scheduler()
    a.choose('huawei_nova3i')
    a.start_run()
