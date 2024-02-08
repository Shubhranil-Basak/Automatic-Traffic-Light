import json
f = open('All.json','r')
y=json.loads(f.read())

num_sets = 1
if (y['pipelines']['ID-ALU']):
    num_sets+=1

if (num_sets == 2):

    s=f'''
from typing import List
from nmigen import *
# from nmigen.sim import *
from nmigen import Elaboratable,Module,Signal
from nmigen.build import Platform
from nmigen.cli import main_parser,main_runner

class Forwarding_ALU(Elaboratable):

	def __init__(self):
		# inputs
		self.s1_data = Signal({y['value_bit_width']})
		self.s2_data = Signal({y['value_bit_width']})
		self.s1 = Signal({y['address_size']})
		self.s2 = Signal({y['address_size']})

		# des0 val0 is for load forwards
		self.des0 = Signal({y['address_size']})
		self.val0 = Signal({y['value_bit_width']})
		self.csb0 = Signal(1)
		self.web0 = Signal(1)

		# des1 val1 is for add forwards
		self.des1 = Signal({y['address_size']})
		self.val1 = Signal({y['value_bit_width']})
		self.csb1 = Signal(1)     
		self.web1 = Signal(1)
		
		#outputs 
		self.ra = Signal({y['value_bit_width']})
		self.rb = Signal({y['value_bit_width']})


	def elaborate(self,platform:Platform)->Module:
		m = Module()

		with m.If((self.s1== self.des1)&(self.csb1==Const(1))):
			with m.If(self.s1!=Const(0)):
				m.d.comb += self.ra.eq(self.val1)
			with m.Else():
				m.d.comb += self.ra.eq(self.s1_data)

		with m.Elif((self.s1 == self.des0) & (self.csb0 == Const(0)) & (self.web0 == Const(1))):
			with m.If(self.s1 != Const(0)):
				m.d.comb += self.ra.eq(self.val0)
			with m.Else():
				m.d.comb += self.ra.eq(self.s1_data)

		with m.Else():
			m.d.comb += self.ra.eq(self.s1_data)

		with m.If((self.s2== self.des1)&(self.csb1==Const(1))):
			with m.If(self.s2!=Const(0)):
				m.d.comb += self.rb.eq(self.val1)
			with m.Else():
				m.d.comb += self.rb.eq(self.s2_data)

		with m.Elif((self.s2 == self.des0) & (self.csb0 == Const(0)) & (self.web0 == Const(1))):
			with m.If(self.s2 != Const(0)):
				m.d.comb += self.rb.eq(self.val0)
			with m.Else():
				m.d.comb += self.rb.eq(self.s2_data)
		
		with m.Else():
			m.d.comb += self.rb.eq(self.s2_data)
		
		return m

	def ports(self)->List[Signal]:
		return []
'''

elif (num_sets == 1):
    s = f'''
from typing import List
from nmigen import *
# from nmigen.sim import *
from nmigen import Elaboratable,Module,Signal
from nmigen.build import Platform
from nmigen.cli import main_parser,main_runner

class Forwarding_ALU(Elaboratable):

	def __init__(self):
		# inputs
		self.s1_data = Signal({y['value_bit_width']})
		self.s2_data = Signal({y['value_bit_width']})
		self.s1 = Signal({y['address_size']})
		self.s2 = Signal({y['address_size']})

		# des0 val0 is for load forwards
		self.des0 = Signal({y['address_size']})
		self.val0 = Signal({y['value_bit_width']})
		self.csb0 = Signal(1)
		self.web0 = Signal(1)

		# des1 val1 is for add forwards
		self.des1 = Signal({y['address_size']})
		self.val1 = Signal({y['value_bit_width']})
		self.csb1 = Signal(1)     
		self.web1 = Signal(1)
		
		#outputs 
		self.ra = Signal({y['value_bit_width']})
		self.rb = Signal({y['value_bit_width']})


	def elaborate(self,platform:Platform)->Module:
		m = Module()

		with m.If((self.s1== self.des1)&(self.csb1==Const(1))):
			with m.If(self.s1!=Const(0)):
				m.d.comb += self.ra.eq(self.val1)
			with m.Else():
				m.d.comb += self.ra.eq(self.s1_data)

		with m.Elif((self.s1 == self.des0) & (self.csb0 == Const(0)) & (self.web0 == Const(1))):
			with m.If(self.s1 != Const(0)):
				m.d.comb += self.ra.eq(self.val0)
			with m.Else():
				m.d.comb += self.ra.eq(self.s1_data)

		with m.Else():
			m.d.comb += self.ra.eq(self.s1_data)

		with m.If((self.s2== self.des1)&(self.csb1==Const(1))):
			with m.If(self.s2!=Const(0)):
				m.d.comb += self.rb.eq(self.val1)
			with m.Else():
				m.d.comb += self.rb.eq(self.s2_data)

		with m.Elif((self.s2 == self.des0) & (self.csb0 == Const(0)) & (self.web0 == Const(1))):
			with m.If(self.s2 != Const(0)):
				m.d.comb += self.rb.eq(self.val0)
			with m.Else():
				m.d.comb += self.rb.eq(self.s2_data)
		
		with m.Else():
			m.d.comb += self.rb.eq(self.s2_data)
		
		return m

	def ports(self)->List[Signal]:
		return []
'''
f1=open('forward_alu.py','w+')
f1.write(s)