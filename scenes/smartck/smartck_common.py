#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common
import re,time,random
import math,datetime
from common import logging
from myexception import MyException

base_path = os.path.dirname(__file__);
dfile = os.path.join(base_path,'./tdata/smartck_common.txt')
data = common.read_json(dfile);

def _fetch_time(struct):
	for istr in struct['stseg']:
		if not struct['stc'].has_key(istr): continue;
		item = struct['stc'][istr];
		if item['type'] <> 'TIME': continue;

		times = item['stime'];
		if item['scope'] == 'day' or item['scope'] == 'hour'\
			or item['scope'] == 'min' or item['scope'] == 'sec':
			tdic = dict();
			tdic['date'] = str(times[0]) + '/' + str(times[1]) + '/' + str(times[2]);
			struct['ck_date'] = tdic;
		if times[3] <> 'null':
			tdic = dict();
			if times[4] == 'null':
				tdic['time'] = str(times[3]) + ':0';
			else:
				tdic['time'] = str(times[3]) + ':' + str(times[4]);
			tdic['str'] = item['str'];
			struct['ck_time'] = tdic;
		elif item.has_key('mvalue'):
			times = time.localtime(item['mvalue']);
			tdic = dict();
			tdic['time'] = str(times[3]) + ':' + str(times[4]);
			tdic['str'] = item['str'];
			struct['ck_time'] = tdic;
		struct['stc'].remove(item);
		break;

def _calc_able(struct):
	if struct.has_key('ck_date'):
		date = struct['ck_date'];
		tdic = dict();
		dates = date['date'].split('/');
		dat = datetime.date(int(dates[0]),int(dates[1]),int(dates[2]));
		week = dat.weekday();
		able = math.pow(2,week);
		tdic['type'] = 'week';
		tdic['repeat'] = 'repeat';
		tdic['able'] = able;
		del struct['ck_date'];
		struct['ck_able'] = tdic;

def _find_ck_name(struct):
	reg_str = '';
	for item in data['template']:
		match = re.findall(item['reg'],struct['ttag']);
		for itr in match:
			if itr == '': continue;
			reg_str = itr;
			break;
	ck_name = '';
	while True:
		if len(reg_str) == 0: break;

		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr):
				if reg_str.find(istr) == 0:
					ck_name = ck_name + istr;
					reg_str = reg_str[len(istr) - 1:];
			else:
				item = struct['stc'][istr];
				comp = re.compile(item['type']);
				mm = comp.match(reg_str);
				if mm is None: continue;
				ck_name = ck_name + istr;
				reg_str = reg_str[len(istr) - 1:];
	return ck_name;

#get the name info after the label
def _find_tag_name(struct,tdic):
	name = None;
	idx = ftag = 0;
	first_tag = last_tag = -1;
	str_list = list();
	for ck in struct['clocks']:
		if tdic['start']['tag'] == '': ftag = 1;
		#break than go to the index of end
		if isinstance(ck,dict):
			if tdic['end']['tag'] <> '' and ck['type'] == tdic['end']['tag']:
				if tdic['end']['type'] == 'left':
					str_list.append(ck['mystr']);
					last_tag = idx;
				break;
			elif tdic['start']['tag'] <> '' and ck['type'] == tdic['start']['tag']:
				if tdic['start']['type'] == 'left':
					str_list.append(ck['mystr']);
					if first_tag == -1: first_tag = idx;
				ftag = 1;
			elif ftag == 1:
				last_tag = idx;
				str_list.append(ck['mystr']);
				if first_tag == -1: first_tag = idx;
		elif ftag == 1:
			last_tag = idx;
			str_list.append(ck);
			if first_tag == -1: first_tag = idx;
		idx = idx + 1;
	if len(str_list) == 0: return None;
	#common.print_dic(str_list);
	#print first_tag,last_tag

	if tdic['ftag'] == 'break':
		start = 0;
		end = len(str_list);
		while True:
			if first_tag >= len(struct['clocks']): break;
			ck = struct['clocks'][first_tag];
			if isinstance(ck,dict):
				first_tag = first_tag + 1;
				start = start + 1;
			else:
				break;
		while True:
			if last_tag < 0: break;
			ck = struct['clocks'][last_tag];
			if isinstance(ck,dict):
				last_tag = last_tag - 1;
				end = end - 1;
			else:
				break;
		if end <= 0: return None;
		if start >= len(str_list): return None;
		name = ''.join(str_list[start:end]);
	else:
		name = ''.join(str_list);
	return name;

