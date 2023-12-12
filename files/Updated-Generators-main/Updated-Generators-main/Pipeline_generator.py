import json 
f = open('All.json','r')
y=json.loads(f.read())

dic = y['pipelines']

value_zeros = '0'*y['value_bit_width']

s=""
if (y['pipelines']['ID-ALU']!=True):

    s=f'''from typing import List
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
        self.inst_in = Signal({y['value_bit_width']})
        self.inst_prev = Signal({y['value_bit_width']})
        self.IF2_out = Signal({y['value_bit_width']})
        self.buffer = Signal({y['value_bit_width']})
        
        self.inst_out = Signal({y['value_bit_width']})

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
            m.d.comb += self.inst_in.eq(0b{value_zeros})
            m.d.comb += self.inst_out.eq(0b{value_zeros})
            
        with m.Elif(self.jump_next == Const(1)):
            m.d.comb += self.inst_in.eq(0b{value_zeros})
            m.d.comb += self.inst_out.eq(0b{value_zeros})
        
        with m.Elif(self.stall_next2 == Const(1)):
            m.d.comb += self.inst_in.eq(self.buffer)
            m.d.comb += self.inst_out.eq(self.inst_in)
        
        with m.Elif(self.branch_next2 == Const(1)):
            m.d.comb += self.inst_in.eq(0b{value_zeros})
            m.d.comb += self.inst_out.eq(0b{value_zeros})
            
        with m.Elif(self.jump_next2 == Const(1)):
            m.d.comb += self.inst_in.eq(0b{value_zeros})
            m.d.comb += self.inst_out.eq(0b{value_zeros})
        
        with m.Elif(self.stall_next3 == Const(1)):
            m.d.comb += self.inst_in.eq(self.buffer)
            m.d.comb += self.inst_out.eq(self.inst_in)
        
        with m.Elif(self.branch_next3 == Const(1)):
            m.d.comb += self.inst_in.eq(0b{value_zeros})
            m.d.comb += self.inst_out.eq(0b{value_zeros})
            
        with m.Elif(self.jump_next3 == Const(1)):
            m.d.comb += self.inst_in.eq(0b{value_zeros})
            m.d.comb += self.inst_out.eq(0b{value_zeros})
        
        with m.Else():
            m.d.comb += self.inst_in.eq(self.IF2_out)
            m.d.comb += self.inst_out.eq(self.inst_in)
            
        return m
    
    def ports(self)->List[Signal]:
        return []
'''

