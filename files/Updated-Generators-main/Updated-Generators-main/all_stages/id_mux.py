from typing import List
from nmigen import *
#from nmigen.sim import *
from nmigen import Elaboratable,Module,Signal
from nmigen.build import Platform
from nmigen.cli import main_parser,main_runner

class ID_mux(Elaboratable):

    def __init__(self):

        #inputs
        self.des_id = Signal(5)
        self.s1_id = Signal(5)
        self.s2_id = Signal(5)
        self.s1data_out_id = Signal(signed(32))
        self.s2data_out_id = Signal(signed(32))
        self.signextended_immediate_id = Signal(signed(32))
        self.instruction_type_id = Signal(3)
        self.it0_id = Signal(17)
        self.it1_id = Signal(11)
        self.it2_id = Signal(11)
        self.it3_id = Signal(7)
        self.ifload_id = Signal(1)
        self.shamt_id = Signal(5)

        self.stall = Signal(1)

        #outputs
        self.des = Signal(5)
        self.s1 = Signal(5)
        self.s2 = Signal(5)
        self.s1data_out = Signal(signed(32))
        self.s2data_out = Signal(signed(32))
        self.signextended_immediate = Signal(signed(32))
        self.instruction_type = Signal(3)
        self.it0 = Signal(17)
        self.it1 = Signal(11)
        self.it2 = Signal(11)
        self.it3 = Signal(7)
        self.ifload = Signal(1)
        self.shamt = Signal(5)

    def elaborate(self,platform:Platform)->Module:
        m = Module()
        with m.If(self.stall == Const(1)):
            m.d.comb += self.des.eq(0b00000)
            m.d.comb += self.s1.eq(0b00000)
            m.d.comb += self.s2.eq(0b00000)
            m.d.comb += self.s1data_out.eq(0b00000000000000000000000000000000)
            m.d.comb += self.s2data_out.eq(0b00000000000000000000000000000000)
            m.d.comb += self.signextended_immediate.eq(0b00000000000000000000000000000000)
            m.d.comb += self.instruction_type.eq(0b000)
            m.d.comb += self.it0.eq(0b00000000000000000)
            m.d.comb += self.it1.eq(0b00000000000)
            m.d.comb += self.it2.eq(0b00000000000)
            m.d.comb += self.it3.eq(0b0000000)
            m.d.comb += self.ifload.eq(0b0)
            m.d.comb += self.shamt.eq(0b00000)
    

        with m.Else():
            m.d.comb += self.des.eq(self.des_id)
            m.d.comb += self.s1.eq(self.s1_id)
            m.d.comb += self.s2.eq(self.s2_id)
            m.d.comb += self.s1data_out.eq(self.s1data_out_id)
            m.d.comb += self.s2data_out.eq(self.s2data_out_id)
            m.d.comb += self.signextended_immediate.eq(self.signextended_immediate_id)
            m.d.comb += self.instruction_type.eq(self.instruction_type_id)
            m.d.comb += self.it0.eq(self.it0_id)
            m.d.comb += self.it1.eq(self.it1_id)
            m.d.comb += self.it2.eq(self.it2_id)
            m.d.comb += self.it3.eq(self.it3_id)
            m.d.comb += self.ifload.eq(self.ifload_id)
            m.d.comb += self.shamt.eq(self.shamt_id)


        return m

    def ports(self)->List[Signal]:
        return []
