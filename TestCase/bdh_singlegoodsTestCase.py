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
from selenium.webdriver.support.ui import Select
from selenium import webdriver
import config
import profileapi as PF
import Public

'''
    必订火测试版本登录页面
    http://a.bdh.com/login?isInit=1
'''

class singlegoods(unittest.TestCase):

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
        cls.Options.add_argument('lang=zh_CN.UTF-8')
        cls.Options.binary_location = broswer_path  # 浏览器路径，不指定的话会自动查找Chrome 路径，如果Chrome安装的话
        # 启动chrome
        cls.driver = Chrome(chrome_options=cls.Options, executable_path=cls.driver_path,
                             port=9151)  # 启动chromedriver，根据浏览器路径启动浏览器
    @classmethod
    def tearDownClass(cls):
        print "End:",time.ctime(time.time()),'\n'
        cls.driver.close()

    def setUp(self):

        self.driver.set_window_size(self.width, self.height)
        self.url = "http://a.bdh.com/main/ordering/singal"
        self.driver.get(self.url)
        while True:
            time.sleep(1)
            if PF.login_fail(self.driver):
                PF.login(self.driver)
                break
            elif PF.login_success(self.driver):
                break
            else:
                break
        self.driver.implicitly_wait(30)

    def tearDown(self):
        pass

    @Public.ErrorHandle
    def test_01(self):
        '''[ipad-单款订货页面]默认主界面，单款订货界面，主框架元素验证'''
        time.sleep(1)
        #检查退出按钮
        self.assertEqual(self.driver.find_element_by_xpath('//*[@id="mainHeader"]/div[1]/div[2]/a').text,
                        u'退出','退出按钮')
        #检查用户图标
        self.assertTrue(self.driver.find_element_by_class_name('userpic').is_displayed(),u'用户默认图标异常')
        self.assertTrue(self.driver.find_element_by_class_name('searchInput').is_displayed(),u'用户默认图标异常')
        #检查已订件数、订单金额、折扣金额

        self.assertTrue(self.driver.find_element_by_css_selector('#mainHeader > div.header-right.ovh > img').is_displayed())
        need_data = PF.homepage_data()
        total,discount,order_money = need_data['data']['total_number'], need_data['data']['discount'], need_data['data']['order_money']
        headertext = self.driver.find_element_by_class_name('header-right').text.strip()
        self.assertIn(u'已订',headertext)
        self.assertIn(u'件',headertext)
        self.assertIn(u'折后金额',headertext)
        s = []
        for v in headertext.split(' '):
            if v:
                s.append(v)
        # print(s[1],s[3],s[5])
        self.assertEqual(str(total).strip(),s[1],u'订单量显示数目异常')
        self.assertEqual(int(order_money),int(s[3].encode('utf-8').replace('¥','').replace(',','')[:-3]),u'订单金额总量异常')
        self.assertEqual(int(discount),int(s[5].encode('utf-8').replace('¥','').replace(',','')[:-3]),u'折扣价格异常')

        #检查搜索框
        search = self.driver.find_element_by_class_name('searchInput').find_element_by_tag_name('input')
        self.assertEqual(search.get_attribute('placeholder'),u'搜索款号/圆牌号')
        #检查轻松订货
        self.assertEqual(self.driver.find_element_by_class_name('tit').text,u'轻松订货')
        #检查单款订货
        dankuan = self.driver.find_element_by_class_name('router-link-active')
        self.assertTrue(dankuan.is_displayed())
        self.assertEqual(dankuan.text,u'单款订货',u'单款订货异常')
        # 检查搭配订货
        dapei = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/ul/li[3]/a')
        self.assertTrue(dapei.is_displayed())
        self.assertEqual(dapei.text, u'搭配订货', '搭配订货')
        # 检查360推演
        tuiyan = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/ul/li[4]/a')
        self.assertTrue(tuiyan.is_displayed())
        self.assertEqual(tuiyan.text, u'360推演', '360推演')
        # 检查推送订货
        tuisong = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/ul/li[5]/a')
        self.assertTrue(tuisong.is_displayed())
        self.assertEqual(tuisong.text, u'推送订货')
        # 检查陈列订货
        chenlie = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/ul/li[6]/a')
        self.assertTrue(chenlie.is_displayed())
        self.assertEqual(chenlie.text, u'陈列订货')
        #检查订货分析
        ddfenxi = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/ul/li[7]')
        self.assertTrue(ddfenxi.is_displayed())
        self.assertEqual(ddfenxi.text.strip(), u'订货分析')
        # 检查订货排名
        dhpm = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/ul/li[8]/a')
        self.assertTrue(dhpm.is_displayed())
        self.assertEqual(dhpm.text.strip(), u'订货排名')
        # 检查我的订单
        wddd = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/ul/li[9]/a')
        self.assertTrue(wddd.is_displayed())
        self.assertEqual(wddd.text.strip(), u'我的订单')
        # 检查指标达成
        zbdc = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/ul/li[11]/a')
        self.assertTrue(zbdc.is_displayed())
        self.assertEqual(zbdc.text.strip(), u'指标达成')
        # 检查订量汇总
        dlhz = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/ul/li[12]/a')
        self.assertTrue(dlhz.is_displayed())
        self.assertEqual(dlhz.text.strip(), u'订量汇总')

        # 检查更多功能
        gdgn = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/ul/li[13]')
        self.assertTrue(gdgn.is_displayed())
        self.assertEqual(gdgn.text.strip(), u'更多功能')

        # 检查明星店铺
        mxdp = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/ul/li[14]/a')
        self.assertTrue(mxdp.is_displayed())
        self.assertEqual(mxdp.text.strip(), u'明星店铺')
        # 检查企划介绍
        qhjs = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/ul/li[15]/a')
        self.assertTrue(qhjs.is_displayed())
        self.assertEqual(qhjs.text.strip(), u'企划介绍')
        # 检查收藏评款
        scpk = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/ul/li[16]/a')
        self.assertTrue(scpk.is_displayed())
        self.assertEqual(scpk.text.strip(), u'收藏评款')
        # 检查异常订单
        ycdd = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/ul/li[17]/a')
        self.assertTrue(ycdd.is_displayed())
        self.assertEqual(ycdd.text.strip(), u'异常订单')
        

    @Public.ErrorHandle
    def test_02(self):
        '''[ipad-单款订货页面]广播轮播信息验证,待定'''
        time.sleep(1)
        #广播测试
        # notic = self.driver.find_element_by_class_name('notic')
        # self.assertTrue(notic.find_element_by_tag_name('img').is_displayed())

    @Public.ErrorHandle
    def test_03(self):
        '''[ipad-单款订货页面]单款订货页面-商品显示检查'''
        #获取服务器品牌商的订货会中商品列表的json文件数据
        data = PF.list_data()
        if not data:
            self.assertTrue(False,'获取商品列表json数据异常')
        goods_list =data['data']
        c = 0
        # print(goods_list)
        for list in goods_list:
            cardno = list['card_no']#圆牌号
            image = list['default_image']#商品图片
            goodsno = list['goods_no']#商品款号
            price = list['meeting_price']#商品价格
            total_money = list['order_money']#商品订单总金额
            total = list['total_number']#商品订单总数
            title = list['title']#商品名称或标题

            #定位圆牌号、图片、款号、标题、价格、订单总数、总订金额
            cmp_cardno = self.driver.find_element_by_xpath('//*[@id="leftMain"]/div/div[2]/div/ul/li[%s]/div/span'%(c+1))
            cmp_image = self.driver.find_element_by_xpath('//*[@id="leftMain"]/div/div[2]/div/ul/li[%s]/div/div[1]/img[2]'%(c+1))
            cmp_goodsno = self.driver.find_element_by_xpath('//*[@id="leftMain"]/div/div[2]/div/ul/li[%s]/div/div[2]/p[2]/span'%(c+1))
            cmp_title = self.driver.find_element_by_xpath('//*[@id="leftMain"]/div/div[2]/div/ul/li[%s]/div/div[2]/p[2]'%(c+1))
            cmp_price = self.driver.find_element_by_xpath('//*[@id="leftMain"]/div/div[2]/div/ul/li[%s]/div/div[2]/p[1]'%(c+1))
            cmp_total = self.driver.find_element_by_xpath('//*[@id="leftMain"]/div/div[2]/div/ul/li[%s]/div/div[2]/p[3]'%(c+1))
            cmp_total_money = self.driver.find_element_by_xpath('//*[@id="leftMain"]/div/div[2]/div/ul/li[%s]/div/div[2]/p[4]'%(c+1))

            #将界面信息与json进行对比验证
            self.assertEqual(cmp_cardno.text.strip(), cardno, u'商品圆牌号异常')
            self.assertEqual(cmp_goodsno.text.strip(),goodsno,u'款号异常')
            self.assertEqual(cmp_title.text.split(' ')[0].split('\n')[0],title.strip(),u'商品标题异常')

            self.assertEqual(cmp_price.text.replace(u'¥ ',''),price,u'商品价格异常'+cardno)
            self.assertEqual(cmp_total.text,u'订货数量：'+str(total)+u'件',u'订货数量异常'+cardno)
            if total_money== 0:
                total_money = '0.00'
            self.assertEqual(cmp_total_money.text.strip().replace(',',''),u'订货金额： ¥'+str(total_money),u'订货金额异常'+cardno)

            if image:
                #检查获取的json图片链接是否正常访问
                self.assertEqual(200,requests.get(image).status_code,u'该图片链接无法访问'+cardno)
                #获取页面该商品的图片链接
                get_img = re.search(r'http:(.+?).png',cmp_image.get_attribute('src'))
                if get_img:
                    self.assertEqual(get_img.group(0),image, u'商品展示图片异常'+cardno)
                else:
                    get_img = re.search(r'http:(.+?).jpeg',cmp_image.get_attribute('src'))
                    if get_img:
                        self.assertEqual(get_img.group(0),image, u'商品展示图片异常'+cardno)
            else:
                #商品没有添加图片时，验证默认图片是否正常显示
                self.assertEqual(config.DEFAULT_IMG,cmp_image.get_attribute('src'),u'该商品图片异常'+cardno)
            c+=1


    @Public.ErrorHandle
    def test_04(self):
        '''[ipad-单款订货页面]筛选功能-检查'''
        data = PF.dh_bar()
        if not data:
            self.assertTrue(False, '获取筛选json数据异常')
        #获取品牌种类
        brands = data['brand'][0]['values']
        if brands:
            c = 0
            #定位品牌下拉按钮
            pingpai = self.driver.find_element_by_xpath('//*[@id="leftMain"]/div/div[1]/div/div/div[1]/button')
            self.assertEqual(pingpai.text.strip(), u'品牌', u'品牌显示')
            pingpai.click()#点击品牌
            #遍历校验筛选栏品牌信息
            for bd in brands:
                time.sleep(1)
                brand = self.driver.find_element_by_xpath('//*[starts-with(@id,"kxSelect_beauty_ul_")]/ul/li[%s]/p'%str(c+2))
                self.assertEqual(brand.text.strip(),bd['name'],u'品牌名显示出错')
                c+=1
            pingpai.click()#收回品牌筛选
        #季节
        season = data['attribute'][2]['values']
        if season:
            c = 0
            #定位季节
            jijie = self.driver.find_element_by_xpath('//*[@id="leftMain"]/div/div[1]/div/div/span[1]/div/button')
            jijie.click()#点击季节
            time.sleep(1)
            ele = self.driver.find_elements_by_xpath('//div[starts-with(@id,"kxSelect_beauty_ul_")]')
            #遍历校验季节信息
            for s in season:
                ss = ele[4].find_elements_by_tag_name('li')[c+1]
                self.assertEqual(ss.text.strip(),s,u'季节出错')
                c+=1
            jijie.click()#收回季节筛选
        #波段
        boduan = data['attribute'][1]['values']
        if boduan:
            c = 0
            #定位波段筛选栏
            boduan_ele = self.driver.find_element_by_xpath('//*[@id="leftMain"]/div/div[1]/div/div/span[2]/div/button')
            boduan_ele.click()
            time.sleep(1)
            ele = self.driver.find_elements_by_xpath('//div[starts-with(@id,"kxSelect_beauty_ul_")]')
            #遍历校验波段信息
            for b in boduan:
                # ele = self.driver.find_element_by_xpath('//*[starts-with(@id,"kxSelect_beauty_ul_")]/ul/li[%s]/p'%(c+2))
                bb = ele[5].find_elements_by_tag_name('li')[c + 1]
                self.assertEqual(bb.text.strip(),b,u'波段异常')
                c+=1
            boduan_ele.click()
        #年份
        year = data['attribute'][3]['values']
        if year:
            c=0
            #定位年份筛选栏
            year_ele = self.driver.find_element_by_xpath('//*[@id="leftMain"]/div/div[1]/div/div/span[3]/div/button')
            year_ele.click()
            time.sleep(1)
            ele = self.driver.find_elements_by_xpath('//div[starts-with(@id,"kxSelect_beauty_ul_")]')
            #遍历校验年份信息
            for y in year:
                yy = ele[6].find_elements_by_tag_name('li')[c + 1]
                # ele = self.driver.find_element_by_xpath('//*[starts-with(@id,"kxSelect_beauty_ul_")]/ul/li[%s]/p'%(c+2))
                self.assertEqual(yy.text.strip(),y,u'年份信息异常')
                c+=1
            year_ele.click()
        #款式类型
        style = data['attribute'][0]['values']
        if style:
            c=0
            #定位款式类型
            style_ele = self.driver.find_element_by_xpath('//*[@id="leftMain"]/div/div[1]/div/div/span[4]/div/button')
            style_ele.click()
            time.sleep(1)
            ele = self.driver.find_elements_by_xpath('//div[starts-with(@id,"kxSelect_beauty_ul_")]')
            #遍历校验款式
            for k in style:
                ks = ele[7].find_elements_by_tag_name('li')[c + 1]
                self.assertEqual(ks.text.strip(),k,u'款式信息出错')
                c+=1
            style_ele.click()

    @Public.ErrorHandle
    def test_05(self):
        '''[ipad-单款订货页面],页面上拉数据显示正常,待定'''
        pass

    @Public.ErrorHandle
    def test_06(self):
        '''[ipad-单款订货页面],搜索功能检查'''
        # 测试数据-搜索关键词,空格、完整圆牌号、部分连续圆牌号
        goodsno = ['  ', '185','18' ]
        # 完整款号、部分连续款号
        cardno = ['E8Z03BS185','E8Z']
        # 圆牌号和款号存在相同字段、无商品关键词
        words = ['185','99999']

        keywords = goodsno
        #---输入空格字符，搜索----
        self.driver.find_element_by_xpath('//*[@id="indexMainSearchInput"]').send_keys(keywords[0])# 输入关键词
        time.sleep(1)
        search_button = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[3]/div[1]/div/form/button')
        search_button.click()  # 点击搜索按钮
        PF.search_assert(self, keywords[0])

        #----输入完整圆牌号----
        self.driver.find_element_by_xpath('//*[@id="indexMainSearchInput"]').clear()
        self.driver.find_element_by_xpath('//*[@id="indexMainSearchInput"]').send_keys(keywords[1])#输入关键词
        time.sleep(1)
        search_button = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[3]/div[1]/div/form/button')
        search_button.click()#点击搜索按钮
        PF.search_assert(self,keywords[1])

        # ----输入部分连续的圆牌号----
        self.driver.find_element_by_xpath('//*[@id="indexMainSearchInput"]').clear()
        self.driver.find_element_by_xpath('//*[@id="indexMainSearchInput"]').send_keys(keywords[2])
        time.sleep(1)
        search_button = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[3]/div[1]/div/form/button')
        search_button.click()  # 点击搜索按钮
        PF.search_assert(self, keywords[2])

        # ----输入完整款号----
        keywords = cardno
        self.driver.find_element_by_xpath('//*[@id="indexMainSearchInput"]').clear()
        self.driver.find_element_by_xpath('//*[@id="indexMainSearchInput"]').send_keys(keywords[0])
        time.sleep(1)
        search_button = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[3]/div[1]/div/form/button')
        search_button.click()  # 点击搜索按钮
        PF.search_assert(self, keywords[0])

        # ----输入部分连续款号----
        keywords = cardno
        self.driver.find_element_by_xpath('//*[@id="indexMainSearchInput"]').clear()
        self.driver.find_element_by_xpath('//*[@id="indexMainSearchInput"]').send_keys(keywords[1])
        time.sleep(1)
        search_button = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[3]/div[1]/div/form/button')
        search_button.click()  # 点击搜索按钮
        PF.search_assert(self, keywords[1])

        # ----输入圆牌号和款号存在相同字段----
        keywords = words
        self.driver.find_element_by_xpath('//*[@id="indexMainSearchInput"]').clear()
        self.driver.find_element_by_xpath('//*[@id="indexMainSearchInput"]').send_keys(keywords[0])
        time.sleep(1)
        search_button = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[3]/div[1]/div/form/button')
        search_button.click()  # 点击搜索按钮
        PF.search_assert(self, keywords[0])

        # ----输入无商品关键词---
        self.driver.find_element_by_xpath('//*[@id="indexMainSearchInput"]').clear()
        self.driver.find_element_by_xpath('//*[@id="indexMainSearchInput"]').send_keys(keywords[1])
        time.sleep(1)
        search_button = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[3]/div[1]/div/form/button')
        search_button.click()  # 点击搜索按钮
        PF.search_assert(self, keywords[1])

    @Public.ErrorHandle
    def test_07(self):
        '''[ipad-单款订货页面]筛选功能，全选/取消[季节、波段、年份、款式类型]'''

        #筛选-季节-全选/取消
        jijie_select_button = self.driver.find_element_by_xpath('//*[@id="leftMain"]/div/div[1]/div/div/span[1]/div/button')
        jijie_select_list = self.driver.find_elements_by_xpath('//div[starts-with(@id,"kxSelect_beauty_ul_")]')[4]
        PF.select_assert(self,jijie_select_button,jijie_select_list)
        print('季节筛选-全选取消功能正常')
        # 筛选-波段-全选/取消
        boduan_select_button = self.driver.find_element_by_xpath('//*[@id="leftMain"]/div/div[1]/div/div/span[2]/div/button')
        boduan_select_list = self.driver.find_elements_by_xpath('//div[starts-with(@id,"kxSelect_beauty_ul_")]')[5]
        PF.select_assert(self,boduan_select_button,boduan_select_list)
        print('波段筛选-全选取消功能正常')

        # 筛选-年份-全选/取消
        year_select_button = self.driver.find_element_by_xpath(
            '//*[@id="leftMain"]/div/div[1]/div/div/span[3]/div/button')
        year_select_list = self.driver.find_elements_by_xpath('//div[starts-with(@id,"kxSelect_beauty_ul_")]')[6]
        PF.select_assert(self, year_select_button, year_select_list)
        print('年份筛选-全选取消功能正常')

        # 筛选-款式-全选/取消
        style_select_button = self.driver.find_element_by_xpath(
            '//*[@id="leftMain"]/div/div[1]/div/div/span[4]/div/button')
        style_select_list = self.driver.find_elements_by_xpath('//div[starts-with(@id,"kxSelect_beauty_ul_")]')[7]
        PF.select_assert(self, style_select_button, style_select_list)
        print('款式筛选-全选取消功能正常')

    def test_08(self):
        '''[ipad-单款订货页面]筛选功能，单个筛选检查[季节，波段，年份，款式]'''

        #循环遍历季节，波段，年份，款式
        for i in range(4):
            select_button = self.driver.find_element_by_xpath(
                '//*[@id="leftMain"]/div/div[1]/div/div/span[%s]/div/button'%(i+1))
            select_list = self.driver.find_elements_by_xpath('//div[starts-with(@id,"kxSelect_beauty_ul_")]')[i+4]
            PF.single_select_assert(self,select_button,select_list)

    def test_09(self):
        '''[ipad-单款订货页面]筛选功能，单个筛选检查[是否已订]'''
        select_button = self.driver.find_element_by_xpath('//*[@id="leftMain"]/div/div[1]/div/div/div[5]/button')
        select_list = self.driver.find_elements_by_xpath('//div[starts-with(@id,"kxSelect_beauty_ul_")]')[8]
        select_button.click()
        time.sleep(1)
        select_list.find_elements_by_tag_name('li')[1].click()
        time.sleep(2)
        #筛选结果列表
        list_goods = self.driver.find_elements_by_xpath('//*[@id="leftMain"]/div/div[2]/div/ul/li')
        for ele in list_goods:
            order_number = filter(str.isdigit,ele.find_element_by_xpath('//div/div[2]/p[3]').text.encode('utf-8'))
            self.assertNotEqual(order_number,u'0')

    def test_10(self):
        '''[ipad-单款订货页面] 排序功能[波段从小到大、...、订额从大到小]'''
        time.sleep(2)
        sort_button = self.driver.find_element_by_xpath('//*[@id="leftMain"]/div/div[1]/div/div/div[6]/button')
        sort_list = self.driver.find_elements_by_xpath('//div[starts-with(@id,"kxSelect_beauty_ul_")]')[9]
        #波段从小到大
        sort_button.click()
        sort_list.find_elements_by_tag_name('li')[0].click()
        time.sleep(1)
        data = PF.sort_list_data([],{"boduan":"0"})
        boduan = []
        c = 0
        for list in data['data']:
            PF.inspect_goods(self,list,c)
            c+=1
            boduan.append(list['boduan'])
        self.assertEqual(sorted(boduan),boduan,'波段从小到大排序出问题')

        # 波段从大到小
        sort_button.click()
        sort_list.find_elements_by_tag_name('li')[1].click()
        time.sleep(1)
        data = PF.sort_list_data([], {"boduan": "1"})

        boduan = []
        c = 0
        for list in data['data']:
            PF.inspect_goods(self, list, c)
            c += 1
            boduan.append(list['boduan'])
        self.assertEqual(sorted(boduan,reverse=True), boduan, '波段从大到小排序出问题')

        #圆牌号从小到大
        sort_button.click()
        sort_list.find_elements_by_tag_name('li')[2].click()
        time.sleep(1)
        data = PF.sort_list_data([], {"card_no": "0"})

        cardno = []
        c = 0
        for list in data['data']:
            PF.inspect_goods(self, list, c)
            c += 1
            cardno.append(list['card_no'])
        self.assertEqual(sorted(cardno, reverse=False), cardno, '圆牌号从小到大排序出问题')

        # 圆牌号从大到小
        sort_button.click()
        sort_list.find_elements_by_tag_name('li')[3].click()
        time.sleep(1)
        data = PF.sort_list_data([], {"card_no": "1"})
        cardno = []
        c = 0
        for list in data['data']:
            PF.inspect_goods(self, list, c)
            c += 1
            cardno.append(list['card_no'])
        print(sorted(cardno, reverse=True))
        cardno = [int(j) for j in [i.encode('utf-8') for i in cardno]]#将列表数据变成int类型
        self.assertEqual(sorted(cardno, reverse=True), cardno, '圆牌号从大到小排序出问题')
        # 订量从小到大
        sort_button.click()
        sort_list.find_elements_by_tag_name('li')[4].click()
        time.sleep(1)
        data = PF.sort_list_data([], {"total_number": "0"})
        totalnumber = []
        c = 0
        for list in data['data']:
            PF.inspect_goods(self, list, c)
            c += 1
            totalnumber.append(list['total_number'])

        self.assertEqual(sorted(totalnumber, reverse=False), totalnumber, '订量从小到大排序出问题')

        # 订量从大到小
        sort_button.click()
        sort_list.find_elements_by_tag_name('li')[5].click()
        time.sleep(1)
        data = PF.sort_list_data([], {"total_number": "1"})
        totalnumber = []
        c = 0
        for list in data['data']:
            PF.inspect_goods(self, list, c)
            c += 1
            if list['total_number']:
                totalnumber.append(list['total_number'])
        totalnumber = [int(j) for j in [i.encode('utf-8') for i in totalnumber]]#将列表数据变成int类型
        self.assertEqual(sorted(totalnumber, reverse=True), totalnumber, '订量从大到小排序出问题')

        # 订额从小到大
        sort_button.click()
        sort_list.find_elements_by_tag_name('li')[6].click()
        time.sleep(1)
        data = PF.sort_list_data([], {"order_money": "0"})
        order_money = []
        c = 0
        for list in data['data']:
            PF.inspect_goods(self, list, c)
            c += 1
            if list['order_money']:
                order_money.append(list['order_money'])
        # order_money =[i.encode('utf-8') for i in order_money]#将列表数据变成int类型
        # self.assertEqual(sorted(order_money, reverse=False), order_money, '订额从小到大排序出问题')

        # 订额从大到小
        sort_button.click()
        sort_list.find_elements_by_tag_name('li')[7].click()
        time.sleep(1)
        data = PF.sort_list_data([], {"order_money": "1"})
        order_money = []
        c = 0
        for list in data['data']:
            PF.inspect_goods(self, list, c)
            c += 1
            if list['order_money']:
                order_money.append(list['order_money'])
        # order_money = [i.encode('utf-8') for i in order_money]
        # self.assertEqual(sorted(order_money, reverse=True), order_money, '订额从大到小排序出问题')

    def test_11(self):
        '''[ipad-单款订货页面] 商品详情页面'''
        goodsno = config.GOODS_NO[0]
        goodsinfo = PF.get_goods_detail(goodsno)

        #搜索框
        self.driver.find_element_by_id('indexMainSearchInput').send_keys(goodsno)
        #搜索按钮
        search_bt = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div[3]/div[1]/div/form/button')
        search_bt.click()
        time.sleep(1)
        #点击商品
        self.driver.find_element_by_xpath('//*[@id="leftMain"]/div/div[2]/div/ul/li/div/div[1]').click()
        time.sleep(1)
        #搜索框
        goods_page_search_input = self.driver.find_element_by_xpath('//*[@id="dialogParent"]/div/div[3]/form[1]/div/input')
        self.assertTrue(goods_page_search_input.is_displayed(),'商品页面搜索框显示异常')
        self.assertEqual(goods_page_search_input.get_attribute('placeholder'),u'搜索款号')
        #搜索按钮
        goods_page_search_bt = self.driver.find_element_by_xpath('//*[@id="dialogParent"]/div/div[3]/form[1]/div/button')
        self.assertTrue(goods_page_search_bt.is_displayed(),'搜索按钮异常')
        self.assertEqual(goods_page_search_bt.text,u'搜索')
        #上一款，下一款
        pre = self.driver.find_elements_by_class_name('prev')[0]
        next = self.driver.find_elements_by_class_name('next')[0]
        self.assertEqual(pre.text,u'上一款')
        self.assertEqual(next.text,u'下一款')
        #关闭按钮
        close_button = self.driver.find_element_by_xpath('//*[@id="dialogParent"]/div/div[3]/i')
        self.assertTrue(close_button.is_displayed(),'关闭按钮异常')
        #商品价格
        price = self.driver.find_elements_by_class_name('group')[0]
        self.assertEqual(price.text.strip(),u'单价： ¥'+goodsinfo['goods']['meeting_price'])
        print('商品价格显示正确')
        #商品圆牌号
        goodcard = self.driver.find_elements_by_class_name('group')[1]
        self.assertEqual(goodcard.text.strip(),u'圆牌号： '+goodsinfo['goods']['card_no'])
        # 商品款号
        goodstyleid = self.driver.find_elements_by_class_name('group')[2]
        self.assertEqual(goodstyleid.text.strip(), u'款号： ' + goodsinfo['goods']['goods_no'])
        #收藏功能
        like = self.driver.find_elements_by_class_name('group')[3]
        self.assertEqual(like.find_element_by_class_name('tit').text.strip(), u'收藏：')
        #属性
        attributes_ele = self.driver.find_elements_by_class_name('group')[4]
        #属性放入list
        attributes = []
        for item in goodsinfo['goods']['attributes'][2:]:
            attributes.append(item['values'])

        #验证元素属性是否存在
        c = 0
        for ele in self.driver.find_elements_by_xpath('//*[@id="dialogContent"]/section[1]/div[2]/div[5]/div/span'):
            self.assertIn(ele.text.strip(),attributes[c],'属性值不存在')
            c+=1

        #订货数量统计
        order_count = self.driver.find_element_by_xpath('//*[@id="dialogContent"]/section[1]/div[2]/div[6]/span')
        self.assertEqual(order_count.text.strip(),u'订货数量：')


