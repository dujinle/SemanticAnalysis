#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,copy
import re,time,random
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
import common,pgsql
import math,datetime
from common import logging
from myexception import MyException
dfile = os.path.join(base_path,'../tdata/scene_param.txt')
data = common.read_json(dfile);

def _if_exist(struct,super_b):
	if struct.has_key('ck_name'):
		ck_name = struct['ck_name'];
		if super_b.clocks.has_key(ck_name): return True;
	if struct.has_key('ck_time'):
		ck_time = struct['ck_time']['time'];
		if super_b.clocks.has_key(ck_time): return True;
	return False;

def _find_time(struct):
	if struct.has_key('intervals') and len(struct['intervals']) > 0:
		myinterval = struct['intervals'][0]
		times = myinterval['start'];
		if myinterval['scope'] == 'day' or myinterval['scope'] == 'month' \
			or myinterval['scope'] == 'year':
			tdic = dict();
			tdic['date'] = str(times[0]) + '/' + str(times[1]) + '/' + str(times[2]);
			tdic['type'] = myinterval['type'];
			struct['ck_date'] = tdic;
		if times[3] <> 0:
			tdic = dict();
			tdic['time'] = str(times[3]) + ':' + str(times[4]);
			tdic['str'] = myinterval['str'];
			struct['ck_time'] = tdic;

def _calc_able(struct):
	if struct.has_key('ck_date'):
		date = struct['ck_date'];
		tdic = dict();
		if date['type'] == 'time_ut' or date['type'] == 'time_nt':
			tdic['repeat'] = 'once';
			tdic['date'] = date['date'];
			tdic['type'] = 'date';
		if date['type'] == 'time_wt':
			dates = date['date'].split('/');
			dat = datetime.date(int(dates[0]),int(dates[1]),int(dates[2]));
			week = dat.weekday();
			able = math.pow(2,week);
			tdic['type'] = 'week';
			tdic['repeat'] = 'repeat';
			tdic['able'] = able;
		del struct['ck_date'];
		struct['ck_able'] = tdic;

def _save_tag(super_b):
	try:
		mydic = dict();
		mydic['value'] = super_b.myclock['time'];
		mydic['type'] = 'time';
		mydic['name'] = super_b.myclock['name'];
		sql = 'insert into mytags (tag,creat_time) values (' \
			+ '\'' + json.dumps(mydic) + '\',' \
			+ '\'now\'' + ')';
		cur = pgsql.pg_cursor(super_b.p_conn);
		pgsql.pg_query(cur,sql,None);
		pgsql.pg_commit(super_b.p_conn);
		pgsql.pg_close_cursor(cur);
	except Exception as e:
		raise e;

def _find_able_cks(struct,super_b):
	cks = list();
	if struct['ttag'].find('_time_to_time') <> -1:
		start = struct['intervals'][0]['start'];
		end = struct['intervals'][1]['start'];
		hid = 3;
		mid = 4;
		for ck in super_b.clocks:
			clock = super_b.clocks[ck];
			hour = int(clock['time'].split(':')[0]);
			mins = int(clock['time'].split(':')[1]);
			if hour > start[hid] or (hour == start[hid] and start[mid] <= mins):
				if hour < end[hid] or (hour == end[hid] and end[mid] >= mins):
					cks.append(ck);
	elif struct['ttag'].find('_time_all_clock') <> -1:
		start = struct['intervals'][0]['start'];
		end = struct['intervals'][0]['end'];
		for ck in super_b.clocks:
			clock = super_b.clocks[ck];
			hour = int(clock['time'].split(':')[0]);
			mins = int(clock['time'].split(':')[1]);
			if hour > start[hid] or (hour == start[hid] and start[mid] <= mins):
				if hour < end[hid] or (hour == end[hid] and end[mid] >= mins):
					cks.append(ck);
	elif struct['ttag'].find('_time') <> -1:
		start = struct['intervals'][0]['start'];
		end = struct['intervals'][0]['end'];
		hid = 3;
		mid = 4;
		for ck in super_b.clocks:
			clock = super_b.clocks[ck];
			hour = int(clock['time'].split(':')[0]);
			mins = int(clock['time'].split(':')[1]);
			if start[0] == 'null':
				if hour < end[hid] or (hour == end[hid] and mins <= end[mid]):
					cks.append(ck);
			elif end[0] == 'null':
				if hour < start[hid] or (hour == start[hid] and mins <= start[mid]):
					cks.append(ck);
			else:
				if hour > start[hid] or (hour == start[hid] and start[mid] <= mins):
					if hour < end[hid] or (hour == end[hid] and end[mid] >= mins):
						cks.append(ck);
	return cks;

