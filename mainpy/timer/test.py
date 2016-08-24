#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json
import re,time
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
sys.path.append(os.path.join(base_path,'../'));
#============================================
import common,config
from time_normal import TNormal,TBucket
from time_week import TWeek
from time_festival import TFestival,TEFestival
from time_solarterm import TSolarTerm
from time_decade import TDecade
from time_front import TFront
from time_tail import TTail
from time_replace import TReplace
from time_mood import TMood

ut = TNormal();
nt = TBucket();
wt = TWeek();
tf = TFestival();
tef = TEFestival();
ts = TSolarTerm();
td = TDecade();
tof = TFront();
tt = TTail();
tmood = TMood();
tre = TReplace();
ut.load_data('./tdata/TNormal.txt');
nt.load_data('./tdata/TBucket.txt');
wt.load_data('./tdata/TWeek.txt');
tf.load_data('./tdata/TFestival.txt');
tef.load_data('./tdata/TEFestival.txt');
ts.load_data('./tdata/TSolarterm.txt');
td.load_data('./tdata/TDecade.txt');
tof.load_data('./tdata/TFront.txt');
tre.load_data('./tdata/TReplace.txt');
tmood.load_data('./tdata/TMood.txt');

struct = dict();
struct['text'] = u'给9月2号设置一个早上8点响的闹铃'#5时3刻'#后晚'#3天后'#周末'#明天'#1季度'#下1世纪30年代'#周3'#明天12点20分'
struct['intervals'] = list();
struct['mood'] = list();
struct['my_inter_id'] = 0;
struct['step_id'] = 0;
idx = 0;
cur_status = False;
while True:
	if struct['step_id'] >= len(struct['text']):
		if cur_status == True: tt.encode(struct);
		break;
	tre.encode(struct);
	ret = tof.encode(struct);
	ret += ut.encode(struct);
	ret += nt.encode(struct);
	ret += wt.encode(struct);
	ret += tf.encode(struct);
	ret += tef.encode(struct);
	ret += ts.encode(struct);
	ret += td.encode(struct);
	ret += tmood.encode(struct);
	if ret == -9:
		if cur_status == True:
			tt.encode(struct);
			cur_status = False;
			struct['my_inter_id'] = struct['my_inter_id'] + 1;
		struct['step_id'] = struct['step_id'] + 1;
	else: cur_status = True;
common.print_dic(struct);
