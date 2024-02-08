import json
f = open('All.json','r')
y=json.loads(f.read())

if (y['pipelines']['ALU-M1']==True):

	s1 = f'''
from typing import List
from nmigen import *
#from nmigen.sim import *
from nmigen import Elaboratable,Module,Signal
from nmigen.build import Platform
from nmigen.cli import main_parser,main_runner

class Forwarding_Mem(Elaboratable):

	def __init__(self):
		# inputs
		self.src = Signal({y['address_size']})
		self.src_data = Signal({y['value_bit_width']})

		self.des0 = Signal({y['address_size']})
		self.val0 = Signal({y['value_bit_width']})
		self.csb0 = Signal(1)
		self.web0 = Signal(1)

		#outputs 
		self.data_in = Signal({y['value_bit_width']})

	def elaborate(self,platform:Platform)->Module:
		m = Module()

		with m.If((self.src == self.des0) & (self.csb0 == Const(0)) & (self.web0 == Const(1))):
			with m.If(self.src != Const(0)):
				m.d.sync += self.data_in.eq(self.val0)
			with m.Else():
				m.d.sync += self.data_in.eq(self.src_data)

		with m.Else():
			m.d.sync += self.data_in.eq(self.src_data)
		
		return m

	def ports(self)->List[Signal]:
		return []

	'''

	f1=open('forward_mem.py','w+')
	f1.write(s1)
