import json
f = open('All.json','r')
y=json.loads(f.read())

addr_zeros = '0'*y['address_size']
value_zeros = '0'*y['value_bit_width']
shamt_zeros = '0'*y['shamt']

s1 = f'''from typing import List
from nmigen import *
#from nmigen.sim import *
from nmigen import Elaboratable,Module,Signal
from nmigen.build import Platform
from nmigen.cli import main_parser,main_runner

class ID_mux(Elaboratable):

    def __init__(self):

        #inputs
        self.des_id = Signal({y['address_size']})
        self.s1_id = Signal({y['address_size']})
        self.s2_id = Signal({y['address_size']})
        self.s1data_out_id = Signal(signed({y['value_bit_width']}))
        self.s2data_out_id = Signal(signed({y['value_bit_width']}))
        self.signextended_immediate_id = Signal(signed({y['value_bit_width']}))
        self.instruction_type_id = Signal(3)
        self.it0_id = Signal(17)
        self.it1_id = Signal(11)
        self.it2_id = Signal(11)
        self.it3_id = Signal(7)
        self.ifload_id = Signal(1)
        self.shamt_id = Signal({y['shamt']})

        self.stall = Signal(1)
'''

if (y['pipelines']['ID-ALU']):

    s1+='''
        self.branch = Signal(1)
        self.jump = Signal(1)
    '''


s1+=f'''
        #outputs
        self.des = Signal({y['address_size']})
        self.s1 = Signal({y['address_size']})
        self.s2 = Signal({y['address_size']})
        self.s1data_out = Signal(signed({y['value_bit_width']}))
        self.s2data_out = Signal(signed({y['value_bit_width']}))
        self.signextended_immediate = Signal(signed({y['value_bit_width']}))
        self.instruction_type = Signal(3)
        self.it0 = Signal(17)
        self.it1 = Signal(11)
        self.it2 = Signal(11)
        self.it3 = Signal(7)
        self.ifload = Signal(1)
        self.shamt = Signal({y['shamt']})

    def elaborate(self,platform:Platform)->Module:
        m = Module()
        with m.If(self.stall == Const(1)):
            m.d.comb += self.des.eq(0b{addr_zeros})
            m.d.comb += self.s1.eq(0b{addr_zeros})
            m.d.comb += self.s2.eq(0b{addr_zeros})
            m.d.comb += self.s1data_out.eq(0b{value_zeros})
            m.d.comb += self.s2data_out.eq(0b{value_zeros})
            m.d.comb += self.signextended_immediate.eq(0b{value_zeros})
            m.d.comb += self.instruction_type.eq(0b000)
            m.d.comb += self.it0.eq(0b00000000000000000)
            m.d.comb += self.it1.eq(0b00000000000)
            m.d.comb += self.it2.eq(0b00000000000)
            m.d.comb += self.it3.eq(0b0000000)
            m.d.comb += self.ifload.eq(0b0)
            m.d.comb += self.shamt.eq(0b{shamt_zeros})
    
'''

if (y['pipelines']['ID-ALU']):

    s1+=f'''
        with m.Elif(self.jump == Const(1)):
            m.d.comb += self.des.eq(0b{addr_zeros})
            m.d.comb += self.s1.eq(0b{addr_zeros})
            m.d.comb += self.s2.eq(0b{addr_zeros})
            m.d.comb += self.s1data_out.eq(0b{value_zeros})
            m.d.comb += self.s2data_out.eq(0b{value_zeros})
            m.d.comb += self.signextended_immediate.eq(0b{value_zeros})
            m.d.comb += self.instruction_type.eq(0b000)
            m.d.comb += self.it0.eq(0b00000000000000000)
            m.d.comb += self.it1.eq(0b00000000000)
            m.d.comb += self.it2.eq(0b00000000000)
            m.d.comb += self.it3.eq(0b0000000)
            m.d.comb += self.ifload.eq(0b0)
            m.d.comb += self.shamt.eq(0b{shamt_zeros})
        
        with m.Elif(self.branch == Const(1)):
            m.d.comb += self.des.eq(0b{addr_zeros})
            m.d.comb += self.s1.eq(0b{addr_zeros})
            m.d.comb += self.s2.eq(0b{addr_zeros})
            m.d.comb += self.s1data_out.eq(0b{value_zeros})
            m.d.comb += self.s2data_out.eq(0b{value_zeros})
            m.d.comb += self.signextended_immediate.eq(0b{value_zeros})
            m.d.comb += self.instruction_type.eq(0b000)
            m.d.comb += self.it0.eq(0b00000000000000000)
            m.d.comb += self.it1.eq(0b00000000000)
            m.d.comb += self.it2.eq(0b00000000000)
            m.d.comb += self.it3.eq(0b0000000)
            m.d.comb += self.ifload.eq(0b0)
            m.d.comb += self.shamt.eq(0b{shamt_zeros})
    '''

s1+='''
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
'''

f1=open('id_mux.py','w+')
f1.write(s1)