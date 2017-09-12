# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import requests
import MySQLdb
from bs4 import BeautifulSoup
import re

###
# MySQL DB 접속 설정
###
mysql_host = "localhost"
mysql_userid = "ipsi"
mysql_password = "ipsi12#"
mysql_dbname = "ipsiDb"

HYU_url = "http://addon.jinhakapply.com/RatioV1/RatioH/Ratio11640051.html"
DGU_url = "http://addon.jinhakapply.com/RatioV1/RatioH/Ratio10550041.html"
SSU_url = "http://ratio.uwayapply.com/2018/susi2/ssu/1/"
AJU_url = "http://addon.jinhakapply.com/RatioV1/RatioH/Ratio11040151.html"


def hanyang_in_parse():
    idx = 0
    hanyang_in_info = {}
    response = requests.get(HYU_url)
    response.encoding = None
    soup = BeautifulSoup(response.text, "html.parser")
    spRes = soup.find("div", {"id": "SelType4L"})
    #print ("HANYANG UNIV")
    #print (spRes)

    table = spRes.find('table', {'class': 'tableRatio3'})
    #print(table)

    td = table.findAll('td')
    #print(td)

    for element in td:
        text = element.renderContents()
        wrap_text = text.strip()
        #print(text)
        decode_text = wrap_text.decode('utf-8')
        #print(decode_text)
        if idx == 0:
            hanyang_in_info['College'] = decode_text
        elif idx == 1:
            hanyang_in_info['Recruitment unit'] = decode_text
        elif idx == 2:
            hanyang_in_info['Recruitment count'] = decode_text
        elif idx == 3:
            hanyang_in_info['Applied count'] = decode_text
        elif idx == 4:
            hanyang_in_info['Competition rate'] = decode_text
        idx += 1

    #print(hanyang_in_info)
    return hanyang_in_info


def hanyang_out_parse():
    idx = 0
    hanyang_out_info = {}
    response = requests.get(HYU_url)
    response.encoding = None
    soup = BeautifulSoup(response.text, "html.parser")
    spRes = soup.find("div", {"id": "SelType4M"})
    #print ("HANYANG UNIV")
    #print (spRes)
    table = spRes.find('table', {'class': 'tableRatio3'})
    #print(table)

    td = table.findAll('td')
    #print(td)

    for element in td:
        text = element.renderContents()
        wrap_text = text.strip()
        #print(text)
        decode_text = wrap_text.decode('utf-8')
        #print(decode_text)
        if idx == 0:
            hanyang_out_info['College'] = decode_text
        elif idx == 1:
            hanyang_out_info['Recruitment unit'] = decode_text
        elif idx == 2:
            hanyang_out_info['Recruitment count'] = decode_text
        elif idx == 3:
            hanyang_out_info['Applied count'] = decode_text
        elif idx == 4:
            hanyang_out_info['Competition rate'] = decode_text
        idx += 1

    #print(hanyang_out_info)
    return hanyang_out_info

def dongguk_parse():
    idx = 0
    dongguk_info = {}
    response = requests.get(DGU_url)
    response.encoding = None
    soup = BeautifulSoup(response.text, "html.parser")
    spRes = soup.find("div", {"id": "SelType41AK"})
    #print ("DONGGUK UNIV")
    #print (spRes)
    table = spRes.find('table', {'class': 'tableRatio3'})
    #print(table)

    td = table.findAll('td')
    #print(td)

    for element in td:
        text = element.renderContents()
        wrap_text = text.strip()
        #print(text)
        decode_text = wrap_text.decode('utf-8')
        if idx >= 5:
            break

        #print(decode_text)

        if idx == 0:
            dongguk_info['College'] = decode_text
        if idx == 1:
            dongguk_info['Recruitment unit'] = decode_text
        elif idx == 2:
            dongguk_info['Recruitment count'] = decode_text
        elif idx == 3:
            dongguk_info['Applied count'] = decode_text
        elif idx == 4:
            dongguk_info['Competition rate'] = decode_text

        idx += 1

    #print(dongguk_info)
    return dongguk_info


def soongsil_parse():
    idx = 0
    soongsil_info = {}
    response = requests.get(SSU_url)
    response.encoding = None
    soup = BeautifulSoup(response.text, "html.parser")
    spRes = soup.find("div", {"id": "Div_0014"})
    #print ("SSU UNIV")
    #print (spRes)
    table = spRes.find('tr', {'id': 'Tr_0014_001470000'})
    #print(table)

    td = table.findAll('td')
    #print(td)

    for element in td:
        #print("1 %s", element)
        text = element.renderContents()
        #print(text)
        wrap_text = text.strip()
        #print(wrap_text)
        decode_text = wrap_text.decode('utf-8')
        #print(decode_text)
        if idx >= 6:
            break

        #print(decode_text)
        if idx == 0:
            soongsil_info['Classification'] = decode_text
        elif idx == 1:
            soongsil_info['College'] = decode_text
        elif idx == 2:
            soongsil_info['Recruitment unit'] = decode_text
        elif idx == 3:
            soongsil_info['Recruitment count'] = decode_text
        elif idx == 4:
            soongsil_info['Applied count'] = decode_text
        elif idx == 5:
            decode_text = cleanhtml(decode_text)
            #print(decode_text)
            soongsil_info['Competition rate'] = decode_text

        idx += 1

    #print(dongguk_info)
    return soongsil_info


