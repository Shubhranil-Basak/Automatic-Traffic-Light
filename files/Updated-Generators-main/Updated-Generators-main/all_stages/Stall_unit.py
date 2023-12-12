
from typing import List
from nmigen.back import rtlil, verilog
from nmigen import *
#from nmigen.back.pysim import Simulator, Delay, Settle
#from nmigen.sim import *
from nmigen import Elaboratable,Module,Signal
from nmigen.build import Platform
from nmigen.cli import main_parser,main_runner

class Stall_Unit(Elaboratable):
    def __init__(self):
        self.csb0 = Signal(1)
        self.web0 = Signal(1)
        self.next_dest0 = Signal(5)
        self.ID_src1 = Signal(5)
        self.ID_src2 = Signal(5)
        self.csb1 = Signal(1)
        self.web1 = Signal(1)
        self.next_dest1 = Signal(5)

        self.stall = Signal(1)
        self.nothing = 0b00

    def elaborate(self, platform:Platform) -> Module:
        m = Module()

        with m.If((self.csb0 == Const(0)) & (self.web0 == Const(1))):
            with m.If(self.ID_src1 == self.next_dest0):
                with m.If(self.ID_src1 != Const(0)):
                    m.d.comb += self.stall.eq(0b1)
                with m.Else():
                    m.d.comb += self.stall.eq(0b0)

            with m.Elif(self.ID_src2 == self.next_dest0):
                with m.If(self.ID_src2 != Const(0)):
                    m.d.comb += self.stall.eq(0b1)
                with m.Else():
                    m.d.comb += self.stall.eq(0b0)
                
            with m.Else():
                m.d.comb += self.stall.eq(0b0)
        
        with m.Elif((self.csb1 == Const(0)) & (self.web1 == Const(1))):
            with m.If(self.ID_src1 == self.next_dest1):
                with m.If(self.ID_src1 != Const(0)):
                    m.d.comb += self.stall.eq(0b1)
                with m.Else():
                    m.d.comb += self.stall.eq(0b0)

            with m.Elif(self.ID_src2 == self.next_dest1):
                with m.If(self.ID_src2 != Const(0)):
                    m.d.comb += self.stall.eq(0b1)
                with m.Else():
                    m.d.comb += self.stall.eq(0b0)
    
            with m.Else():
                m.d.comb += self.stall.eq(0b0)
            
        with m.Else():
            m.d.comb += self.stall.eq(0b0)
        
        return m
    
    def ports(self)->List[Signal]:
        return []
