# from Common.common import *
from Common.common3 import *
from Tool.parser.parser_excel import *
class Scheduler:


    def __init__(self,path):
        self.parser=ReadExcel().read_excel(path)
        self.kdt=test()

    def start_run(self,num):
        for line in self.parser:
            keyword = line[2]
            print("------------------------------------")
            print(keyword)
            a= line[1]
            b= line[3:]
            tmp=[a,]
            for i in b:
                tmp.append(i)
            params=tmp
            print(params)
            # print("------------------------------------")
            if hasattr(self.kdt, keyword):
                self.really=getattr(self.kdt, keyword)(*params)
                n = 2
                if self.really == '异常' or self.really == '错误':
                    for i in range(num):
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




if __name__ == '__main__':
    #保存case表格，清空screenshot
    # a=Scheduler('../Excel/excel_case/case_excel.xls')
    a=Scheduler('../Excel/excel_case/case_excel_test.xls')
    a.start_run(5)
