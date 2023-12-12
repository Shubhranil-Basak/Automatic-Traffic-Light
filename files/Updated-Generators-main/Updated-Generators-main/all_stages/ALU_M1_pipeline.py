
from typing import List
from nmigen.back import rtlil, verilog
from nmigen import *
#from nmigen.back.pysim import Simulator, Delay, Settle
#from nmigen.sim import *
from nmigen import Elaboratable,Module,Signal
from nmigen.build import Platform
from nmigen.cli import main_parser,main_runner

class ALU_M1_Pipeline(Elaboratable):
    def __init__(self):

        #ALU-MEM pipeline

        self.ALU_Rb_out = Signal(signed(32))
        self.memory_data_in_in = Signal(signed(32))
        self.ALU_result_out = Signal(signed(32))
        self.memory_addr_in = Signal(signed(32))
        self.ALU_load_wb_out = Signal(1)
        self.memory_load_wb_in = Signal(1)
        self.ALU_reg_addr_out_out = Signal(5)
        self.memory_reg_addr_out_in = Signal(5)
        self.memory_alu_result_in = Signal(32)

        self.ALU_csb = Signal(1)
        self.memory_csb = Signal(1)
        self.ALU_web = Signal(1)
        self.memory_web = Signal(1)
        self.ALU_wmask = Signal(4)
        self.mem_wmask = Signal(4)
                        
        self.s1_in = Signal(5)
        self.s2_in = Signal(5)
        self.s1_out = Signal(5)
        self.s2_out = Signal(5)
    
    def elaborate(self, platform:Platform) -> Module:
        m = Module()

        m.d.sync += self.memory_data_in_in.eq(self.ALU_Rb_out)
        m.d.sync += self.memory_addr_in.eq(self.ALU_result_out)
        m.d.sync += self.memory_load_wb_in.eq(self.ALU_load_wb_out)
        m.d.sync += self.memory_reg_addr_out_in.eq(self.ALU_reg_addr_out_out)
        m.d.sync += self.memory_alu_result_in.eq(self.ALU_result_out)
        m.d.sync += self.s1_out.eq(self.s1_in)
        m.d.sync += self.s2_out.eq(self.s2_in)
        m.d.sync += self.mem_wmask.eq(self.ALU_wmask)
        m.d.sync += self.memory_web.eq(self.ALU_web)
        m.d.sync += self.memory_csb.eq(self.ALU_csb)

        return m
    
    def ports(self)->List[Signal]:
        return []
