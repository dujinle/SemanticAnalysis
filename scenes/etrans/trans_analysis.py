#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from scene_base import SceneBase
import com_funcs as ComFuncs

#处理 英文翻译 场景
class TransAnalysis(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into trans analysis......');
			if not struct.has_key('step'): struct['step'] = 'start';
			if struct['step'] == 'start':
				func = self._fetch_func(struct);
				if func == 'get':
					self._get_words_info(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _get_words_info(self,struct,super_b):
		eng = None;
		for istr in struct['inlist']:
			comp = re.compile('[a-zA-Z]+');
			match = comp.match(istr);
			if match is None: continue;
			eng = match.group(0);
			break;
		if eng is None:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
		else:
			winfo = super_b.get_words_info(eng);
			if winfo is None:
				ComFuncs._set_msg(struct,self.data['msg']['unknow']);
				return None;
			struct['result']['winfo'] = winfo;
			struct['result']['msg'] = winfo['meaning']

