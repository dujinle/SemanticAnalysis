#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common
from myexception import MyException
from com_base import ComBase as O2oBase
import struct_utils as Sutil
#标记用户列表中的数据
class O2oData(O2oBase):
	def __init__(self):
		O2oBase.__init__(self);
		self.history = None;

	def get_home_keep(self):
		self.history = 'home_keep';
		return self.data['HOME_KEEP'];
