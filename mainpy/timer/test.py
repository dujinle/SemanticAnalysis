#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
reload(sys)
sys.setdefaultencoding('utf-8')

''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));

import common
from extend_modified_time import Time_Notion
from calc_time import Calc_Time_Notion
from label_units import LabelUnits
tn = Time_Notion();
tn.load_data('./extend_modified_time.txt');
struct = dict();
#struct['inlist'] = [u'明天',u'上半天'];
#struct['taglist'] = [u'明天',u'上半天'];
struct['inlist'] = [u'2014',u'年','03',u'月','18',u'号'];
struct['taglist'] = [u'2014',u'年','03',u'月','18',u'号'];
tn.encode(struct);

lu = LabelUnits();
lu.load_data('./time_unit.txt');
lu.encode(struct)

calc_time = Calc_Time_Notion();
calc_time.encode(struct);
common.print_dic(struct);
