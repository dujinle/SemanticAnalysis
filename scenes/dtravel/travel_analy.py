#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from scene_base import SceneBase
import com_funcs as ComFuncs

#处理预定 航班 酒店 信息
class TravelAnaly(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into travel analysis......');
			if not struct.has_key('step'): struct['step'] = 'start';

			func = self._fetch_func(struct);
			print 'func:',func,'.......';
			if struct['step'] == 'start':
				if func == 'set_trip':
					self._fetch_flight(struct,super_b);
					return None;
			elif struct['step'] == 'set_trip'\
				or struct['step'] == 'set_trip_time' \
				or struct['step'] == 'set_trip_start'\
				or struct['step'] == 'set_trip_end':
				self._fetch_flight(struct,super_b);
				return None;
			elif struct['step'] == 'sel_flight':
				if func == 'book':
					self._book_flight(struct,super_b);
				elif func == 'book':
					self._book_travel_or_hotel(struct,super_b);
			elif struct['step'] == 'if_book_hotel':
				if func == 'book_hotel':
					self._get_hotel_info(struct,super_b);
					struct['step'] = 'select';
					return None;
			elif struct['step'] == 'book_sure':
				self._book_hotel(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _fetch_flight(self,struct,super_b):

		self._get_flight_info(struct,super_b);
		self._check_flight(struct,super_b);

	def _get_flight_info(self,struct,super_b):
		if super_b.flight is None: super_b.flight = dict();
		to = False;
		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item.has_key('stype') and item['stype'] == 'TIME':
				super_b.flight['time'] = item;
			if item.has_key('type') and item['type'] == 'NP':
				if to == True:
					super_b.flight['end'] = item['str'];
				else:
					super_b.flight['start'] = item['str'];
			if item.has_key('stype') and item['stype'] == 'TO':
				to = True;
			elif item.has_key('stype') and item['stype'] == 'FLY':
				to = True;
		if super_b.flight.has_key('start') and super_b.flight.has_key('end'):
			if super_b.flight['start'] == super_b.flight['end']:
				super_b.flight['start'] = 'local';

	def _check_flight(self,struct,super_b):
		if super_b.flight is None:
			struct['step'] = 'set_trip';
			ComFuncs._set_msg(struct,self.data['msg']['set_trip']);
		elif not super_b.flight.has_key('start'):
			struct['step'] = 'set_trip_start';
			ComFuncs._set_msg(struct,self.data['msg']['set_trip_start']);
		elif not super_b.flight.has_key('end'):
			struct['step'] = 'set_trip_end';
			ComFuncs._set_msg(struct,self.data['msg']['set_trip_end']);
		elif not super_b.flight.has_key('time'):
			struct['step'] = 'set_trip_time';
			ComFuncs._set_msg(struct,self.data['msg']['set_trip_time']);
		else:
			ComFuncs._set_msg(struct,self.data['msg']['flight_succ']);
			super_b.get_flight_info();
			struct['step'] = 'sel_flight';
			struct['result']['flight'] = super_b.flight;
		return None;

	def _book_flight(self,struct,super_b):
		if super_b.flight is None:
			self._check_flight(struct,super_b);
			return None;

		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item.has_key('stype') and item['stype'] == 'TIME':
				super_b.book_flight_time(item);
				break;
			if item.has_key('type') and item['type'] == 'NUM':
				super_b.book_flight_fno(item);
				break;

		if super_b.flight.has_key('book'):
			struct['result']['flight'] = super_b.flight;
			ComFuncs._set_msg(struct,self.data['msg']['book_succ']);
		else:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);

	def _book_travel(self,struct,super_b):
		time = None;
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			if item['stype'] == 'TIME':
				time = item;
				break;
		if time is None:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
		else:
			travel = super_b.get_travel(time);
			if travel is None:
				ComFuncs._set_msg(struct,self.data['msg']['unknow']);
			else:
				struct['result']['book'] = travel;
				ComFuncs._set_msg(struct,self.data['msg']['book_succ']);
	def _get_hotel_info(self,struct,super_b):
		level = addr = None;
		tdic = dict();
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			while True:
				if item['stype'] == 'HOTEL':
					if item.has_key('belong'):
						addr = item['belong'];
					if item.has_key('num'):
						level = item['num'];
				if item.has_key('child'):
					item = item['child'];
				else:
					break;
		hotel = super_b.get_hotel(addr,level);
		if hotel is None:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
		else:
			struct['result']['hotel'] = hotel;
			ComFuncs._set_msg(struct,self.data['msg']['hotel_select']);
		return None;

	def _book_travel_or_hotel(self,struct,super_b):
		if super_b.history == 'travel':
			self._book_travel(struct,super_b);
		elif super_b.history == 'Hotel':
			ComFuncs._set_msg(struct,self.data['msg']['hotel_pnum']);
			struct['step'] = 'book_sure';
		return None;

	def _book_hotel(self,struct,super_b):
		pls = days = None;
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			if item['stype'] == 'PEOPLE':
				if item.has_key('num'):
					num = item['num'];
					if num.has_key('stc'):
						pls = num['stc'][0]['stype'];
					else:
						pls = num['stype'];
			elif item['stype'] == 'STAY':
				if item.has_key('num'):
					ds = item['num'];
					if ds.has_key('stc'):
						days = ds['stc'][0]['stype'];
		if pls is None or days is None:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
		else:
			struct['result']['hotel'] = {'pl':pls,'days':days};
			ComFuncs._set_msg(struct,self.data['msg']['hotel_succ']);
