import random
import time

from loguru import logger
from faker import Faker
from pyfunctions import fun
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


logger.add('call.log', rotation='20 MB')


class ColdCall:
    # 密码只要符合网站注册密码要求即可
    password = 'aiahdia6'
    # 映射配置文件中定位元素的模式
    mode_map = {
        'id': By.ID,
        'xpath': By.XPATH,
        'name': By.NAME,
        'class_name': By.CLASS_NAME,
        'link_text': By.LINK_TEXT
    }

    def __init__(self, phone_number, name=''):
        self.driver = fun.make_driver(load_img=True)
        self.driver.set_page_load_timeout(30)
        self.driver.set_script_timeout(30)
        self.phone_number = phone_number
        self.name = name or Faker('zh_CN').name()

    def tease_site(self, site):
        """根据配置点击网站进行注册/登录"""
        self.driver.get(site['url'])
        # 获取site字段
        username, password = site.get('username_path'), site.get('password_path')
        phone_path, submit_path = site['phone_path'], site.get('submit_path')
        iframe, password_confirm = site.get('iframe'), site.get('password_confirm_path')
        sleep_time, message = float(site.get('sleep_time', 0)), site.get('message_path')
        # 不填写留言内容默认使用手机号
        message_content = message and message.get('msg', self.phone_number)
        preset, postset = site.get('preset'), site.get('postset')
        # 等待表单页面加载完全
        sleep_time and time.sleep(sleep_time)
        iframe and self.driver.switch_to.frame(iframe)
        preset and self._parse_type(preset)
        # 填写表单
        self._send_optional_value(username, self.name)
        self.send_phone_number(phone_path)
        fun.random_sleep(3)
        self._send_optional_value(password, self.password)
        fun.random_sleep(3)
        self._send_optional_value(password_confirm, self.password)
        fun.random_sleep(3)
        self._send_optional_value(message, message_content)
        fun.random_sleep(3)
        submit_path and self._find_element(submit_path).click()
        postset and self._parse_type(postset)
        fun.random_sleep(2)
        # 处理alert
        try:
            alert = self.driver.switch_to.alert()
            alert.accept()
        except:
            pass
        fun.random_sleep(60)

    def send_phone_number(self, phone_path):
        """逐个字符输入手机号"""
        time.sleep(1)
        self._find_element(phone_path).clear()
        for i in range(11):
            self._find_element(phone_path).send_keys(self.phone_number[i])
            fun.random_sleep(0.3)

    def _parse_type(self, item):
        """解析preset和postset字段，执行点击命令/脚本"""
        set_type = item.get('type', 'click')
        if set_type == 'click':
            self._find_element(item).click()
        elif set_type == 'script':
            self.driver.execute_script(item['value'])
        time.sleep(0.2)

    @staticmethod
    def _load_sites(verify_code_only=False):
        """
        加载配置文件，通过rate字段区分短信/电话
        :param verify_code_only: 只返回验证码
        :return: 需要请求的网站
        """
        sites = fun.load_json_file("sites.json")
        rate_sites = [(site, int(site['rate'])) for site in sites if 'rate' in site]
        if verify_code_only:
            sites = []
            for site in rate_sites:
                sites.extend([site[0]] * site[1])
            random.shuffle(sites)
            return sites

        for site in rate_sites:
            sites.extend([site[0]] * (site[1]-1))
            random.shuffle(sites)
        return sites

    def _parse_mode(self, item):
        """解析配置文件中的mode,默认为xpath"""
        mode = item.get('mode', 'xpath')
        return self.mode_map[mode]

    def _find_element(self, item):
        """对driver.find_element的封装"""
        return self.driver.find_element(self._parse_mode(item), item['value'])

    def _send_optional_value(self, key, value):
        """对于可能存在的值进行填写"""
        if key:
            self._find_element(key).send_keys(value)

    def run(self, verify_code_only=False):
        # self.tease_site(fun.load_json_file('sites.json')[-1])
        # sites = fun.load_json_file("sites.json")[-2:]
        sites = self._load_sites(verify_code_only)
        for site in sites:
            try:
                self.tease_site(site)
                logger.info(f"[SUCCESS] {site['url']}")
            except TimeoutException:
                try:
                    self.driver.refresh()
                except:
                    logger.info(f"[ERROR] {site['url']}")
            except:
                logger.info(f"[ERROR] {site['url']}")

        self.driver.quit()


if __name__ == '__main__':
    cc = ColdCall("")
    cc.run()
