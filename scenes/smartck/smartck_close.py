#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,re,common
from common import logging
from myexception import MyException
from scene_base import SceneBase
import com_funcs as SceneParam
import smartck_common as SmartckCom

class SmartckClose(SceneBase):

	def encode(self,struct,super_b):
		try:
			if not struct.has_key('ck_scene'): return None;
			if struct['ck_scene'] <> 'ck_close': return None;
			logging.info('go into scene close action......');
			if not struct.has_key('step'): struct['step'] = 'start';

			#启动时响应回复
			if struct['step'] == 'start':
				cks = self._find_cks(struct,super_b);
				if not cks is None and len(cks) > 0:
					close_num = self._close_cks(cks,super_b);
					SceneParam._set_msg(struct,self.data['msg']['close_succ']);
				else:
					SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());


	def _close_cks(self,cks,super_b):
		close_num = 0;
		for ck in cks:
			clock = super_b.clocks[ck];
			if not clock.has_key('status'):
				clock['status'] = dict();
				clock['status']['type'] = 'close';
				close_num = close_num + 1;
			elif clock['status']['type'] <> 'close':
				clock['status']['type'] = 'close';
				close_num = close_num + 1;
		return close_num;

	def _find_cks(self,struct,super_b):
		match = self._get_match_info(struct['ttag']);
		if match is None:
			cks = SmartckCom._find_cks_by_sample(struct,super_b);
			return cks;
		elif match['func'] == 't2t':
			print 'go into _find_cks_time_to_time......'
			cks = SmartckCom._find_cks_time_to_time(struct,super_b);
			return cks;
		elif match['func'] == 'num':
			print 'go into _find_num cks......'
			cks = SmartckCom._find_cks_by_num(struct,super_b);
			return cks;
		elif match['func'] == 'time':
			print 'go into _find_cks by time......'
			cks = SmartckCom._find_cks_bytime(struct,super_b);
			return cks;
		elif match['func'] == 'relate':
			print 'go into _find_relate cks......'
			cks = SmartckCom._find_cks_by_relate(struct,super_b);
			return cks;
		elif match['func'] == 'all':
			print 'go into _find_all_cks......'
			cks = super_b.clocks.keys();
			return cks;
		return None;

	def _get_match_info(self,ttag):
		for temp in self.data['template']:
			comp = re.compile(temp['reg']);
			match = comp.search(ttag);
			if not match is None: return temp;
		return None;
