# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import requests
import logging
import MySQLdb
import logging.handlers
import re
from bs4 import BeautifulSoup


###
# Logging Information
###
logger = logging.getLogger('mylogger')
logging.basicConfig(filename='./parse.log',level=logging.WARNING)
fileMaxByte = 1024 * 1024 * 100 #100MB
#fileHandler = logging.handlers.RotatingFileHandler(filename, \
#		maxBytes=fileMaxByte, backupCount=10)

fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] \
			%(asctime)s > %(message)s')

fileHandler = logging.FileHandler('./parse.log')
streamHandler = logging.StreamHandler()

fileHandler.setFormatter(fomatter)
streamHandler.setFormatter(fomatter)

logger.addHandler(fileHandler)
logger.addHandler(streamHandler)


###
# MySQL DB 접속 설정
###
mysql_host = ""
mysql_userid = ""
mysql_password = ""
mysql_dbname = ""


###
# 경쟁률 정보를 가져올 URL
# HYU = 한양대학교
# DGU = 동국대학교
# SSU = 숭실대학교
# AJU = 아주대학교
###
# Jinhak Apply (진학어플라이)
HYU_url = "http://addon.jinhakapply.com/RatioV1/RatioH/Ratio11640051.html"
DGU_url = "http://addon.jinhakapply.com/RatioV1/RatioH/Ratio10550041.html"
AJU_url = "http://addon.jinhakapply.com/RatioV1/RatioH/Ratio11040151.html"

# U-way Apply (유웨이어플라이)
SSU_url = "http://ratio.uwayapply.com/2018/susi2/ssu/1/"

###
# @univ_name 	: 5글자 이내의 통상적인 대학교 이니셜
# 			   	  - 정원 내/외가 별도인 경우, 끝에 IN/OUT postfix
# Postfix		: JHA => JinHak Apply
def competition_rate_parser_JHA(univ_name):
	idx = 0
	univ_comp_info = {}
	type_name = ""

	if univ_name == "HYU-IN":
		response = requests.get(HYU_url)
		type_name = "SelType4L"
	elif univ_name == "HYU-OUT":
		response = requests.get(HYU_url)
		type_name = "SelType4M"
	elif univ_name == "DGU":
		response = requests.get(DGU_url)
		type_name = "SelType41AK"
	elif univ_name == "AJU":
		response = requests.get(AJU_url)
		type_name = "SelType410"
	else:
		logger.warning("Not supported college/university", univ_name)
		return

	logger.debug("univ_name :", univ_name, "type_name :", type_name)

	response.encoding = None
	sp = BeautifulSoup(response.text, "html.parser")
	searched_sp = sp.find("div",{"id":type_name})
	logger.debug("searched_sp :", searched_sp)

	table = searched_sp.find("table", {"class":"tableRatio3"})
	logger.debug("table :", table)

	tds = table.findAll("td")

	for element in tds:
		raw_text = element.renderContents()
		text = raw_text.strip()
		logger.debug("text :", text)

		decoded_text = text.decode("utf-8")
		logger.debug("decoded_text :", decoded_text)

		univ_comp_info[idx] = decoded_text
		idx += 1

	logger.debug(univ_comp_info)
	return univ_comp_info


###
# @univ_name 	: 5글자 이내의 통상적인 대학교 이니셜
# 			   	  - 정원 내/외가 별도인 경우, 끝에 IN/OUT postfix
# Postfix		: UWA => U-Way Apply
def competition_rate_parser_UWA(univ_name):
	idx = 0
	univ_comp_info = {}
	type_name = ""

	if univ_name == "SSU":
		response = requests.get(SSU_url)
		type_name_1 = "Div_0014"
		type_name_2 = "Tr_0014_001470000"
	else:
		logger.warning("Not supported college/university", univ_name)
		return

	logger.debug("univ_name :", univ_name, "type_name :", type_name)

	response.encoding = None
	sp = BeautifulSoup(response.text, "html.parser")
	searched_sp = sp.find("div", {"id":type_name_1})
	logger.debug("searched_sp :", searched_sp)

	tr = searched_sp.find("tr", {"id":type_name_2})
	logger.debug("tr :", tr)

	tds = tr.findAll("td")

	for element in tds:
		raw_text = element.renderContents()
		text = raw_text.strip()
		logger.debug("text :", text)

		decoded_text = text.decode("utf-8")
		decoded_text = cleanhtml(decoded_text)
		logger.debug("decoded_text :", decoded_text)

		univ_comp_info[idx] = decoded_text
		idx += 1

	logger.debug(univ_comp_info)
	return univ_comp_info


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def insert_info_to_db(db, info, univ_name):
    if univ_name == "HYU-IN":
        sql_query = "INSERT INTO `hanyang_in_ratio` (`College`, `unit`, `count`, `apply_count`, `ratio`) \
		VALUES ('{}', '{}', {}, {}, '{}')".format(info[0], info[1], info[2], info[3], info[4], info[5])
    elif univ_name == "HYU-OUT":
        sql_query = "INSERT INTO `hanyang_out_ratio` (`College`, `unit`, `count`, `apply_count`, `ratio`) \
		VALUES ('{}', '{}', {}, {}, '{}')".format(info[0], info[1], info[2], info[3], info[4], info[5])
    elif univ_name == "DGU":
        sql_query = "INSERT INTO `dongguk_ratio` (`College`, `unit`, `count`, `apply_count`, `ratio`) \
		VALUES ('{}', '{}', {}, {}, '{}')".format(info[0], info[1], info[2], info[3], info[4], info[5])
    elif univ_name == "SSU":
        sql_query = "INSERT INTO `soongsil_ratio` (`Classification`, `College`, `unit`, `count`, `apply_count`, `ratio`) \
                    VALUES ( '{}', '{}', '{}', {}, {}, '{}')".format(info[0], info[1], info[2], info[3], info[4], info[5])
    elif univ_name == "AJU":
        sql_query = "INSERT INTO `ajou_ratio` (`unit`, `count`, `apply_count`, `ratio`) \
		VALUES ('{}', {}, {}, '{}')".format(info[0], info[1], info[2], info[3])


	logger.debug("SQL Query : ", sql_query)

	cursor = db.cursor()
	set_database_for_utf8(cursor)
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
	hyu_in = competition_rate_parser_JHA("HYU-IN")
	hyu_out = competition_rate_parser_JHA("HYU-OUT")
	dgu = competition_rate_parser_JHA("DGU")
	aju = competition_rate_parser_JHA("AJU")

	ssu = competition_rate_parser_UWA("SSU")

	db = connect_mysql_database()

	insert_info_to_db(db, hyu_in, "HYU-IN")
	insert_info_to_db(db, hyu_out, "HYU-OUT")
	insert_info_to_db(db, dgu, "DGU")
	insert_info_to_db(db, aju, "AJU")

	insert_info_to_db(db, ssu, "SSU")

	disconnect_mysql_database(db)


if __name__ == '__main__':
    main()
