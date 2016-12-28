#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys,os
reload(sys);
sys.setdefaultencoding('utf-8');
#=======================================================
''' import tagpy wordsegs '''
abspath = os.path.abspath(__file__);
base_path = os.path.split(abspath)[0];

sys.path.append(base_path + '/../commons');
sys.path.append(base_path + '/../mainpy');
#=======================================================
from mager import Mager
import common
if __name__ == '__main__':
	if len(sys.argv) == 1:
		print 'Usage:%s file > outfile' %sys.argv[0];
		sys.exit(-1);
	mg = Mager();
	mg.init();
	infile = sys.argv[1];
	try:
		fp = open(infile,'r');
		while True:
			struct = None;
			line = fp.readline().strip('\n');
			if not line:
				break;
			if len(line) == 0 or line[0] == '#':
				continue;
			array = line.split(' ');
			dirs = array[1];
			value = 'NULL';
			if len(array) == 3:
				value = array[2];
			sys.stdout.write(array[0] + ' \t' + array[1] + '\t' + value);
			struct = mg.encode(array[0].decode('utf-8'),'Voice');
			if struct.has_key('dir'):
				if cmp(dirs,struct['dir']) <> 0:
					sys.stdout.write(' failed\n');
					common.print_dic(struct);
				elif struct['dir'] == 'NULL' and dirs == 'NULL':
					sys.stdout.write(' success\n');
				elif cmp(struct['value'],value) == 0:
					sys.stdout.write(' success\n');
				else:
					sys.stdout.write(' failed\n');
					common.print_dic(struct);
			else:
				sys.stdout.write(' failed\n');
				common.print_dic(struct);
	except Exception as e:
		print format(e);
		sys.stdout.write('except failed \n');
