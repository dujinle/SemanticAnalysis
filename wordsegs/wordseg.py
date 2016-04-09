#!/usr/bin/python
#-*- coding:utf-8 -*-
###################################
###################################
import mmseg

class WordSeg:
	def __init__(self):
		self.mmseg = mmseg;
		self.separator = ' ';
		# load default dictionaries
		try:
			self.mmseg.dict_load_defaults();
		except Exception, e:
			print e;

	def tokens(self,intext):
		seglist = [];
		algor = self.mmseg.Algorithm(intext);
		first = True
		for tk in algor:
			seglist.append(tk.text);
		return seglist;
	def add_word(self,intext):
		try:
			self.mmseg.dict_add_word(intext);
		except Exception,e:
			raise e;
	def del_word(self,intext):
		try:
			self.mmseg.dict_del_word(intext);
		except Exception,e:
			raise e;

#wd = WordSeg();
#print wd.tokens(u'你打野');
#wd.add_word(u'你打野');
#print wd.tokens(u'你打野');
#wd.del_word(u'你打野');
#print wd.tokens(u'你打野');
