from xlrd import open_workbook
from xlutils.copy import copy
class save_excel:

    def save_excel_w(self,list):
        reexcel=open_workbook('../Excel/excel_information_report/report.xls')
        rows=reexcel.sheets()[0].nrows
        excel=copy(reexcel)
        table=excel.get_sheet(0)
        row=rows
        for i in range(0,len(list)):
            table.write(row,i,list[i])
        excel.save('../Excel/excel_information_report/report.xls')