#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,copy
import re,time
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
import common,alarm_common
from myexception import MyException
from common import logging

from base import Base
class SceneEffDate(Base):

	def encode(self,struct,super_b):
		try:
			logging.info('go into set effective date......');
			if super_b.myclock is None:
				struct['result']['msg'] = self.data['msg']['ck_unknow'][0];
				struct['code'] = 'exit';
				return None;
			if struct.has_key('question') and struct['question'] == "set_bell_type":
				self._set_bell_type(struct,super_b);
			if struct.has_key('question') and struct['question'] == "set_bell_ring":
				self._select_bell_name(struct,super_b);
			self._set_bell(struct,super_b);
		except Exception as e:
			raise MyException(format(e));

	#modify clock attribute#
	def _set_bell(self,struct,super_b):
		myclock = super_b.myclock;
		if not myclock.has_key('bell'):
			struct['result']['msg'] = self.data['msg']['set_bell_type'][0];
			struct['code'] = 'answer';
			struct['question'] = 'set_bell_type';
		elif not myclock['bell'].has_key('name'):
			if myclock['bell']['type'] == 'music':
				struct['result']['msg'] = self.data['msg']['set_bell_music'][0];
				struct['result']['music'] = self.data['music'];
			elif myclock['bell']['type'] == 'ring':
				struct['result']['msg'] = self.data['msg']['set_bell_ring'][0];
				struct['result']['ring'] = self.data['rings'];
			struct['code'] = 'select';
			struct['question'] = "set_bell_ring";
		else:
			struct['code'] = 'succ';
			struct['result']['msg'] = self.data['msg']['set_bell_succ'];

	def _set_bell_type(self,struct,super_b):
		if not struct.has_key('question'): return None;
		myclock = super_b.myclock;
		if not myclock.has_key('bell'): myclock['bell'] = dict();

		for ck in struct['clocks']:
			if ck['type'] == '_music' and struct['question'] == 'set_bell_type':
				myclock['bell']['type'] = 'music';
				del struct['question'];
				break;
			elif ck['type'] == '_bell' and struct['question'] == 'set_bell_type':
				myclock['bell']['type'] = 'ring';
				del struct['question'];
				break;

	def _select_bell_name(self,struct,super_b):
		myclock = super_b.myclock;
		if myclock.has_key('bell') and myclock['bell'].has_key('type'):
			btype = myclock['bell']['type'];
			data = self.data['music'];
			if btype == 'ring': data = self.data['rings'];
			for key in data.keys():
				if struct['text'].find(key) <> -1:
					myclock['bell']['name'] = key;
					myclock['bell']['addr'] = data[key]['addr'];
					break;
			if not myclock['bell'].has_key('name'):
				self._select_bell_num(struct,myclock);

	def _select_bell_num(self,struct,super_b):
		pass;
