#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,copy
import re,time,math
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
import common,datetime
from myexception import MyException
from common import logging
import scene_param as SceneParam
from scene_base import SceneBase

#直接设置闹铃生效日期
class SceneAble(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into set alarm date able......');
			if not struct.has_key('step'): struct['step'] = 'start';

			if struct['step'] == 'start':
				self._encode_able(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(format(e));

	def _encode_able(self,struct,super_b):
		cks = None;
		if struct['ttag'].find('time_no_call_me_wake') <> -1:
			ptag_id = struct['ttag'].find('time_no_call_me_wake');
			prev_tag = struct['ttag'][:ptag_id];
			cks = SceneParam._find_cks_bytype('getup',super_b);
			if len(cks) == 0:
				SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
				return None;
			for ck in cks:
				clock = super_b.clocks[ck];
				able = 127;
				if clock.has_key('able'): able = int(clock['able']['able']);
				for inter in struct['intervals']:
					if inter['scope'] == 'day':
						times = inter['start'];
						dat = datetime.date(int(times[0]),int(times[1]),int(times[2]));
						week = dat.weekday();
						if int(able) & int(math.pow(2,week)) > 0:
							able = able - math.pow(2,week);
				clock['able']['able'] = able;
			if struct.has_key('intervals'): del struct['intervals'];
		elif struct['ttag'].find('_workday_call') <> -1:
			ptag_id = struct['ttag'].find('_workday_call');
			prev_tag = struct['ttag'][:ptag_id];
			if prev_tag.find('time') <> -1:
				cks = SceneParam._find_cks_bytime(struct,super_b);
			if cks is None or len(cks) == 0:
				cks = SceneParam._find_cks_byinfo(struct,super_b);
			if len(cks) == 0 and super_b.myclock is None:
				SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
				return None;
			elif len(cks) == 0:
				cks.append(super_b.myclock['key']);
			for ck in cks:
				clock = super_b.clocks[ck];
				if not clock.has_key('able'):
					clock['able'] = dict();
					clock['able']['type'] = 'workday';
				clock['able']['able'] = math.pow(2,5) - 1;
		elif struct['ttag'].find('_pass_workday') <> -1:
			ptag_id = struct['ttag'].find('_pass_workday');
			prev_tag = struct['ttag'][:ptag_id];
			if prev_tag.find('time') <> -1:
				cks = SceneParam._find_cks_bytime(struct,super_b);
			if cks is None or len(cks) == 0:
				cks = SceneParam._find_cks_byinfo(struct,super_b);
			if len(cks) == 0 and super_b.myclock is None:
				SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
				return None;
			elif len(cks) == 0:
				cks.append(super_b.myclock['key']);
			for ck in cks:
				clock = super_b.clocks[ck];
				if not clock.has_key('able'):
					clock['able'] = dict();
					clock['able']['type'] = 'workend';
				clock['able']['able'] = math.pow(2,7) - math.pow(2,5);
		elif struct['ttag'].find('_everyday') <> -1:
			ptag_id = struct['ttag'].find('_everyday');
			prev_tag = struct['ttag'][:ptag_id];
			if prev_tag.find('time') <> -1:
				cks = SceneParam._find_cks_bytime(struct,super_b);
			if cks is None or len(cks) == 0:
				cks = SceneParam._find_cks_byinfo(struct,super_b);
			if len(cks) == 0 and super_b.myclock is None:
				SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
				return None;
			elif len(cks) == 0:
				cks.append(super_b.myclock['key']);
			for ck in cks:
				clock = super_b.clocks[ck];
				if not clock.has_key('able'):
					clock['able'] = dict();
					clock['able']['type'] = 'week';
				clock['able']['able'] = math.pow(2,7) - 1;
		SceneParam._set_msg(struct,self.data['msg']['set_able_succ']);
