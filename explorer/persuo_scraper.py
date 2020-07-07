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


class PersUOScraper:
	"""UO采集器，UO邮件解析，没有PNR。"""
	
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