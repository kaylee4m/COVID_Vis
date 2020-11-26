# coding=UTF-8
import sys
import os
import json
import requests
import unittest
from decimal import *
from utils import get_r1_data, get_time
from app import LoginUsers

class TestFunc(unittest.TestCase):
    def test_get_r1_data(self):
        '''
        Test method get_r1_data()
        '''
        self.assertEqual((('武汉', Decimal('50340')), ('香港', Decimal('5701')), ('孝感', Decimal('3518')), ('黄冈', Decimal('2907')), ('荆州', Decimal('1580'))), get_r1_data())
    def test_get_time(self):
        result= get_time()

        self.assertEqual('2020',result[:4])

    # def setUp(self):
    #     url = "http://127.0.0.1:5000/"
    #     uerinfo = {'regName': '111','pwd':'222'}
    #     response = requests.post(url,data = uerinfo).text #这个请求对象，调用post方法传入参数
    #     print(response)
    #     response_dict = json.loads(response)
    #     self.get_token = response_dict['data']

    # def test_case2(self):
    #     url1 = "http://127.0.0.1:5000/"
    #     Forget_token = self.get_token
    #     uerinfo1 = {'regName': '111','psw':'222'}
    #     response1 = requests.post(url1,data = uerinfo1).text #这个请求对象，调用post方法传入参数
    #     print(response1)


if __name__ == '__main__':
    unittest.main()

