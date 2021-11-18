'''
# -*- coding: UTF-8 -*-
# __Author__: Yingyu Wang
# __date__: 
# __Version__: 生成GUI 
'''

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QDateTime
from Ui_Gui import Ui_MainWindow
from random_gen import Generate
from GewinnSpiel import run

class MyAction(Ui_MainWindow):
	def __init__(self,mainWindow):
		super().__init__()
		self.setupUi(mainWindow)
		self.initUI()
	def initUI(self):
		self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
		self.pushButton_3.clicked.connect(self.confirm_to_run)
		date=self.dateTimeEdit.dateTime()
		self.pushButton_4.clicked.connect(self.cancel_to_run)
		self.pushButton_2.clicked.connect(self.gene)
		self.pushButton.clicked.connect(self.datecleaning)

	def onTimeChanged(date):
		print(date.toString)
	def confirm_to_run(self):
		datetime = self.dateTimeEdit.dateTime()
		date = []
		for i in datetime.toString('dd-MM-yyyy-HH-mm').split('-'):
			date.append(i) # 获取数据并切片
		print(date)
		# print(datetime.toString('dd-MM-yyyy HH:mm'))
	def cancel_to_run(self):
		print('cancel')
	def btn_clicked(self):
		btn.setText('clicked')
	def gene(self):
		num = Generate()
		print('生成数字:',num)
	def datecleaning(self):
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