from decimaltohexconverter import decToHexa
import json
f = open('All.json','r')
y=json.loads(f.read())

stack = decToHexa(2**(y['data_mem_bit_width'])-1, y['value_bit_width'])
gp = decToHexa(2**(y['data_mem_bit_width']) + 2047 , y['value_bit_width'])
s=f'''from typing import List

from nmigen import *
#from nmigen.sim import *

from nmigen import Elaboratable,Module,Signal
from nmigen.build import Platform
from nmigen.cli import main_parser,main_runner

class Register_file(Elaboratable):
    def __init__(self):
        #inputs
        self.load_Rs1_addr = Signal({y['address_size']})
        self.load_Rs2_addr = Signal({y['address_size']})
        self.write = Signal(1)
        self.write_addr = Signal({y['address_size']})
        self.write_data = Signal({y['value_bit_width']})

        #output 
        self.write_Rs1_data = Signal({y['value_bit_width']})
        self.write_Rs2_data = Signal({y['value_bit_width']})
        self.reg_update = Array([Signal(1) for i in range(2**5)])

        self.reg = Array([Signal(signed({y['value_bit_width']})) for i in range(2**5)])

        self.load_Rs1_addr = Signal({y['address_size']})
        self.load_Rs2_addr = Signal({y['address_size']})
        self.pc = Signal({y['pc_bit_width']})

        self.write_alu = Signal(1)
        self.write_addr_alu = Signal({y['address_size']})
        self.write_data_alu = Signal({y['value_bit_width']})
        self.csb_alu = Signal(1)
        self.web_alu = Signal(1)

        self.write_mem = Signal(1)
        self.write_addr_mem = Signal({y['address_size']})
        self.write_data_mem = Signal({y['value_bit_width']})
        self.csb_mem = Signal(1)
        self.web_mem = Signal(1)

        self.gpio_input = Signal({y['value_bit_width']})

        #output 
        self.write_Rs1_data = Signal({y['value_bit_width']})
        self.write_Rs2_data = Signal({y['value_bit_width']})
        self.reg_update = Array([Signal(1) for i in range(2**5)])

        self.reg =   Array([Signal(signed({y['value_bit_width']})) for i in range(2**{y['address_size']})])


    def elaborate(self,platform:Platform)->Module:
        m = Module()

        with m.If(self.pc < 3):

            m.d.neg += self.reg_update[Const(2)].eq(Const(0)) 
            m.d.neg += self.reg[Const(2)].eq(Const(0x{stack}))

        with m.If(self.reg_update[Const(2)] == Const(0)):
            m.d.neg += self.reg[Const(2)].eq(Const(0x{stack}))
        
        m.d.neg += self.reg[Const(30)].eq(self.gpio_input)
        m.d.neg += self.reg[Const(3)].eq(Const(0x{gp}))
        m.d.neg += self.reg[Const(0)].eq(Const(0x00000000)) 
        m.d.comb += self.write_Rs1_data.eq(self.reg[self.load_Rs1_addr])
        m.d.comb += self.write_Rs2_data.eq(self.reg[self.load_Rs2_addr])

        with m.If(self.write_mem):
            with m.If((self.csb_mem  == Const(0)) & (self.web_mem == Const(1))):
                m.d.neg += self.reg[self.write_addr_mem].eq(self.write_data_mem)
                m.d.neg += self.reg_update[self.write_addr_mem].eq(Const(1))
            with m.Else():
                m.d.neg += self.reg[Const(0)].eq(0)
                # m.d.neg += self.reg_update[Const(2)].eq(Const(0))
        with m.Else():
            m.d.neg += self.reg[Const(0)].eq(0)
            # m.d.neg += self.reg_update[Const(2)].eq(Const(0))
		
        with m.If((self.write_alu)):
            with m.If((self.csb_alu != Const(0))):
                m.d.neg += self.reg[self.write_addr_alu].eq(self.write_data_alu)
                m.d.neg += self.reg_update[self.write_addr_alu].eq(Const(1))
            with m.Else():
                m.d.neg += self.reg[Const(0)].eq(0)
                # m.d.neg += self.reg_update[Const(2)].eq(Const(0))
        with m.Else():
            m.d.neg += self.reg[Const(0)].eq(0)
            # m.d.neg += self.reg_update[Const(2)].eq(Const(0))
        
        return m

    def ports(self)->List[Signal]:
        return [] 

'''

f1=open('reg_file.py','w+')
f1.write(s)

