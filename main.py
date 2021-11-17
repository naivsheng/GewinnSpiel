'''
# -*- coding: UTF-8 -*-
# __Author__: Yingyu Wang
# __date__: 
# __Version__: 生成GUI 
'''

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from Ui_Gui import Ui_MainWindow
from random_gen import Generate
from GewinnSpiel import run

class QMainWindow(QMainWindow,Ui_MainWindow):
	def __init(self):
		super(QMainWindow,self).__init__()
		self.setupUi(self)
		self.action(self)
		# timeEdit = QDateTimeEdit(QTime.currentTime(), self)
	def action(self):
		self.pushButton.clicked.connect()
		# 当时间改变时触发槽函数
		# self.dateEdit.timeChanged.connect(self.onTimeChanged)
		self.pushButton_3.clicked.connect(self.confirm_to_run)
		date=self.dateEdit.dateTime()
		self.pushButton_4.clicked.connect(self.cancel_to_run)
		self.pushButton_2.clicked.connect(self.gene)
		self.pushButton.clicked.connet(self.datecleaning)
	def onTimeChanged(date):
		print(date)
	def confirm_to_tun(self):
		date = self.dateEdit.dateTime()
		print(date)
	def cancel_to_run(self):
		print('cancel')
	def btn_clicked(self):
		btn.setText('clicked')
	def gene(self):
		num = Generate()
		print('生成数字:',num)
	def datecleaning(self):
		run()

if __name__ =='__main__':
	app = QApplication(sys.argv)
	MainWindow = QMainWindow()	
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())	

