#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,copy
import re,time,math

import common
from common import logging
import scene_param as SceneParam
from myexception import MyException
from scene_base import SceneBase

#修改闹钟时间的场景设置
class SceneTime(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into scene modify time......');
			if not struct.has_key('step'): struct['step'] = 'start';

			#启动时响应回复
			if struct['step'] == 'start':
				self._change_cks(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _change_cks(self,struct,super_b):
		cks = self._find_cks(struct,super_b);
		if cks is None or len(cks) == 0:
			SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
			return None;
		if struct['ttag'].find('_ahead_time') <> -1:
			self._change_time(cks,struct,'prev',super_b);
		elif struct['ttag'].find('_defer_time') <> -1:
			self._change_time(cks,struct,'after',super_b);
		elif struct['ttag'].find('_pass_time_recall') <> -1:
			self._change_time(cks,struct,'after',super_b);
		elif struct['ttag'].find('_moveto_time') <> -1:
			self._change_able(struct,cks,super_b);
			self._reset_time(struct,cks,super_b);
		elif struct['ttag'].find('_info_swap') <> -1:
			self._swap_cks_info(cks,struct,super_b);
		if struct.has_key('intervals'): del struct['intervals'];

	def _change_time(self,cks,struct,tdir,super_b):
		inters = struct['intervals'][0];
		if not inters.has_key('num'):
			SceneParam._set_msg(struct,self.data['msg']['invalid_com']);
			return None;
		for ck in cks:
			clock = super_b.clocks[ck];
			time = clock['time'];
			tarray = time.split(':');
			hour = int(tarray[0]);
			tmin = int(tarray[1]);
			num = inters['num'];
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
		common.print_dic(cks);
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
		inter = struct['intervals'][0];
		start = inter['start'];
		end = inter['end'];
		able = SceneParam._get_time_able(start,end);
		for ck in cks:
			clock = super_b.clocks[ck];
			if not clock.has_key('able'):
				clock['able'] = dict();
			clock['able']['able'] = able;
		SceneParam._set_msg(struct,self.data['msg']['ck_able']);

	def _reset_time(self,struct,cks,super_b):
		inter = struct['intervals'][0];
		if inter['start'][3] == 'null' and inter['end'][3] == 'null': return None;
		if inter['start'][4] == 'null':
			time = str(inter['start'][3]) + ':0';
		else:
			time = str(inter['start'][3]) + ':' + str(inter['start'][4]);
		for ck in cks:
			clock = super_b.clocks[ck];
			clock['time'] = time;
		SceneParam._set_msg(struct,self.data['msg']['ck_time']);

	def _find_cks(self,struct,super_b):
		match = self._get_match_info(struct['ttag'],'template');
		if match is None: return None;
		common.print_dic(match);
		if match['func'] == 't2t':
			print 'go into _find_cks_time_to_time......'
			cks = SceneParam._find_cks_time_to_time(struct,super_b);
			del struct['intervals'][0];
			del struct['intervals'][0];
			return cks;
		if match['func'] == 'time':
			cks = SceneParam._find_cks_bytime(struct,super_b);
			del struct['intervals'][0];
			return cks;
		if match['func'] == 'info':
			print 'go into _find info cks......'
			cks = SceneParam._find_cks_byinfo(struct,super_b);
			if cks is None or len(cks) == 0:
				tmatch = self._get_match_info(struct['ttag'],'temptag');
				if not tmatch is None:
					print 'go into _find tag name......'
					name = SceneParam._find_tag_name(struct,tmatch);
					if not name is None and len(name) > 0 and super_b.clocks.has_key(name): return [name];
			else:
				return cks;
		if match['func'] == 'tat':
			print 'go into _find_time and time_cks......'
			cks = SceneParam._find_cks_time_and_time(struct,super_b);
			del struct['intervals'][0];
			del struct['intervals'][0];
			return cks;
		if match['func'] == 'this':
			if not super_b.myclock is None:
				cks = [super_b.myclock['key']];
				return cks;
		return None;

	def _get_match_info(self,ttag,template):
		for temp in self.data[template]:
			comp = re.compile(temp['reg']);
			match = comp.search(ttag);
			if not match is None: return temp;
		return None;
