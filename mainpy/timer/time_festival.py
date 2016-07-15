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
import time_common
import time_calendar
from myexception import MyException
from base import Base

class FT(Base):

	def encode(self,struct):
		try:
			intext = struct['text'];
			rlist = time_common._if_has_key(intext,self.data['keys']);
			regs = self.data['regs'];
			for key in rlist:
				self._match_reg(struct,key);
		except MyException as e: raise e;

	def _match_reg(self,struct,key):
		if not struct.has_key('taglist'): struct['taglist'] = list();
		text = struct['text'];
		regs = self.data['regs'];
		matchs = dict();
		tregs = dict();
		for reg in regs:
			regtr = '|'.join(reg['same']);
			if regtr.find(key) == -1: continue;
			comp = re.compile(regtr);
			match = comp.search(text);
			if match is None: continue;
			matchs[key] = match;
			tregs[key] = reg;
		if len(matchs) == 0: return None;
		mykey = time_common._make_only_one(matchs);
		match = matchs[mykey];
		reg = tregs[mykey];

		tmat = match.group(0);
		idx = time_common._find_idx(text,tmat,'null');
		tdic = copy.deepcopy(reg);
		tdic['value'] = tmat;
		tdic['type'] = 'time_ft';
		struct['taglist'].insert(idx,tdic);
		struct['text'] = text.replace(tdic['value'],'FT',1);


	def _add(self,data):
		try:
			scope = data['scope'];
			interval = json.loads(data['interval']);
			value = data['value'];
			func = data['func'];
			mdata = self.data;
			if value in mdata['keys']:
				for tt in mdata['regs']:
					if value in tt['same']:
						tt['scope'] = scope;
						tt['func'] = func;
						tt['interval'] = interval;
						break;
			else:
				mdata['keys'].append(value);
				tdic = dict();
				tdic['same'] = [value];
				tdic['scope'] = scope;
				tdic['func'] = func;
				tdic['interval'] = interval;
				mdata['regs'].append(tdic);
		except Exception as e:
			raise MyException(format(e));

	def _del(self,data):
		try:
			value = data['value'];
			mdata = self.data;
			if value in mdata['keys']:
				for tt in mdata['regs']:
					if value in tt['same']:
						tt['same'].remove(value);
						if len(tt['same']) == 0:
							mdata['regs'].remove(tt);
							mdata['keys'].remove(value);
						break;
		except Exception as e:
			raise MyException(format(e));


class FTE(Base):

	def encode(self,struct):
		try:
			intext = struct['text'];
			rlist = time_common._if_has_key(intext,self.data['keys']);
			regs = self.data['regs'];
			for key in rlist:
				self._match_reg(struct,key);
			self._make_interval(struct);
		except MyException as e: raise e;

	def _match_reg(self,struct,key):
		if not struct.has_key('taglist'): struct['taglist'] = list();
		text = struct['text'];
		regs = self.data['regs'];
		matchs = dict();
		tregs = dict();
		for reg in regs:
			regtr = '|'.join(reg['same']);
			if regtr.find(key) == -1: continue;
			myreg = reg['reg'].replace('K','(' + regtr + ')');
			comp = re.compile(myreg);
			match = comp.search(text);
			if match is None: continue;
			matchs[reg['reg']] = match;
			tregs[reg['reg']] = reg;
		if len(matchs) == 0: return None;
		mykey = time_common._make_only_one(matchs);
		match = matchs[mykey];
		reg = tregs[mykey];

		tmat = match.group(0);
		tdic = dict();
		tdic.update(reg);
		tdic['value'] = tmat.replace('NT','');
		tdic['type'] = 'time_nte';
		self._insert_taglist(struct,tdic,tmat,key);
		nt_num = len(re.findall('NT',tmat));
		struct['text'] = text.replace(tmat,('NTE') * nt_num,1);

	def _insert_taglist(self,struct,tdic,tmat,key):
		taglist = struct['taglist'];
		text = struct['text'];
		first_idx = time_common._find_idx(text,tmat,'null');
		tag = taglist[first_idx];
		if tdic['position'] == 'left':
			tag['times'].insert(0,tdic);
		elif tdic['position'] == 'right':
			tag['times'].append(tdic);
		tag['type'] = 'time_nte';

	# 找到一个扩展的修饰时间词组 则可以进行区间的计算 为后续使用 #
	def _make_interval(self,struct):
		if not struct.has_key('taglist'): return None;
		taglist = struct['taglist'];
		for tag in taglist:
			if tag['type'] == 'time_nte':
				times = tag['times'];
				t_num = len(times);
				nt_num = tag['ntimes'];
				nte_num = t_num - nt_num;
				while nte_num > 0:
					for tt in times:
						if tt['type'] == 'time_nte':
							#处理 『大大』NT的模型#
							if tt['position'] == 'left':
								if tt['dir'] == 'off':
									v_num = len(tt['value']);
									mytime = times[times.index(tt) + 1];
									interval = mytime['interval'];
									if int(interval[0]) > 0:
										mytime['interval'][0] = interval[0] + v_num;
										mytime['interval'][1] = interval[1] + v_num;
									elif int(interval[0]) < 0:
										mytime['interval'][0] = interval[0] - v_num;
										mytime['interval'][1] = interval[1] - v_num;
							elif tt['position'] == 'right':
								mytime = times[times.index(tt) - 1];
								if tt['dir'] == '-':
									mytime['interval'] = ['<',mytime['interval'][0]];
								elif tt['dir'] == '+':
									mytime['interval'] = [mytime['interval'][1],'>'];
							nte_num = nte_num - 1;

#计算ft模式下的时间区间包括FTE模式
class CFTE(Base):
	def encode(self,struct):
		try:
			if not struct.has_key('taglist'): return None;
			curtime = time.localtime();
			taglist = struct['taglist'];
			for tag in taglist:
				if tag['type'] == 'time_ft':
					self._calc_ft_date_time(curtime,tag);
		except MyException as e: raise e;

	def _calc_ft_date_time(self,curtime,tag):
		start_time = list(curtime);
		end_time = list(curtime);
		date = tag['date'];
		mon = date.split('/')[0];
		day = date.split('/')[1];
		idx = time_common.tmenu['month'];
		start_time[idx] = int(mon);
		end_time[idx] = int(mon);
		idx = time_common.tmenu['day'];
		start_time[idx] = int(day);
		if tag['year_type'] == 'lunar':
			(year,month,day) = time_calendar.ToSolarDate(start_time[0],start_time[1],start_time[2]);
			start_time[0] = end_time[0] = year;
			start_time[1] = end_time[1] = month;
			start_time[2] = end_time[2] = day;
		end_time[idx] = end_time[idx] + 1;
		start_time[idx + 1:] = [0] * (len(start_time) - idx - 1);
		end_time[idx + 1:] = [0] * (len(end_time) - idx - 1);
		time_common._make_sure_time(start_time,idx);
		time_common._make_sure_time(end_time,idx);
		tag['interval'] = [start_time,end_time];

