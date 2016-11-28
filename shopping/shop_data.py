#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,random
from common import logging
from myexception import MyException
from shop_base import ShopBase

class ShopData(ShopBase):

	def get_shop_by_sp(self,sp):
		if self.data.has_key(sp):
			return self.data[sp];
		return None;

	def get_more_info(self,local):
		if self.data.has_key(local):
			return self.data[local];
		return None;
