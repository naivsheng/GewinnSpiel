'''
# -*- coding: UTF-8 -*-
# __Author__: Yingyu Wang
# __date__: 
# __Version__: 生成GUI,实现定时启动
'''

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QDateTime, pyqtSignal,QThread
from Ui_Gui import Ui_MainWindow
from random_gen import Generate
from GewinnSpiel import run
# from threading import Timer,Thread
import time
from Multi import Runthread
from LavaralConnect import LavaralConnect


class MyAction(Ui_MainWindow):
	signal = pyqtSignal(str)
	def __init__(self,mainWindow):
		super().__init__()
		self.setupUi(mainWindow)
		self.initUI()
		self.thread = None
	def initUI(self):
		self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
		self.pushButton_3.clicked.connect(self.confirm_to_run)
		self.pushButton_4.clicked.connect(self.cancel_to_run)
		self.pushButton_2.clicked.connect(self.gene)
		self.pushButton.clicked.connect(self.datecleaning)

	def confirm_to_run(self):
		self.pushButton_4.setEnabled(True)
		self.pushButton_2.setEnabled(False)
		self.pushButton_3.setEnabled(False)
		datetime = self.dateTimeEdit.dateTime()
		# settime = self.dateTimeEdit.time()
		setTime = datetime.toString('yyyy-MM-dd HH:mm:00')
		local = time.mktime(time.strptime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),"%Y-%m-%d %H:%M:%S"))
		setTime = time.mktime(time.strptime(setTime,'%Y-%m-%d %H:%M:%S'))
		# print(local,setTime,setTime-local)
		delay = setTime-local
		if delay > 0:
			s = '设置抽奖时间：\n' + datetime.toString('yyyy-MM-dd HH:mm:00')
			self.textBrowser.setText(s)
			self.thread = Runthread(delay)
			self.thread._signal.connect(self.call_backlog) # 线程连接传回到GUI
			self.thread.start()
		else:
			self.textBrowser.setText('时间设置错误')
			self.pushButton_4.setEnabled(False)
			self.pushButton_2.setEnabled(True)
			self.pushButton_3.setEnabled(True)
		
		'''date = []
		for i in datetime.toString('dd-MM-yyyy-HH-mm').split('-'):
			date.append(i) # 获取数据并切片
		print(date)'''
	def call_backlog(self,data):
		self.textBrowser.setText(data)
		self.thread.terminate()	# 结束线程
		self.pushButton_4.setEnabled(False)
		self.pushButton_2.setEnabled(True)
		self.pushButton_3.setEnabled(True)
			
	def cancel_to_run(self):
		self.pushButton_4.setEnabled(False)
		self.pushButton_2.setEnabled(True)
		self.pushButton_3.setEnabled(True)
		self.thread.terminate()
		# self.t.cancel()
		self.textBrowser.setText('已取消自动抽奖')
	def gene(self):
		'''
			生成随机数，获取中奖号码、预留邮箱信息
		'''
		num = Generate()
		# print('生成数字:',num)
		self.pushButton_4.setEnabled(False)
		self.pushButton_2.setEnabled(True)
		self.pushButton_3.setEnabled(True)
		s = '当前抽奖时间：\n' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
		s = '\n' + '生成数字：' + str(num)
		self.textBrowser.setText(s)	
		# 找到num指向的单据
		data_dict = LavaralConnect(num)
		dict_new = dict(zip(data_dict.values(),data_dict.keys()))   # 图片名：id
		# 连接		
		AWS_ACCESS_KEY_ID = ''
		AWS_SECRET_ACCESS_KEY = ''
		AWS_BUCKET = 'gewinn-spiel'
		AWS_DEFAULT_REGION = 'eu-central-1'
		AWS_USE_PATH_STYLE_ENDPOINT = False

		s3_resource = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_DEFAULT_REGION)
		gewinn_spiel = s3_resource.Bucket(name = AWS_BUCKET)

		for object in gewinn_spiel.objects.all():
			if 'images/' not in object.key.split('.')[0]:
				continue
			if object.key.split('/')[1] in dict_new:
				f = 'Gewinn_result.' + object.key.split('.')[1]
        s3_resource.Object(AWS_BUCKET, object.key).download_file(f) # download tmp file
		self.textBrowser.setText(f'中奖信息id为：{num}\n具体信息为：{data_dict}\n单据文件为Gewinn_result\n')

	def datecleaning(self):
		'''
			数据清洗
		'''
		self.textBrowser.setText('开始数据清洗')
		# 返回当前参与人次、有效参与人次
		# run()
		self.progressBar.setProperty("value", 100)

if __name__ =='__main__':
	app = QApplication(sys.argv)
	mainWindow = QMainWindow()
	form = MyAction(mainWindow)
	mainWindow.show()
	sys.exit(app.exec_())	