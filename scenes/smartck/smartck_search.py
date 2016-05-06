#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys,os,re,common
from myexception import MyException
from common import logging
import com_funcs as SceneParam
import smartck_common as SmartckCom
from scene_base import SceneBase

class SmartckSearch(SceneBase):

	def encode(self,struct,super_b):
		try:
			if not struct.has_key('ck_scene'): return None;
			if struct['ck_scene'] <> 'ck_search': return None;
			logging.info('go into search scene......');
			if not struct.has_key('step'): struct['step'] = 'start';
			if struct['step'] == 'start':
				cks = self._find_cks(struct,super_b);
				if cks is None or len(cks) == 0:
					SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
				else:
					self._post_clocks(cks,struct,super_b);
				struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _find_cks(self,struct,super_b):
		match = self._get_match_info(struct['ttag'],'template');
		if match is None: return None;
		if match['func'] == 't2t':
			print 'go into _find_cks_time_to_time......'
			cks = SceneParam._find_cks_time_to_time(struct,super_b);
			return cks;
		elif match['func'] == 'after':
			print 'go into _find_cks_after......'
			cks = SceneParam._find_cks_after(struct,super_b);
			return cks;
		elif match['func'] == 'all':
			print 'go into _find_all_cks......'
			cks = super_b.clocks.keys();
			return cks;
		elif match['func'] == 'num':
			cks = SceneParam._find_cks_by_num(struct,super_b);
			return cks;
		else:
			cks = SceneParam._find_cks_by_sample(struct,super_b);
			return cks;
		return None;

	def _post_clocks(self,cks,struct,super_b):
		struct['result']['clocks'] = list();
		for ck in cks:
			if super_b.clocks.has_key(ck):
				clock = super_b.clocks[ck];
				struct['result']['clocks'].append(clock);
			else:
				SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
				return None;
		msg_id = SceneParam._get_random_id(len(self.data['msg']['ck_num']));
		struct['result']['msg'] = (self.data['msg']['ck_num'][msg_id] %len(cks));

	def _get_match_info(self,ttag,template):
		for temp in self.data[template]:
			comp = re.compile(temp['reg']);
			match = comp.search(ttag);
			if not match is None: return temp;
		return None;
