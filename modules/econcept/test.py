#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
reload(sys)
sys.setdefaultencoding('utf-8');

base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
sys.path.append(os.path.join(base_path,'../../modules/wordsegs'));
import common
from wordseg import WordSeg
from net_data import NetData
from mark_objs import MarkObjs
from merge_objs import MergeObjs
from merge_sds import MergeSbDoSth

word_seg = WordSeg();
net_data = NetData();
net_data.set_noun_net(os.path.join(base_path,'./tdata/noun_dic.data'));
net_data.set_verb_net(os.path.join(base_path,'./tdata/verb_dic.data'));
net_data.set_gerund_net(os.path.join(base_path,'./tdata/gerund_dic.data'));

mk_objs = MarkObjs(net_data);
me_objs = MergeObjs(net_data);
ms_objs = MergeSbDoSth(net_data);

struct = dict();
fp = open('./test.txt','rb');
for line in fp.readlines():
	line = line.strip('\n');
	if line[0] == '#' or len(line) == 0: continue;
	struct['text'] = line.decode('utf-8');
	struct['inlist'] = word_seg.tokens(struct['text']);
	mk_objs.encode(struct);
	me_objs.encode(struct);
	ms_objs.encode(struct);
	common.print_dic(struct);
	break;

