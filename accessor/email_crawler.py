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
"""The crawler is use for crawl structure data."""
import imaplib
from email.header import decode_header
import email.iterators


class EmailCrawler:
	"""email，爬行器用于交互数据。"""
	
	def __init__(self):
		self.logger: any = None  # 日志记录器。
		self.conn: any = None    # 连接对象。
	
	def set_to_login(self, server: str = "", port: int = 993,
	                 username: str = "", password: str = "") -> bool:
		"""
		
		Args:
			server: 服务器地址
			port: 服务器端口
			username: 用户名
			password: 密码

		Returns:
			bool
		"""
		try:
			self.conn = imaplib.IMAP4_SSL(host=server, port=port)
			self.conn.login(username, password)
		except Exception as ex:
			self.logger.info(f"邮件服务登录失败(*>﹏<*)【{username}】【{ex}】")
			return False
		else:
			return True
	
	def set_to_close(self) -> bool:
		"""
		
		Returns:
			bool
		"""
		try:
			self.conn.close()
		except Exception as ex:
			self.logger.info(f"邮件服务关闭失败(*>﹏<*)【{ex}】")
			return False
		else:
			return True
	
	def set_to_logout(self) -> bool:
		"""
		
		Returns:
			bool
		"""
		try:
			self.conn.logout()
		except Exception as ex:
			self.logger.info(f"邮件服务退出失败(*>﹏<*)【{ex}】")
			return False
		else:
			return True
	
	def set_to_select(self, folder: str = "inbox") -> bool:
		"""
		
		Args:
			folder:

		Returns:
			bool
		"""
		try:
			status, result = self.conn.select(folder)
			result = result[0]
		except Exception as ex:
			self.logger.info(f"邮件服务选择失败(*>﹏<*)【{folder}】【{ex}】")
			return False
		else:
			if "OK" in status and result is not None:
				return True
			else:
				self.logger.info(f"邮件服务选择失败(*>﹏<*)【{folder}】【{result}】")
				return False
	
	def set_to_search(self, search_type: str = "all", search_range: int = 50) -> tuple:
		"""
		
		Args:
			search_type:
			search_range:

		Returns:
			tuple
		"""
		try:
			status, result = self.conn.uid('search', search_type)
			result = result[0]
			if "OK" in status:
				if result is not None and type(result) is bytes:
					result = result.decode('utf-8')
					result = result.split()
					return True, result[:search_range]
				else:
					return True, []
			else:
				self.logger.info(f"邮件服务搜索失败(*>﹏<*)【{search_type}】【{result}】")
				return False, []
		except Exception as ex:
			self.logger.info(f"邮件服务搜索失败(*>﹏<*)【{search_type}】【{ex}】")
			return False, []

	def set_to_fetch(self, uid: str = "") -> tuple:
		"""
		
		Args:
			uid:

		Returns:
			tuple
		"""
		try:
			status, result = self.conn.uid("fetch", uid, 'BODY[]')
			result = result[0][1]
			if "OK" in status:
				if result is not None and type(result) is bytes:
					result = result.decode('utf-8')
					return True, result
				else:
					return True, ""
			else:
				self.logger.info(f"邮件服务获取失败(*>﹏<*)【{uid}】【{result}】")
				return False, ""
		except Exception as ex:
			self.logger.info(f"邮件服务获取失败(*>﹏<*)【{uid}】【{ex}】")
			return False, ""
	
	def set_to_copy(self, uid: str = "", folder: str = "") -> bool:
		"""
		
		Args:
			uid:
			folder:

		Returns:
			bool
		"""
		try:
			status, result = self.conn.uid("copy", uid, folder)
			result = result[0]
		except Exception as ex:
			self.logger.info(f"邮件服务复制失败(*>﹏<*)【{uid}】【{ex}】")
			return False
		else:
			if "OK" in status:
				return True
			else:
				self.logger.info(f"邮件服务复制失败(*>﹏<*)【{uid}】【{result}】")
				return False
	
	def set_to_seen(self, is_seen: bool = False, uid: str = "") -> bool:
		"""
		
		Args:
			is_seen:
			uid:

		Returns:
			bool
		"""
		try:
			if is_seen:
				status, result = self.conn.uid("store", uid, '+FLAGS', '(\Seen)')
				result = result[0]
			else:
				status, result = self.conn.uid("store", uid, '-FLAGS', '(\Seen)')
				result = result[0]
		except Exception as ex:
			self.logger.info(f"邮件服务状态失败(*>﹏<*)【{uid}】【{ex}】")
			return False
		else:
			if "OK" in status and result is not None:
				return True
			else:
				self.logger.info(f"邮件服务状态失败(*>﹏<*)【{uid}】【{result}】")
				return False
	
	def set_to_delete(self, uid: str = "") -> bool:
		"""
		
		Args:
			uid:

		Returns:
			bool
		"""
		try:
			status, result = self.conn.uid("store", uid, '+FLAGS', '(\Deleted)')
			result = result[0]
		except Exception as ex:
			self.logger.info(f"邮件服务删除失败(*>﹏<*)【{uid}】【{ex}】")
			return False
		else:
			if "OK" in status and result is not None:
				return True
			else:
				self.logger.info(f"邮件服务删除失败(*>﹏<*)【{uid}】【{result}】")
				return False
	
	def set_to_object(self, source_data: str = "") -> any:
		"""
		
		Args:
			source_data:

		Returns:
			any
		"""
		try:
			messageObject = email.message_from_string(source_data)
		except Exception as ex:
			self.logger.info(f"邮件转换对象失败(*>﹏<*)【{ex}】")
			return None
		else:
			return messageObject
	
	def set_to_body(self, msg_part: any = None) -> str:
		"""
		
		Args:
			msg_part:

		Returns:
			str
		"""
		content = ""
		try:
			content_type = msg_part.get_content_type()  # 判断邮件内容的类型,text/html
			if content_type == 'text/plain' or content_type == 'text/html':
				content = msg_part.get_payload(decode=True)
				charset = msg_part.get_charset()
				if charset is None:
					content_type = msg_part.get('Content-Type', '').lower()
					position = content_type.find('charset=')
					if position >= 0:
						charset = content_type[position + 8:].strip()
				if charset:
					content = content.decode(charset)
		except Exception as ex:
			self.logger.info(f"邮件转换部分失败(*>﹏<*)【{ex}】")
			return ""
		else:
			return content
	
	def set_to_message(self, message_object: any = None) -> str:
		"""邮件解析正文
		
		Args:
			message_object:

		Returns:

		"""
		
		contents = []
		try:
			if message_object.is_multipart():  # 判断邮件是否由多个部分构成
				message_parts = message_object.get_payload()  # 获取邮件附载部分
				for i in message_parts:
					body_content = self.set_to_body(i)
					if body_content:
						contents.append(body_content)
			else:
				body_content = self.set_to_body(message_object)
				if body_content:
					contents.append(body_content)
					
			if contents:
				if len(contents) > 1:
					return contents[1]
				else:
					return contents[0]
			else:
				self.logger.info(f"邮件解析正文失败(*>﹏<*)【为空】")
				return ""
		except Exception as ex:
			self.logger.info(f"邮件解析正文失败(*>﹏<*)【{ex}】")
			return ""
			
	def set_to_header(self, text):
		try:
			aaa = decode_header(text)
		except Exception as ex:
			return ""
		else:
			if type(aaa[0][0]) is str:
				return aaa[0][0]
			elif type(aaa[0][0]) is bytes:
				return aaa[0][0].decode("utf-8")