def _find_cks_bytime(struct,super_b):
	cks = list();
	inter = None;
	for istr in struct['stseg']:
		if not struct['stc'].has_key(istr): continue;
		item = struct['stc'][istr];
		if item['type'] == 'TIME':
			inter = dict(item);
			del struct['stc'][istr];
			break;
	if inter is None: return cks;

	start = inter['stime'];
	end = inter['etime'];
	able = _get_time_able(start,end);
	hid = 3;
	mid = 4;
	for ck in super_b.clocks:
		clock = super_b.clocks[ck];
		hour = int(clock['time'].split(':')[0]);
		mins = int(clock['time'].split(':')[1]);
		#print hour,mins,able,start,end
		if start[hid] == 'null' and end[hid] == 'null':
			if clock.has_key('able') and int(clock['able']['able']) & int(able) > 0:
				cks.append(ck);
		elif start[0] == 'null':
			if end[hid] <> 'null' and hour > end[hid]: continue;
			elif end[mid] <> 'null' and hour == end[hid] and mins > end[mid]: continue;
			elif clock.has_key('able') and int(clock['able']['able']) & int(able) > 0:
				cks.append(ck);
		elif end[0] == 'null':
			if start[hid] <> 'null' and hour < start[hid]: continue;
			elif start[mid] <> 'null' and mins < start[mid]: continue;
			elif clock.has_key('able') and int(clock['able']['able']) & int(able) > 0:
				cks.append(ck);
		else:
			if start[hid] <> 'null' and hour < start[hid]: continue;
			if start[mid] <> 'null' and hour == start[hid] and start[mid] > mins: continue;

			if end[hid] <> 'null' and hour > end[hid]: continue;
			#if end[mid] == 'null' and hour == end[hid]: continue;
			if end[mid] <> 'null' and hour == end[hid] and end[mid] < mins: continue;
			if clock.has_key('able') and int(clock['able']['able']) & int(able) > 0:
				cks.append(ck);
	return cks;

def _find_cks_by_relate(struct,super_b):
	cks = list();
	tdic = _make_tag_dic('AND','filter','RELATETO','filter','continue');
	info = _find_tag_name(struct,tdic);
	if info is None: return cks;
	for ck in super_b.clocks.keys():
		clock = super_b.clocks[ck];
		if clock.has_key('info') and clock['info'].find(info) >= 0:
			cks.append(ck);
	return cks;

def _find_cks_by_sample(struct,super_b):
	cks = list();
	if struct.has_key('ck_tag'):
		ck_tag = struct['ck_tag'];
		if ck_tag['type'] == 'time':
			return self._find_cks_bytime(struct,super_b);
		else:
			if super_b.clocks.has_key(struct['ck_name']):
				cks.append(struct['ck_name']);
				del struct['ck_name'];
				return cks;

def _find_cks_byinfo(struct,super_b):
	cks = list();
	if struct.has_key('ck_name'):
		if super_b.clocks.has_key(struct['ck_name']):
			cks.append(struct['ck_name']);
		del struct['ck_name'];
	elif struct['ttag'].find('_prev_prep_clock') <> -1:
		if super_b.myclock is None: return cks;
		cur_key = super_b.myclock['key'];
		mycks = super_b.clocks.keys();
		idx = mycks.index(cur_key);
		if idx == 0: return cks;
		cks.append(mycks[idx - 1]);
	elif struct['ttag'].find('_next_prep_clock') <> -1:
		if super_b.myclock is None: return cks;
		cur_key = super_b.myclock['key'];
		mycks = super_b.clocks.keys();
		idx = mycks.index(cur_key);
		if (idx + 1) >= len(mycks): idx = -1;
		key = mycks[idx + 1];
		cks.append(key);
	return cks;

