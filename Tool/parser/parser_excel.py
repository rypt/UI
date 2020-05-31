import xlrd
class ReadExcel:

    def __init__(self):
        pass

    def read_excel(self,path):
        case_list=[]
        casebook=xlrd.open_workbook(path)
        casesheet=casebook.sheet_by_index(0)
        nrows=casesheet.nrows
        for i in range(nrows):
            case=(casesheet.row_values(i))
            print(case)
            # del case[0]
            case_list.append(case)
        return case_list


if __name__ == '__main__':
    a=ReadExcel()
    a.read_excel('../../Excel/excel_case/case_excel.xls')