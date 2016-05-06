#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,re,time,math
import common,datetime
from myexception import MyException
from common import logging
import com_funcs as SceneParam
import smartck_common as SmartckCom
from scene_base import SceneBase

#直接设置闹铃生效日期
class SmartckAble(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into set alarm date able......');
			if not struct.has_key('ck_scene'): return None;
			if struct['ck_scene'] <> 'ck_able': return None;
			if not struct.has_key('step'): struct['step'] = 'start';

			if struct['step'] == 'start':
				self._encode_able(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _encode_able(self,struct,super_b):
		cks = None;
		match = self._get_match_info(struct['ttag'],'template');
		if match is None: return None;
		if match['func'] == 'close_getup':
			cks = SceneParam._find_cks_bytype('getup',super_b);

			if len(cks) == 0:
				SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
				return None;
			for ck in cks:
				clock = super_b.clocks[ck];
				able = 127;
				if clock.has_key('able'): able = int(clock['able']['able']);
				for istr in struct['stseg']:
					if not struct.has_key(istr): continue;
					item = struct['stc'][istr];
					if item['type'] <> 'TIME': continue;
					if item['scope'] == 'day':
						times = item['stime'];
						dat = datetime.date(int(times[0]),int(times[1]),int(times[2]));
						week = dat.weekday();
						if int(able) & int(math.pow(2,week)) > 0:
							able = able - math.pow(2,week);
				clock['able']['able'] = able;
		elif match['func'] == 'workday_ring':
			cks = SceneParam._find_cks_by_sample(struct,super_b);
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
		elif match['func'] == 'workend_close':
			cks = SceneParam._find_cks_by_sample(struct,super_b);
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
		elif match['func'] == 'everyday_ring':
			cks = SceneParam._find_cks_by_sample(struct,super_b);
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

	def _get_match_info(self,ttag,template):
		for temp in self.data[template]:
			comp = re.compile(temp['reg']);
			match = comp.search(ttag);
			if not match is None: return temp;
		return None;
