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

    def select_db(self,select,num):
        if select=='code':
            sql = "select code from hjm.h_mobile_captcha where mobile='{}' order by updated_at desc limit 1;".format(num)
        elif select=='group_permission':
            sql = "SELECT group_permission FROM live.h_live_user_group where user_id ='{}' order by updated_at desc limit 1;".format(num)
        else:
            pass
        # 执行游标的sql语句
        rest = self.cursor.execute(sql)
        # 通过游标查询
        db = self.cursor.fetchall()
        key=select
        for temp in db: value = ("%s" % temp[key])
        return value

    def change_db(self,sql):
        rest = self.cursor.execute(sql)
        db = self.cursor.fetchall()
        # 修改需要提交
        self.conn.commit()

    def delete_db_group(self,num):
        sql1="delete from live.h_live_user_group where user_id ={};".format(num)
        sql2="delete from live.h_live_user_group_permission where user_id ={};".format(num)
        sql3="delete from live.h_live_user_group_permission_log where user_id={};".format(num)
        sql4="delete from live.h_live_user_group_video_permission where user_id={};".format(num)
        sql5="delete from live.h_live_user_group_video_permission_log where user_id={};".format(num)
        sql6="Delete FROM hjm.h_order  where user_id in({}) and order_member_type is not null;".format(num)
        sql_list=[sql1,sql2,sql3,sql4,sql5,sql6]
        for i in sql_list:
            sql=i
            self.cursor.execute(sql)
            self.conn.commit()


if __name__ == '__main__':
    a=domysql()
    a.delete_db_group(18134727)
