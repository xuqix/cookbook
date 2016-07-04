# -*- coding: utf-8 -*-

import os, sys, time, platform, random
import termcolor

class Logger:
    flag = True
    stream = sys.stdout

    @staticmethod
    def write(s):
        Logger.stream.write(s + os.linesep)

    @staticmethod
    def error(msg):
        if Logger.flag == True:
            Logger.write("".join(  [ termcolor.colored("ERROR", "red"), ": ", termcolor.colored(msg, "white") ] ))
    @staticmethod
    def warn(msg):
        if Logger.flag == True:
            Logger.write("".join(  [ termcolor.colored("WARN", "yellow"), ": ", termcolor.colored(msg, "white") ] ))
    @staticmethod
    def info(msg):
        if Logger.flag == True:
            Logger.write("".join(  [ termcolor.colored("INFO", "magenta"), ": ", termcolor.colored(msg, "white") ] ))
    @staticmethod
    def debug(msg):
        if Logger.flag == True:
            Logger.write("".join(  [ termcolor.colored("DEBUG", "magenta"), ": ", termcolor.colored(msg, "white") ] ))
    @staticmethod
    def success(msg):
        if Logger.flag == True:
            Logger.write("".join(  [ termcolor.colored("SUCCES", "green"), ": ", termcolor.colored(msg, "white") ] ))

def gen_captcha(content, fmt="png"):
    clean = True
    try:
        image_name = u"verify." + fmt
        open( image_name, "wb").write(content)
        """ System platform: https://docs.python.org/2/library/platform.html """
        Logger.info(u"正在调用外部程序渲染验证码 ... ")
        if platform.system() == "Linux":
            Logger.info(u"Command: xdg-open %s &" % image_name )
            os.system("xdg-open %s &" % image_name )
        elif platform.system() == "Darwin":
            Logger.info(u"Command: open %s &" % image_name )
            os.system("open %s &" % image_name )
        elif platform.system() in ("SunOS", "FreeBSD", "Unix", "OpenBSD", "NetBSD"):
            os.system("open %s &" % image_name )
        elif platform.system() == "Windows":
            os.system("%s" % image_name )
        else:
            Logger.info(u"我们无法探测你的作业系统，请自行打开验证码 %s 文件，并输入验证码。" % os.path.join(os.getcwd(), image_name) )
            clean = False

        sys.stdout.write(termcolor.colored(u"请输入验证码: ", "cyan") )
        captcha_code = raw_input( )
    finally:
        if clean and os.path.exists(image_name):
            os.remove(image_name)
    return captcha_code

if __name__=='__main__':
    gen_capthca("https://www.zhihu.com/capthca.gif?r=12345677&type=login", 'gif')