def _find_cks_bytype(ttype,super_b):
	cks = list();
	for ck in super_b.clocks.keys():
		clock = super_b.clocks[ck];
		if clock.has_key('type') and clock['type'] == ttype:
			cks.append(ck);
	return cks;

def _find_cks_by_only(struct,super_b):
	cks = _find_cks_by_sample(struct,super_b);
	if cks == None: return list();
	cks = list();
	idx = 0;
	while True:
		keys = super_b.clocks.keys();
		if idx >= len(keys): break;
		ck = super_b.clocks[keys[idx]];
		if ck['key'] in cks: continue;
		cks.append(ck['key']);
		idx = idx + 1;
	return cks;

def _find_cks_pastdue(super_b):
	cks = list();
	week = _get_cur_week();
	left_able = 127;
	if week > 0:
		left_able = math.pow(2,7) - math.pow(2,week);
	mtime = _get_cur_time();
	for ck in super_b.clocks:
		clock = super_b.clocks[ck];
		hour = int(clock['time'].split(':')[0]);
		mins = int(clock['time'].split(':')[1]);
		if int(left_able) & int(clock['able']['able']) == 0:
			cks.append(ck);
		elif int(left_able) & int(clock['able']['able']) == math.pow(2,week):
			if hour < mtime[3] or (hour == mtime[3] and mins < mtime[4]):
				cks.append(ck);
	return cks;

def _find_cks_nouse(super_b):
	cks = list();
	for ck in super_b.clocks.keys():
		clock = super_b.clocks[ck];
		if clock.has_key('status') and clock['status']['type'] == 'close':
			cks.append(ck);
	return cks;

def _find_cks_by_num(struct,super_b):
	cks = list();
	keys = super_b.clocks.keys();
	for istr in struct['stseg']:
		if not struct['stc'].has_key(istr): continue;
		item = struct['stc'][istr];
		if item['type'] == 'NUM':
			num = int(item['str']);
			if num - 1 < 0 or num - 1 >= len(keys): return cks;
			cks.append(keys[num] - 1);
		elif item['type'] == 'NUNIT':
			num = int(item['stc'][0]['str']);
			if num - 1 < 0 or num - 1 >= len(keys): return cks;
			cks.append(keys[num] - 1);
	return cks;

