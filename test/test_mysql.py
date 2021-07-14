#!/usr/bin/env python
# encoding: utf-8
"""
@author: liubowen
@contact: 15178940382@163.com
@site: http://www.liubowen.icu/
@file: test_mysql.py
@time: 2021/7/14 9:36
"""
from pymysql import connect, cursors


class DBConnect:
    def __init__(self, host='localhost', port=3306, db='', user='root', passwd='root', charset='utf8'):
        # 建立连接
        self.conn = connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)
        # 创建游标，操作设置为字典类型
        self.cur = self.conn.cursor(cursor=cursors.DictCursor)

    def __enter__(self):
        # 返回游标
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 提交数据库并执行
        self.conn.commit()
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()


def main():
    conn = DBConnect(host='47.240.57.43', port=3306, db='test', user='root', passwd='123456')
    sql = 'select * from new_studentinformation'

    conn.__enter__().execute(sql)
    results = conn.__enter__().fetchall()
    # print(type(results))
    for row in results:
        # name = list(row.values())[3]
        # addr = list(row.values())[5]
        print("姓名：%s,地址：%s" % (list(row.values())[3], list(row.values())[5]))


if __name__ == '__main__':
    main()
