# -*- coding:utf-8 -*-
# 导入 smtplib 和 MIMEText
import smtplib
from email.mime.text import MIMEText

# 定义发送列表
mailto_list=["12345678@qq.com"]

# 设置服务器名称、用户名、密码以及邮件后缀
mail_host = "smtp.qq.com"
mail_user = "1109567094"
mail_pass = "lenovo"
mail_postfix="qq.com"

# 发送邮件函数
def send_mail(to_list, sub, context):
    '''''
    to_list: 发送给谁
    sub: 主题
    context: 内容
    send_mail("xxx@126.com","sub","context")
    '''
    me = mail_user + "<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(context)
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        send_smtp = smtplib.SMTP()
        send_smtp.connect(mail_host)
        send_smtp.login(mail_user, mail_pass)
        send_smtp.sendmail(me, to_list, msg.as_string())
        send_smtp.close()
        return True
    except Exception, e:
        print(str(e))
        return False

if __name__ == '__main__':
    if (True == send_mail(mailto_list,"subject","context")):
        print ("测试成功")
    else:
        print ("测试失败")

raw_input()
