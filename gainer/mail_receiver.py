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
"""The receiver is use for receive the data."""
# # # Import current path.
import sys
sys.path.append('..')
# # # Base package.
from flask import Flask, request, jsonify
import logging
import time
import configparser
import requests
import json
# # # Packages.
from booster.callback_formatter import CallBackFormatter
from explorer.acquire_scraper import AcquireScraper
from explorer.alter_scraper import AlterScraper
# # # App instances. App实例。
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
# # # 日志格式化。
app.logger = logging.getLogger('flask')
app.logger.setLevel(level=logging.INFO)
app.formatter = logging.Formatter('[%(asctime)s]%(message)s')
app.handler = logging.FileHandler("mail.log")
# app.handler = logging.StreamHandler()
app.handler.setFormatter(app.formatter)
app.logger.addHandler(app.handler)


# # # 接口请求地址，http://x.x.x.x:18081/mail/acquire/。
@app.route('/mail/acquire/', methods=['POST'])
def mail_acquire() -> dict:
    """获取邮件接口。

    Returns:
        dict
    """
    # # # 开始计时，回调声明。
    start_time = time.time()
    call_back = CallBackFormatter()
    call_back.logger = app.logger
    return_error = call_back.format_to_sync()
    # # # 解析数据并获取日志任务号。
    try:
        get_dict = json.loads(request.get_data())
        task_id = get_dict.get('requestId')
        log_path = f"log/mail-{task_id}.log"
    except Exception as ex:
        msg = "邮件抓取数据格式有误"
        return_error['msg'] = msg
        app.logger.info(msg)
        app.logger.info(ex)
        return jsonify(return_error)
    else:
        # # # 读取配置文件信息并配置。
        config = configparser.ConfigParser()
        config.read("config.ini", encoding="utf-8")
        # # # 读取并检查转发配置类型。
        forward_address = "" # 转发地址。
        if 'forward' in config:
            forward = config.options('forward')
            if "acquire" in forward:
                forward_address = config.get('forward', "acquire")
        # # # 判断地址是否需要转发。
        if forward_address:
            msg = "邮件抓取转发声明完成"
            app.logger.info(msg)
            try:
                request_url =  f"{forward_address}/acquire/"
                response = requests.post(url=request_url, json=get_dict, timeout=60)
                result_data = response.json()
                result_msg = result_data.get('msg')
            except Exception as ex:
                msg = "邮件抓取转发地址超时"
                return_error['msg'] = msg
                app.logger.info(msg)
                app.logger.info(ex)
                return jsonify(return_error)
            else:
                end_time = (time.time() - start_time).__round__(2)
                msg = f"邮件抓取转发请求成功【{end_time}】【{task_id}】【{result_msg}】"
                app.logger.info(msg)
                return jsonify(result_data)
        else:
            msg = "邮件抓取本地声明完成"
            app.logger.info(msg)
            try:
                # # # 拼接请求参数。
                process_dict = {
                    "task_id": task_id, "log_path": log_path, "source_dict": get_dict,
                    "enable_proxy": "False", "address": "", "retry_count": 1
                }
                # # # 声明航司类。
                scraper = AcquireScraper()
                result_data = scraper.process_to_main(process_dict)
                result_msg = result_data.get('msg')
            except Exception as ex:
                msg = "邮件抓取本地未知错误"
                return_error['msg'] = msg
                app.logger.info(msg)
                app.logger.info(ex)
                return jsonify(return_error)
            else:
                end_time = (time.time() - start_time).__round__(2)
                msg = f"邮件抓取本地请求成功【{end_time}】【{task_id}】【{result_msg}】"
                app.logger.info(msg)
                return jsonify(result_data)


# # # 接口请求地址，http://x.x.x.x:18081/mail/alter/。
@app.route('/mail/alter/', methods=['POST'])
def mail_alter() -> dict:
    """邮件移动接口。

    Returns:
        dict
    """
    # # # 开始计时，回调声明。
    start_time = time.time()
    call_back = CallBackFormatter()
    call_back.logger = app.logger
    return_error = call_back.format_to_async()
    # # # 解析数据并获取日志任务号。
    try:
        get_dict = json.loads(request.get_data())
        task_id = get_dict.get('requestId')
        log_path = f"log/mail-{task_id}.log"
    except Exception as ex:
        msg = "邮件移动数据格式有误"
        return_error['msg'] = msg
        app.logger.info(msg)
        app.logger.info(ex)
        return jsonify(return_error)
    else:
        # # # 读取配置文件信息并配置。
        config = configparser.ConfigParser()
        config.read("config.ini", encoding="utf-8")
        # # # 读取并检查转发配置类型。
        forward_address = "" # 转发地址。
        if 'forward' in config:
            forward = config.options('forward')
            if "alter" in forward:
                forward_address = config.get('forward', "alter")
        # # # 判断地址是否需要转发。
        if forward_address:
            msg = "邮件移动转发声明完成"
            app.logger.info(msg)
            try:
                request_url =  f"{forward_address}/alter/"
                response = requests.post(url=request_url, json=get_dict, timeout=60)
                result_data = response.json()
                result_msg = result_data.get('msg')
            except Exception as ex:
                msg = "邮件移动转发地址超时"
                return_error['msg'] = msg
                app.logger.info(msg)
                app.logger.info(ex)
                return jsonify(return_error)
            else:
                end_time = (time.time() - start_time).__round__(2)
                msg = f"邮件移动转发请求成功【{end_time}】【{task_id}】【{result_msg}】"
                app.logger.info(msg)
                return jsonify(result_data)
        else:
            msg = "邮件移动本地声明完成"
            app.logger.info(msg)
            try:
                # # # 拼接请求参数。
                process_dict = {
                    "task_id": task_id, "log_path": log_path, "source_dict": get_dict,
                    "enable_proxy": "False", "address": "", "retry_count": 1
                }
                # # # 声明航司类。
                scraper = AlterScraper()
                result_data = scraper.process_to_main(process_dict)
                result_msg = result_data.get('msg')
            except Exception as ex:
                msg = "邮件移动本地未知错误"
                return_error['msg'] = msg
                app.logger.info(msg)
                app.logger.info(ex)
                return jsonify(return_error)
            else:
                end_time = (time.time() - start_time).__round__(2)
                msg = f"邮件移动本地请求成功【{end_time}】【{task_id}】【{result_msg}】"
                app.logger.info(msg)
                return jsonify(result_data)

        

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=18085)
