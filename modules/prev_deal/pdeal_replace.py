#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,re,common
from myexception import MyException
from pdeal_base import PDealBase

#前期的替换处理
class PDealReplace(PDealBase):

	def encode(self,struct):
		try:
			self._replace_str(struct);
			self._deal_time_rep(struct);
		except Exception as e: raise e;

	def _replace_str(self,struct):
		for reg in self.data['rep']:
			regstr = reg['reg'];
			value = reg['value'];
			compstr = re.compile(regstr);
			match = compstr.search(struct['text']);
			if not match is None:
				struct['text'] = struct['text'].replace(match.group(0),value);
				if match.group(0) in struct['inlist']:
					struct['inlist'].remove(match.group(0));

	def _deal_time_rep(self,struct):
		com = re.compile(self.data['time_rep']);
		match = com.search(struct['text']);
		if not match is None:
			tstr = match.group(0);
			if len(tstr) <> 4: return None;
			thour = tstr[2:];
			tnum = thour[0];
			nnum = int(tnum) + 10;
			phour = thour.replace(tnum,str(nnum));
			pstr = tstr.replace(thour,phour);
			struct['text'] = struct['text'].replace(tstr,pstr);

