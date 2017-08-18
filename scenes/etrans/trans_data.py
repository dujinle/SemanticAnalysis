#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common
from common import logging
from myexception import MyException
from scene_base import SceneBase

class TransData(SceneBase):

	def get_words_info(self,eng):
		return self.data[eng];
