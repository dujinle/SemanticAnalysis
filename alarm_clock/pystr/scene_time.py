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
import scene_param as SceneParam
from common import logging
from myexception import MyException
from base import Base

#修改闹钟时间的场景设置
class SceneTime(Base):

	def encode(self,struct,super_b):
		try:
			logging.info('go into scene modify time......');
			if not struct.has_key('step'): struct['step'] = 'start';

			#启动时响应回复
			if struct['step'] == 'start':
				self._change_cks(struct,super_b);
				struct['step'] = 'end';
		except Exception as e:
			raise MyException(format(e));

	def _change_cks(self,struct,super_b):
		if struct['ttag'].find('_ahead_time_call') <> -1:
			self._change_time_bytag('_ahead_time_call',struct,super_b,'-');
		elif struct['ttag'].find('_defer_time') <> -1:
			self._change_time_bytag('_defer_time',struct,super_b,'+');
		elif struct['ttag'].find('_pass_time_recall') <> -1:
			self._change_time_bytag('_pass_time_recall',struct,super_b,'+');
		elif struct['ttag'].find('_moveto_time') <> -1:
			self._reset_ck_bytag('_moveto_time',struct,super_b);
		elif struct['ttag'].find('_info_swap') <> -1:
			self._swap_cks_info('_info_swap',struct,super_b);
		if struct.has_key('intervals'): del struct['intervals'];

	def _change_time(self,cks,num,scope,tdir,super_b):
		for ck in cks:
			clock = super_b.clocks[ck];
			time = clock['time'];
			tarray = time.split(':');
			hour = int(tarray[0]);
			tmin = int(tarray[1]);
			if scope == 'min':
				if tdic == '-': tmin = tmin - num;
				elif tdic == '+': tmin = tmin + num;
			elif scope == 'hour':
				if tdic == '-': hour = hour - num;
				elif tdic == '+': tmin = tmin + num;
			if tmin >= 60:
				tmin = tmin - 60;
				hour = hour + 1;
			elif tmin < 0:
				tmin = tmin + 60;
				hour = hour - 1;
			clock['time'] = str(hour) + ':' + str(tmin);

	def _change_time_bytag(self,tag,struct,super_b,tdir):
		end = struct['ttag'].find(tag);
		pre_tag = struct['ttag'][:end];
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
			cks.append(super_b.myclock['key']);
		inters = struct['intervals'][0];
		if not inters.has_key('num'):
			struct['result']['msg'] = self.data['msg']['invalid_com'][0];
			return None;
		self._change_time(cks,inters['num'],inters['scope'],tdir);
		if tdir == '-':
			struct['result']['msg'] = (self.data['msg']['ahead_succ'][0] %(inters['num'],self.data[inters['scope']]));
		elif tdir == '+':
			struct['result']['msg'] = (self.data['msg']['defer_succ'][0] %(inters['num'],self.data[inters['scope']]));

	def _swap_cks_info(self,tag,struct,super_b):
		end = struct['ttag'].find(tag);
		pre_tag = struct['ttag'][:end];
		cks = None;
		if pre_tag.find('_and') == -1:
			struct['result']['msg'] = self.data['msg']['swap_unknow'][0];
			return None;
		start_tag = pre_tag[:pre_tag.find('_and')];
		struct['ttag'] = start_tag;
		if start_tag.find('time') <> -1:
			cks = SceneParam._find_cks_bytime(struct,super_b);
			del struct['intervals'][0];
		else:
			cks = SceneParam._find_cks_byinfo(struct,super_b);
		if (cks is None or len(cks) == 0):
			struct['result']['msg'] = self.data['msg']['swap_unknow'][0];
			return None;
		elif not cks is None and len(cks) > 1:
			struct['result']['msg'] = self.data['msg']['more_cks'][0];
			return None;
		start_key = cks[0];
		cks = None;
		second_tag = pre_tag[pre_tag.find('_and') + 4:];
		struct['ttag'] = second_tag;
		if second_tag.find('time') <> -1:
			cks = SceneParam._find_cks_bytime(struct,super_b);
			del struct['intervals'][0];
		else:
			cks = SceneParam._find_cks_byinfo(struct,super_b);

		if (cks is None or len(cks) == 0):
			struct['result']['msg'] = self.data['msg']['swap_unknow'][0];
			return None;
		elif not cks is None and len(cks) > 1:
			struct['result']['msg'] = self.data['msg']['more_cks'][0];
			return None;
		second_key = cks[0];
		start_ck = super_b.clocks[start_key];
		second_ck = super_b.clocks[second_key];
		super_b.clocks[start_key] = second_ck;
		super_b.clocks[second_key] = start_ck;
		struct['result']['msg'] = self.data['msg']['swap_succ'][0];

	def _reset_ck_bytag(self,tag,struct,super_b):
		end = struct['ttag'].find(tag);
		pre_tag = struct['ttag'][:end];
		cks = None;
		if pre_tag.find('_time') <> -1:
			cks = SceneParam._find_cks_bytime(struct,super_b);
			del struct['intervals'][0];
		else:
			cks = SceneParam._find_cks_byinfo(struct,super_b);

		if (cks is None or len(cks) == 0) and super_b.myclock is None:
			struct['result']['msg'] = self.data['msg']['ck_unknow'][0];
			return None;
		elif cks is None or len(cks) == 0:
			if super_b.myclock.has_key('info'): cks.append(super_b.myclock['info']);
			elif super_b.myclock.has_key('time'): cks.append(super_b.myclock['time']);
		self._change_able(struct,cks,super_b);
		self._reset_time(struct,cks,super_b);
		struct['result']['msg'] = self.data['msg']['modify_succ'][0];

	def _change_able(self,struct,cks,super_b):
		inter = struct['intervals'][0];
		if inter['scope'] <> 'day': return None;
		if inter['start'][3] <> 0 or inter['end'][3] <> 0: return None;
		start = inter['start'];
		end = inter['end'];
		week = SceneParam._get_week(start[0],start[1],start[2]);
		able = math.pow(2,week);
		if end[3] - start[3] > 1: able = able + math.pow(2,week + 1);
		for ck in cks:
			clock = super_b.clocks[ck];
			if not clock.has_key('able'):
				clock['able'] = dict();
			clock['able']['able'] = able;
		struct['result']['msg'] = self.data['msg']['ck_able'][0];

	def _reset_time(self,struct,cks,super_b):
		inter = struct['intervals'][0];
		if inter['start'][3] == 0 and inter['end'][3] == 0: return None;
		time = str(inter['start'][3]) + ':' + str(inter['start'][4]);
		for ck in cks:
			clock = super_b.clocks[ck];
			clock['time'] = time;
		struct['result']['msg'] = self.data['msg']['ck_time'][0];

