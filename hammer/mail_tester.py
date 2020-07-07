#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""Script test.

written by pyLeo.
"""
# # # Import current path.
import sys
sys.path.append('..')
# # # Analog interface.
import requests
import time
from explorer.acquire_scraper import AcquireScraper
from explorer.alter_scraper import AlterScraper
#cxigrrhwvpwjbebe

post_data = {
    "requestId": "1111", "uid": "1580703522", "handleResult": 2,
    "email": "hthy777@vip.163.com", "password": "tianye123",
    "server": "imap.vip.163.com",
    "port": 993
}

def post_test():
    """
    
    Returns:

    """
    company = "acquire"
    # company = "alter"
    url = f"http://119.3.249.135:18083/mail/{company}/"
    response = requests.post(url=url, json=post_data)
    print(response.text)


if __name__ == '__main__':
    
    # post_test()
    while 1:

        process_dict = {
            "task_id": 1111, "log_path": "test.log", "source_dict": post_data,
            "enable_proxy": False, "address": "", "retry_count": 1
        }

        scraper = AcquireScraper()
        result = scraper.process_to_main(process_dict)
        time.sleep(600)

