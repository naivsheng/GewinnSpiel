from base_email import BaseEmail

# 邮箱的host和port
email_host = 'smtp.exmail.qq.com' # TODO
email_port = 465    # TODO

# 发送者邮箱、密码、昵称
sender = '' # TODO
password = '' # TODO
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
        subject = 'Danke für die Teilnahme' # 成功上传图片
        # message = message # 点击链接以确认
        message = 'Sie haben schon ihre Document hochgeladen.\n Klicken Sie auf den untenstehenden Link, \
            um Ihre E-Mail zu bestätigen.\n 您已成功上传文件，请点击以下链接以确认您的邮箱地址\n {}\n \
                Mit freundlichen Grüßen.\n GoAsia Supermarkt'
        self.email_infos = {
            'subject' : subject,
            'message' : message}
        
    def entry(self):
        """
        收到表单信息后，自动发送确认邮件
        :return:
        """
        try:
            subject = self.email_infos.get('subject') # erfolgt upload
            message = self.email_infos.get('message') # click links to confirm 
        except:
            print('邮件模板获取失败')
            return False
        # 生成邮箱验证码，提供点击确认功能
        checkCode = ""  
        for i in range(4):  
            num = random(1, 10)  
            checkCode += num.ToString() 
        validataCode = FormsAuthentication.HashPasswordForStoringInConfigFile(checkCode, "md5")
        # strBody = 'http://localhost:2493/web/Operate.aspx?userId=' + userId +'validateCode=' + validateCode # TODO 确定验证 
        strBody = 'http://localhost:3000/web/ActiveServlet?userId=' + userId + 'validateCode=' + validataCode
        # result = self.my_email.send_email(subject,message.format(**validateCode),email)
        result = self.my_email.send_email(subject,message.format(strBody),email)
        if result:
            print('发送成功')
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

