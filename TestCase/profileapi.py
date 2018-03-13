#-*- coding:utf-8 -*-
import config
import requests
import json
import re,time
from time import sleep

'''
必订火封装通用方法
'''
#登录测试账号
def login(driver):
    sleep(1)
    driver.get('http://%s.bdh.com/login'%config.BRAND_BUSINESS)
    username = config.TEST_PERSONAL_ACCOUNT[0]
    password = config.TEST_PERSONAL_ACCOUNT[1]
    sleep(3)
    select = driver.find_element_by_xpath('//*[@id="bg"]/div/div/div/div[2]/form/div[1]/span/select')
    select.click()
    select.find_elements_by_tag_name('option')[1].click()  # 订货会为不确定性值，需维护性修改
    username_input = driver.find_elements_by_tag_name('input')[0]
    password_input = driver.find_elements_by_tag_name('input')[1]
    username_input.send_keys(username)
    password_input.send_keys(password)
    driver.find_element_by_class_name('yellow').click()
    count = 0
    while True:
        if login_success(driver):
            print('登录成功')
            return driver.get_cookies()
        count+=1
        if count>30:
            assert False,'登录失败'
        sleep(1)

#登录成功
def login_success(driver,*args):

    url = 'http://%s.bdh.com/main'%config.BRAND_BUSINESS
    if config.USER_MAINPAGE_URL==driver.current_url:
        return True
    elif url in driver.current_url:
        return True
    else:
        return False

#登录失败
def login_fail(drvier,*args):
    url = "http://%s.bdh.com/login"%config.BRAND_BUSINESS
    if config.USER_LOGINPAGE_URL == drvier.current_url:
        return True
    elif url == drvier.current_url:
        return True
    else:
        return False

#获取homepage页面json数据
def homepage_data():
    url = config.HOMEPAGE_JSON_URL
    headers = {
        'Host':'a.bdh.com',
        'Accept':'application/json, text/plain, */*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Content-Length':'15',
        'Content-Type':'application/json;charset=UTF-8',
        'Cookie':'laravel_session=J3Ua8LgFuNFe5J643j8nbhTvhthIS0KX3qj8cDQL',
        'Origin':'http://a.bdh.com',
        'Referer':'http://a.bdh.com/main/',
        'User-Agent':'Mozilla/5.0 (Linux; Android 4.1.1; GT-N7100 Build/JRO03C) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3'
    }
    data = {
        'is_detail':'0'
    }
    res = requests.post(url,headers=headers,data=data)
    need_data = json.loads(res.content)
    return need_data

#获取单款页面商品列表数据
def list_data():
    url = config.LIST_JSON_URL
    headers = {
        'Host': 'a.bdh.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Length': '140',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': config.USER_COOKIE,
        'Origin': 'http://a.bdh.com',
        'Referer': 'http://a.bdh.com/main/ordering/singal',
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
        'Proxy-Connection':'keep-alive'
    }
    data = {
            "offset": 0,
            "limit": 20,
            "keyword": "",
            "attributes": [],
            "brand_ids": [],
            "category_id": "",
            "category_ids": [],
            "sort": {
                "boduan": "0"
            },
            "is_ordered": ""
        }
    res = requests.post(url, headers=headers,data=json.dumps(data))
    need_data = json.loads(res.content)
    return need_data

#排序结果
def sort_list_data(id,sortby):
    url = config.LIST_JSON_URL
    headers = {
        'Host': 'a.bdh.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Length': '140',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': config.USER_COOKIE,
        'Origin': 'http://a.bdh.com',
        'Referer': 'http://a.bdh.com/main/ordering/singal',
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
        'Proxy-Connection': 'keep-alive'
    }
    data = {
        "offset": 0,
        "limit": 20,
        "keyword": '',
        "attributes": [],
        "brand_ids": [],
        "category_id": "",
        "category_ids": id,
        "sort": sortby,
        "is_ordered": ""
    }
    res = requests.post(url, headers=headers, data=json.dumps(data))
    need_data = json.loads(res.content)
    return need_data




#搜索结果json数据
def search_data(keyword):
    url = config.LIST_JSON_URL
    headers = {
        'Host': 'a.bdh.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Length': '140',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': config.USER_COOKIE,
        'Origin': 'http://a.bdh.com',
        'Referer': 'http://a.bdh.com/main/ordering/singal',
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
        'Proxy-Connection':'keep-alive'
    }
    data = {
            "offset": 0,
            "limit": 20,
            "keyword": keyword,
            "attributes": [],
            "brand_ids": [],
            "category_id": "",
            "category_ids": [],
            "sort": {
                "boduan": "0"
            },
            "is_ordered": ""
        }
    res = requests.post(url, headers=headers,data=json.dumps(data))
    need_data = json.loads(res.content)
    return need_data
