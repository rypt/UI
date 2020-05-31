import time
import xlrd

class replace_html:

    def __init__(self):
        html_path ='../html_report/MB.html'
        html_read = open(html_path, mode='r', encoding='utf-8')
        self.content = html_read.read()

    def data_excel(self,path_excel):
        workbook=xlrd.open_workbook(path_excel)
        worksheet=workbook.sheet_by_index(0)
        nrows=worksheet.nrows
        ncols=worksheet.ncols
        self.data = []
        for i in range(nrows):
            a=(worksheet.row_values(i))
            self.data.append(a)
        # print(self.data)

    def test_date_replace(self,version):
        timelocal = time.strftime('%Y-%m-%d %H:%M:%S')
        self.content=self.content.replace('$test-date',timelocal)
        self.content = self.content.replace('$test-version',version)
        count_pass = 0
        count_fail = 0
        count_error = 0
        j = 0
        k = 0
        h = 0
        for a in self.data:
            if self.data[j][5] == '成功':
                count_pass += 1
            if j < len(self.data):
                j += 1
        # print(count_pass)
        self.content = self.content.replace('$pass-count', str(count_pass))
        for a in self.data:
            if self.data[k][5] == '失败':
                count_fail += 1
            if k < len(self.data):
                k += 1
        # print(count_fail)
        self.content = self.content.replace('$fail-count', str(count_fail))
        for a in self.data:
            if self.data[h][5] == '错误':
                count_error += 1
            if h < len(self.data):
                h += 1
        # print(count_error)
        self.content = self.content.replace('$error',str(count_error))
        test_result=""
        for record in self.data:
            test_result+="<tr height='40'>"
            test_result+="<td width='7%'>"+str(record[0])+"</td>"
            test_result+="<td width='9%'>"+record[1]+"</a></td>"
            test_result+="<td width='9%'>"+record[2]+"</td>"
            test_result += "<td width='7%'>" + record[3] + "</td>"
            test_result += "<td width='20%'>" + record[4] + "</td>"
            if record[5]=='成功':
                test_result+="<td width='7%' bgcolor='lightgreen'>"+record[5]+"</td>"
            elif record[5]=='失败':
                test_result += "<td width='7%' bgcolor='red'>" + record[5] + "</td>"
            elif record[5]=='错误':
                test_result += "<td width='7%' bgcolor='yellow'>" + record[5] + "</td>"
            test_result+="<td width='16%'>"+str(record[6])+"</td>"
            test_result+="<td width='15%'>"+record[7]+"</td>"
            if record[8]=="无":
                test_result+="<td width='10%'>"+record[8]+"</td>"
            else:
                test_result+="<td width='10%'><a href='"+record[8]+"'>查看图片</a></td>"
                test_result+="</tr>\r\n"
        self.content=self.content.replace("$test-result",str(test_result))

    def export_html(self):
        report_path = '../excel_information_report/report.html'
        report = open(report_path, mode='w', encoding='utf8')
        report.write(self.content)
        print('--------------------HTML报告已生成------------------------')

# if __name__ == '__main__':
#     a=abc_html()
#     a.data_excel('../excel_information_report/report.xls')
#     a.test_date_replace('test')
#     a.export_html()