#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,random
from common import logging
from myexception import MyException
from music_base import MusicBase

#处理音乐场景
class MusicData(MusicBase):

	#获取音乐 根据人名
	def get_favorite(self,owner):
		if self.data.has_key(owner):
			return self.data[owner];
		return None;
