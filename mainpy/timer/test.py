#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
reload(sys)
sys.setdefaultencoding('utf-8')

''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));

import common,time
from notion_time import Time_Notion
from calc_time import Calc_Time_Notion
from units_time import LabelUnits
from composite_time import CompositeTime

struct = dict();
struct['inlist'] = ['3',u'月',u'前'];
struct['taglist'] = ['3',u'月',u'前'];
#struct['start'] = list(time.localtime());
#struct['end'] = list(time.localtime());
#struct['inlist'] = [u'大前天',u'前'];
#struct['taglist'] = [u'大前天',u'前'];
#struct['inlist'] = [u'2014',u'年','03',u'月','18',u'号',u'上午',u'前'];
#struct['taglist'] = [u'2014',u'年','03',u'月','18',u'号',u'上午',u'前'];

tn = Time_Notion();
tn.load_data('./notion_time.txt');
tn.encode(struct);
#common.print_dic(struct);

lu = LabelUnits();
lu.load_data('./unit_time.txt');
lu.encode(struct)
#common.print_dic(struct);

ct = CompositeTime();
ct.load_data('./composite_time.txt');
ct.encode(struct);

#calc_time = Calc_Time_Notion();
#calc_time.encode(struct);
common.print_dic(struct);
