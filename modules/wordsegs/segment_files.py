#!/usr/bin/python
#-*- coding:utf-8 -*-
###################################
###################################
import os,sys
import mmseg,codecs
#=============================================
''' import common module '''
base_path = os.path.dirname(__file__);
sys.path.append(base_path + '/../../commons');
#=============================================
sys.stdout = codecs.getwriter('utf8')(sys.stdout);

class WordSeg:
	def __init__(self):
		self.mmseg = mmseg;
		self.separator = ' ';
		# load default dictionaries
		try:
			self.mmseg.dict_load_defaults();
		except MyException as e:
			raise e;

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
		except MyException,e:
			raise e;

	def write_file(self):
		try:
			self.mmseg.dict_rename_wordsfile();
			self.mmseg.dict_write_file();
		except MyException as e:
			raise e;

if __name__ == '__main__':

	if len(sys.argv) <> 2:
		print 'Usage: %s filename > outfile' %sys.argv[0]
		sys.exit(-1);
	filename = sys.argv[1];

	wd = WordSeg();
	with codecs.open(filename,'r','utf8') as f:
		for line in f.readlines():
			line = line.strip('\r\n');
			seg_line = wd.tokens(line);
			print '  '.join(seg_line);
