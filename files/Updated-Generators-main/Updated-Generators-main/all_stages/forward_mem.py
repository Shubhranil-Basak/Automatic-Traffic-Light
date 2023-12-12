
from typing import List
from nmigen import *
#from nmigen.sim import *
from nmigen import Elaboratable,Module,Signal
from nmigen.build import Platform
from nmigen.cli import main_parser,main_runner

class Forwarding_Mem(Elaboratable):

	def __init__(self):
		# inputs
		self.src = Signal(5)
		self.src_data = Signal(32)

		self.des0 = Signal(5)
		self.val0 = Signal(32)
		self.csb0 = Signal(1)
		self.web0 = Signal(1)

		#outputs 
		self.data_in = Signal(32)

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

	