def ajou_parse():
    idx = 0
    ajou_info = {}
    response = requests.get(AJU_url)
    response.encoding = None
    soup = BeautifulSoup(response.text, "html.parser")
    spRes = soup.find("div", {"id": "SelType410"})
    #print (spRes)

    table = spRes.find('table', {'class': 'tableRatio3'})
    print(table)

    td = table.findAll('td')
    #print(td)

    for element in td:
        text = element.renderContents()
        wrap_text = text.strip()
        #print(text)
        decode_text = wrap_text.decode('utf-8')
        #print(decode_text)

        if idx >= 4:
            break

        if idx == 0:
            ajou_info['Recruitment unit'] = decode_text
        elif idx == 1:
            ajou_info['Recruitment count'] = decode_text
        elif idx == 2:
            ajou_info['Applied count'] = decode_text
        elif idx == 3:
            ajou_info['Competition rate'] = decode_text

        idx += 1

    #print(ajou_info)
    return ajou_info


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def insert_info_to_db(db, info, univ_name):
    #print(univ_name)
    #print(info['College'])
    #print(info['Recruitment unit'])
    #print(info['Recruitment count'])
    #print(info['Applied count'])
    #print(info['Competition rate'])
    if univ_name == "HYU_in":
        sql_query = "INSERT INTO `hanyang_in_ratio` (`College`, `unit`, `count`, `apply_count`, `ratio`) \
		VALUES ('{}', '{}', {}, {}, '{}')".format(info['College'], info['Recruitment unit'], \
		info['Recruitment count'], info['Applied count'], info['Competition rate'])
    elif univ_name == "HYU_out":
        sql_query = "INSERT INTO `hanyang_out_ratio` (`College`, `unit`, `count`, `apply_count`, `ratio`) \
		VALUES ('{}', '{}', {}, {}, '{}')".format(info['College'], info['Recruitment unit'], \
		info['Recruitment count'], info['Applied count'], info['Competition rate'])
    elif univ_name == "DGU":
        sql_query = "INSERT INTO `dongguk_ratio` (`College`, `unit`, `count`, `apply_count`, `ratio`) \
		VALUES ('{}', '{}', {}, {}, '{}')".format(info['College'], info['Recruitment unit'], \
		info['Recruitment count'], info['Applied count'], info['Competition rate'])
    elif univ_name == "SSU":
        sql_query = "INSERT INTO `soongsil_ratio` (`Classification`, `College`, `unit`, `count`, `apply_count`, `ratio`) \
                    VALUES ( '{}', '{}', '{}', {}, {}, '{}')".format(info['Classification'], info['College'], info['Recruitment unit'], \
		    info['Recruitment count'], info['Applied count'], info['Competition rate'])
    elif univ_name == "AJU":
        sql_query = "INSERT INTO `ajou_ratio` (`unit`, `count`, `apply_count`, `ratio`) \
		VALUES ('{}', {}, {}, '{}')".format(info['Recruitment unit'], \
		info['Recruitment count'], info['Applied count'], info['Competition rate'])

    cursor = db.cursor()
    set_database_for_utf8(cursor)
    #print(sql_query)
    cursor.execute(sql_query)
    db.commit()


def set_database_for_utf8(cursor):
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    return


def connect_mysql_database():
    db = MySQLdb.connect(mysql_host, mysql_userid, mysql_password, mysql_dbname)
    db.set_character_set('utf8')
    return db


def disconnect_mysql_database(db):
    db.close()
    return


def main():
    hy_in = hanyang_in_parse()
    #print(hy_in)
    hy_out = hanyang_out_parse()
    #print(hy_out)
    dg = dongguk_parse()
    #print(dg)
    ssu = soongsil_parse()
    #print(ssu)
    aju = ajou_parse()
    #print(aju)

    db = connect_mysql_database()

    insert_info_to_db(db, hy_in, "HYU_in")
    insert_info_to_db(db, hy_out, "HYU_out")
    insert_info_to_db(db, dg, "DGU")
    insert_info_to_db(db, ssu, "SSU")
    insert_info_to_db(db, aju, "AJU")

    disconnect_mysql_database(db)


if __name__ == '__main__':
    main()
