#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@file: yabo259.py.py
@time: 2020/8/10 10:44
@author: Rezalt
@desc: python 模拟登录亚博体育
"""
import requests
import time
import random
import base64
import hashlib
import hmac


class YaboLogin(object):
    def __init__(self, ):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/84.0.4147.105 Safari/537.36'
        }

    def base_change(self, num, b):
        return ((num == 0) and "0") or (
                self.base_change(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])

    def get_nonce_str(self):
        """
        Math.random().toString(36).substr(2)
        :return:
        """
        nonce_str = self.base_change(int(str(random.random()).split('.')[-1]), 36)
        return nonce_str

    @staticmethod
    def get_sign(data):
        app_securit = 'd77f7fcff637bc61bfb82fcbcd767bfa'
        s = f'appKey={data["appKey"]}&domain={data["domain"]}&name={data["name"]}&nonce_str={data["nonce_str"]}&' \
            f'password={data["password"]}&timestamp={data["timestamp"]}&uuid={data["uuid"]}&appSecurit={app_securit}'
        u = base64.b64encode(s.encode()).decode()
        signature = hmac.new(bytes(app_securit, 'latin-1'), msg=bytes(u, 'latin-1'),
                             digestmod=hashlib.sha256).hexdigest()
        return signature

    def check_datas(self, u_name, pwd):
        data = {
            'name': u_name,
            'password': pwd,
            'domain': 'www.yabo259.com',
            'XCodeId': '',
            'code': '',
            'uuid': '请自己抓包使用自己的机器码',         # 固定机器码
            'g_code': '',
            'geetest_challenge': '',
            'geetest_validate': '',
            'geetest_seccode': '',
            'geetest_code_id': '',
            'geetest_offline': '',
            'appKey': 'c97823e281c071c39e',                 # 固定值
            'timestamp': int(time.time()),                  # 时间戳
            'nonce_str': self.get_nonce_str(),
        }
        sign = self.get_sign(data)
        data['sign'] = sign
        return data

    def login(self, user_name, pass_word):
        data = self.check_datas(u_name=user_name, pwd=pass_word)
        url = 'https://www.yabo259.com/member/v2/web_login'
        response = requests.post(url=url, headers=self.headers, data=data)
        print(response.text)
        print(response.headers)
        # success!!!
        # {"data":{"grade":"1","id":9084255,"is_daili":false,"name":"rezalt9","real_name":"","token":"93839060653355660","upgrade_version":"1629c5daa628d4b4"},"flags":"1","message":"登录成功","status":"success","status_code":200}
        # faile
        # {"data":{"errTotal":"2"},"flags":"1","message":"用户名或密码错误，第1次尝试，20次输入错误账户将锁定","status":"error","status_code":403}


if __name__ == '__main__':
    yb = YaboLogin()
    username = 'xiaoming'
    password = '1234567890'
    yb.login(user_name=username, pass_word=password)
