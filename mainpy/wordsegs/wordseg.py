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

	def deal_word(self,action,word):
		try:
			if action == 'add':
				self.mmseg.dict_add_word(word.get('value'));
			elif action == 'del':
				self.mmseg.dict_del_word(word.get('value'));
		except Exception,e:
			raise e;
	def write2file(self):
		try:
			self.mmseg.dict_rename_wordsfile();
			#self.mmseg.dict_write_file();
		except Exception as e:
			raise e;

wd = WordSeg();
print wd.tokens(u'你打野');
wd.write2file();
#print wd.tokens(u'你打野');
#wd.del_word(u'你打野');
#print wd.tokens(u'你打野');