#获取商品详情页面信息
def get_goods_detail(goodsno):

    data = search_data(goodsno)['data'][0]
    good_id = data['id']
    good_data = 'http://%s.bdh.com/wapi/goods/info.json?id=%s&goods_no=' % (config.BRAND_BUSINESS, good_id)

    headers = {
        'Host': 'a.bdh.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': config.USER_COOKIE,
        'Origin': 'http://a.bdh.com',
        'Referer': 'http://a.bdh.com/main/ordering/singal',
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
        'Proxy-Connection': 'keep-alive'
    }
    result = requests.get(good_data, headers=headers)
    need_data = json.loads(result.content)
    return need_data
#获取单款页面筛选数据
def dh_bar():
    url = config.DH_BAR
    headers = {
        'Host': 'a.bdh.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Length': '89',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': config.USER_COOKIE,
        'Origin': 'http://a.bdh.com',
        'Referer': 'http://a.bdh.com/main/ordering/singal',
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
        'Proxy-Connection': 'keep-alive'
    }
    data = {
        "meeting_id": "1",
        "select": ["品牌", "分类", "款式类型", "波段", "季节", "年份"]
    }
    res = requests.post(url, headers=headers, data=json.dumps(data))
    need_data = json.loads(res.content)
    # print(need_data['brand'][0]['values'])
    return need_data

#验证单款订货页面单个商品数据显示是否正常
def inspect_goods(self,list,no):

    c = no
    cardno = list['card_no']  # 圆牌号
    image = list['default_image']  # 商品图片
    goodsno = list['goods_no']  # 商品款号
    price = list['meeting_price']  # 商品价格
    total_money = list['order_money']  # 商品订单总金额
    total = list['total_number']  # 商品订单总数
    title = list['title']  # 商品名称或标题
    # 定位圆牌号、图片、款号、标题、价格、订单总数、总订金额
    cmp_cardno = self.driver.find_element_by_xpath('//*[@id="leftMain"]/div/div[2]/div/ul/li[%s]/div/span' % (c + 1))
    cmp_image = self.driver.find_element_by_xpath(
        '//*[@id="leftMain"]/div/div[2]/div/ul/li[%s]/div/div[1]/img[2]' % (c + 1))
    cmp_goodsno = self.driver.find_element_by_xpath(
        '//*[@id="leftMain"]/div/div[2]/div/ul/li[%s]/div/div[2]/p[2]/span' % (c + 1))
    cmp_title = self.driver.find_element_by_xpath(
        '//*[@id="leftMain"]/div/div[2]/div/ul/li[%s]/div/div[2]/p[2]' % (c + 1))
    cmp_price = self.driver.find_element_by_xpath(
        '//*[@id="leftMain"]/div/div[2]/div/ul/li[%s]/div/div[2]/p[1]' % (c + 1))
    cmp_total = self.driver.find_element_by_xpath(
        '//*[@id="leftMain"]/div/div[2]/div/ul/li[%s]/div/div[2]/p[3]' % (c + 1))
    cmp_total_money = self.driver.find_element_by_xpath(
        '//*[@id="leftMain"]/div/div[2]/div/ul/li[%s]/div/div[2]/p[4]' % (c + 1))
    # 将界面信息与json进行对比验证
    self.assertEqual(cmp_cardno.text.strip(), cardno, u'商品圆牌号异常')
    self.assertEqual(cmp_goodsno.text.strip(), goodsno, u'款号异常')
    self.assertEqual(cmp_title.text.split(' ')[0].split('\n')[0], title.strip(), u'商品标题异常')
    self.assertEqual(cmp_price.text.replace(u'¥ ', ''), price, u'商品价格异常' + cardno)
    self.assertEqual(cmp_total.text, u'订货数量：' + str(total) + u'件', u'订货数量异常' + cardno)
    if total_money == 0:
        total_money = '0.00'
    self.assertEqual(cmp_total_money.text.strip().replace(',', ''), u'订货金额： ¥' + str(total_money), u'订货金额异常' + cardno)
    if image:
        # 检查获取的json图片链接是否正常访问
        self.assertEqual(200, requests.get(image).status_code, u'该图片链接无法访问' + cardno)
        # 获取页面该商品的图片链接
        get_img = re.search(r'http:(.+?).png', cmp_image.get_attribute('src'))
        if get_img:
            self.assertEqual(get_img.group(0), image, u'商品展示图片异常' + cardno)
        else:
            get_img = re.search(r'http:(.+?).jpeg', cmp_image.get_attribute('src'))
            if get_img:
                self.assertEqual(get_img.group(0), image, u'商品展示图片异常' + cardno)
    else:
        # 商品没有添加图片时，验证默认图片是否正常显示
        self.assertEqual(config.DEFAULT_IMG, cmp_image.get_attribute('src'), u'该商品图片异常' + cardno)

