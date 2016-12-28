#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,random
from common import logging
from myexception import MyException
from com_base import ComBase as TransBase

class TransData(TransBase):

	def get_words_info(self,eng):
		return self.data[eng];
