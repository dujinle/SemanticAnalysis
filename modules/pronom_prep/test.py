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
sys.path.append(os.path.join(base_path,'../wordsegs'));
#============================================
import common,config
from wordseg import WordSeg
from pprep_mager import PPrepMager

wd = WordSeg();
nmager = PPrepMager();
nmager.init('PrepPronom');

struct = dict();
struct['text'] = u'在家里';
struct['objs'] = [{
	"str":"家",
	"stype":"SP"
}];


struct['inlist'] = wd.tokens(struct['text']);
nmager.encode(struct);
common.print_dic(struct);
