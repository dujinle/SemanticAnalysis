#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,re,common
from myexception import MyException
from pdeal_base import PDealBase

#前期的替换处理
class PDealReplace(PDealBase):

	def encode(self,struct):
		try:
			pass;
			self._replace_err_str(struct);
			self._deal_time_rep(struct);
		except Exception as e:
			raise e;

	def _replace_err_str(self,struct):
		for reg in self.data['rep']:
			regstr = reg['reg'];
			value = reg['value'];
			compstr = re.compile(regstr);
			match = compstr.findall(struct['text']);
			for mat in match:
				struct['text'] = struct['text'].replace(mat,value);

	def _deal_time_rep(self,struct):
		for reg in self.data['time_rep']:
			com = re.compile(reg['reg']);
			match = com.findall(struct['text']);
			for item in match:
				if item == '': continue;
				if reg['func'] == 'replace':
					struct['text'] = struct['text'].replace(item,reg['value'],1);
					print struct['text'];
				elif reg['func'] == 'add':
					mstr = item + reg['value'];
					if struct['text'].find(mstr) == -1:
						struct['text'] = struct['text'].replace(item,mstr,1);
				elif reg['func'] == 'hour_half':
					mstr = item.replace(reg['value'],'');
					mstr = mstr + u'30分';
					struct['text'] = struct['text'].replace(item,mstr,1);
