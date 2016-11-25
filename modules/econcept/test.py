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
from mark_adjs import MarkAdjs
from mark_ppronoun import MarkPpronoun
from mark_lpronoun import MarkLpronoun
from fetch_belongs import FetchBelongs
from fetch_action import FetchAction
from fetch_adjs import FetchAdjs
from fetch_artist import FetchArtist
from fetch_verb_stc import FetchVerbs
from merge_objs import MergeObjs
from merge_sds import MergeSbDoSth

word_seg = WordSeg();
net_data = NetData();
net_data.set_noun_net(os.path.join(base_path,'./tdata/noun_dic.json'));
net_data.set_verb_net(os.path.join(base_path,'./tdata/verb_dic.json'));
net_data.set_gerund_net(os.path.join(base_path,'./tdata/gerund_dic.json'));

mk_objs = MarkObjs(net_data);
madj = MarkAdjs(net_data);
mppr = MarkPpronoun(net_data);
mlpr = MarkLpronoun(net_data);
fadj = FetchAdjs(net_data);
fact = FetchAction(net_data);
fart = FetchArtist(net_data);
fverb = FetchVerbs(net_data);
fbel = FetchBelongs(net_data);
madj.load_data('./tdata/adj_dic.json');
mppr.load_data('./tdata/people_pronoun.json');
mlpr.load_data('./tdata/logic_pronoun.json');
fbel.load_data('./tdata/fetch_belongs.json');
fadj.load_data('./tdata/fetch_adjs.json');
fact.load_data('./tdata/fetch_action.json');
fart.load_data('./tdata/fetch_artist.json');
fverb.load_data('./tdata/fetch_verb_stc.json');

struct = dict();
fp = open('./test.txt','rb');
for line in fp.readlines():
	line = line.strip('\n');
	if line[0] == '#' or len(line) == 0: continue;
	struct['text'] = line.decode('utf-8');
	struct['inlist'] = word_seg.tokens(struct['text']);
	mk_objs.encode(struct);
	madj.encode(struct);
	mppr.encode(struct);
	mlpr.encode(struct);
	fadj.encode(struct);
	fbel.encode(struct);
	fact.encode(struct);
	fart.encode(struct);
	fverb.encode(struct);
	common.print_dic(struct);
	break;

