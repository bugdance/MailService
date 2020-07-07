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
from booster.basic_formatter import BasicFormatter
from booster.basic_parser import BasicParser
from booster.date_formatter import DateFormatter
from booster.dom_parser import DomParser


class PersAKScraper:
	"""AK采集器，AK邮件解析，取消和航变，航变没有原始信息，没有中转。"""
	
	def __init__(self) -> None:
		self.logger = None
		self.BFR = BasicFormatter()  # 基础格式器。
		self.BPR = BasicParser()  # 基础解析器。
		self.DFR = DateFormatter()  # 日期格式器。
		self.DPR = DomParser()  # 文档解析器。
	
	def init_to_assignment(self) -> bool:
		"""Assignment to logger. 赋值日志。

		Returns:
			bool
		"""
		self.BFR.logger = self.logger
		self.BPR.logger = self.logger
		self.DFR.logger = self.logger
		self.DPR.logger = self.logger
		return True
	
	def set_to_cancel(self, uid: str = "", uid_date: str = "", data: str = ""):
		"""

		Returns:

		"""
		result = {}
		# # # PNR
		pnr, temp_list = self.DPR.parse_to_attributes(
			"value", "xpath",
			"//table[contains(.//td, 'Booking number:')]//td//text()[contains(., 'Booking number:')]", data)
		pnr = self.BPR.parse_to_clear(pnr)
		pnr, temp_list = self.BPR.parse_to_regex(":(.*)", pnr)
		
		# # # set value
		result['uid'] = uid
		result['time'] = uid_date
		result['pnr'] = pnr
		result['type'] = 2
		result['carrierCode'] = "AK"
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
	
	def set_to_change(self, uid: str = "", uid_date: str = "", data: str = ""):
		"""

		Args:
			uid:
			uid_date:
			data:

		Returns:

		"""
		result = {}
		# # # pnr
		pnr, temp_list = self.DPR.parse_to_attributes(
			"value", "xpath",
			"//table[contains(.//td, 'Booking number:')]//td//text()[contains(., 'Booking number:')]", data)
		pnr = self.BPR.parse_to_clear(pnr)
		pnr, temp_list = self.BPR.parse_to_regex(":(.*)", pnr)
		# # # new all
		new_all, temp_list = self.DPR.parse_to_attributes(
			"value", "xpath",
			"//table//tbody//td[contains(., 'Flight number:')]/text()",
			data)
		new_all = ""
		for i in temp_list:
			new_all += f"{i} "
		new_all = self.BPR.parse_to_separate(new_all)
		# # # flight number
		new_number, temp_list = self.BPR.parse_to_regex("Flight number:(.*?)Depart date:", new_all)
		new_number = self.BPR.parse_to_clear(new_number)
		# # # 出发地全文
		new_place, temp_list = self.DPR.parse_to_attributes(
			"value", "xpath",
			"//table//tbody//td[contains(., 'Flight number:')]/strong/text()",
			data)
		new_place = self.BPR.parse_to_separate(new_place)
		# # # 出发地名字
		new_depart_name, temp_list = self.BPR.parse_to_regex("(.*?) to", new_place)
		new_depart_name = self.BPR.parse_to_separate(new_depart_name)
		# # # 出发地时间
		new_depart_time, temp_list = self.BPR.parse_to_regex("Depart :(.*?)Arrive :", new_all)
		new_depart_time = self.BPR.parse_to_clear(new_depart_time)
		new_depart_time, temp_list = self.BPR.parse_to_regex("\((.*?)hrs", new_depart_time)
		new_depart_time = self.DFR.format_to_transform(new_depart_time, "%H%M")
		# # # 到达地名字
		new_arrival_name, temp_list = self.BPR.parse_to_regex("to (.*)", new_place)
		new_arrival_name = self.BPR.parse_to_separate(new_arrival_name)
		# # # 到达地时间
		new_arrival_time, temp_list = self.BPR.parse_to_regex("Arrive :(.*)", new_all)
		new_arrival_time = self.BPR.parse_to_clear(new_arrival_time)
		new_arrival_time, temp_list = self.BPR.parse_to_regex("\((.*?)hrs", new_arrival_time)
		new_arrival_time = self.DFR.format_to_transform(new_arrival_time, "%H%M")
		# # # 新日期
		new_date, temp_list = self.BPR.parse_to_regex("Depart date:(.*?)Depart :", new_all)
		new_date = self.BPR.parse_to_clear(new_date)
		new_date = self.DFR.format_to_transform(new_date, "%d%B%Y")
		next_new = self.DFR.format_to_custom(new_date, 1)
		# # # 对比
		if new_depart_time.hour <= new_arrival_time.hour:
			new_depart_date = f'{new_date.strftime("%Y-%m-%d")} {new_depart_time.strftime("%H:%M")}'
			new_arrival_date = f'{new_date.strftime("%Y-%m-%d")} {new_arrival_time.strftime("%H:%M")}'
		else:
			new_depart_date = f'{new_date.strftime("%Y-%m-%d")} {new_depart_time.strftime("%H:%M")}'
			new_arrival_date = f'{next_new.strftime("%Y-%m-%d")} {new_arrival_time.strftime("%H:%M")}'
		
		new_depart_terminal = ""
		new_arrival_terminal = ""
		if "terminal" in new_place.lower():
			new_depart_terminal = "发现航站楼"
		if "terminal" in new_place.lower():
			new_arrival_terminal = "发现航站楼"
		
		# # # set value
		result['uid'] = uid
		result['time'] = uid_date
		result['pnr'] = pnr
		result['type'] = 1
		result['carrierCode'] = "AK"
		result['oldFlightNum'] = ""
		result['oldDepartureAirport'] = ""
		result['oldArrivalAirport'] = ""
		result['oldDepartureTime'] = ""
		result['oldArrivalTime'] = ""
		result['newFlightNum'] = new_number
		result['newDepartureAirport'] = new_depart_name
		result['newArrivalAirport'] = new_arrival_name
		result['newDepartureTime'] = new_depart_date
		result['newArrivalTime'] = new_arrival_date
		result['newDepartureTerminal'] = new_depart_terminal
		result['newArrivalTerminal'] = new_arrival_terminal
		
		return result



