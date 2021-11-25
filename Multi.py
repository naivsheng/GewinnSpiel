'''
# -*- coding: UTF-8 -*-
# __Author__: Yingyu Wang
# __date__: 18.11.2021
# __Version__: 子线程返回数据
'''
from PyQt5.QtCore import pyqtSignal,QThread,QTimer
from random_gen import Generate
import time

class Runthread(QThread):
	_signal = pyqtSignal(str)
	def __init__(self,delay):
		super(Runthread,self).__init__()
		self.delay = delay
	def __del__(self):
		self.wait()

	def run(self):
		# self.timer = QTimer()
		# self.timer.setSingleShot(True)
		# self.timer.timeout.connect(self.gen)
		# self.timer.start(self.delay * 1)	 # 计时单位：毫秒
		print('start',self.delay)
		time.sleep(self.delay)
		self.gen()
	def gen(self):
		# self.timer.stop()
		num = Generate()
		# print('生成数字:',num)
		s = '当前抽奖时间：\n' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
		s = '\n' + '生成数字：' + str(num)
		self._signal.emit(s)

class Multi(QThread):
	def __init__(self,func,args=()):
		super(MyThread,self).__init__()
		self.func = func
		self.args = args
	def run(self):
		self.result = self.func(*self.args)
	def get_result(self):
		Thread.join(self) #等待线程完成
		try:
			self.pushButton_4.setEnabled(False)
			self.pushButton_2.setEnabled(True)
			self.pushButton_3.setEnabled(True)

			return self.result
		except:
			return None