else:
    s=f'''from typing import List
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
        self.inst_in = Signal({y['value_bit_width']})
        self.inst_prev = Signal({y['value_bit_width']})
        self.IF2_out = Signal({y['value_bit_width']})
        self.buffer = Signal({y['value_bit_width']})
        self.buffer2 = Signal({y['value_bit_width']})
        
        self.inst_out = Signal({y['value_bit_width']})

        self.stall = Signal(1)
        self.branch = Signal(1)
        self.jump = Signal(1)
        self.stall_next = Signal(1)
        self.stall_next2 = Signal(1)
        self.stall_next3 = Signal(1)
        self.stall_next4 = Signal(1)
        self.branch_next = Signal(1)
        self.jump_next = Signal(1)
        self.branch_next2 = Signal(1)
        self.jump_next2 = Signal(1)
        self.branch_next3 = Signal(1)
        self.jump_next3 = Signal(1)
    
    def elaborate(self, platform:Platform) -> Module:
        m = Module()
        
        m.d.sync += self.branch_next.eq(self.branch)
        m.d.sync += self.jump_next.eq(self.jump)
        m.d.sync += self.branch_next2.eq(self.branch_next)
        m.d.sync += self.jump_next2.eq(self.jump_next)
        m.d.sync += self.branch_next3.eq(self.branch_next2)
        m.d.sync += self.jump_next3.eq(self.jump_next2)
        m.d.sync += self.stall_next.eq(self.stall)
        m.d.sync += self.stall_next2.eq(self.stall_next)
        m.d.sync += self.stall_next3.eq(self.stall_next2)
        m.d.sync += self.stall_next4.eq(self.stall_next3)
        m.d.sync += self.inst_prev.eq(self.inst_out)
        m.d.sync += self.buffer2.eq(self.buffer)

        with m.If((self.stall_next == Const(1)) & (self.stall_next2 != Const(1))):
            m.d.sync += self.buffer.eq(self.IF2_out)
            m.d.comb += self.inst_in.eq(self.IF2_out)
            m.d.comb += self.inst_out.eq(self.inst_prev)       
        
        with m.Elif((self.stall_next == Const(1)) & (self.stall_next2 == Const(1))):
            m.d.sync += self.buffer.eq(self.IF2_out)
            m.d.comb += self.inst_in.eq(self.buffer2)
            m.d.comb += self.inst_out.eq(self.inst_prev)
            
        with m.Elif(self.branch_next == Const(1)):
            m.d.sync += self.buffer.eq(self.IF2_out)
            m.d.comb += self.inst_in.eq(0b{value_zeros})
            m.d.comb += self.inst_out.eq(0b{value_zeros})
            
        with m.Elif(self.jump_next == Const(1)):
            m.d.sync += self.buffer.eq(self.IF2_out)
            m.d.comb += self.inst_in.eq(0b{value_zeros})
            m.d.comb += self.inst_out.eq(0b{value_zeros})
        
        with m.Elif((self.stall_next2 == Const(1)) & (self.stall_next3 == Const(1))):
            m.d.sync += self.buffer.eq(self.IF2_out)
            m.d.comb += self.inst_in.eq(self.buffer2)
            m.d.comb += self.inst_out.eq(self.inst_in)
        
        with m.Elif(self.branch_next2 == Const(1)):
            m.d.sync += self.buffer.eq(self.IF2_out)
            m.d.comb += self.inst_in.eq(0b{value_zeros})
            m.d.comb += self.inst_out.eq(0b{value_zeros})
            
        with m.Elif(self.jump_next2 == Const(1)):
            m.d.sync += self.buffer.eq(self.IF2_out)
            m.d.comb += self.inst_in.eq(0b{value_zeros})
            m.d.comb += self.inst_out.eq(0b{value_zeros})
        
        with m.Elif((self.stall_next3 == Const(1)) & (self.stall_next4 == Const(1))):
            m.d.sync += self.buffer.eq(self.buffer)
            m.d.comb += self.inst_in.eq(self.buffer2)
            m.d.comb += self.inst_out.eq(self.inst_in)
        
        with m.Elif(self.branch_next3 == Const(1)):
            m.d.sync += self.buffer.eq(self.IF2_out)
            m.d.comb += self.inst_in.eq(0b{value_zeros})
            m.d.comb += self.inst_out.eq(0b{value_zeros})
            
        with m.Elif(self.jump_next3 == Const(1)):
            m.d.sync += self.buffer.eq(self.IF2_out)
            m.d.comb += self.inst_in.eq(0b{value_zeros})
            m.d.comb += self.inst_out.eq(0b{value_zeros})
        
        with m.Else():
            m.d.sync += self.buffer.eq(self.IF2_out)
            m.d.comb += self.inst_in.eq(self.IF2_out)
            m.d.comb += self.inst_out.eq(self.inst_in)
            
        return m
    
    def ports(self)->List[Signal]:
        return []


'''

f1=open('IF_ID_pipeline.py','w+')
f1.write(s)

