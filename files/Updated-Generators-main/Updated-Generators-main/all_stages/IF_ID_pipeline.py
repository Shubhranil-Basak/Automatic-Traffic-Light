from typing import List
from nmigen.back import rtlil, verilog
from nmigen import *
#from nmigen.back.pysim import Simulator, Delay, Settle
# from nmigen.sim import *
from nmigen import Elaboratable,Module,Signal
from nmigen.build import Platform
from nmigen.cli import main_parser,main_runner

class IF_ID_Pipeline(Elaboratable):
    def __init__(self):
        # IF-ID pipeline
        self.inst_in = Signal(32)
        self.inst_prev = Signal(32)
        self.IF2_out = Signal(32)
        self.buffer = Signal(32)
        
        self.inst_out = Signal(32)

        self.stall = Signal(1)
        self.branch = Signal(1)
        self.jump = Signal(1)
        self.stall_next = Signal(1)
        self.stall_next2 = Signal(1)
        self.stall_next3 = Signal(1)
        self.branch_next = Signal(1)
        self.jump_next = Signal(1)
        self.branch_next2 = Signal(1)
        self.jump_next2 = Signal(1)
        self.branch_next3 = Signal(1)
        self.jump_next3 = Signal(1)
    
    def elaborate(self, platform:Platform) -> Module:
        m = Module()
        m.d.sync += self.buffer.eq(self.IF2_out) 
        m.d.sync += self.branch_next.eq(self.branch)
        m.d.sync += self.jump_next.eq(self.jump)
        m.d.sync += self.branch_next2.eq(self.branch_next)
        m.d.sync += self.jump_next2.eq(self.jump_next)
        m.d.sync += self.branch_next3.eq(self.branch_next2)
        m.d.sync += self.jump_next3.eq(self.jump_next2)
        m.d.sync += self.stall_next.eq(self.stall)
        m.d.sync += self.stall_next2.eq(self.stall_next)
        m.d.sync += self.stall_next3.eq(self.stall_next2)
        m.d.sync += self.inst_prev.eq(self.inst_out)
        
        with m.If(self.stall_next == Const(1)):
            m.d.comb += self.inst_in.eq(self.IF2_out)
            m.d.comb += self.inst_out.eq(self.inst_prev)
            
        with m.Elif(self.branch_next == Const(1)):
            m.d.comb += self.inst_in.eq(0b00000000000000000000000000000000)
            m.d.comb += self.inst_out.eq(0b00000000000000000000000000000000)
            
        with m.Elif(self.jump_next == Const(1)):
            m.d.comb += self.inst_in.eq(0b00000000000000000000000000000000)
            m.d.comb += self.inst_out.eq(0b00000000000000000000000000000000)
        
        with m.Elif(self.stall_next2 == Const(1)):
            m.d.comb += self.inst_in.eq(self.buffer)
            m.d.comb += self.inst_out.eq(self.inst_in)
        
        with m.Elif(self.branch_next2 == Const(1)):
            m.d.comb += self.inst_in.eq(0b00000000000000000000000000000000)
            m.d.comb += self.inst_out.eq(0b00000000000000000000000000000000)
            
        with m.Elif(self.jump_next2 == Const(1)):
            m.d.comb += self.inst_in.eq(0b00000000000000000000000000000000)
            m.d.comb += self.inst_out.eq(0b00000000000000000000000000000000)
        
        with m.Elif(self.stall_next3 == Const(1)):
            m.d.comb += self.inst_in.eq(self.buffer)
            m.d.comb += self.inst_out.eq(self.inst_in)
        
        with m.Elif(self.branch_next3 == Const(1)):
            m.d.comb += self.inst_in.eq(0b00000000000000000000000000000000)
            m.d.comb += self.inst_out.eq(0b00000000000000000000000000000000)
            
        with m.Elif(self.jump_next3 == Const(1)):
            m.d.comb += self.inst_in.eq(0b00000000000000000000000000000000)
            m.d.comb += self.inst_out.eq(0b00000000000000000000000000000000)
        
        with m.Else():
            m.d.comb += self.inst_in.eq(self.IF2_out)
            m.d.comb += self.inst_out.eq(self.inst_in)
            
        return m
    
    def ports(self)->List[Signal]:
        return []
