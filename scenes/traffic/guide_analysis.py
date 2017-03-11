#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from com_base import ComBase as GuideBase
import com_funcs as ComFuncs

#处理新闻场景
class GuideAnalysis(GuideBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into news analysis ......');
			if not struct.has_key('step'): struct['step'] = 'start';
			func = self._fetch_func(struct,'type');
			if struct['step'] == 'start':
				if func is None:
					ComFuncs._set_msg(struct,self.data['msg']['unknow']);
					return None;
				print 'get func:[' + func + ']......';
				if func == 'gop':
					self._get_end_guide(struct,super_b);
				elif func == 'ptp':
					self._get_guide(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	#获取轨迹路线
	def _get_guide(self,struct,super_b):
		start = end = None;
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			if item['stype'].find('SPTOSP') <> -1:
				if item.has_key('stc'):
					for nit in item['stc']:
						if nit['stype'] == 'SP' and start is None:
							start = nit['str'];
						elif nit['stype'] == 'SP' and end is None:
							end = nit['str'];
		guide = super_b.get_guide(start,end);
		if guide is None:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
		else:
			struct['result']['msg'] = self.data['traffic'];

	#获取轨迹路线
	def _get_end_guide(self,struct,super_b):
		start = end = None;
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			if item['stype'] == 'GO':
				if item.has_key('child'):
					nit = item['child'];
					if nit['type'] == 'SP':
						end = nit['str'];
						break;
			if not end is None: break;
		start = self.data['local'];
		guide = super_b.get_guide(start,end);
		if guide is None:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
		else:
			struct['result']['msg'] = self.data['traffic'];
