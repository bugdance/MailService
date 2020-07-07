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


class Pers5JScraper:
	"""5J采集器，5J邮件解析，取消和航变，信息最全。"""
	
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
			"//div[@class='main-cont']//p/text()[contains(., 'Booking reference no.:')]", data)
		pnr = self.BPR.parse_to_clear(pnr)
		pnr, temp_list = self.BPR.parse_to_regex(":(.*)", pnr)
		# # # flight number
		old_number, temp_list = self.DPR.parse_to_attributes(
			"value", "xpath",
			"//table[contains(.//thead/., 'CANCELLED')]//tbody//td//text()[contains(., 'Flight No:')]", data)
		old_number = self.BPR.parse_to_clear(old_number)
		old_number, temp_list = self.BPR.parse_to_regex(":(.*)", old_number)
		# # # 出发地全文
		old_depart, temp_list = self.DPR.parse_to_attributes(
			"value", "xpath",
			"//table[contains(.//thead/., 'CANCELLED')]//tbody//p[contains(., 'Departure:')]//text()", data)
		old_depart = ""
		for i in temp_list:
			old_depart += f"{i} "
		old_depart = self.BPR.parse_to_separate(old_depart)
		# # # 取名字
		depart_name, temp_list = self.BPR.parse_to_regex("\)(.*)", old_depart)
		depart_name = self.BPR.parse_to_separate(depart_name)
		# # # 取时间
		depart_time, temp_list = self.BPR.parse_to_regex(": (.*?) \(", old_depart)
		depart_time = self.DFR.format_to_transform(depart_time, "%H:%M")
		# # # 到达地全文
		old_arrival, temp_list = self.DPR.parse_to_attributes(
			"value", "xpath",
			"//table[contains(.//thead/., 'CANCELLED')]//tbody//p[contains(., 'Arrival:')]//text()", data)
		old_arrival = ""
		for i in temp_list:
			old_arrival += f"{i} "
		old_arrival = self.BPR.parse_to_separate(old_arrival)
		# # # 取名字
		arrival_name, temp_list = self.BPR.parse_to_regex("\)(.*)", old_arrival)
		arrival_name = self.BPR.parse_to_separate(arrival_name)
		# # # 取时间
		arrival_time, temp_list = self.BPR.parse_to_regex(": (.*?) \(", old_arrival)
		arrival_time = self.DFR.format_to_transform(arrival_time, "%H:%M")
		# # # 取日期
		old_date, temp_list = self.DPR.parse_to_attributes(
			"value", "xpath",
			"//table[contains(.//thead/., 'CANCELLED')]//tbody//p//text()[contains(., 'Date:')]", data)
		old_date = self.BPR.parse_to_clear(old_date)
		old_date, temp_list = self.BPR.parse_to_regex(":(.*)", old_date)
		old_date = self.DFR.format_to_transform(old_date, "%B%d,%Y")
		next_date = self.DFR.format_to_custom(old_date, 1)
		
		# # # 比较
		if depart_time.hour <= arrival_time.hour:
			depart_date = f'{old_date.strftime("%Y-%m-%d")} {depart_time.strftime("%H:%M")}'
			arrival_date = f'{old_date.strftime("%Y-%m-%d")} {arrival_time.strftime("%H:%M")}'
		else:
			depart_date = f'{old_date.strftime("%Y-%m-%d")} {depart_time.strftime("%H:%M")}'
			arrival_date = f'{next_date.strftime("%Y-%m-%d")} {arrival_time.strftime("%H:%M")}'
		
		# # # set value
		result['uid'] = uid
		result['time'] = uid_date
		result['pnr'] = pnr
		result['type'] = 2
		result['carrierCode'] = "5J"
		result['oldFlightNum'] = old_number
		result['oldDepartureAirport'] = depart_name
		result['oldArrivalAirport'] = arrival_name
		result['oldDepartureTime'] = depart_date
		result['oldArrivalTime'] = arrival_date
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
			"//div[@class='main-cont']//p/text()[contains(., 'Booking reference no.:')]", data)
		pnr = self.BPR.parse_to_clear(pnr)
		pnr, temp_list = self.BPR.parse_to_regex(":(.*)", pnr)
		# # # flight number
		old_number, temp_list = self.DPR.parse_to_attributes(
			"value", "xpath",
			"//table[contains(.//thead/., 'ORIGINAL')]//tbody//td//text()[contains(., 'Flight No:')]", data)
		old_number = self.BPR.parse_to_clear(old_number)
		old_number, temp_list = self.BPR.parse_to_regex(":(.*)", old_number)
		# # # 出发地全文
		old_depart, temp_list = self.DPR.parse_to_attributes(
			"value", "xpath",
			"//table[contains(.//thead/., 'ORIGINAL')]//tbody//p[contains(., 'Departure:')]//text()", data)
		old_depart = ""
		for i in temp_list:
			old_depart += f"{i} "
		old_depart = self.BPR.parse_to_separate(old_depart)
		# # # 出发地名字
		old_depart_name, temp_list = self.BPR.parse_to_regex("\)(.*)", old_depart)
		old_depart_name = self.BPR.parse_to_separate(old_depart_name)
		# # # 出发地时间
		old_depart_time, temp_list = self.BPR.parse_to_regex(": (.*?) \(", old_depart)
		old_depart_time = self.DFR.format_to_transform(old_depart_time, "%H:%M")
		# # # 到达地全文
		old_arrival, temp_list = self.DPR.parse_to_attributes(
			"value", "xpath",
			"//table[contains(.//thead/., 'ORIGINAL')]//tbody//p[contains(., 'Arrival:')]//text()", data)
		old_arrival = ""
		for i in temp_list:
			old_arrival += f"{i} "
		old_arrival = self.BPR.parse_to_separate(old_arrival)
		# # # 到达地名字
		old_arrival_name, temp_list = self.BPR.parse_to_regex("\)(.*)", old_arrival)
		old_arrival_name = self.BPR.parse_to_separate(old_arrival_name)
		# # # 到达地时间
		old_arrival_time, temp_list = self.BPR.parse_to_regex(": (.*?) \(", old_arrival)
		old_arrival_time = self.DFR.format_to_transform(old_arrival_time, "%H:%M")
		# # # 旧日期
		old_date, temp_list = self.DPR.parse_to_attributes(
			"value", "xpath",
			"//table[contains(.//thead/., 'ORIGINAL')]//tbody//p//text()[contains(., 'Date:')]", data)
		old_date = self.BPR.parse_to_clear(old_date)
		old_date, temp_list = self.BPR.parse_to_regex(":(.*)", old_date)
		old_date = self.DFR.format_to_transform(old_date, "%B%d,%Y")
		next_old = self.DFR.format_to_custom(old_date, 1)
		# # # 对比
		if old_depart_time.hour <= old_arrival_time.hour:
			old_depart_date = f'{old_date.strftime("%Y-%m-%d")} {old_depart_time.strftime("%H:%M")}'
			old_arrival_date = f'{old_date.strftime("%Y-%m-%d")} {old_arrival_time.strftime("%H:%M")}'
		else:
			old_depart_date = f'{old_date.strftime("%Y-%m-%d")} {old_depart_time.strftime("%H:%M")}'
			old_arrival_date = f'{next_old.strftime("%Y-%m-%d")} {old_arrival_time.strftime("%H:%M")}'
		
		# # # flight number
		new_number, temp_list = self.DPR.parse_to_attributes(
			"value", "xpath",
			"//table[contains(.//thead/., 'NEW')]//tbody//td//text()[contains(., 'Flight No:')]", data)
		new_number = self.BPR.parse_to_clear(new_number)
		new_number, temp_list = self.BPR.parse_to_regex(":(.*)", new_number)
		# # # 出发地全文
		new_depart, temp_list = self.DPR.parse_to_attributes(
			"value", "xpath",
			"//table[contains(.//thead/., 'NEW')]//tbody//p[contains(., 'Departure:')]//text()", data)
		new_depart = ""
		for i in temp_list:
			new_depart += f"{i} "
		new_depart = self.BPR.parse_to_separate(new_depart)
		# # # 出发地名字
		new_depart_name, temp_list = self.BPR.parse_to_regex("\)(.*)", new_depart)
		new_depart_name = self.BPR.parse_to_separate(new_depart_name)
		# # # 出发地时间
		new_depart_time, temp_list = self.BPR.parse_to_regex(": (.*?) \(", new_depart)
		new_depart_time = self.DFR.format_to_transform(new_depart_time, "%H:%M")
		# # # 到达地全文
		new_arrival, temp_list = self.DPR.parse_to_attributes(
			"value", "xpath",
			"//table[contains(.//thead/., 'NEW')]//tbody//p[contains(., 'Arrival:')]//text()", data)
		new_arrival = ""
		for i in temp_list:
			new_arrival += f"{i} "
		new_arrival = self.BPR.parse_to_separate(new_arrival)
		# # # 到达地名字
		new_arrival_name, temp_list = self.BPR.parse_to_regex("\)(.*)", new_arrival)
		new_arrival_name = self.BPR.parse_to_separate(new_arrival_name)
		# # # 到达地时间
		new_arrival_time, temp_list = self.BPR.parse_to_regex(": (.*?) \(", new_arrival)
		new_arrival_time = self.DFR.format_to_transform(new_arrival_time, "%H:%M")
		# # # 新日期
		new_date, temp_list = self.DPR.parse_to_attributes(
			"value", "xpath",
			"//table[contains(.//thead/., 'NEW')]//tbody//p//text()[contains(., 'Date:')]", data)
		new_date = self.BPR.parse_to_clear(new_date)
		new_date, temp_list = self.BPR.parse_to_regex(":(.*)", new_date)
		new_date = self.DFR.format_to_transform(new_date, "%B%d,%Y")
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
		if "terminal" in new_depart.lower():
			new_depart_terminal = "发现航站楼"
		if "terminal" in new_arrival.lower():
			new_arrival_terminal = "发现航站楼"
			
		# # # set value
		result['uid'] = uid
		result['time'] = uid_date
		result['pnr'] = pnr
		result['type'] = 1
		result['carrierCode'] = "5J"
		result['oldFlightNum'] = old_number
		result['oldDepartureAirport'] = old_depart_name
		result['oldArrivalAirport'] = old_arrival_name
		result['oldDepartureTime'] = old_depart_date
		result['oldArrivalTime'] = old_arrival_date
		result['newFlightNum'] = new_number
		result['newDepartureAirport'] = new_depart_name
		result['newArrivalAirport'] = new_arrival_name
		result['newDepartureTime'] = new_depart_date
		result['newArrivalTime'] = new_arrival_date
		result['newDepartureTerminal'] = new_depart_terminal
		result['newArrivalTerminal'] = new_arrival_terminal
		
		return result
	


