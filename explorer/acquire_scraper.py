# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2018-, pyLeo Developer. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
"""The scraper is use for website process interaction."""
from accessor.request_worker import RequestWorker
from accessor.email_crawler import EmailCrawler
from booster.aes_formatter import AESFormatter
from booster.basic_formatter import BasicFormatter
from booster.basic_parser import BasicParser
from booster.callback_formatter import CallBackFormatter
from booster.callin_parser import CallInParser
from booster.date_formatter import DateFormatter
from booster.dom_parser import DomParser
# # #
from explorer.pers5j_scraper import Pers5JScraper
from explorer.perstr_scraper import PersTRScraper
from explorer.persak_scraper import PersAKScraper


class AcquireScraper(RequestWorker):
	"""SL采集器，SL网站流程交互，企业账号不支持并发，行李价格区分人不准。"""
	
	def __init__(self) -> None:
		RequestWorker.__init__(self)
		self.ECR = EmailCrawler()  # 请求爬行器。
		self.AFR = AESFormatter()  # AES格式器。
		self.BFR = BasicFormatter()  # 基础格式器。
		self.BPR = BasicParser()  # 基础解析器。
		self.CFR = CallBackFormatter()  # 回调格式器。
		self.CPR = CallInParser()  # 接入解析器。
		self.DFR = DateFormatter()  # 日期格式器。
		self.DPR = DomParser()  # 文档解析器。
		# # #
		self.P5J = Pers5JScraper()
		self.PTR = PersTRScraper()
		self.PAK = PersAKScraper()
		# # #
		self.num_count: int = 50
		self.emails: list = []
	
	def init_to_assignment(self) -> bool:
		"""Assignment to logger. 赋值日志。

		Returns:
			bool
		"""
		self.ECR.logger = self.logger
		self.AFR.logger = self.logger
		self.BFR.logger = self.logger
		self.BPR.logger = self.logger
		self.CFR.logger = self.logger
		self.CPR.logger = self.logger
		self.DFR.logger = self.logger
		self.DPR.logger = self.logger
		# # #
		self.P5J.logger = self.logger
		self.PTR.logger = self.logger
		return True
	
	def process_to_main(self, process_dict: dict = None) -> dict:
		"""Main process. 主程序入口。

		Args:
			process_dict (dict): Parameters. 传参。

		Returns:
			dict
		"""
		task_id = process_dict.get("task_id")
		log_path = process_dict.get("log_path")
		source_dict = process_dict.get("source_dict")

		# # # 初始化日志。
		self.init_to_logger(task_id, log_path)
		self.init_to_assignment()
		# # # 同步返回参数。
		self.callback_data = self.CFR.format_to_sync()
		# # # 解析接口参数。
		if not self.CPR.parse_to_interface(source_dict):
			self.callback_data['msg'] = "请通知技术检查接口数据参数。"
			return self.callback_data
		self.logger.info(source_dict)
		# # # 主体流程。
		if self.process_to_verify():
				self.process_to_return()
				self.ECR.set_to_logout()
				self.logger.removeHandler(self.handler)
				return self.callback_data
		# # # 错误返回。
		self.callback_data['msg'] = self.callback_msg
		# self.callback_data['msg'] = "解决问题中，请手工支付。"
		self.logger.info(self.callback_data)
		self.ECR.set_to_logout()
		self.logger.removeHandler(self.handler)
		return self.callback_data
	
	def process_to_verify(self, count: int = 0, max_count: int = 3) -> bool:
		"""Verify process. 验证过程。

		Args:
			count (int): 累计计数。
			max_count (int): 最大计数。

		Returns:
			bool
		"""
		# # # 登录
		password = self.AFR.decrypt_into_aes(
			self.AFR.encrypt_into_sha1(self.AFR.password_key), self.CPR.password)
		if not self.ECR.set_to_login(
				self.CPR.server, self.CPR.port, self.CPR.username, password):
			self.callback_msg = "账户登录失败"
			return False
		# # # 根据邮箱选择文件夹
		if "qq.com" in self.CPR.server:
			# # # 选文件夹
			if not self.ECR.set_to_select('&UXZO1mWHTvZZOQ-/AvatarNew'):
				self.callback_msg = "选择初始文件夹失败"
				return False
		elif "163.com" in self.CPR.server:
			# # # 选文件夹
			if not self.ECR.set_to_select('AvatarNew'):
				self.callback_msg = "选择初始文件夹失败"
				return False
		# # # 选取邮件范围，并判断。
		status, search_list = self.ECR.set_to_search('all', 50)
		if status:
			if not search_list:
				self.logger.info("没有新的邮件")
				return True
		else:
			self.callback_msg = "搜索邮件失败"
			return False
		# # # 循环取邮件。
		for i in search_list:
			# # #
			msg_date = ""
			status, data = self.ECR.set_to_fetch(i)
			if not status:
				result = self.set_to_failure(i, msg_date)
				self.emails.append(result)
				continue
			if not data:
				result = self.set_to_failure(i, msg_date)
				self.emails.append(result)
				continue
			# # #
			obj = self.ECR.set_to_object(data)
			if not obj:
				result = self.set_to_failure(i, msg_date)
				self.emails.append(result)
				continue
			msg = self.ECR.set_to_message(obj)
			if not msg:
				result = self.set_to_failure(i, msg_date)
				self.emails.append(result)
				continue
			# # #
			msg_date = obj.get("date")
			msg_date = self.BPR.parse_to_clear(msg_date)
			base_date, temp_list = self.BPR.parse_to_regex(".*\d{2}:\d{2}:\d{2}", msg_date)
			base_date = self.DFR.format_to_transform(base_date, "%a,%d%b%Y%H:%M:%S")
			# # #
			add_date, temp_list = self.BPR.parse_to_regex("\+\d{4}", msg_date)
			minus_date, temp_list = self.BPR.parse_to_regex("\-\d{4}", msg_date)
			if add_date and len(add_date) == 5:
				hours = int(add_date[1:3])
				minutes = int(add_date[3:])
				if hours > 8:
					hours -= 8
					msg_date = self.DFR.format_to_custom(base_date, custom_hours=-hours, custom_minutes=-minutes)
				else:
					hours = 8 - hours
					msg_date = self.DFR.format_to_custom(base_date, custom_hours=hours, custom_minutes=minutes)
			elif minus_date and len(minus_date) == 5:
				hours = int(minus_date[1:3]) + 8
				minutes = int(minus_date[3:])
				msg_date = self.DFR.format_to_custom(base_date, custom_hours=hours, custom_minutes=minutes)
			else:
				msg_date = base_date
				
			msg_date = msg_date.strftime("%Y-%m-%d %H:%M:%S")
			# # #
			msg = self.BPR.parse_to_separate(msg)
			if "cebupacificair.com" in msg:
				self.P5J.init_to_assignment()
				cancel, temp_list = self.DPR.parse_to_attributes(
					"value", "xpath", "//table//thead//td/text()[contains(., 'CANCELLED')]", msg)
				change, temp_list = self.DPR.parse_to_attributes(
					"value", "xpath", "//table//thead//td//strong/text()[contains(., 'NEW FLIGHT')]", msg)
				if cancel:
					result = self.P5J.set_to_cancel(i, msg_date, msg)
					self.emails.append(result)
					self.BFR.format_to_file("w", f"static/5j-{i}.html", msg)
				elif change:
					result = self.P5J.set_to_change(i, msg_date, msg)
					self.emails.append(result)
					self.BFR.format_to_file("w", f"static/5j-{i}.html", msg)
				else:
					result = self.set_to_failure(i, msg_date)
					self.emails.append(result)
			elif "flyscoot.com" in msg:
				self.PTR.init_to_assignment()
				cancel_en, temp_list = self.DPR.parse_to_attributes(
					"value", "xpath",
					"//table//tbody//td//span/text()[contains(., 'Cancellation of Scoot')]",
					msg)
				cancel_cn, temp_list = self.DPR.parse_to_attributes(
					"value", "xpath",
					"//table//tbody//td//span/text()[contains(., '取消通知')]",
					msg)
				change_en, temp_list = self.DPR.parse_to_attributes(
					"value", "xpath",
					"//table//tbody//td//span/text()[contains(., 'Revised Schedule')]",
					msg)
				if cancel_en:
					result = self.PTR.set_en_cancel(i, msg_date, msg)
					self.emails.append(result)
					self.BFR.format_to_file("w", f"static/tr-{i}.html", msg)
				elif cancel_cn:
					result = self.PTR.set_cn_cancel(i, msg_date, msg)
					self.emails.append(result)
					self.BFR.format_to_file("w", f"static/tr-{i}.html", msg)
				elif change_en:
					result = self.PTR.set_en_change(i, msg_date, msg)
					self.emails.append(result)
					self.BFR.format_to_file("w", f"static/tr-{i}.html", msg)
				else:
					result = self.set_to_failure(i, msg_date)
					self.emails.append(result)
			elif "airasia.com" in msg:
				self.PAK.init_to_assignment()
				cancel, temp_list = self.DPR.parse_to_attributes(
					"value", "xpath",
					"//table//tbody//*/text()[contains(., 'Flight cancellation notice')]", msg)
				new, temp_list = self.DPR.parse_to_attributes(
					"value", "xpath",
					"//table//tbody//strong//u/text()[contains(., 'New Flight Time')]", msg)
				change, temp_list = self.DPR.parse_to_attributes(
					"value", "xpath",
					"//table//tbody//td/text()[contains(., 'New flight details')]", msg)
				if cancel:
					if new:
						result = self.set_to_failure(i, msg_date)
						self.emails.append(result)
					else:
						result = self.PAK.set_to_cancel(i, msg_date, msg)
						self.emails.append(result)
						self.BFR.format_to_file("w", f"static/ak-{i}.html", msg)
				elif change:
					result = self.PAK.set_to_change(i, msg_date, msg)
					self.emails.append(result)
					self.BFR.format_to_file("w", f"static/ak-{i}.html", msg)
				else:
					result = self.set_to_failure(i, msg_date)
					self.emails.append(result)
			else:
				result = self.set_to_failure(i, msg_date)
				self.emails.append(result)
			
				
		return True
	
	def set_to_failure(self, uid: str = "", uid_date: str = ""):
		"""

		Returns:

		"""
		result = {}
		# # # set value
		result['uid'] = uid
		result['time'] = uid_date
		result['pnr'] = ""
		result['type'] = 0
		result['carrierCode'] = ""
		result['oldFlightNum'] = ""
		result['oldDepartureAirport'] = ""
		result['oldArrivalAirport'] = ""
		result['oldDepartureTime'] = ""
		result['oldArrivalTime'] = ""
		result['newFlightNum'] = ""
		result['newDepartureAirport'] = ""
		result['newArrivalAirport'] = ""
		result['newDepartureTime'] = ""
		result['newArrivalTime'] = ""
		
		return result
	
	def process_to_return(self) -> bool:
		"""Return process. 返回过程。

		Returns:
			bool
		"""
		self.callback_data["success"] = "true"
		self.callback_data['msg'] = "邮件同步成功"
		self.callback_data['emails'] = self.emails
		self.logger.info(self.callback_data)
		return True
