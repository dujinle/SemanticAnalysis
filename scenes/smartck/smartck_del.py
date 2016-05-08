#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from scene_base import SceneBase
import com_funcs as SceneParam
import smartck_common as SmartckCom

#删除指定的闹钟场景设置
class SmartckDel(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into scene delete action......');
			if not struct.has_key('ck_scene'): return None;
			if struct['ck_scene'] <> 'ck_del': return None;

			if not struct.has_key('step'): struct['step'] = 'start';
			#启动时响应回复
			if struct['step'] == 'start':
				cks = self._find_cks(struct,super_b);
				if cks is None or len(cks) == 0:
					SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
				else:
					self._del_cks(cks,super_b,struct);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _del_cks(self,cks,super_b,struct):
		delnum = 0;
		for ck in cks:
			if super_b.clocks.has_key(ck):
				if not super_b.myclock is None and super_b.myclock['key'] == ck:
					super_b.myclock = None;
				clk = super_b.clocks[ck];
				del super_b.clocks[ck];
				delnum = delnum + 1
			else:
				SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
				return None;
		SceneParam._set_msg(struct,self.data['msg']['del_cks']);

	def _find_cks(self,struct,super_b):
		match = self._get_match_info(struct['ttag']);
		if match is None:
			cks = SmartckCom._find_cks_by_sample(struct,super_b);
			return cks;
		elif match['func'] == 't2t':
			print 'go into _find_cks_time_to_time......'
			cks = SmartckCom._find_cks_time_to_time(struct,super_b);
			return cks;
		elif match['func'] == 'pastdue':
			cks = SmartckCom._find_cks_pastdue(super_b);
			return cks;
		elif match['func'] == 'unuse':
			print 'go into _find__cks_unuse......'
			cks = SmartckCom._find_cks_nouse(super_b);
			return cks;
		elif match['func'] == 'time':
			print 'go into _find__cks_bytime......'
			cks = SmartckCom._find_cks_bytime(struct,super_b);
			return cks;
		elif match['func'] == 'all':
			print 'go into _find_all_cks......'
			cks = super_b.clocks.keys();
			return cks;
		elif match['func'] == 'num':
			print 'go into _find_num cks......'
			cks = SmartckCom._find_cks_by_num(struct,super_b);
			return cks;
		elif match['func'] == 'just':
			cks = list();
			if not super_b.myclock is None: cks.append(super_b.myclock['key']);
			return cks;
		elif match['func'] == 'only_left':
			print 'go into _find_cks by only......'
			cks = SmartckCom._find_cks_by_only(struct,super_b);
			return cks;
		return None;

	def _get_match_info(self,ttag):
		for temp in self.data['template']:
			comp = re.compile(temp['reg']);
			match = comp.search(ttag);
			if not match is None: return temp;
		return None;
