
from typing import List
from nmigen import *
# from nmigen.sim import *
from nmigen import Elaboratable,Module,Signal
from nmigen.build import Platform
from nmigen.cli import main_parser,main_runner

class Forwarding_ALU(Elaboratable):

	def __init__(self):
		# inputs
		self.s1_data = Signal(32)
		self.s2_data = Signal(32)
		self.s1 = Signal(5)
		self.s2 = Signal(5)

		# des0 val0 is for load forwards
		self.des0 = Signal(5)
		self.val0 = Signal(32)
		self.csb0 = Signal(1)
		self.web0 = Signal(1)

		# des1 val1 is for add forwards
		self.des1 = Signal(5)
		self.val1 = Signal(32)
		self.csb1 = Signal(1)     
		self.web1 = Signal(1)
		
		#outputs 
		self.ra = Signal(32)
		self.rb = Signal(32)


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
