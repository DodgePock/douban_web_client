from config import client_init
from douban_web_client import DoubanWebClient
import logging
import re

logging.basicConfig(level=logging.INFO)


dwc = DoubanWebClient(**client_init)

home_page= dwc.get_html_page('https://www.douban.com/')

username_res = re.search(r'<span>(.+?)的账号</span>', home_page)

if username_res:
    username = username_res.group(1)
    logging.info(f'Username found: {username}')
else:
    logging.error('Username not found in the home page HTML.')
