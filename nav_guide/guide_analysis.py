#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from guide_base import GuideBase
import com_funcs as ComFuncs

#处理新闻场景
class GuideAnalysis(GuideBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into news analysis ......');
			if not struct.has_key('step'): struct['step'] = 'start';
			self._fetch_all_types(struct);

			func = self._fetch_func(struct);
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

	def _fetch_all_types(self,struct):
		self._fetch_type(struct,'Objs');
		self._fetch_type(struct,'Sds');
		self._fetch_type(struct,'LocalPrep');
		self._fetch_type(struct,'PerPronom');
		self._fetch_type(struct,'PrepCom');
		self._fetch_type(struct,'VerbCom');

	def _fetch_type(self,struct,key):
		if struct.has_key(key):
			for item in struct[key]: struct[item['str']] = item;
			del struct[key];

	def _fetch_func(self,struct):
		reg = '';
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			reg = reg + struct[istr]['stype'];

		for model in self.data['models']:
			comp = re.compile(model['reg']);
			match = comp.search(reg);
			if not match is None: return model['func'];
		return None;

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
			if item['stype'].find('GOTOSP') <> -1:
				if item.has_key('stc'):
					for nit in item['stc']:
						if nit['stype'] == 'SP':
							end = nit['str'];
							break;
			if not end is None: break;
		start = self.data['local'];
		guide = super_b.get_guide(start,end);
		if guide is None:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
		else:
			struct['result']['msg'] = self.data['traffic'];