if dic["ID-ALU"] == True:
    s=f'''
from typing import List
from nmigen.back import rtlil, verilog
from nmigen import *
#from nmigen.back.pysim import Simulator, Delay, Settle
#from nmigen.sim import *
from nmigen import Elaboratable,Module,Signal
from nmigen.build import Platform
from nmigen.cli import main_parser,main_runner

class ID_ALU_Pipeline(Elaboratable):
    def __init__(self):

        # ID-ALU pipeline
        self.RA_in = Signal({y['value_bit_width']})
        self.RB_in = Signal({y['value_bit_width']})
        self.RA_out = Signal({y['value_bit_width']})
        self.RB_out = Signal({y['value_bit_width']})
        self.ID_ALU_reg_addr_in = Signal({y['address_size']})
        self.ID_ALU_reg_addr_out = Signal({y['address_size']})
        self.shamt_in = Signal({y['shamt']})
        self.shamt_out = Signal({y['shamt']})
        self.immediate_in = Signal({y['value_bit_width']})
        self.immediate_out = Signal({y['value_bit_width']})
        self.instruction_type_in = Signal(3)
        self.instruction_type_out = Signal(3)
        self.it0_in = Signal(17)
        self.it0_out = Signal(17)
        self.it1_in = Signal(11)
        self.it1_out = Signal(11)
        self.it2_in = Signal(11)
        self.it2_out = Signal(11)
        self.it3_in = Signal(7)
        self.it3_out = Signal(7)
        self.s1_in = Signal({y['address_size']})
        self.s2_in = Signal({y['address_size']})
        self.s1_out = Signal({y['address_size']})
        self.s2_out = Signal({y['address_size']})

    
    def elaborate(self, platform:Platform) -> Module:
        m = Module()

        m.d.sync += self.RA_out.eq(self.RA_in)
        m.d.sync += self.RB_out.eq(self.RB_in)
        m.d.sync += self.ID_ALU_reg_addr_out.eq(self.ID_ALU_reg_addr_in)
        m.d.sync += self.shamt_out.eq(self.shamt_in)
        m.d.sync += self.immediate_out.eq(self.immediate_in)
        m.d.sync += self.instruction_type_out.eq(self.instruction_type_in)
        m.d.sync += self.it0_out.eq(self.it0_in)
        m.d.sync += self.it1_out.eq(self.it1_in)
        m.d.sync += self.it2_out.eq(self.it2_in)
        m.d.sync += self.it3_out.eq(self.it3_in)
        m.d.sync += self.s1_out.eq(self.s1_in)
        m.d.sync += self.s2_out.eq(self.s2_in)

        return m
    
    def ports(self)->List[Signal]:
        return []
'''
    f1=open('ID_ALU_pipeline.py','w+')
    f1.write(s)

if dic["ALU-M1"] == True:
    s=f'''
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

        self.ALU_Rb_out = Signal(signed({y['value_bit_width']}))
        self.memory_data_in_in = Signal(signed({y['value_bit_width']}))
        self.ALU_result_out = Signal(signed({y['value_bit_width']}))
        self.memory_addr_in = Signal(signed({y['value_bit_width']}))
        self.ALU_load_wb_out = Signal(1)
        self.memory_load_wb_in = Signal(1)
        self.ALU_reg_addr_out_out = Signal({y['address_size']})
        self.memory_reg_addr_out_in = Signal({y['address_size']})
        self.memory_alu_result_in = Signal({y['value_bit_width']})

        self.ALU_csb = Signal(1)
        self.memory_csb = Signal(1)
        self.ALU_web = Signal(1)
        self.memory_web = Signal(1)
        self.ALU_wmask = Signal(4)
        self.mem_wmask = Signal(4)
                        
        self.s1_in = Signal({y['address_size']})
        self.s2_in = Signal({y['address_size']})
        self.s1_out = Signal({y['address_size']})
        self.s2_out = Signal({y['address_size']})
    
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
'''
    f1=open('ALU_M1_pipeline.py','w+')
    f1.write(s)


s=f'''
from typing import List
from nmigen.back import rtlil, verilog
from nmigen import *
#from nmigen.back.pysim import Simulator, Delay, Settle
#from nmigen.sim import *
from nmigen import Elaboratable,Module,Signal
from nmigen.build import Platform
from nmigen.cli import main_parser,main_runner

class M1_M2_Pipeline(Elaboratable):
    def __init__(self):
        
        self.reg_file_write_in = Signal(1)
        self.reg_file_write_out = Signal(1)
        self.memory_reg_addr_out_out = Signal({y['address_size']})
        self.reg_file_write_addr_in = Signal({y['address_size']})
        self.memory_data_out_out = Signal({y['value_bit_width']})
        self.reg_file_write_data_in = Signal({y['value_bit_width']})

        self.s1_in = Signal({y['address_size']})
        self.s2_in = Signal({y['address_size']})
        self.s1_out = Signal({y['address_size']})
        self.s2_out = Signal({y['address_size']})

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

'''
f1=open('M1_M2_pipeline.py','w+')
f1.write(s)


s=f'''
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
        self.memory_reg_addr_out_out = Signal({y['address_size']})
        self.reg_file_write_addr_in = Signal({y['address_size']})
        self.memory_data_out_out = Signal({y['value_bit_width']})
        self.reg_file_write_data_in = Signal({y['value_bit_width']})

        self.s1_in = Signal({y['address_size']})
        self.s2_in = Signal({y['address_size']})
        self.s1_out = Signal({y['address_size']})
        self.s2_out = Signal({y['address_size']})

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

'''
f1=open('M2_WB_pipeline.py','w+')
f1.write(s)

