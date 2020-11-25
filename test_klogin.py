# -*- coding: utf-8 -*-

import unittest
from selenium import webdriver
path='/usr/local/bin/chromedriver'
from base import Base

class TestKlogin(unittest.TestCase):

    #定位手机号
    username = ("name","regName")
    #定位密码
    psw = ("name","pwd")
    #定位登录按钮
    loginbutton = ("id","submit")
    #定位帮助中心
    help = ("xpath","//*[contains(text(),'全国疫情实时')]")
    print("help",help)
    #定位提示信息
    message = ("xpath","//*[contains(text(),'重新输入')]")
    print("message" ,message)

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(executable_path=path)
        cls.baselei = Base(cls.driver)

    def setUp(self):
        self.driver.get("http://127.0.0.1:5000")

    def tearDown(self):
        # 清空cookies
        self.driver.delete_all_cookies()
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


    def test_01_loginsuccess(self):
        '''正确输入用户名和密码'''
        self.baselei.send(self.username,"111")
        self.baselei.send(self.psw,"222")
        self.baselei.click(self.loginbutton)
        result1=self.baselei.is_element_exist(self.help)
        self.assertTrue(result1)

    def test_02_bushuru(self):
        '''不输入，点击登录'''
        self.baselei.click(self.loginbutton)
        result2 =self.baselei.find(self.message).text
        print("我是内容test02：",result2)
        exp2 = "输入信息不全，请重新输入"
        self.assertEqual(result2,exp2)

    def test_03_shuruname(self):
        '''只输入用户名，不输入密码'''
        self.baselei.send(self.username,"111")
        self.baselei.click(self.loginbutton)
        result3 = self.baselei.find(self.message).text
        #result3=self.baselei.is_element_exist(self.message)
        print("我是内容test03：",result3)
        exp3="输入信息不全，请重新输入"
        self.assertTrue(result3==exp3)
        #self.assertTrue(result3)

    def test_04_shurupsw(self):
        '''只输入密码，不输入用户名'''
        self.baselei.send(self.psw,"222")
        self.baselei.click(self.loginbutton)
        result4 = self.baselei.find(self.message).text
        print("我是内容test04:",result4)
        exp4="输入信息不全，请重新输入"
        self.assertTrue(result4==exp4)

    def test_05_shurufail(self):
        '''输入错误的账号和密码'''
        self.baselei.send(self.username,"4334668")
        self.baselei.send(self.psw,"325465")
        self.baselei.click(self.loginbutton)
        result5 = self.baselei.find(self.message).text
        print("我是内容test05",result5)
        exp5 = "用户不存在，请重新输入"
        #self.assertTrue(result4==exp4)
        self.assertEqual(result5,exp5)


if __name__ == '__main__':
    unittest.main()