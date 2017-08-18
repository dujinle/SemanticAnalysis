#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,random
from common import logging
from myexception import MyException
from com_base import ComBase as PhoneBase

class PhoneData(PhoneBase):
	def __init__(self):
		PhoneBase.__init__(self);
		self.user = None;

	def get_phone_by_name(self,owner):
		phones = self.data['Phone'];
		if phones.has_key(owner):
			self.user = phones[owner];
		return self.user;

	def get_message(self):
		return self.data['Message'];
