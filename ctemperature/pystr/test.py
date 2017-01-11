#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
reload(sys);
sys.setdefaultencoding('utf-8');
import collections

#==============================================================
''' import tagpy wordsegs '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
sys.path.append(os.path.join(base_path,'../../modules/wordsegs'));
#==============================================================

import common,config
from myexception import MyException
from marktag import M,C,F,X
from numtag import Nt
from extendtag import X1,M1,F1,Z
from checktag import PM
from calctag import Calc
from wordseg import WordSeg

wordseg = WordSeg();
tag_objs = list();
# mark tag objs #
tag_objs.append(M());
tag_objs.append(C());
tag_objs.append(F());
tag_objs.append(X());
tag_objs.append(Nt());
# extend tag objs #
tag_objs.append(X1());
tag_objs.append(M1());
tag_objs.append(F1());
tag_objs.append(Z());
# calc tag obj #
tag_objs.append(PM());
tag_objs.append(Calc());

step = 1;
dfiles = config.dfiles['Temp'];
for obj in tag_objs:
	obj.load_data(dfiles[str(step)]);
	step = step + 1;

struct = dict();
struct['text'] = u'温度太高了';
struct['inlist'] = wordseg.tokens(struct['text']);
struct['taglist'] = list();
for obj in tag_objs:
	obj.init();
	obj.encode(struct);
common.print_dic(struct);
