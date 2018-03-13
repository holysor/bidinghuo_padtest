#-*- coding:utf-8 -*-
import unittest
import os
import time

import HTMLTestReport

from TestCase import bdh_loginTestCase


def all_case():
    testcase = unittest.TestSuite()
    casepath = os.getcwd()+os.sep+'TestCase'
    if os.path.exists(casepath):
        discover = unittest.defaultTestLoader.discover(casepath, pattern='*TestCase.py', top_level_dir=None)
    else:
        raise OSError,'目录不存在:'+casepath

    for testsuite in discover:
        for case in testsuite:
            testcase.addTest(case)

    print "测试用例数:",testcase.countTestCases(),'条'
    return testcase

def outPutWithHTML(testcase):
    import shutil
    now = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
    print '开始时间:',now
    day = time.strftime('%Y-%m-%d')
    file_is_exist = os.path.exists(os.getcwd()+os.sep+'result'+ os.sep + day)
    if not os.path.exists(os.getcwd()+os.sep+'result'):
        os.mkdir(os.getcwd()+os.sep+'result')
    if not file_is_exist:
        os.makedirs(os.getcwd()+os.sep+'result'+ os.sep + day)
        os.mkdir(os.getcwd()+os.sep+'result'+ os.sep + day + os.sep + 'screencap')

    filename = os.getcwd()+os.sep+'result'+ os.sep + day + '/result.html'
    runner = HTMLTestReport.HTMLTestRunner(title=u'必订火',
                                           description=u'必订火-自动化测试报告',
                                           stream=open(filename,"wb"),verbosity=2,retry=1)
    runner.run(testcase)

if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    # testsuite.addTest(TestForReportTestCase.Test('test_fail1'))
    outPutWithHTML(all_case())
    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(all_case())