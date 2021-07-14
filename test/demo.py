#!/usr/bin/env python
# encoding: utf-8
"""
@author: liubowen
@contact: 15178940382@163.com
@site: http://www.liubowen.icu/
@file: demo.py
@time: 2021/7/14 9:19
"""
list_stu = []
stu1 = {'name': '张三', 'age': 30, 'sex': '男', 'address': '上海'}
stu2 = {'name': '李四', 'age': 26, 'sex': '女', 'address': '重庆'}
list_stu.append(stu1)
list_stu.append(stu2)
if __name__ == '__main__':
    for i in list_stu:
        print(list(i.values())[0])

