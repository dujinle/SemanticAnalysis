#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common
from myexception import MyException
from scene_base import SceneBase as LJFLBase
import struct_utils as Sutil
#标记用户列表中的数据
class LJFLMkobj(LJFLBase):

	def encode(self,struct,super_b):
		try:
			super_b.objs = [];
			self._mark_obj(struct,super_b);
		except Exception:
			raise MyException(sys.exc_info());

	def _mark_obj(self,struct,super_b):
		data = self.data['objs'];
		idx = 0;
		while True:
			if idx >= len(struct['stseg']): break;
			mstr = struct['stseg'][idx];
			for item in data:
				ret,next_idx = self._mk_one_obj(idx,struct,item);
				idx += next_idx;

				if ret is None:
					continue;
				else:
					super_b.objs.append(ret);
			idx = idx + 1;
	
	def _mk_one_obj(self,idx,struct,item):
		if idx >= len(struct['stseg']):
			return None,0;
		mkobj = [];
		itm_idx = 0;
		while True:
			mstr_obj = None;
			it = None;
			if idx < len(struct['stseg']):
				mstr = struct['stseg'][idx];
				if struct['stc'].has_key(mstr):
					mstr_obj = struct['stc'][mstr];
			if itm_idx < len(item):
				it = item[itm_idx];
			ret = self._deep_match(mstr_obj,it,mkobj);
			if ret == 0: return mkobj,idx;
			if ret == -1:return None,0;
			if ret == 1:
				idx += 1;
			if ret == 2:
				idx += 1;
				itm_idx += 1;

	#如果为0 则匹配结束，-1失败，1处理物前进，2，匹配成功，都前进
	def _deep_match(self,mstr_obj,it,deep):
		if it is None:return 0;
		if mstr_obj is None:return -1;
		flag = 0;
		total_num = 0;
		for key in it:
			total_num += 1;
			if mstr_obj.has_key(key) and mstr_obj[key] == it[key]:
				flag += 1;
		if total_num == flag:
			deep.append(mstr_obj)
			return 2
		else:
			return 1;
