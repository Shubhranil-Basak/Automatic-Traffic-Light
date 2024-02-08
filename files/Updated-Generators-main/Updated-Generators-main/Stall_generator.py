import json
f = open('All.json','r')
y=json.loads(f.read())

num_sets = 1
if (y['pipelines']['ID-ALU']):
    num_sets+=1

if (num_sets == 1):

    s=f'''
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
        self.next_dest0 = Signal({y['address_size']})
        self.ID_src1 = Signal({y['address_size']})
        self.ID_src2 = Signal({y['address_size']})
        self.csb1 = Signal(1)
        self.web1 = Signal(1)
        self.next_dest1 = Signal({y['address_size']})

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
'''

elif (num_sets == 2):

    s = f'''
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
        self.next_dest0 = Signal({y['address_size']})
        self.ID_src1 = Signal({y['address_size']})
        self.ID_src2 = Signal({y['address_size']})
        self.csb1 = Signal(1)
        self.web1 = Signal(1)
        self.next_dest1 = Signal({y['address_size']})

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
'''
f1=open('Stall_unit.py','w+')
f1.write(s)