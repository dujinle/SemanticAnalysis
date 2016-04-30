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
import common,datetime,math
from common import logging
from myexception import MyException
from scene_base import SceneBase
import scene_param as SceneParam

#删除指定的闹钟场景设置
class SceneDel(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into scene delete action......');
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
		info = '';
		delnum = 0;
		if struct['ttag'].find('_only_left_time') <> -1:
			for ck in super_b.clocks.keys():
				if ck in cks: continue;
				clk = super_b.clocks[ck];
				if clk.has_key('info'): info = clk['info'];
				if not super_b.myclock is None and super_b.myclock['key'] == ck:
					super_b.myclock = None;
				del super_b.clocks[ck];
				delnum = delnum + 1;
		else:
			for ck in cks:
				if super_b.clocks.has_key(ck):
					if not super_b.myclock is None and super_b.myclock['key'] == ck:
						super_b.myclock = None;
					clk = super_b.clocks[ck];
					if clk.has_key('info'): info = clk['info'];
					del super_b.clocks[ck];
					delnum = delnum + 1
				else:
					SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
					return None;
		SceneParam._set_msg(struct,self.data['msg']['del_cks']);

	def _find_cks(self,struct,super_b):
		match = self._get_match_info(struct['ttag']);
		common.print_dic(match);
		if match is None: return None;
		if match['func'] == 't2t':
			print 'go into _find_cks_time_to_time......'
			cks = SceneParam._find_cks_time_to_time(struct,super_b);
			return cks;
		if match['func'] == 'time':
			cks = SceneParam._find_cks_bytime(struct,super_b);
			return cks;
		if match['func'] == 'info':
			cks = SceneParam._find_cks_byinfo(struct,super_b);
			return cks;
		if match['func'] == 'pastdue':
			cks = SceneParam._find_cks_pastdue(super_b);
			return cks;
		if match['func'] == 'all':
			print 'go into _find_all_cks......'
			cks = super_b.clocks.keys();
			return cks;
		if match['func'] == 'num':
			print 'go into _find_num cks......'
			cks = SceneParam._find_cks_by_num(struct,super_b);
			return cks;
		if match['func'] == 'just':
			cks = list();
			if not super_b.myclock is None: cks.append(super_b.myclock['key']);
			return cks;
		if match['func'] == 'nouse':
			cks = SceneParam._find_cks_nouse(super_b);
			return cks;
		return None;

	def _get_match_info(self,ttag):
		for temp in self.data['template']:
			comp = re.compile(temp['reg']);
			match = comp.search(ttag);
			if not match is None: return temp;
		return None;
