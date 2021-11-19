
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from email.utils import formataddr


class BaseEmail(object):
    def __init__(self, email_host, email_port, sender, password, sender_name=None):
        """
        初始化参数
        :param email_host: 邮箱的host
        :param email_port: 邮箱的port
        :param sender: 发送者邮箱
        :param password: 发送者邮箱密码
        """
        # 邮件发送者
        self.sender = sender
        # 邮件发送者昵称
        self.sender_name = sender_name
        # 连接邮箱并登录
        self.smtp = smtplib.SMTP_SSL(email_host, email_port)
        self.smtp.login(self.sender, password)

    def create_att(self, file_full_path, file_name):
        """
        创建文件附件
        :param file_full_path: 文件完整路径
        :param file_name: 文件名
        :return: 文件附件对象
        """
        att = MIMEApplication(open(file_full_path, 'rb').read())
        att.add_header('Content-Disposition', 'attachment', filename=file_name)
        return att

    def send_email(self, subject, message_text, receiver, receiver_name=None,
                   message_type='plain', message_encoding='utf-8', atts=None):
        """
        发送邮件
        :param subject:  邮件主题
        :param message_text: 邮件正文
        :param receiver: 收件人邮箱
        :param receiver_name: 收件人昵称
        :param message_type: 邮件类型
        :param message_encoding: 邮件编码格式
        :param atts: 邮件附件对象类别 类型：列表，列表成员类型：邮件附件对象
        :return:
        """
        message = MIMEMultipart()
        # 邮件主题，编码
        message['Subject'] = Header(subject, message_encoding)
        if self.sender_name:
            # 发件人昵称、发件人邮箱
            message['From'] = formataddr([self.sender_name, self.sender])
        else:
            # 发件人邮箱，编码
            message['From'] = Header(self.sender, message_encoding)

        if isinstance(receiver, list):
            receiver = ','.join(receiver)
        if receiver_name:
            # 收件人昵称、收件人邮箱
            message['To'] = formataddr([receiver_name, receiver])
        else:
            message['To'] = Header(receiver, message_encoding)
        receiver = receiver.split(',')

        # 邮件正文，格式，编码
        content = MIMEText(message_text, message_type, message_encoding)
        message.attach(content)
        # 若有附件,则创建带附件的邮件
        if atts:
            # 依次吧附件添加到邮件对象中
            for att in atts:
                message.attach(att)
        try:
            # 发件人，收件人，邮件内容
            self.smtp.sendmail(self.sender, receiver, message.as_string())
            print('邮件发送成功,收件人:{}'.format(receiver))
            return True
        except Exception as e:
            print('邮件发送失败,收件人:{},原因:{}'.format(receiver, e))
            return False

    def __del__(self):
        try:
            # 退出邮箱登录
            self.smtp.quit()
        except:
            pass
