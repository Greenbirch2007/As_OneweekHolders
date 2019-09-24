# -*- coding:utf-8 -*-
import datetime
import time

import pymysql

from lxml import etree
from selenium import webdriver

driver = webdriver.Chrome()


def get_first_page(url):

    driver.get(url)
    html = driver.page_source
    return html



# 可以尝试第二种解析方式，更加容易做计算
def parse_stock_note(html):
    big_list = []
    selector = etree.HTML(html)
    code = selector.xpath('//*[@id="cctable"]/div[1]/div/table/tbody/tr/td[2]/a/text()')
    name = selector.xpath('//*[@id="cctable"]/div[1]/div/table/tbody/tr/td[3]/a/text()')

    for i1,i2 in zip(code,name):
        big_list.append((i1,i2))

    return big_list







# 尝试在这个模块提取代码和板块，用代码去拼接个股链接，同时往大ｌist传入个股
def Python_sel_Mysql():
    # 使用cursor()方法获取操作游标
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='AS_fundinfos',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cur = connection.cursor()
    #sql 语句
    for i in range(1,51):
        sql = 'select * from Funds_s where id = %s ' % i
        # #执行sql语句
        cur.execute(sql)
        # #获取所有记录列表
        data = cur.fetchone()
        url = data['f_sh_link']
        yield url



def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='AS_fundinfos',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        cursor.executemany('insert into Stocks_s (code,name) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass


if __name__ == '__main__':
    for url_str in Python_sel_Mysql():
        html = get_first_page(url_str)
        content = parse_stock_note(html)
        insertDB(content)
        print(datetime.datetime.now())
        time.sleep(1)
    driver.quit()


# create table Stocks_s(
# id int not null primary key auto_increment,
# code varchar(20),
# name varchar(20)
# ) engine=InnoDB default charset=utf8;

