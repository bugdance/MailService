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


class PersTRScraper:
	"""TR采集器，TR邮件解析，取消和航变，中英文俩种，不支持航变没有原始信息得邮件。"""
	
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
	
	def set_en_cancel(self, uid, d, data):
		"""

		Returns:

		"""
		result = {}
		pnr, temp_list = self.DPR.parse_to_attributes(
			"value", "xpath",
			"//strong/text()[contains(., 'Booking Ref:')]", data)
		pnr = self.BPR.parse_to_clear(pnr)
		pnr, temp_list = self.BPR.parse_to_regex(":(.*)", pnr)

		# # # set value
		result['uid'] = uid
		result['time'] = d
		result['pnr'] = pnr
		result['type'] = 2
		result['carrierCode'] = "TR"
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
	
	def set_cn_cancel(self, uid, d, data):
		"""

		Returns:

		"""
		result = {}
		pnr, temp_list = self.DPR.parse_to_attributes(
			"value", "xpath",
			"//strong/text()[contains(., '预订编码：')]", data)
		pnr = self.BPR.parse_to_clear(pnr)
		pnr, temp_list = self.BPR.parse_to_regex("：(.*)", pnr)
		
		# # # set value
		result['uid'] = uid
		result['time'] = d
		result['pnr'] = pnr
		result['type'] = 2
		result['carrierCode'] = "TR"
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
	
	def set_en_change(self, uid, uid_date, data):
		"""

		Returns:

		"""
		result = {}
		pnr, temp_list = self.DPR.parse_to_attributes(
			"value", "xpath",
			"//strong/text()[contains(., 'Booking Ref:')]", data)
		pnr = self.BPR.parse_to_clear(pnr)
		pnr, temp_list = self.BPR.parse_to_regex(":(.*)", pnr)
		# # # old all
		old_all, all_list = self.DPR.parse_to_attributes(
			"value", "xpath",
			"//table//tbody//td[contains(.//span, 'Original Schedule')]//del/text()",
			data)
		if not all_list:
			old_all, all_list = self.DPR.parse_to_attributes(
				"value", "xpath",
				"//table//tbody//td[contains(.//span, 'Old Schedule')]//del/text()",
				data)
		if len(all_list) < 4:
			old_number = ""
			old_depart_name = ""
			old_arrival_name = ""
			old_depart_date = ""
			old_arrival_date = ""
		else:
			# # # flight number
			old_number = all_list[1]
			old_number = self.BPR.parse_to_clear(old_number)
			# # # 出发地全文
			old_place = all_list[0]
			old_place = self.BPR.parse_to_separate(old_place)
			# # # 出发地名字
			old_depart_name, temp_list = self.BPR.parse_to_regex("(.*?) to", old_place)
			old_depart_name = self.BPR.parse_to_separate(old_depart_name)
			# # # 出发地时间
			old_depart_time = all_list[2]
			old_depart_time = self.BPR.parse_to_clear(old_depart_time)
			old_depart_time = old_depart_time.replace("-", "")
			old_depart_time = self.DFR.format_to_transform(old_depart_time, "%d%B%Y,%I:%M%p")
			old_depart_date = old_depart_time.strftime("%Y-%m-%d %H:%M")
			# # # 到达地名字
			old_arrival_name, temp_list = self.BPR.parse_to_regex("to (.*)", old_place)
			old_arrival_name = self.BPR.parse_to_separate(old_arrival_name)
			# # # 到达地时间
			old_arrival_time = all_list[3]
			old_arrival_time = self.BPR.parse_to_clear(old_arrival_time)
			old_arrival_time = old_arrival_time.replace("-", "")
			old_arrival_time = self.DFR.format_to_transform(old_arrival_time, "%d%B%Y,%I:%M%p")
			old_arrival_date = old_arrival_time.strftime("%Y-%m-%d %H:%M")
	
		# # # new all
		new_all, temp_list = self.DPR.parse_to_attributes(
			"value", "xpath",
			"//table//tbody//td[contains(.//span, 'Revised Schedule')]//text()",
			data)
		new_all = ""
		for i in temp_list:
			new_all += f"{i} "
		new_all = self.BPR.parse_to_separate(new_all)
		# # # flight number
		new_number, temp_list = self.BPR.parse_to_regex("Flight No\.:(.*?)Departure\*", new_all)
		new_number = self.BPR.parse_to_clear(new_number)
		# # # 出发地全文
		new_place, temp_list = self.BPR.parse_to_regex("Revised Schedule Route:(.*?)Flight No\.", new_all)
		new_place = self.BPR.parse_to_separate(new_place)
		# # # 出发地名字
		new_depart_name, temp_list = self.BPR.parse_to_regex("(.*?) to", new_place)
		new_depart_name = self.BPR.parse_to_separate(new_depart_name)
		# # # 出发地时间
		new_depart_time, temp_list = self.BPR.parse_to_regex("Departure\*:(.*?)Arrival\*:", new_all)
		new_depart_time = self.BPR.parse_to_clear(new_depart_time)
		new_depart_time = new_depart_time.replace("-", "")
		new_depart_time = self.DFR.format_to_transform(new_depart_time, "%d%B%Y,%I:%M%p")
		new_depart_date = new_depart_time.strftime("%Y-%m-%d %H:%M")
		# # # 到达地名字
		new_arrival_name, temp_list = self.BPR.parse_to_regex("to (.*)", new_place)
		new_arrival_name = self.BPR.parse_to_separate(new_arrival_name)
		# # # 到达地时间
		new_arrival_time, temp_list = self.BPR.parse_to_regex("Arrival\*:(.*)", new_all)
		new_arrival_time = self.BPR.parse_to_clear(new_arrival_time)
		new_arrival_time = new_arrival_time.replace("-", "")
		new_arrival_time = self.DFR.format_to_transform(new_arrival_time, "%d%B%Y,%I:%M%p")
		new_arrival_date = new_arrival_time.strftime("%Y-%m-%d %H:%M")
		
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
		result['carrierCode'] = "TR"
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

