#-*- coding:utf-8 -*-

__author__ = 'wujiajia'
__data__ = "2018/03/5"

from functools import wraps
from PIL import Image
import os,sys
import time
import traceback

def ErrorHandle(func):
    """
        用例失败截图
    """
    funcname = func.__name__ + '.png'
    day = time.strftime('%Y-%m-%d')
    path = os.getcwd() +os.sep+'result'+os.sep + day + os.sep+'screencap'
    imagepath = path + os.sep + funcname

    if os.path.exists(path):
        if os.path.exists(imagepath):
            os.remove(imagepath)
    else:
        os.makedirs(path)

    @wraps(func)
    def _deco(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except:
            if args:
                args[0].__init__.im_self.driver.get_screenshot_as_file(imagepath)
                # args[0].__init__.im_self.driver.get_screenshot_as_base64()
                img = Image.open(imagepath)
                w, h = img.size
                dimg = img
                if w > 1980 and h > 1080:
                    dimg = img.resize((w / 4, h / 4), Image.ANTIALIAS)  # 设置压缩尺寸和选项
                    dimg.save(imagepath)
                elif w >1280 and h > 800:
                    dimg = img.resize((w/2,h/2),Image.ANTIALIAS)#设置压缩尺寸和选项
                    dimg.save(imagepath)
                else:
                    dimg.save(imagepath)


            traceback.print_exc()
            info = sys.exc_info()
            raise info[0],info[1]
        finally:
            pass
    return _deco
