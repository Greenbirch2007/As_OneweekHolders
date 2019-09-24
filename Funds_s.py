# -*- coding:utf-8 -*-
import datetime
import re
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
    big_list= []

    selector = etree.HTML(html)
    fund_name = selector.xpath('//*[@id="dbtable"]/tbody/tr/td[4]/a/text()')
    fund_link = selector.xpath('//*[@id="dbtable"]/tbody/tr/td[4]/a/@href')
    fund_pr = selector.xpath('//*[@id="dbtable"]/tbody/tr/td[9]/text()')
    f_sh_link = []
    for item in fund_link:
        fl = item[-11:-5]
        f_sh_link.append('http://fundf10.eastmoney.com/ccmx_'+str(fl)+'.html')

    for i1,i2,i3 in zip(fund_name,fund_pr,f_sh_link):

        big_list.append((i1,i2,i3))

    return big_list




def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='AS_fundinfos',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        cursor.executemany('insert into Funds_s (fund_name,fund_pr,f_sh_link) values (%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass

#
if __name__ == '__main__':
    url = 'http://fund.eastmoney.com/data/fundranking.html#tgp;c0;r;szzf;pn50;ddesc;qsd20180924;qed20190924;qdii;zq;gg;gzbd;gzfs;bbzt;sfbb'
    html = get_first_page(url)
    content =parse_stock_note(html)
    insertDB(content)
    driver.quit()




# (fund_name,fund_pr,f_sh_link)
# 因为板块数据是最后嵌套进去的，所以要保持，１．数据库表结构，２．解析整理后的数据结构　３．　插入的字段结构　三者之间都要保持一致
# create table Funds_s(
# id int not null primary key auto_increment,
# fund_name varchar(50),
# fund_pr varchar(50),
# f_sh_link varchar(150)
# ) engine=InnoDB  charset=utf8;

#  drop table Funds_s;