def _find_cks_time_to_time(struct,super_b):
	cks = list();
	inter_1 = inter_2 = None;
	for istr in struct['stseg']:
		if not struct['stc'].has_key(istr): continue;
		item = struct['stc'][istr];
		if item['type'] == 'TIME':
			if inter_1 is None:
				inter_1 = dict(item);
				del struct['stc'][istr];
			else:
				inter_2 = dict(item);
				del struct['stc'][istr];
				break;
	start = inter_1['stime'];
	if start[common.enable] == '-1': start = inter_1['etime'];
	end = inter_2['stime'];
	if end[common.enable] == '-1': end = inter_2['etime'];
	able,diff,sweek,eweek = _get_time_to_time_able(start,end);
	#print able,diff
	if inter_1['scope'] == 'day' and inter_2['scope'] == 'day':
		for ck in super_b.clocks:
			clock = super_b.clocks[ck];
			if clock.has_key('able') and int(clock['able']['able']) & int(able) > 0:
				cks.append(ck);
	elif inter_1['scope'] <> 'day' and inter_2['scope'] == 'day':
		for ck in super_b.clocks:
			clock = super_b.clocks[ck];
			hour = int(clock['time'].split(':')[0]);
			mins = int(clock['time'].split(':')[1]);
			if hour < start[3] and int(clock['able']['able']) & int(math.pow(2,sweek)) > 0:
				continue;
			elif int(clock['able']['able']) & int(able) <= 0:
				continue;
			cks.append(ck);
	elif inter_1['scope'] == 'day' and inter_2['scope'] <> 'day':
		for ck in super_b.clocks:
			clock = super_b.clocks[ck];
			hour = int(clock['time'].split(':')[0]);
			mins = int(clock['time'].split(':')[1]);
			if hour > end[3] and int(clock['able']['able']) & int(math.pow(2,eweek)) > 0:
				continue;
			elif hour == end[3] and int(clock['able']['able']) & int(math.pow(2,eweek)) > 0:
				if end[4] <> 'null' and end[4] < mins:
					continue;
			elif int(clock['able']['able']) & int(able) <= 0:
				continue;
			cks.append(ck);
	elif inter_1['scope'] <> 'day' and inter_2['scope'] <> 'day':
		for ck in super_b.clocks:
			clock = super_b.clocks[ck];
			hour = int(clock['time'].split(':')[0]);
			mins = int(clock['time'].split(':')[1]);
			#print hour,mins,start,end
			if diff == 0:
				if hour < start[3] and int(clock['able']['able']) & int(math.pow(2,sweek)) > 0:
					continue;
				if hour > end[3] and int(clock['able']['able']) & int(math.pow(2,eweek)) > 0:
					continue;
				if hour == end[3] and int(clock['able']['able']) & int(math.pow(2,eweek)) > 0:
					if end[4] <> 'null' and end[4] < mins:
						continue;
				if int(clock['able']['able']) & int(able) <= 0:
					continue;
			else:
				if hour < start[3]: continue;
				if start[4] <> 'null' and hour == start[3]:
					if start[4] > mins: continue;
				if hour > end[3]: continue;
				if end[4] <> 'null' and hour == end[3]:
					if mins > end[4]: continue;
			#print ck
			cks.append(ck);
	return cks;

def _find_cks_time_and_time(struct,super_b):
	cks = list();
	inter_1 = inter_2 = None;
	for istr in struct['stseg']:
		if not struct['stc'].has_key(istr): continue;
		item = struct['stc'][istr];
		if item['type'] == 'TIME':
			if inter_1 is None:
				inter_1 = dict(item);
				del struct['stc'][istr];
			else:
				inter_2 = dict(item);
				del struct['stc'][istr];
				break;
	start = inter_1['stime'];
	end = inter_2['stime'];
	if start[0] == 'null' or end[0] == 'null': return cks;
	stime = etime = '';
	if start[3] == 'null' or end[3] == 'null': return cks;
	stime = str(start[3]) + ':';
	etime = str(end[3]) + ':';
	if start[4] == 'null':
		stime = stime + '0';
	else:
		stime = stime + str(start[4]);
	if end[4] == 'null':
		etime = etime + '0';
	else:
		etime = etime + str(end[4]);

	for ck in super_b.clocks:
		clock = super_b.clocks[ck];
		tstr = clock['time'];
		if stime == tstr or etime == tstr:
			cks.append(ck);
	return cks;

