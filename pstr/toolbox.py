#!/usr/bin/python
#-*- coding:utf-8 -*-
from base import Base
import common
# you can register every tool(radio,tcl) which you want.

class ToolBox(Base):

	def load_data(self,dfile):
		try:
			if type(dfile) == list:
				self.data = dict();
				for tfile in dfile:
					tool = common.read_json(tfile);
					tname = tool['name'];
					self.data[tname] = tool;
			else:
				tool = common.read_json(dfile);
				tname = tool['name'];
				self.data[tname] = tool;
		except Exception, e:
			raise e;

	def encode(self,struct):
		try:
			inlist = struct['inlist'];
			tools = self.data;
			self._gettool(tools,struct);
			if struct.has_key('tool'):
				for tname in struct['tool']:
					tool = self.data[tname];
					attr = self._getattr(tool,struct);
					if not attr is None:
						if struct.has_key('attr'):
							raise Exception('has one more attr be founded');
						else:
							struct['attr'] = attr;
					else:
						struct['tool'].remove(tool);
			if struct.has_key('attr'):
				if struct.has_key('value') and struct.has_key('dir'):
					tname = struct['tool'][0];
					tool = self.data[tname];
					struct['api'] = tool['move'];
		except Exception as e:
			raise e;

	def _gettool(self,tools,struct):
		try:
			if not struct.has_key('tool'):
				struct['tool'] = list();
			inlist = struct['inlist'];
			for st in inlist:
				if struct.has_key(st) and struct[st].get('type') == 'M':
					for tool in tools.values():
						if tool['name'] == st:
							struct['tool'].append(tool['name']);
							continue;
						elif st in tool['alias']:
							struct['tool'].append(tool['name']);
							continue;
						elif not self._getattr(tool,struct) is None:
							struct['tool'].append(tool['name']);
							continue;
		except Exception as e:
			raise e;
	def _getattr(self,tool,struct):
		try:
			inlist = struct['inlist'];
			for st in inlist:
				if struct.has_key(st) and struct[st].get('type') == 'M':
					attrdic = tool['attr'];
					for tattr in attrdic.values():
						if st in tattr['alias']:
							return tattr;
		except Exception as e:
			raise e;
		return None;
