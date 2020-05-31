import pymysql
class domysql():
    def __init__(self):
        self.conn = pymysql.connect(host='10.10.82.107', user='hjm_dev', password='hjm_dev', database='hjm', port=3306,
                               charset='utf8')
        # 获取数据库游标
        # self.cursor = self.conn.cursor()
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
    def __del__(self):
        self.conn.close()
        self.cursor.close()

    def select_db(self,num):

        # 执行游标的sql语句
        sql = "select code from hjm.h_mobile_captcha where mobile='{}' order by updated_at desc limit 1;".format(num)
        rest = self.cursor.execute(sql)
        # 通过游标查询
        db = self.cursor.fetchall()
        key='code'
        for temp in db: value = ("%s" % temp[key])
        return value

    def change_db(self,sql):
        rest = self.cursor.execute(sql)
        db = self.cursor.fetchall()
        # 修改需要提交
        self.conn.commit()



