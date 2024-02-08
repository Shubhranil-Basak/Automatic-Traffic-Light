import json
f = open('All.json','r')
y=json.loads(f.read())

s1 = f'''from typing import List
from nmigen import *
#from nmigen.sim import *
from nmigen import Elaboratable,Module,Signal
from nmigen.build import Platform
from nmigen.cli import main_parser,main_runner

class PC_controller(Elaboratable):

    def __init__(self):

        #inputs
        self.stall = Signal(1)
        self.branch = Signal(1)
        self.jump = Signal(1)
        self.immediate = Signal({y['value_bit_width']})
        self.ra = Signal({y['value_bit_width']})
        self.pc_in = Signal({y['pc_bit_width']})

        self.read_flag = Signal(1)

        #outputs
        self.pc = Signal({y['pc_bit_width']})
       

    def elaborate(self,platform:Platform)->Module:
        m = Module()

        with m.If(self.read_flag == 0): 
            m.d.sync += self.pc.eq(Const(0))

        with m.Else(): 
            with m.If(self.stall == Const(1)):
                m.d.sync += self.pc.eq(self.pc_in)
            
            with m.Elif(self.branch == Const(1)):
                m.d.sync += self.pc.eq(self.pc_in + self.immediate//4 - Const({y['ALU_dist']}))
            
            with m.Elif(self.jump == Const(1)):
                m.d.sync += self.pc.eq(self.ra + self.immediate//4 )
            
            with m.Else():
                m.d.sync += self.pc.eq(self.pc_in + Const(1))

        return m

    def ports(self)->List[Signal]:
        return []
    
'''

f1=open('pc_controller.py','w+')
f1.write(s1)