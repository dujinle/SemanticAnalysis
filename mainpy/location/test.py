#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json
import re,time
reload(sys);
sys.setdefaultencoding('utf8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
sys.path.append(os.path.join(base_path,'../'));
#============================================
import common,config
from AD import AD
from CR import CR
from CM import CM
from CELL import CELL
ad = AD();
cr = CR();
cm = CM();
cell = CELL();
ad.init('./HD');
cm.init('./HD');
cell.init('./HD');
struct = dict();
#struct['text'] = u'海淀西二旗翠微路14号'
#struct['inlist'] = [u'海淀',u'翠微路',u'与',u'翠微路',u'交叉口']
#struct['locals'] = [u'海淀',u'翠微路',u'与',u'翠微路',u'交叉口']
#struct['text'] = u'海淀翠微路前方100米'
struct['inlist'] = [u'上地西里',u'前方','100',u'米']
struct['locals'] = [u'上地西里',u'前方','100',u'米']
#struct['text'] = u'上林溪家属楼'
#struct['inlist'] = [u'上林溪',u'家属楼']
#struct['locals'] = [u'上林溪',u'家属楼']
#struct['text'] = u'上林溪18号院'
#struct['inlist'] = [u'上林溪','18',u'号院']
#struct['locals'] = [u'上林溪','18',u'号院']
ad.encode(struct);
cr.encode(struct);
cell.encode(struct);
cm.encode(struct);
common.print_dic(struct);