def _find_cks_after(struct,super_b):
	cks = list();
	time = list(_get_cur_time());
	cur_week = _get_cur_week();
	able = math.pow(2,cur_week);
	for istr in struct['stseg']:
		if not struct['stc'].has_key(istr): continue;
		item = struct['stc'][istr];
		if item['type'] <> 'TIME': continue;

		start = item['stime'];
		end = item['etime'];
		if start[common.enable] == '-1':
			week = _get_week(end[0],end[1],end[2]);
			able = math.pow(2,week);
			if end[3] <> 'null': time[3] = int(end[3]);
			if end[4] <> 'null': time[4] = int(end[4]);
		elif end[common.enable] == '-1':
			week = _get_week(start[0],start[1],start[2]);
			able = math.pow(2,week);
			if start[3] <> 'null': time[3] = int(start[3]);
			if start[4] <> 'null': time[4] = int(start[4]);
		else:
			week = _get_week(start[0],start[1],start[2]);
			able = math.pow(2,week);
			eweek = _get_week(end[0],end[1],end[2]);
			if eweek - week > 1 or eweek - week < -1:
				able = able + math.pow(2,week + 1);
			if start[3] <> 'null': time[3] = int(start[3]);
			if start[4] <> 'null': time[4] = int(start[4]);
		break;
	for ck in super_b.clocks.keys():
		clock = super_b.clocks[ck];
		hour = int(clock['time'].split(':')[0]);
		mins = int(clock['time'].split(':')[1]);
		if time[3] < hour or (time[3] == hour and time[4] <= mins):
			if int(clock['able']['able']) & int(able) > 0:
				cks.append(ck);
	return cks;

def _get_time_to_time_able(start,end):
	sweek = _get_week(start[0],start[1],start[2]);
	eweek = _get_week(end[0],end[1],end[2]);
	able = diff = 0;
	if sweek > eweek: eweek = eweek + 7;
	if sweek == eweek: diff = 1;
	able = 0;
	idx = sweek;
	while True:
		if sweek > eweek: break;
		if sweek >= 7:
			able = able + math.pow(2,sweek - 7);
		else:
			able = able + math.pow(2,sweek);
		sweek = sweek + 1;
	if eweek >= 7: eweek = eweek - 7;
	return (able,diff,idx,eweek);

def _get_time_able(start,end):
	able = 0;
	if start[0] == 'null':
		week = _get_week(end[0],end[1],end[2]);
		able = math.pow(2,week);
	elif end[0] == 'null':
		week = _get_week(start[0],start[1],start[2]);
		able = math.pow(2,week);
	else:
		week = _get_week(start[0],start[1],start[2]);
		able = math.pow(2,week);
		eweek = _get_week(end[0],end[1],end[2]);
		if eweek - week > 1 or eweek - week < -1:
			able = able + math.pow(2,week + 1);
	return able;

def _get_num_cks(struct):
	num = 0;
	for s in struct['inlist']:
		if data['num'].has_key(s):
			num = int(data['num'][s]);
			return num;
	return num;

def _get_cur_week():
	times = time.localtime();
	return times[6];

def _get_cur_time(): return time.localtime();

def _get_week(year,month,day):
	dat = datetime.date(year,month,day);
	return dat.weekday();

def _get_random_id(total):
	ret = random.randint(0,total);
	if ret == total:
		ret = ret - 1;
	return ret;

def _set_msg(struct,datamsg):
	msg_id = _get_random_id(len(datamsg));
	struct['result']['msg'] = datamsg[msg_id];

def _degbu_info(struct):
	if struct.has_key('clocks'):
		debug_strs = ''
		for ck in struct['clocks']:
			if isinstance(ck,dict):
				debug_strs = debug_strs + '<' + ck['mystr'] + '>';
		struct['debug_strs'] = debug_strs;
	if struct.has_key('ttag'):
		debug_strs = ''
		tarray = struct['ttag'].split('_');
		for tag in tarray:
			if tag == '': continue;
			debug_strs = debug_strs + '<' + tag + '>';
		struct['debug_tag'] = debug_strs;
		del struct['ttag'];
	if struct.has_key('mcks'):
		cks = list();
		for ck in struct['mcks'].keys():
			clock = struct['mcks'][ck];
			cks.append(ck + '|' + clock['time']);
		struct['cks'] = cks;
	if struct.has_key('Times'): del struct['Times'];

def _make_tag_dic(start,stype,end,etype,ctype):
	tdic = dict();
	tdic['start'] = dict();
	tdic['start']['tag'] = start;
	tdic['start']['type'] = stype;
	tdic['end'] = dict();
	tdic['end']['tag'] = end;
	tdic['end']['type'] = etype;
	tdic['ftag'] = ctype;
	return tdic;

