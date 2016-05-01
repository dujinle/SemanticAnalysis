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
import common
from common import logging
from myexception import MyException
import scene_param as SceneParam
from base import Base

class SceneClose(Base):

	def encode(self,struct,super_b):
		try:
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
		ms = self._get_match_info(struct['ttag']);
		if len(ms) == 0: return None;
		for match in ms:
			if match['func'] == 't2t':
				print 'go into _find_cks_time_to_time......'
				cks = SceneParam._find_cks_time_to_time(struct,super_b);
				if cks is None or len(cks) == 0: continue;
				return cks;
			if match['func'] == 'time':
				print 'go into _find_cks_time......'
				cks = SceneParam._find_cks_bytime(struct,super_b);
				if cks is None or len(cks) == 0: continue;
				return cks;
			if match['func'] == 'info':
				print 'go into _find_cks_info......'
				cks = SceneParam._find_cks_byinfo(struct,super_b);
				if cks is None or len(cks) == 0: continue;
				return cks;
			if match['func'] == 'pastdue':
				cks = SceneParam._find_cks_pastdue(super_b);
				if cks is None or len(cks) == 0: continue;
				return cks;
			if match['func'] == 'all':
				print 'go into _find_all_cks......'
				cks = super_b.clocks.keys();
				if cks is None or len(cks) == 0: continue;
				return cks;
			if match['func'] == 'num':
				print 'go into _find_num cks......'
				cks = SceneParam._find_cks_by_num(struct,super_b);
				if cks is None or len(cks) == 0: continue;
				return cks;
			if match['func'] == 'just':
				cks = list();
				if not super_b.myclock is None: cks.append(super_b.myclock['key']);
				if cks is None or len(cks) == 0: continue;
				return cks;
			if match['func'] == 'nouse':
				cks = SceneParam._find_cks_nouse(super_b);
				if cks is None or len(cks) == 0: continue;
				return cks;
		return None;

	def _get_match_info(self,ttag):
		mtsc = list();
		for temp in self.data['template']:
			comp = re.compile(temp['reg']);
			match = comp.search(ttag);
			if not match is None: mtsc.append(temp);
		return mtsc;
