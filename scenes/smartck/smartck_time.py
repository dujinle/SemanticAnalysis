#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,re,common
from common import logging
import com_funcs as SceneParam
import smartck_common as SmartckCom
from myexception import MyException
from scene_base import SceneBase

#修改闹钟时间的场景设置
class SmartckTime(SceneBase):

	def encode(self,struct,super_b):
		try:
			if not struct.has_key('ck_scene'): return None;
			if struct['ck_scene'] <> 'ck_time': return None;
			logging.info('go into scene modify time......');
			if not struct.has_key('step'): struct['step'] = 'start';

			#启动时响应回复
			if struct['step'] == 'start': self._change_cks(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _change_cks(self,struct,super_b):
		cks = self._find_cks(struct,super_b);
		if cks is None or len(cks) == 0:
			cks = [super_b.myclock['key']];

		if struct['ttag'].find('AHEAD') <> -1:
			self._change_time(cks,struct,'prev',super_b);
		elif struct['ttag'].find('DELAY') <> -1:
			self._change_time(cks,struct,'after',super_b);
		elif struct['ttag'].find('PASS') <> -1:
			self._change_time(cks,struct,'after',super_b);
		elif struct['ttag'].find('MOVETO') <> -1:
			self._change_able(struct,cks,super_b);
			self._reset_time(struct,cks,super_b);
		elif struct['ttag'].find('CONTENTSWAP') <> -1:
			self._swap_cks_info(cks,struct,super_b);

	def _change_time(self,cks,struct,tdir,super_b):
		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item['type'] <> 'TIME': continue;
			for ck in cks:
				clock = super_b.clocks[ck];
				time = clock['time'];
				tarray = time.split(':');
				hour = int(tarray[0]);
				tmin = int(tarray[1]);
				num = item['num'];
				if inters['scope'] == 'min':
					if tdir == 'prev': tmin = tmin - int(num);
					elif tdir == 'after': tmin = tmin + int(num);
				elif inters['scope'] == 'hour':
					if tdir == 'prev': hour = hour - int(num);
					elif tdir == 'after': hour = hour + int(num);
				if tmin >= 60:
					tmin = tmin - 60;
					hour = hour + 1;
				elif tmin < 0:
					tmin = tmin + 60;
					hour = hour - 1;
				clock['time'] = str(hour) + ':' + str(tmin);

	def _swap_cks_info(self,cks,struct,super_b):
		if len(cks) <> 2:
			SceneParam._set_msg(struct,self.data['msg']['more_cks']);
			return None;
		start_key = cks[0];
		second_key = cks[1];
		start_ck = super_b.clocks[start_key];
		second_ck = super_b.clocks[second_key];
		super_b.clocks[start_key] = second_ck;
		super_b.clocks[second_key] = start_ck;
		SceneParam._set_msg(struct,self.data['msg']['swap_succ']);

	def _change_able(self,struct,cks,super_b):
		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item['type'] <> 'TIME': continue;
			start = item['stime'];
			end = item['etime'];
			able = SceneParam._get_time_able(start,end);
			for ck in cks:
				clock = super_b.clocks[ck];
				if not clock.has_key('able'):
					clock['able'] = dict();
				clock['able']['able'] = able;
			SceneParam._set_msg(struct,self.data['msg']['ck_able']);
			break;

	def _reset_time(self,struct,cks,super_b):
		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item['type'] <> 'TIME': continue;
			if item['stime'][3] == 'null' and item['end'][3] == 'null': return None;
			if item['stime'][4] == 'null':
				time = str(item['stime'][3]) + ':0';
			else:
				time = str(item['stime'][3]) + ':' + str(item['stime'][4]);
			for ck in cks:
				clock = super_b.clocks[ck];
				clock['time'] = time;
			SceneParam._set_msg(struct,self.data['msg']['ck_time']);
			break;

	def _find_cks(self,struct,super_b):
		match = self._get_match_info(struct['ttag'],'template');
		if match is None: return None;
		if match['func'] == 't2t':
			print 'go into _find_cks_time_to_time......'
			cks = SmartckCom._find_cks_time_to_time(struct,super_b);
			return cks;
		elif match['func'] == 'tat':
			cks = SmartckCom._find_cks_time_and_time(struct,super_b);
			return cks;
		elif match['func'] == 'after':
			cks = SmartckCom._find_cks_after(struct,super_b);
			return cks;
		else:
			cks = SmartckCom._find_cks_by_sample(struct,super_b);
			return cks;
		return None;

	def _get_match_info(self,ttag,template):
		for temp in self.data[template]:
			comp = re.compile(temp['reg']);
			match = comp.search(ttag);
			if not match is None: return temp;
		return None;
