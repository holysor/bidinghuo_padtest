#-*- coding:utf-8 -*-

__author__ = 'wujiajia'
__data__ = "2018/03/5"

import unittest
import time
import re
import requests
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import config
import profileapi as PF
import Public

'''
    必订火测试版本登录页面
    http://a.bdh.com/login?isInit=1
'''

class login_bdh(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print "Start:",time.ctime(time.time()),'\n'
        # 配置pad端页面显示
        mobileEmulation = config.DEVICE_ORIENTATION[0]
        cls.width = config.DEVICE_ORIENTATION[1]
        cls.height = config.DEVICE_ORIENTATION[2]
        broswer_path = config.CHROME_PATH  # 浏览器exe路径
        cls.driver_path = config.CHROMEDRIVER_PATH  # chromedriver 路径
        cls.Options = ChromeOptions()
        cls.Options.add_experimental_option('mobileEmulation', mobileEmulation)
        cls.Options.binary_location = broswer_path  # 浏览器路径，不指定的话会自动查找Chrome 路径，如果Chrome安装的话


    @classmethod
    def tearDownClass(cls):
        print "End:",time.ctime(time.time())

    def setUp(self):

        #启动chrome
        self.driver = Chrome(chrome_options=self.Options, executable_path=self.driver_path,
                            port=9151)  # 启动chromedriver，根据浏览器路径启动浏览器
        self.driver.set_window_size(self.width, self.height)
        self.url = config.TEST_AIM_ADDRESS['env_test']
        self.driver.get(self.url)
        self.driver.implicitly_wait(30)

    def tearDown(self):
        self.driver.close()
        # self.driver.quit()

    @Public.ErrorHandle
    def test_01(self):
        '''[ipad 登录]采购商登录界面元素验证'''
        #验证pad采购商页面HTML框架是否显示
        assert self.driver.find_element_by_id('app').is_displayed(),"主界面不存在"
        #验证采购商标题
        assert self.driver.find_element_by_xpath('//*[@id="bg"]/div/div/div/div[2]/form/h3').text==u"采购商登录","采购商登录页面标题异常"
        print('采购商登录页面标题-正常')
        #验证图片
        time.sleep(2)
        bg_image = re.search(r'http.*?.jpg', self.driver.find_element_by_id('bg').get_attribute('style'))
        assert bg_image,'无背景图片链接'
        print('背景图片链接存在')
        if bg_image:
            assert requests.get(bg_image.group(0)).status_code == 200,'图片背景异常'
            print('背景图片访问正常')
        #下拉选框-
        select = self.driver.find_element_by_xpath('//*[@id="bg"]/div/div/div/div[2]/form/div[1]/span/select')
        dinghuohui_name = select.find_elements_by_tag_name('option')[1].text
        assert dinghuohui_name==config.TEST_DHH,'采购商登录页面，该品牌商未显示%s'%config.TEST_DHH
        print('采购商登录页面，品牌商显示正常')
        select.click()
        select.find_elements_by_tag_name('option')[1].click()

        #账号密码输入框
        username_input = self.driver.find_elements_by_tag_name('input')[0].get_attribute('placeholder')
        password_input = self.driver.find_elements_by_tag_name('input')[1].get_attribute('placeholder')
        assert username_input == u'请输入用户名', '用户名输入框,"请输入用户名"异常'
        print('用户名输入框-正常')
        self.assertEqual(password_input,u'请输入密码',u'密码输入框,"请输入密码"异常')

        #个人和品牌商选择
        personal = self.driver.find_element_by_class_name('pull-left').text
        self.assertEqual(personal.strip().split(' ')[0],u'个人',u'个人按钮异常')
        print('个人按钮正常')
        self.assertTrue(self.driver.find_element_by_class_name('fa-check').is_displayed(),u'个人按钮旁边勾选异常')
        print('勾选正常')
        brand = self.driver.find_element_by_class_name('pull-right').text
        self.assertEqual(brand.strip().split(' ')[0], u'品牌公司', u'品牌商按钮异常')
        print('品牌公司按钮正常')
        #进入系统按钮
        login_button = self.driver.find_element_by_class_name("yellow").text
        self.assertEqual(login_button,u'进入系统',u'进入系统按钮异常')
        print('进行系统按钮正常')
        time.sleep(1)

    @Public.ErrorHandle
    def test_02(self):
        '''[ipad 登录]个人登录异常场景测试'''
        #账号密码为空
        time.sleep(2)
        select = self.driver.find_element_by_xpath('//*[@id="bg"]/div/div/div/div[2]/form/div[1]/span/select')
        select.click()
        select.find_elements_by_tag_name('option')[1].click()#考虑可维护性
        self.driver.find_element_by_class_name('yellow').click()
        # print self.driver.find_element_by_class_name("mint-toast").text

        # 进入系统按钮[目的验证登录失败]
        self.assertTrue(PF.login_fail(self.driver), u'测试异常登录，出错')
        print('异常登录测试，正常')
        login_button = self.driver.find_element_by_class_name("yellow").text
        self.assertEqual(login_button, u'进入系统', u'账号密码为空登录异常')
        print('账号密码为空，登录失败测试，正常')

        time.sleep(1)

        #账号不为空，密码为空
        username = config.TEST_BRAND_ACCOUNT[0]
        password = config.TEST_BRAND_ACCOUNT[1]
        username_input = self.driver.find_elements_by_tag_name('input')[0]
        password_input = self.driver.find_elements_by_tag_name('input')[1]

        username_input.send_keys(username)
        self.driver.find_element_by_class_name('yellow').click()
        # 验证登录失败
        self.assertTrue(PF.login_fail(self.driver),u'测试异常登录，出错')
        print('账号不为空，密码为空-登录测试，正常')
        login_button = self.driver.find_element_by_class_name("yellow").text
        self.assertEqual(login_button, u'进入系统', u'账号不为空，密码为空,出现异常')
        print('账号不为空，密码为空-登录测试，正常')
        time.sleep(1)
        # 账号不为空，密码少于6
        password_input.send_keys('12345')
        self.driver.find_element_by_class_name('yellow').click()
        # 验证登录失败
        time.sleep(2)
        self.assertTrue(PF.login_fail(self.driver), u'测试异常登录，出错')
        print('账号不为空，密码少于6-登录测试，正常')
        login_button = self.driver.find_element_by_class_name("yellow").text
        self.assertEqual(login_button, u'进入系统', u'账号不为空，密码少于6，登录异常')
        print('账号不为空，密码少于6-登录测试，正常')
        time.sleep(1)
        #账号不存在
        username_input.clear()
        username_input.send_keys('dinghuohui110')
        password_input.clear()
        password_input.send_keys('abcd1234')
        self.driver.find_element_by_class_name('yellow').click()
        # 验证登录失败
        time.sleep(2)
        self.assertTrue(PF.login_fail(self.driver), u'测试异常登录，出错')
        print('账号不存在-登录测试，正常')

        login_button = self.driver.find_element_by_class_name("yellow").text
        self.assertEqual(login_button, u'进入系统', u'账号不存在，登录异常')
        print('账号不存在-登录测试，正常')
        time.sleep(1)

        #账号存在，密码错误
        username_input.clear()
        username_input.send_keys(config.TEST_BRAND_ACCOUNT[0])
        password_input.clear()
        password_input.send_keys('abcd1234')
        #验证登录失败
        time.sleep(2)
        self.assertTrue(PF.login_fail(self.driver), u'测试异常登录，出错')
        print('账号存在，密码错误-登录测试，正常')
        login_button = self.driver.find_element_by_class_name("yellow").text
        self.assertEqual(login_button, u'进入系统', u'账号存在，密码错误')
        print('账号存在，密码错误-登录测试，正常')
        time.sleep(1)

    @Public.ErrorHandle
    def test_03(self):
        '''[ipad 登录]登录账号-账号密码正确'''
        print('登录账号')
        username = config.TEST_PERSONAL_ACCOUNT[0]
        password = config.TEST_PERSONAL_ACCOUNT[1]
        time.sleep(3)
        select = self.driver.find_element_by_xpath('//*[@id="bg"]/div/div/div/div[2]/form/div[1]/span/select')
        select.click()
        select.find_elements_by_tag_name('option')[1].click()#订货会为不确定性值，需维护性修改
        username_input = self.driver.find_elements_by_tag_name('input')[0]
        password_input = self.driver.find_elements_by_tag_name('input')[1]

        username_input.send_keys(username)
        password_input.send_keys(password)

        self.driver.find_element_by_class_name('yellow').click()
        element = WebDriverWait(self.driver,25).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#mainHeader > div.pull-left.name-wrapper > div.ovh")))
        # self.assertIn("8001",element.text.encode('utf-8'))
        self.assertIn(config.TEST_PERSONAL_ACCOUNT[2],element.text)
        print('账号登录后，界面显示账号正确')
        self.assertIn(u"退出",element.text)
        time.sleep(2)
        self.assertTrue(PF.login_success(self.driver),u'登录失败')
        print('登录正确账号密码测试-正常')

        # login_cookies=self.driver.get_cookies()
        # 退出账号
        self.driver.find_element_by_css_selector("#mainHeader > div.pull-left.name-wrapper > div.ovh").click()
        time.sleep(2)
        # logout_cookies = self.driver.get_cookies()
        self.assertTrue(PF.login_fail(self.driver),u'退出失败')
        print('退出账号正常')
    @Public.ErrorHandle
    def test_04(self):
        '''[ipad 登录]品牌经纪人-异常场景登录-'''
        time.sleep(2)
        self.driver.find_element_by_class_name('pull-right').click()
        # 账号密码为空
        time.sleep(2)
        select = self.driver.find_element_by_xpath('//*[@id="bg"]/div/div/div/div[2]/form/div[1]/span/select')
        select.click()
        select.find_elements_by_tag_name('option')[1].click()  # 考虑可维护性
        self.driver.find_element_by_class_name('yellow').click()
        # print self.driver.find_element_by_class_name("mint-toast").text

        # 进入系统按钮[目的验证登录失败]
        self.assertTrue(PF.login_fail(self.driver), u'测试异常登录，出错')
        login_button = self.driver.find_element_by_class_name("yellow").text
        self.assertEqual(login_button, u'进入系统', u'账号密码为空登录异常')
        print('品牌经济人-账号密码为空登录测试-pass')
        time.sleep(1)

        # 账号不为空，密码为空
        username = config.TEST_BRAND_ACCOUNT[0]
        password = config.TEST_BRAND_ACCOUNT[1]
        username_input = self.driver.find_elements_by_tag_name('input')[0]
        password_input = self.driver.find_elements_by_tag_name('input')[1]

        username_input.send_keys(username)
        self.driver.find_element_by_class_name('yellow').click()
        # 验证登录失败
        self.assertTrue(PF.login_fail(self.driver), u'测试异常登录，出错')
        print('品牌经济人-账号不为空，密码为空登录测试-pass')

        login_button = self.driver.find_element_by_class_name("yellow").text
        self.assertEqual(login_button, u'进入系统', u'账号不为空，密码为空,出现异常')
        time.sleep(1)
        # 账号不为空，密码少于6
        password_input.send_keys('12345')
        self.driver.find_element_by_class_name('yellow').click()
        # 验证登录失败
        time.sleep(2)
        self.assertTrue(PF.login_fail(self.driver), u'测试异常登录，出错')
        login_button = self.driver.find_element_by_class_name("yellow").text
        self.assertEqual(login_button, u'进入系统', u'账号不为空，密码少于6，登录异常')
        print('品牌经济人-账号不为空，密码少于6登录测试-pass')
        time.sleep(1)

        # 账号不存在
        username_input.clear()
        username_input.send_keys('dinghuohui110')
        password_input.clear()
        password_input.send_keys('abcd1234')
        self.driver.find_element_by_class_name('yellow').click()
        # 验证登录失败
        time.sleep(2)
        self.assertTrue(PF.login_fail(self.driver), u'测试异常登录，出错')
        login_button = self.driver.find_element_by_class_name("yellow").text
        self.assertEqual(login_button, u'进入系统', u'账号不存在，登录异常')
        print('品牌经济人-账号不存在登录测试-pass')
        time.sleep(1)

        # 账号存在，密码错误
        username_input.clear()
        username_input.send_keys(config.TEST_BRAND_ACCOUNT[0])
        password_input.clear()
        password_input.send_keys('abcd1234')

        # 验证登录失败
        time.sleep(2)
        self.assertTrue(PF.login_fail(self.driver), u'测试异常登录，出错')
        login_button = self.driver.find_element_by_class_name("yellow").text
        self.assertEqual(login_button, u'进入系统', u'账号存在，密码错误')
        print('品牌经济人-账号存在，密码错误登录测试-pass')
        time.sleep(1)

    @Public.ErrorHandle
    def test_05(self):
        '''[ipad 登录]登录品牌账号-账号密码正确'''
        print('登录账号')
        time.sleep(2)
        self.driver.find_element_by_class_name('pull-right').click()
        username = config.TEST_BRAND_ACCOUNT[0]
        password = config.TEST_BRAND_ACCOUNT[1]
        time.sleep(3)
        select = self.driver.find_element_by_xpath('//*[@id="bg"]/div/div/div/div[2]/form/div[1]/span/select')
        select.click()
        select.find_elements_by_tag_name('option')[1].click()  # 订货会为不确定性值，需维护性修改
        username_input = self.driver.find_elements_by_tag_name('input')[0]
        password_input = self.driver.find_elements_by_tag_name('input')[1]

        username_input.send_keys(username)
        password_input.send_keys(password)

        self.driver.find_element_by_class_name('yellow').click()
        element = WebDriverWait(self.driver, 25).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainHeader > div.pull-left.name-wrapper > div.ovh")))
        self.assertIn(config.TEST_BRAND_ACCOUNT[2], element.text)
        print('登录后，验证界面是否有经纪人账号-pass')
        self.assertIn(u"退出", element.text)
        time.sleep(2)
        self.assertTrue(PF.login_success(self.driver), u'登录失败')
        print('登录成功')
        time.sleep(2)
        #验证订单审核，存在侧边栏列表中
        order_eidt = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/ul/li[8]/a')
        self.assertEqual(order_eidt.text.strip(),u'订单审核')
        print('验证品牌经纪人侧边栏存在订单审核功能-pass')

        element = self.driver.find_elements_by_xpath('//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/ul/li')
        #验证u'明星店铺',u'收藏评款',u'异常订单'，不存在侧边栏列表中
        side_tag = [u'明星店铺',u'收藏评款',u'异常订单']
        for tag in side_tag:
            for e in element:
                if e.text.strip() in side_tag:
                    self.assertTrue(False,tag+u',存在品牌经纪人侧边栏列表中')
        print('验证品牌经纪人侧边栏没有-明显店铺、收藏评款、异常订单-pass')

        # login_cookies=self.driver.get_cookies()
        #退出账号
        self.driver.find_element_by_css_selector("#mainHeader > div.pull-left.name-wrapper > div.ovh > a").click()
        time.sleep(2)
        # logout_cookies = self.driver.get_cookies()
        self.assertTrue(PF.login_fail(self.driver), '退出失败')




