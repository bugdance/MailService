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
"""The parser is use for parse the data."""


class CallInParser:
    """接入解析器，解析接口结构数据。"""
    
    def __init__(self, enable_corp: bool = True):
        """Init.
        
        Args:
            enable_corp (bool): Whether it is a corporate account(True/False). 是否是企业账户。
        """
        self.logger: any = None  # 日志记录器。
        self.enable_corp: bool = enable_corp  # 是否是企业类型。
        # # # Interface data. 接口数据。
        self.task_id: any = None  # 任务编号。
        self.username: str = ""  # 最终用的用户名。
        self.password: str = ""  # 最终用的密码。
        self.server: str = ""
        self.port: int = 0
        self.uid: str = ""
        self.result: int = 2
        
    def parse_to_interface(self, source_dict: dict = None) -> bool:
        """Parsing interface parameters. 解析接口数据。
        
        Args:
            source_dict (dict): The source dict. 来源字典。

        Returns:
            bool
        """
        if not source_dict or type(source_dict) is not dict:
            self.logger.info(f"解析接口参数有误(*>﹏<*)【{source_dict}】")
            return False
        # # # Parse the username and password. 解析账户名和密码，不区分企业个人。
        
        # # # Parse the detail. 解析航班信息。
        self.task_id = source_dict.get('requestId')
        self.username = source_dict.get('email')
        self.password = source_dict.get('password')
        self.server = source_dict.get('server')
        self.port = source_dict.get('port')
        self.uid = source_dict.get('uid')
        self.result = source_dict.get('handleResult')
        return True
    

    


