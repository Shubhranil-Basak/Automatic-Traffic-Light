
from typing import List
from nmigen.back import rtlil, verilog
from nmigen import *
#from nmigen.back.pysim import Simulator, Delay, Settle
#from nmigen.sim import *
from nmigen import Elaboratable,Module,Signal
from nmigen.build import Platform
from nmigen.cli import main_parser,main_runner

class M2_WB_Pipeline(Elaboratable):
    def __init__(self):
        
        self.reg_file_write_in = Signal(1)
        self.reg_file_write_out = Signal(1)
        self.memory_reg_addr_out_out = Signal(5)
        self.reg_file_write_addr_in = Signal(5)
        self.memory_data_out_out = Signal(32)
        self.reg_file_write_data_in = Signal(32)

        self.s1_in = Signal(5)
        self.s2_in = Signal(5)
        self.s1_out = Signal(5)
        self.s2_out = Signal(5)

        self.csb_in = Signal(1)
        self.csb_out = Signal(1)
        self.web_in = Signal(1)
        self.web_out = Signal(1)

    
    def elaborate(self, platform:Platform) -> Module:
        m = Module()

        m.d.sync += self.reg_file_write_out.eq(self.reg_file_write_in)
        m.d.sync += self.reg_file_write_addr_in.eq(self.memory_reg_addr_out_out)
        m.d.sync += self.reg_file_write_data_in.eq(self.memory_data_out_out)
        m.d.sync += self.s1_out.eq(self.s1_in)
        m.d.sync += self.s2_out.eq(self.s2_in)
        m.d.sync += self.csb_out.eq(self.csb_in)
        m.d.sync += self.web_out.eq(self.web_in)

        return m
    
    def ports(self)->List[Signal]:
        return []

