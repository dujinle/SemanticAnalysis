#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys
reload(sys);
sys.setdefaultencoding('utf-8');

class String:
	def __init__(self,strs):
		self.string = strs;
		self.byte = str.encode(strs);
		self.strlist = list();
		self.tmplist = list();
		self.ifhasnum = False;
		self.ifhasletter = False;
		for byte in self.byte:
			try:
				if self.__byteisnum(byte):
					self.strlist.append(str(self.tmplist));
					del self.tmplist[:];
					self.strlist.append(str(byte));
				elif self.__byteisletter(byte):
					self.strlist.append(str(self.tmplist));
					del self.tmplist[:];
					self.strlist.append(str(byte));
				else:
					self.tmplist.append(byte);
			except Exception as e:
				raise e;

	def __byteisnum(self,byte):
		if byte >= '0' and byte <= '9':
			self.ifhasnum = True;
			return True;
		return False;

	def __byteisletter(self,byte):
		if byte >= 'a' and byte <= 'z':
			self.ifhasletter = True;
			return True;
		elif byte >= 'A' and byte <= 'Z':
			self.ifhasletter = True;
			return True;
		return False;

	def contain_num(self):
		return self.ifhasnum;

	def contain_letter(self):
		return self.ifhasletter;
st = String('我们是1000abggg');
print st.contain_num();
print st.contain_letter();