#
def search_assert(self,keywords):
    '''搜索验证'''
    result = search_data(keywords)#获取搜索结果列表的json数据
    c = 1

    #当搜索列表为空时验证
    if not result['data']:
        ele = self.driver.find_element_by_xpath('//*[@id="leftMain"]/div/div[2]/div[2]')
        self.assertEqual(ele.text.strip(), u'当前列表空')
        self.assertEqual(ele.find_element_by_tag_name('img').get_attribute('src'), config.DEFAULT_PROMPT_IMG,
                         '列表显示为空图片异常')
    for list in result['data']:
        #圆牌号
        goodno = self.driver.find_element_by_css_selector(
            '#leftMain > div > div.mod-body > div > ul > li:nth-child(%s) > div > span' % c).text.strip()
        #款号
        cardno = self.driver.find_element_by_xpath(
            '//*[@id="leftMain"]/div/div[2]/div/ul/li[%s]/div/div[2]/p[2]/span' % c).text.strip()
        if keywords != '  ':
            if (keywords not in goodno) and (keywords not in cardno):
                sleep(1)
                self.assertTrue(False, u'关键词搜索后结果不匹配:' + keywords + ',' + goodno + ',' + cardno)

        inspect_goods(self, list, c - 1)#验证列表单个商品显示数据是否正常
        c += 1
    sleep(1)

def select_assert(self,select_button,select_list):
    '''筛选栏--全选和取消测试公共api'''

    select_button.click()  # 点击筛选按钮
    select_all = select_list.find_elements_by_tag_name('button')[0]
    cancel = select_list.find_elements_by_tag_name('button')[1]
    select_all.click()
    time.sleep(1)
    selected_flag = select_list.find_elements_by_tag_name('li')[1:-1]
    element_property = []
    # 检查每项是否被勾选--待定
    for ele in selected_flag:
        self.assertTrue(ele.find_element_by_tag_name('i').is_displayed(), u'全选后，存在未选中项:' + ele.text)
        element_property.append(ele.text.strip())
    list_goods = self.driver.find_elements_by_xpath('//*[@id="leftMain"]/div/div[2]/div/ul/li')
    if list_goods:
        # 每第三个检查一次商品属性
        for list in list_goods[1:-1:3]:
            list.click()  # 点击商品
            # 获取商品中的属性值
            goods_property = self.driver.find_element_by_xpath('//*[@id="dialogContent"]/section[1]/div[2]/div[5]/div')
            goods_property_text = []  # 存储商品属性值
            time.sleep(1)
            # 遍历商品属性值一一存入列表goods_property_text
            for t in goods_property.find_elements_by_tag_name('span'):
                goods_property_text.append(t.text.strip())

            if set(goods_property_text) & set(element_property):  # 判断属性值是否存在筛选栏
                pass
            else:
                self.assertTrue(False, '全选结果中有不存在的项目')
            time.sleep(1)
            self.driver.find_element_by_css_selector('#dialogParent > div > div.mod-head.clearfix > i').click()
            time.sleep(1)

    # 取消全选
    select_button.click()  # 点击季节
    cancel.click()
    # 检查是否所有项被取消选中
    for ele in selected_flag:
        self.assertTrue(not ele.find_element_by_tag_name('i').is_displayed(), u'取消全选后，存在未选中项:' + ele.text)

def single_select_assert(self,select_button,select_list):
    '''单个筛选结果筛查'''
    select_button.click()
    time.sleep(1)
    cancel = select_list.find_elements_by_tag_name('button')[1]
    select_value = select_list.find_elements_by_tag_name('li')[1].text.strip()
    select_list.find_elements_by_tag_name('li')[1].click()
    list_goods = self.driver.find_elements_by_xpath('//*[@id="leftMain"]/div/div[2]/div/ul/li')
    if len(list_goods) > 15:
        skip = 5
    else:
        skip = 3
    for list in list_goods[:-1:skip]:
        time.sleep(1)
        list.click()
        # 获取商品中的属性值
        time.sleep(1)
        goods_property = self.driver.find_element_by_xpath('//*[@id="dialogContent"]/section[1]/div[2]/div[5]/div')
        goods_property_text = []  # 存储商品属性值
        time.sleep(1)
        # 遍历商品属性值一一存入列表goods_property_text
        for t in goods_property.find_elements_by_tag_name('span'):
            goods_property_text.append(t.text.strip())
        # 判断商品时否是筛选结果
        if select_value not in goods_property_text:
            self.assertTrue(False, '单项筛选结果出错')
        self.driver.find_element_by_css_selector('#dialogParent > div > div.mod-head.clearfix > i').click()
    select_button.click()
    cancel.click()


if __name__=='__main__':
    # homepage_data()
    # list_data()
    # dh_bar()
    get_goods_detail(config.GOODS_NO[0])