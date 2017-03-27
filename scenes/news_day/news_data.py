#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,random
#====================================================================
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../scene_common'));
#====================================================================
from scene_base import SceneBase

#处理新闻场景
class NewsData(SceneBase):

	def encode(self,struct): pass;

	#新闻数据中根据标题模糊匹配数据
	def get_news_by_title(self,title):
		for data in self.data:
			item = self.data[data];
			for ni in item:
				if ni['title'].find(title) <> -1:
					return ni;

	#随机获取指定板块的几条新闻数据
	def get_news_by_plate(self,plate,n):
		if not self.data.has_key(plate): return None;
		item = self.data[plate];
		if len(item) >= n: return item[:n];
		return item;

	def get_news_by_random(self,n):
		plate = self.data.keys();
		nlist = list();
		while True:
			if n <= 0: break;
			idx = random.randint(0,len(plate) - 1);
			items = self.data[plate[idx]];
			nidx = random.randint(0,len(items) - 1);
			if items[nidx] in nlist:
				n = n - 1;
				continue;
			nlist.append(items[nidx]);
			n = n - 1;
		return nlist;
