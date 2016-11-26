#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,random
from common import logging
from myexception import MyException
from phone_base import PhoneBase

class PhoneData(PhoneBase):

	def get_phone_by_name(self,owner):
		phones = self.data['Phone'];
		if phones.has_key(owner):
			return phones[owner];
		return None;

	def get_message(self):
		return self.data['Message'];
