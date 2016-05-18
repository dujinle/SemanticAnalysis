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
import common,alarm_common,pgsql
from myexception import MyException
from base import Base
class AlarmAdd(Base):

	def encode(self,struct,super_b):
		try:
			print 'go into alarm add action';
			if self._if_exist(struct,super_b):
				struct['result']['msg'] = self.data['alarm_exist'][0];
				struct['result']['extra'] = self.data['help_modifye'][0];
				struct['code'] = 'error';
				return None;
			if super_b.myclock is None:
				super_b.myclock = dict();
			elif super_b.action is None and super_b.myclock.has_key('time'):
				super_b.myclock = dict();
			self._deal_getup_tag(struct,super_b);
			self._set_clock(struct,super_b);
			self._analysis(struct,super_b);
		except Exception as e:
			raise MyException(format(e));

	def _set_clock(self,struct,super_b):
		myclock = super_b.myclock;
		if struct.has_key('ck_name') and struct['ck_name'] <> '':
			if not myclock.has_key('time') or myclock['time'] <> struct['ck_name']:
				myclock['name'] = struct['ck_name'];

		if struct.has_key('ck_time'):
			myclock['time'] = struct['ck_time']['time'];
			self._make_getup_tag(struct,super_b);
			del struct['ck_time'];

		if struct.has_key('ck_delay'):
			myclock['delay'] = struct['ck_delay'];
			del struct['ck_delay'];

		if struct.has_key('ck_able'):
			myclock['able'] = struct['ck_able'];
			del struct['ck_able'];
		return 0;

	def _analysis(self,struct,super_b):
		if not struct.has_key('result'): return None;
		result = struct['result'];
		if result.has_key('msg'): return None;

		ck = super_b.myclock;
		if self._analysis_mytag(struct,super_b): return None;

		if not ck.has_key('time'):
			struct['result']['msg'] = self.data['time'][0];
			return None;

		ck['status'] = 'on';
		struct['result']['msg'] = self.data['add_suc'][0];
		struct['code'] = 'success';
		return None;

	def _if_exist(self,struct,super_b):
		if struct.has_key('ck_name'):
			ck_name = struct['ck_name'];
			if super_b.clocks.has_key(ck_name): return True;
		if struct.has_key('ck_time'):
			ck_time = struct['ck_time']['time'];
			if super_b.clocks.has_key(ck_time): return True;
		return False;

	def _deal_getup_tag(self,struct,super_b):
		if super_b.myclock.has_key('question') and super_b.myclock['question'] == 'getup':
			yes = False;
			for ck in struct['clocks']:
				if ck['type'] == 'yes':
					yes = True;
					break;
			if yes == True:
				super_b.myclock['name'] = super_b.myclock['tname'];
				mydic = dict();
				mydic['value'] = super_b.myclock['time'];
				mydic['type'] = 'time';
			del super_b.myclock['tname'];
			del super_b.myclock['question'];

	def _make_getup_tag(self,struct,super_b):
		myclock = super_b.myclock;
		ctime = struct['ck_time'];
		hour = ctime['time'].split(':')[0];
		if int(hour) > 9 or (struct.has_key('ck_name') and struct['ck_name'] == u'起床') \
			or super_b.clocks.has_key(u'起床'):
			pass;
		else:
			struct['result']['msg'] = self.data['tag_getup'][0];
			myclock['question'] = 'getup';
			myclock['tname'] = u'起床';
			return 1;
		return 0;

	def _analysis_mytag(self,struct,super_b):
		ck = super_b.myclock;
		if struct.has_key('tag') and ck.has_key('name') and struct['tag'].has_key(ck['name']):
			usual_time = struct['tag'][ck['name']];
			mytime = ck['time'];
			if usual_time['type'] == 'time':
				uhour = usual_time['value'].split(':')[0];
				umin = usual_time['value'].split(':')[1];
				mhour = mytime.split(':')[0];
				mmin = mytime.split(':')[1];
				if int(uhour) > int(mhour):
					struct['result']['msg'] = self.data['getup_early'][0];
				elif int(uhour) == int(mhour) and int(mmin) < int(umin) + 20:
					struct['result']['msg'] = self.data['getup_early'][0];
				else:
					struct['result']['msg'] = self.data['add_suc'][0];
				ck['status'] = 'on';
				struct['code'] = 'success';
				return True;
		return False;

	def _save_tag(self,super_b):
		try:
			mydic = dict();
			mydic['value'] = super_b.myclock['time'];
			mydic['type'] = 'time';
			mydic['name'] = super_b.myclock['name'];
			sql = 'insert into mytags (jobdesc) values (' + json.dumps(mydic) + ')';
			cur = pgsql.pg_cursor();
			pgsql.pg_query(cur,sql,None);
			pgsql.pg_commit(super_b.p_conn);
			pgsql.pg_cursor_close(cur);
		except Exception as e:
			raise e;

