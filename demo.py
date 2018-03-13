# import re
#
# strings = '''background-image: url("http://biding365.oss-cn-hangzhou.aliyuncs.com/public/front_bg.jpg");'''
# print re.search(r'http(.+?).jpg',strings).group(0)
import time
from selenium import webdriver
from time import sleep
#
# print(time.ctime(1520417341))
#
# login_url = 'https://passport.cnblogs.com/user/signin?ReturnUrl=https%3A%2F%2Fwww.cnblogs.com%2F'
# url ='http://a.bdh.com/main/ordering/singal'
#
# d = webdriver.Chrome()
# d.get(url)
# d.find_element_by_id('input1').send_keys('holysor')
# d.find_element_by_id('input2').send_keys('wkp5201952#')
#
# print d.get_cookies()
# sleep(1)
#
#
# cookies = [{u'domain': u'a.bdh.com',
#                           u'secure': False,
#                           u'value': u'7nWndeueVoUXyoSiepMqOudGuHbpmKUj8K6EAgrF',
#                           u'expiry': 1520417341,
#                           u'path': u'/',
#                           u'httpOnly': True,
#                           u'name': u'laravel_session'}]
#
# cookie1 = {u'name':u'laravel_session',u'value':u'7nWndeueVoUXyoSiepMqOudGuHbpmKUj8K6EAgrF'}
# d.add_cookie(cookies[0])
# #
# d.get(url)


list = [[u'999'], u'998', u'998', u'997', u'997', u'996', u'996', u'995', u'995', u'994', u'994', u'993', u'993', u'992', u'991', u'6767', u'56512', u'56512', u'5565']

print(u'999' in list[0])