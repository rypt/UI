from Tool.database.db_code_test import domysql


a=domysql()
b=a.select_db('group_permission',18134727)
print(b)
c=a.select_db('code',18555258798)
print(c)