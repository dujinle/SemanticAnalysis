#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,copy
import re,time,math,datetime
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
import common,pgsql
from myexception import MyException

class MyTagEncode():
	def __init__(self):
		self.data = dict();

	def encode(self,struct):
		try:
			self._deal_getup_tag(struct,u'起床');
		except MyException as e: raise e;

	def _get_tags(self,mtype):
		p_conn = pgsql.pg_conncet();
		p_cur = pgsql.pg_cursor(p_conn);
		pquery = pgsql.pg_query(p_cur,'SELECT tag FROM mytags WHERE tag->>\'name\'=\'' + mtype + '\' ORDER BY creat_time DESC',None);
		res = p_cur.fetchall();
		result = list();
		for re in res: result.append(re[0]);
		pgsql.pg_close_cursor(p_cur);
		return result;

	def _deal_getup_tag(self,struct,tagname):
		res = self._get_tags(tagname);
		i = j = None;
		t_hour = t_min = 0;
		for i,j in enumerate(res):
			if j['type'] <> 'time': break;
			if i >= 3: break;
			hour = j['value'].split(':')[0];
			mins = j['value'].split(':')[1];
			t_hour = t_hour + int(hour);
			t_min = t_min + int(mins);
		myhour = t_hour // i;
		mymin = (t_min + myhour % i * 60) // i;
		if not struct.has_key('tag'): struct['tag'] = dict();
		getup_tag = dict();
		getup_tag['type'] = 'time';
		getup_tag['name'] = tagname;
		getup_tag['value'] = str(myhour) + ':' + str(mymin);
		struct['tag'][tagname] = getup_tag;

struct = dict();
s = MyTagEncode();
s.encode(struct);
print common.print_dic(struct);
