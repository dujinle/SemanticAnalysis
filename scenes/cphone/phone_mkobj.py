#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common
from myexception import MyException
from scene_base import SceneBase
#标记用户列表中的数据
class PhoneMkobj(SceneBase):

	def encode(self,struct,super_b):
		try:
			self._mark_body(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _mark_body(self,struct):
		pass;
