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


class AlterScraper(RequestWorker):
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
		
		self.emails = []
	
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
		self.retry_count = process_dict.get("retry_count")
		if not self.retry_count:
			self.retry_count = 1
		# # # 初始化日志。
		self.init_to_logger(task_id, log_path)
		self.init_to_assignment()
		# # # 同步返回参数。
		self.callback_data = self.CFR.format_to_async()
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
		# # #
		result = self.BFR.format_to_int(self.CPR.result)
		if result == 1:
			if "qq.com" in self.CPR.server:
				if not self.ECR.set_to_copy(self.CPR.uid, "&UXZO1mWHTvZZOQ-/AvatarSuccess"):
					self.callback_msg = "复制到成功文件夹失败"
					return False
				else:
					if not self.ECR.set_to_delete(self.CPR.uid):
						self.callback_msg = "删除邮件失败，可能没有此邮件"
						return False
					else:
						return True
			elif "163.com" in self.CPR.server:
				if not self.ECR.set_to_copy(self.CPR.uid, "AvatarSuccess"):
					self.callback_msg = "复制到成功文件夹失败"
					return False
				else:
					if not self.ECR.set_to_delete(self.CPR.uid):
						self.callback_msg = "删除邮件失败，可能没有此邮件"
						return False
					else:
						return True
		elif result == 2:
			if "qq.com" in self.CPR.server:
				if not self.ECR.set_to_copy(self.CPR.uid, "&UXZO1mWHTvZZOQ-/AvatarFailure"):
					self.callback_msg = "复制到失败文件夹失败"
					return False
				else:
					if not self.ECR.set_to_delete(self.CPR.uid):
						self.callback_msg = "删除邮件失败，可能没有此邮件"
						return False
					else:
						return True
			elif "163.com" in self.CPR.server:
				if not self.ECR.set_to_copy(self.CPR.uid, "AvatarFailure"):
					self.callback_msg = "复制到失败文件夹失败"
					return False
				else:
					if not self.ECR.set_to_delete(self.CPR.uid):
						self.callback_msg = "删除邮件失败，可能没有此邮件"
						return False
					else:
						return True
		else:
			self.callback_msg = "接口处理结果参数不对"
			return False

	def process_to_return(self) -> bool:
		"""Return process. 返回过程。

		Returns:
			bool
		"""
		self.callback_data["success"] = "true"
		self.callback_data['msg'] = "移动邮件成功"
		self.callback_data['emails'] = []
		self.logger.info(self.callback_data)
		return True