def _find_cks_bytime(struct,super_b):
	cks = list();
	if struct['ttag'].find('_time') == -1: return cks;
	inter = struct['intervals'][0];
	start = inter['start'];
	end = inter['end'];

	able = 0;
	hid = 3;
	mid = 4;
	idx = start[2];
	while True:
		if able == 0 and idx == end[2]:
			if start[0] == 'null':
				week = _get_week(end[0],end[1],end[2]);
				able = math.pow(2,week);
				break;
			elif end[0] == 'null':
				week = _get_week(start[0],start[1],start[2]);
				able = math.pow(2,week);
				break;
			else:
				week = _get_week(start[0],start[1],start[2]);
				able = math.pow(2,week);
				break;
		elif idx == end[2]: break;
		week = _get_week(end[0],end[1],idx);
		able = able + math.pow(2,week);
		idx = idx + 1;
	for ck in super_b.clocks:
		clock = super_b.clocks[ck];
		hour = int(clock['time'].split(':')[0]);
		mins = int(clock['time'].split(':')[1]);
		print able,clock['time'],clock['able'],start,end
		if start[0] == 'null':
			if hour < end[hid] or (hour == end[hid] and mins <= end[mid]):
				if clock.has_key('able') and clock['able']['able'] == able:
					cks.append(ck);
		elif end[0] == 'null':
			if hour < start[hid] or (hour == start[hid] and mins <= start[mid]):
				if clock.has_key('able') and clock['able']['able'] == able:
					cks.append(ck);
		else:
			if hour > start[hid] or (hour == start[hid] and start[mid] <= mins):
				if hour < end[hid]:
					if clock.has_key('able') and int(clock['able']['able']) & int(able) > 0:
						cks.append(ck);
	return cks;

def _find_cks_byinfo(struct,super_b):
	cks = list();
	global data;
	if struct['ttag'].find('_moveto') <> -1:
		tstr =_get_match_str(struct,'_moveto');
		if tstr is None: return cks;
		cinfo_id = struct['text'].find(tstr);
		if cinfo_id == 0 or cinfo_id == -1: return cks;
		cinfo = struct['text'][:cinfo_id];
		if super_b.clocks.has_key(cinfo):
			cks.append(cinfo);
	elif struct['ttag'].find('_ahead') <> -1:
		tstr =_get_match_str(struct,'_ahead');
		if tstr is None: return cks;
		cinfo_id = struct['text'].find(tstr);
		if cinfo_id == 0 or cinfo_id == -1: return cks;
		cinfo = struct['text'][:cinfo_id];
		if super_b.clocks.has_key(cinfo):
			cks.append(cinfo);
	elif struct['ttag'].find('_prev_prep_clock') <> -1:
		if super_b.myclock is None: return cks;
		cur_key = super_b.myclock['key'];
		mycks = super_b.clocks.keys();
		idx = mycks.index(cur_key);
		key = mycks[idx - 1];
		cks.append(key);
	elif struct['ttag'].find('_next_prep_clock') <> -1:
		if super_b.myclock is None: return cks;
		cur_key = super_b.myclock['key'];
		mycks = super_b.clocks.keys();
		idx = mycks.index(cur_key);
		if (idx + 1) >= len(mycks): idx = -1;
		key = mycks[idx + 1];
		cks.append(key);
	elif struct['ttag'].find('_clock') <> -1:
		tstr =_get_match_str(struct,'_clock');
		if tstr is None: return cks;
		cinfo_id = struct['text'].find(tstr);
		if cinfo_id == 0 or cinfo_id == -1: return cks;
		cinfo = struct['text'][:cinfo_id];
		if super_b.clocks.has_key(cinfo):
			cks.append(cinfo);

def _get_match_str(struct,tag):
	comp = re.compile(data[tag]['str']);
	match = comp.search(struct['text']);
	if match is None: return None;
	tstr = match.group(0);
	return tstr;

def _get_cks_num(struct):
	inum = 0;
	global data;
	nums = data['num'].keys();
	for num in nums:
		if struct['text'].find(num) <> -1:
			inum = data['num'][num];
			break;
	return inum;

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
			debug_strs = debug_strs + '<' + ck['mystr'] + '>';
		struct['debug_strs'] = debug_strs;
		del struct['clocks'];
	if struct.has_key('ttag'):
		debug_strs = ''
		tarray = struct['ttag'].split('_');
		for tag in tarray:
			if tag == '': continue;
			debug_strs = debug_strs + '<' + tag + '>';
		struct['debug_tag'] = debug_strs;
		del struct['ttag'];
	if struct.has_key('cks'):
		cks = list();
		for ck in struct['cks'].keys():
			clock = struct['cks'][ck];
			cks.append(ck + '|' + clock['time']);
		struct['cks'] = cks;
