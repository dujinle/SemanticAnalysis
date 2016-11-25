#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
from myexception import MyException
import struct_utils as Sutil

#标记人称代词
class MarkPpronoun():
	def __init__(self,net_data):
		self.net_data = net_data;
		self.data = None;

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			if not struct.has_key('Ppronoun'): struct['Ppronoun'] = list();
			self._mark_people_pronoun(struct);
			Sutil._link_split_words(struct,'Ppronoun');
		except Exception:
			raise MyException(sys.exc_info());

	def _mark_people_pronoun(self,struct):
		for key in self.data.keys():
			item = self.data[key];
			pstr = '';
			for istr in item['reg']:
				pstr = pstr + '(' + istr + ')|';
			if pstr[-1] == '|': pstr = pstr[0:-1];
			comp = re.compile(pstr);
			match = comp.findall(struct['text']);
			for it in match:
				if isinstance(it,tuple) == True:
					for isr in it:
						if len(isr) == 0: continue;
						tdic = dict();
						tdic['str'] = isr;
						tdic['type'] = 'PPRONOUN';
						tdic['stype'] = key;
						struct['Ppronoun'].append(tdic);
				else:
					tdic = dict();
					tdic['str'] = isr;
					tdic['type'] = 'PPRONOUN';
					tdic['stype'] = key;
					struct['Ppronoun'].append(tdic);


