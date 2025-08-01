import requests
import logging
from .tools import is_dict_proxy_available, proxy_format_dict_to_url
import time

logger = logging.getLogger(__name__)


class DoubanWebClient:
    def __init__(
        self,
        cookies_str: str|None = None,
        proxy_url: str|None = "http://blackhole.webpagetest.org",
        user_agent: str|None = None,
        init_ck: bool = False,
        default_request_timeout: int = 10,
        default_exception_retry: int = 3,
        **kwargs,
    ):
        logger.info(f"{'*'*20} Douban Web Client init {'*'*20}")
        self.init_proxies(proxy_url, **kwargs)
        default_user_agent = "MMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
        self.user_agent = user_agent if user_agent else default_user_agent
        self.default_headers = {
            "User-Agent": self.user_agent,
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://www.douban.com/",
        }

        self.init_session(cookies_str)
        self.default_request_timeout = default_request_timeout
        self.default_request_exception_retry = default_exception_retry

        if init_ck: # 是否初始化ck
            # 1. 检查是否有ck
            self.ck = self.session.cookies.get('ck', None)
            
            # 2. 如果没有ck，则访问豆瓣首页获取ck
            if not self.ck:
                logger.info("No ck found, fetching from Douban homepage.")
                self.get_html_page("https://www.douban.com/")
                self.ck = self.session.cookies.get('ck', None)
            
            # 3. 如果仍然没有ck，则抛出异常
            if not self.ck:
                raise ValueError("Failed to initialize ck. Please check your cookies or network connection.")


    def init_session(self, cookies_str: str|None):
        self.session = requests.Session()
        self.session.proxies.update(self.proxies)
        self.session.trust_env = False

        # 设置cookies
        if cookies_str:
            for cookie_pair in cookies_str.split(";"):
                cookie_name, cookie_value = cookie_pair.strip().split("=", maxsplit=1)
                self.session.cookies.set(
                    name=cookie_name, value=cookie_value, domain=".douban.com", path="/"
                )
            self.is_cookie_set = True
            self.ck = self.session.cookies.get('ck', None)
            logger.info("加载cookies")
        else:
            self.is_cookie_set = False
            logger.info("未加载cookies")

        # 设置headers
        self.session.headers.update(self.default_headers)

    def init_proxies(self, proxy_url, **kwargs):
        # 初始化代理, 优先级：kwargs['proxy'] > proxy_url > proxy_url(default)
        # 如不使用代理，则需要同时设置proxy_url和kwargs['proxy']为None
        proxy = kwargs.get("proxy", None)
        proxy_url = (
            proxy_format_dict_to_url(proxy)
            if is_dict_proxy_available(proxy)
            else proxy_url
        )
        if proxy_url is None:
            logger.info("No proxy is set.")
            self.proxies = None
        logger.info(f"Using proxy: {proxy_url}")
        self.proxies = {"http": proxy_url, "https": proxy_url}

    def get_html_page(
        self,
        url: str,
        except_status_code: int = 200,
        exception_retry: int|None = None,
        retry_interval: int = 3,
        **kwargs,
    ):
        kwargs["timeout"] = kwargs.get("timeout", self.default_request_timeout)
        exception_retry = (
            exception_retry
            if exception_retry is not None
            else self.default_request_exception_retry
        )
        try:
            response = self.session.get(url, **kwargs)
            if response.status_code != except_status_code:
                logger.warning(
                    f'get html page {url} failed with status code {response.status_code}' + \
                    ('\n'+response.text) if response.text else ''
                )
                retry = True
            else:
                logger.info(f'get html page {url} successed. params {kwargs.get("params")}')
                retry = False
                return response.text
        except Exception as e:
            logger.error(f"get html page {url} failed with error: {e}")
            retry = True
        finally:
            if retry and exception_retry > 0:
                time.sleep(retry_interval)
                return self.get_html_page(
                    url, except_status_code, exception_retry - 1, **kwargs
                )
            elif retry:
                return None
