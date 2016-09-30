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
				cks = self._get_match_cks(struct,super_b);
				if cks is None or len(cks) == 0:
					SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
				else:
					self._del_cks(cks,super_b,struct);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(format(e));

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
		msg_id = SceneParam._get_random_id(len(self.data['msg']['del_cks']));
		struct['result']['msg'] = self.data['msg']['del_cks'][msg_id];
		'''
		if delnum > 1 and len(info) > 0:
			struct['result']['msg'] = (self.data['msg']['del_cks'][0] %(info,u'等'));
		else:
			struct['result']['msg'] = (self.data['msg']['del_cks'][0] %(info,''));
		'''

	def _get_match_cks(self,struct,super_b):
		cks = list();
		ttag = struct['ttag'];
		if len(re.findall('((_del)|(_cancle))_pastdue_clock',ttag)) > 0:
			cks = SceneParam._find_cks_pastdue(super_b);
		elif len(re.findall('(_cancle)|(_del)_all_clock',ttag)) > 0:
			cks = super_b.clocks.keys();
		elif len(re.findall('_all((_clock)|(_remind)).*(_cancle)|(_del)',ttag)) > 0:
			cks = super_b.clocks.keys();
		#处理 删除/取消.....闹钟/提醒
		elif len(re.findall('((_cancle)|(_del)).*_clock',ttag)) > 0:
			cks = self._get_cks_by_tag(struct,super_b,'_clock');
		elif len(re.findall('((_cancle)|(_del)).*_remind',ttag)) > 0:
			cks = self._get_cks_by_tag(struct,super_b,'_remind');
		#....闹钟/提醒....删了/不要了
		elif len(re.findall('.*_clock(_all)*((_no)|(_del)|(_cancle))',ttag)) > 0:
			cks = self._get_cks_by_tag(struct,super_b,'_clock');
		elif len(re.findall('.*_remind(_all)*((_no)|(_del)|(_cancle))',ttag)) > 0:
			cks = self._get_cks_by_tag(struct,super_b,'_remind');
		elif len(re.findall('_time(_all)*((_no)|(_del)|(_cancle))',ttag)) > 0:
			cks = self._get_cks_by_tag(struct,super_b,None);
		elif len(re.findall('_time',ttag)) > 0:
			cks = self._get_cks_by_tag(struct,super_b,None);
		elif len(re.findall('_prep((_del)|(_cancle))',ttag)) > 0:
			cks = SceneParam._find_cks_prep(struct,super_b);
		elif len(re.findall('_just_that((_no)|(_del)|(_cancle))',ttag)) > 0:
			if super_b.myclock is None: return None;
			cks = list();
			cks.append(super_b.myclock['key']);
		elif len(re.findall('_nouse((_no)|(_del)|(_cancle))',ttag)) > 0:
			cks = SceneParam._find_cks_nouse(super_b);
		return cks

	def _get_cks_by_tag(self,struct,super_b,tag):
		ttag = struct['ttag'];
		pre_tag = ttag;
		if not tag is None: pre_tag = ttag[:ttag.find(tag)];
		cks = None;
		if pre_tag.find('time') <> -1:
			cks = SceneParam._find_cks_bytime(struct,super_b);
			del struct['intervals'][0];
		else:
			cks = SceneParam._find_cks_byinfo(struct,super_b);
		if (cks is None or len(cks) == 0) and super_b.myclock is None:
			struct['result']['msg'] = self.data['msg']['ck_unknow'][0];
			return None;
		elif cks is None or len(cks) == 0:
			cks = list();
			cks.append(super_b.myclock['key']);
		return cks;

