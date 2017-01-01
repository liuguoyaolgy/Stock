
import smtplib
from email.mime.text import MIMEText
from email.header import Header
def smtp_send(context):
    sender = 'liuguoyao_lgy@163.com'
    receiver = 'liuguoyao_lgy@163.com'
    smtpserver = 'smtp.163.com'
    username = 'liuguoyao_lgy@163.com'
    password = 'liu514257'

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(context, 'plain', 'utf-8')
    message['Subject'] = Header('stock-week', 'utf-8').encode()
    message['From'] = 'liuguoyao_lgy@163.com<liuguoyao_lgy@163.com>'
    message['To'] = "sniff&scratch<liuguoyao_lgy@163.com>"


    smtpObj = smtplib.SMTP()
    smtpObj.connect(smtpserver)    # 25 为 SMTP 端口号
    smtpObj.login(username,password)
    smtpObj.sendmail(sender, [receiver], message.as_string())
    print("邮件发送成功")
    # try:
    #     smtpObj = smtplib.SMTP()
    #     smtpObj.connect(smtpserver)    # 25 为 SMTP 端口号
    #     smtpObj.login(username,password)
    #     smtpObj.sendmail(sender, receiver, message.as_string())
    #     print("邮件发送成功")
    # except smtplib.SMTPException:
    #     print("Error: 无法发送邮件")
    smtpObj.quit()
