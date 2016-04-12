#!/usr/bin/python
import os

abspath = os.path.abspath(__file__);
abspath = abspath.replace('commons','data');
abspath = abspath.replace('/config.pyc','');
abspath = abspath.replace('/config.py','');
print abspath
dfiles = {
	'Voice':{
		"1":os.path.join(abspath,'voice','M.txt'),
		"2":os.path.join(abspath,'voice','C.txt'),
		"3":os.path.join(abspath,'voice','F.txt'),
		"4":os.path.join(abspath,'voice','X.txt'),
		"5":os.path.join(abspath,'voice','X1.txt'),
		"6":os.path.join(abspath,'voice','M1.txt'),
		"7":os.path.join(abspath,'voice','F1.txt'),
		"8":os.path.join(abspath,'voice','PM.txt'),
		"9":os.path.join(abspath,'voice','Num.txt')
	},
	'Temp':{
		"1":os.path.join(abspath,'Temp','M.txt'),
		"2":os.path.join(abspath,'Temp','C.txt'),
		"3":os.path.join(abspath,'Temp','F.txt'),
		"4":os.path.join(abspath,'Temp','X.txt'),
		"5":os.path.join(abspath,'Temp','T.txt'),
		"6":os.path.join(abspath,'Temp','Z.txt'),
		"7":os.path.join(abspath,'Temp','PM.txt'),
		"8":os.path.join(abspath,'Temp','Num.txt'),
		"9":[
				os.path.join(abspath,'data','Temp','radio.txt')
		]
	}
};
