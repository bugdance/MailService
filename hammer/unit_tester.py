#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""Unit test.

written by pyLeo.
"""
# # # Import current path.
import sys

sys.path.append('..')
# # # Analog Function.
from loguru import logger
from accessor.request_crawler import RequestCrawler
from accessor.selenium_crawler import SeleniumCrawler
# from booster.aes_formatter import AESFormatter
from booster.basic_formatter import BasicFormatter
from booster.basic_parser import BasicParser
from booster.date_formatter import DateFormatter
from booster.dom_parser import DomParser
from accessor.email_crawler import EmailCrawler
from hammer.data_tester import a

logger.add("unit_tester.log", colorize=True, enqueue=True,
           format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level="INFO")




if __name__ == '__main__':
	
	RC = RequestCrawler()
	SC = SeleniumCrawler()
	# AF = AESFormatter()
	BF = BasicFormatter()
	BP = BasicParser()
	DF = DateFormatter()
	DP = DomParser()
	EC = EmailCrawler()
	EC.logger = logger
	# AF.logger = logger
	RC.logger = logger
	SC.logger = logger
	BF.logger = logger
	BP.logger = logger
	DF.logger = logger
	DP.logger = logger
	
	
	
	# emails = "hthy777@vip.163.com"
	# password = "13810254174"
	# server = "imap.vip.163.com"
	# port = 993
	#
	# EC.set_to_login(server, port, emails, password)
	# EC.set_to_folder("inbox")
	# # # # 选取邮件范围，并判断。
	# status, search_list = EC.set_to_search('all', 50)
	#
	# # # # 循环取邮件。
	# for i in search_list:
	# 	# # #
	# 	status, data = EC.set_to_fetch(i)
	# 	if not status:
	# 		continue
	# 	if not data:
	# 		continue
	# 	# # #
	# 	obj = EC.set_to_object(data)
	# 	if not obj:
	# 		continue
	# 	msg = EC.set_to_message(obj)
	# 	if not msg:
	# 		continue
	#
	# EC.set_to_logout()
	
	a = "Tue, 18 Feb 2020 19:01:54 -0600"
	b, temp_list = BP.parse_to_regex("\-\d{4}", a)
	print(b)