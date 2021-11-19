from base_email import BaseEmail

# 邮箱的host和port
email_host = 'smtp.exmail.qq.com'
email_port = 465

# 发送者邮箱、密码、昵称
sender = ''
password = ''
sender_name = 'Goasia Supermarkt'

class CandidateEmail(object):
    def __init__(self):
        """
        初始化参数
        """
        # 发送邮件对象
        self.my_email = BaseEmail(email_host, email_port, sender, password, sender_name)
        # 保存邮件模板信息
        self.email_infos = {}

    def get_email_info(self):
        """
        获取要发送邮件模板信息
        :return:
        """
        subject = subject
        message = message
        self.email_infos = {
            'subject' : subject,
            'message' : message}
        
    def entry(self):
        """
        收到表单信息后，自动发送确认邮件
        :return:
        """
        try:
            subject = self.email_infos.get('subject')
            message = self.email_infos.get('message')
        except:
            print('邮件模板获取失败')
            return False
        # 遍历数据库，获取用户邮箱信息，发送邮件，对已发送项进行标记
        # 新建函数，确认回执信息，并标记
        '''for record in self.air.get_all(view='已录取'):
            # 若已发送或没有邮箱，则跳过
            if record.get('fields').get('已发送-入职') or not record.get('fields').get('邮箱'):
                continue
            result = self.my_email.send_email(subject, message.format(**record.get('fields')),
                                              record.get('fields').get('邮箱'), record.get('fields').get('姓名'))
            if result:
                print('已发送 入职指引 邮件:{}'.format(record.get('fields').get('姓名')))
                self.air.update(record.get('id'), {'已发送-入职': True})'''

