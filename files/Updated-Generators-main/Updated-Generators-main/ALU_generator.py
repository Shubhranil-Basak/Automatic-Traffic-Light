import json
f = open('All.json','r')
y=json.loads(f.read())

d = 1 - y['ALU_dist']
d1 = -y['ALU_dist']

s = f'''
from typing import List
from nmigen.back import rtlil, verilog
from nmigen import *
from nmigen.sim import *
from nmigen import Elaboratable,Module,Signal
from nmigen.build import Platform
from nmigen.cli import main_parser,main_runner

class ALU(Elaboratable):
\t\tdef __init__(self):
\t\t\tself.Ra_unsigned = Signal({y['value_bit_width']})
\t\t\tself.Rb_unsigned = Signal({y['value_bit_width']})
\t\t\tself.Ra = Signal(signed({y['value_bit_width']}))
\t\t\tself.Rb= Signal(signed({y['value_bit_width']}))
\t\t\tself.result = Signal({y['value_bit_width']})
\t\t\tself.result64 = Signal(signed({2*y['value_bit_width']}))
\t\t\tself.inst_type = Signal(3)
\t\t\tself.inst_type0 = Signal(17)
\t\t\tself.inst_type1 = Signal(11)
\t\t\tself.inst_type2 = Signal(11)
\t\t\tself.inst_type3 = Signal(7)
\t\t\tself.reg_addr_in = Signal({y['address_size']})
\t\t\tself.immediate = Signal(signed({y['value_bit_width']}))
\t\t\tself.branching = Signal(1)
\t\t\tself.data_to_mem = Signal({y['value_bit_width']})
\t\t\tself.inst_type_out = Signal(3)
\t\t\tself.inst_type1_out = Signal(11)
\t\t\tself.inst_type2_out = Signal(11)
\t\t\tself.inst_type3_out = Signal(7)
\t\t\tself.reg_addr_out = Signal({y['address_size']})
\t\t\tself.jump = Signal(1)
\t\t\tself.pc = Signal({y['pc_bit_width']})
\t\t\tself.shamt = Signal({y['shamt']})
\t\t\tself.shamt1 = Signal({y['shamt']})
\t\t\tself.csb = Signal(1)
\t\t\tself.web = Signal(1)
\t\t\t# self.load_mem = Signal(2)
\t\t\t# self.write_mem = Signal(2)
\t\t\tself.load_wb = Signal(1)
\t\t\tself.wmask = Signal(4,reset = 0x0)
\t\t\tself.s1 = Signal({y['address_size']})
\t\t\tself.s2 = Signal({y['address_size']})\n'''

inits = {
    "LUI" 	: "\t\t\tself.LUI     =   0b0110111",	
    "AUIPC" : "\t\t\tself.AUIPC   =   0b0010111",	
    "JAL" 	: "\t\t\tself.JAL     =   0b1101111",	
    "JALR"	: "\t\t\tself.JALR	=	0b0001100111",
    "BEQ"	: "\t\t\tself.BEQ     =   0b0001100011",
    "BNE" 	: "\t\t\tself.BNE     =   0b0011100011",
    "BLT" 	: "\t\t\tself.BLT     =   0b1001100011",
    "BGE" 	: "\t\t\tself.BGE     =   0b1011100011",
    "BLTU" 	: "\t\t\tself.BLTU    =   0b1101100011",
    "BGEU" 	: "\t\t\tself.BGEU    =   0b1111100011",
    "LB" 	: "\t\t\tself.LB 	=	0b0000000011",
    "LH"	: "\t\t\tself.LH		=	0b0010000011",
    "LW"	: "\t\t\tself.LW      =   0b0100000011",
    "LBU" 	: "\t\t\tself.LBU 	=	0b1000000011",
    "LHU" 	: "\t\t\tself.LHU 	=	0b1010000011",
    "SB" 	: "\t\t\tself.SB 	=	0b0000100011",
    "SH"	: "\t\t\tself.SH		=	0b0010100011",
    "SW"	: "\t\t\tself.SW		=	0b0100100011",
    "ADDI" 	: "\t\t\tself.ADDI    =   0b0000010011",
    "SLTI" 	: "\t\t\tself.SLTI    =   0b0100010011",
    "SLTIU":  "\t\t\tself.SLTIU   =   0b0110010011",
    "XORI"	: "\t\t\tself.XORI    =   0b1000010011",
    "ORI"	: "\t\t\tself.ORI     =   0b1100010011",
    "ANDI"	: "\t\t\tself.ANDI    =   0b1110010011",
    "SLLI" 	: "\t\t\tself.SLLI   =   0b00010010011",
    "SRLI" 	: "\t\t\tself.SRLI   =   0b01010010011",
    "SRAI" 	: "\t\t\tself.SRAI   =   0b11010010011",
    "ADD" 	: "\t\t\tself.ADD = 0b00000110011",
    "SUB" 	: "\t\t\tself.SUB = 0b10000110011",
    "SLL" 	: "\t\t\tself.SLL = 0b00010110011",
    "SLT" 	: "\t\t\tself.SLT = 0b00100110011",
    "SLTU" 	: "\t\t\tself.SLTU = 0b00110110011",
    "XOR" 	: "\t\t\tself.XOR = 0b01000110011",
    "SRL" 	: "\t\t\tself.SRL = 0b01010110011",
    "SRA" 	: "\t\t\tself.SRA = 0b11010110011",
    "OR" 	: "\t\t\tself.OR = 0b01100110011",
    "AND" 	: "\t\t\tself.AND = 0b01110110011",
    "MUL"   : "\t\t\tself.MUL =   0b00000010000110011",
    "MULH"  : "\t\t\tself.MULH =  0b00000010010110011",
    "MULHSU": "\t\t\tself.MULHSU =0b00000010100110011",
    "MULHU" : "\t\t\tself.MULHU = 0b00000010110110011",
    "DIV"   : "\t\t\tself.DIV =   0b00000011000110011",
    "DIVU"  : "\t\t\tself.DIVU =  0b00000011010110011",
    "REM"   : "\t\t\tself.REM =   0b00000011100110011",
    "REMU"  : "\t\t\tself.REMU =  0b00000011110110011",
    "R_type" : "\t\t\tself.R_type = 0b111",
    "I_type" : "\t\t\tself.I_type = 0b001",
    "S_type" : "\t\t\tself.S_type = 0b011",
    "B_type" : "\t\t\tself.B_type = 0b100",
    "U_type" : "\t\t\tself.U_type = 0b101",
    "J_type" : "\t\t\tself.J_type = 0b110",
    "M_type" : "\t\t\tself.M_type = 0b010"
}

dic = y['instructions']
for i in dic:
    if dic[i] == True:
        s+=inits[i]
        s+="\n"


s+= f'''
\t\tdef elaborate(self,platform:Platform)->Module:
\t\t\tm = Module()
\t\t\tm.d.comb += self.inst_type_out.eq(self.inst_type)    
\t\t\tm.d.comb += self.inst_type1_out.eq(self.inst_type1)
\t\t\tm.d.comb += self.inst_type2_out.eq(self.inst_type2)
\t\t\tm.d.comb += self.inst_type3_out.eq(self.inst_type3)
\t\t\tm.d.comb += self.reg_addr_out.eq(self.reg_addr_in)
\t\t\tm.d.comb += self.shamt1.eq(self.Rb[0:{y['shamt']}])
'''

R = ['ADD',"SUB","SLL","SLTU","SLT","XOR","SRL","SRA","OR","AND"]
M = ["MUL","MULH","MULHSU","MULHU","DIV","DIVU","REM","REMU"]
U = ["LUI","AUIPC"]
# J = ["JAL"]
S=['SB','SH','SW']
B=['BEQ','BNE','BLT','BGE','BLTU',"BGEU"]
I1=['ADDI','SLTI','SLTIU','XORI','ORI','ANDI','JALR','SLLI','SRLI','SRAI','LB','LH','LW','LBU','LHU']


dicR = {
    "ADD" 	:"\t\t\t\twith m.If(self.inst_type1==self.ADD):\n\t\t\t\t\t\tm.d.comb += self.result.eq(self.Ra+self.Rb)",
    "SUB" 	:"\t\t\t\twith m.If(self.inst_type1==self.SUB):\n\t\t\t\t\t\tm.d.comb += self.result.eq(self.Ra-self.Rb)",
    "SLT" 	:"\t\t\t\twith m.If(self.inst_type1==self.SLT):\n\t\t\t\t\twith m.If(self.Ra<self.Rb):\n\t\t\t\t\t\t\tm.d.comb+=self.result.eq(1)\n\t\t\t\t\twith m.Else():m.d.comb+=self.result.eq(0)",
    "SLL" 	:"\t\t\t\twith m.If(self.inst_type1==self.SLL):\n\t\t\t\t\tm.d.comb += self.result.eq(self.Ra << self.shamt1)",
    "SLTU" 	:"\t\t\t\twith m.If(self.inst_type1==self.SLTU):\n\t\t\t\t\twith m.If(self.Ra<self.Rb):\n\t\t\t\t\t\tm.d.comb+=self.result.eq(1)\n\t\t\t\t\twith m.Else():m.d.comb+=self.result.eq(0)",
    "XOR" 	:"\t\t\t\twith m.If(self.inst_type1==self.XOR):\n\t\t\t\t\tm.d.comb+=self.result.eq((self.Ra & (~self.Rb)))",
    "SRL" 	:"\t\t\t\twith m.Elif(self.inst_type1==self.SRL):\n\t\t\t\t\tm.d.comb += self.Ra_unsigned.eq(self.Ra)\n\t\t\t\t\tm.d.comb += self.result.eq(self.Ra_unsigned >> self.shamt1)",
    "SRA" 	:"\t\t\t\twith m.Elif(self.inst_type1==self.SRA):\n\t\t\t\t\tm.d.comb += self.result.eq(self.Ra >> self.shamt1)",
    "OR" 	:"\t\t\t\twith m.If(self.inst_type1==self.OR):\n\t\t\t\t\tm.d.comb+=self.result.eq(self.Rb | self.Ra)",
    "AND" 	:"\t\t\t\twith m.If(self.inst_type1==self.AND):\n\t\t\t\t\tm.d.comb+=self.result.eq(self.Rb & self.Ra)",
}

dicM={
    "MUL"   :"\t\t\t\twith m.If(self.inst_type0==self.MUL):\n\t\t\t\t\tm.d.comb+=self.Ra_unsigned.eq(self.Ra)\n\t\t\t\t\tm.d.comb+=self.Rb_unsigned.eq(self.Rb)\n\t\t\t\t\tm.d.comb+=self.result64.eq(self.Ra_unsigned*self.Rb_unsigned)\n\t\t\t\t\tm.d.comb+=self.result.eq(self.result64[0:32])",
    "MULH"  :"\t\t\t\twith m.If(self.inst_type0==self.MULH):#Both are signed\n\t\t\t\t\tm.d.comb+=self.result64.eq(self.Ra*self.Rb)\n\t\t\t\t\tm.d.comb+=self.result.eq(self.result64[32:64])",
    "MULHSU":"\t\t\t\twith m.If(self.inst_type0==self.MULHSU):\n\t\t\t\t\tm.d.comb+=self.Rb_unsigned.eq(self.Rb)\n\t\t\t\t\tm.d.comb+=self.result64.eq(self.Ra*self.Rb_unsigned)\n\t\t\t\t\tm.d.comb+=self.result.eq(self.result64[32:64])",
    "MULHU" :"\t\t\t\twith m.If(self.inst_type0==self.MULHU):\n\t\t\t\t\tm.d.comb+=self.Ra_unsigned.eq(self.Ra)\n\t\t\t\t\tm.d.comb+=self.Rb_unsigned.eq(self.Rb)\n\t\t\t\t\tm.d.comb+=self.result64.eq(self.Ra_unsigned*self.Rb_unsigned)\n\t\t\t\t\tm.d.comb+=self.result.eq(self.result64[32:64])",
    "DIV"   :"\t\t\t\twith m.If(self.inst_type0==self.DIV):\n\t\t\t\t\tself.Ra_unsigned.eq(self.Ra)\n\t\t\t\t\tm.d.comb+=self.Rb_unsigned.eq(self.Rb)\n\t\t\t\t\tm.d.comb+=self.result.eq(self.Ra_unsigned//self.Rb_unsigned)",
    "DIVU"  :"\t\t\t\twith m.If(self.inst_type0==self.DIVU):\n\t\t\t\t\tm.d.comb+=self.Ra_unsigned.eq(self.Ra)\n\t\t\t\t\tm.d.comb+=self.Rb_unsigned.eq(self.Rb)\n\t\t\t\t\tm.d.comb+=self.result.eq(self.Ra_unsigned//self.Rb_unsigned)",
    "REM"   :"\t\t\t\twith m.If(self.inst_type0==self.REM):\n\t\t\t\t\tm.d.comb+=self.Ra_unsigned.eq(self.Ra)\n\t\t\t\t\tm.d.comb+=self.Rb_unsigned.eq(self.Rb)\n\t\t\t\t\tm.d.comb+=self.result.eq(self.Ra_unsigned%self.Rb_unsigned)",
    "REMU"  :"\t\t\t\twith m.If(self.inst_type0==self.REM):\n\t\t\t\t\tm.d.comb+=self.Ra_unsigned.eq(self.Ra)\n\t\t\t\t\tm.d.comb+=self.Rb_unsigned.eq(self.Rb)\n\t\t\t\t\tm.d.comb+=self.result.eq(self.Ra_unsigned%self.Rb_unsigned)",
}

dicU = {
    "LUI"  :"\t\t\t\twith m.If(self.inst_type3==self.LUI):\n\t\t\t\t\tm.d.comb+=self.result.eq(self.immediate)",
    "AUIPC":f"\t\t\t\twith m.If(self.inst_type3==self.AUIPC):\n\t\t\t\t\tm.d.comb+=self.result.eq(self.immediate+self.pc+{d1}) "
}

dicS = {
    "SB":"\t\t\t\twith m.If(self.inst_type2==self.SB):\n\t\t\t\t\tm.d.comb += self.data_to_mem.eq(self.Rb)\n\t\t\t\t\tm.d.comb+=self.result.eq(self.Ra + self.immediate)\n\t\t\t\t\tm.d.comb += self.wmask.eq(0b0001)",
    "SH":"\t\t\t\twith m.If(self.inst_type2==self.SH):\n\t\t\t\t\tm.d.comb += self.data_to_mem.eq(self.Rb)\n\t\t\t\t\tm.d.comb+=self.result.eq(self.Ra + self.immediate)\n\t\t\t\t\tm.d.comb += self.wmask.eq(0b0011)",
    "SW":"\t\t\t\twith m.If(self.inst_type2==self.SW):\n\t\t\t\t\tm.d.comb += self.data_to_mem.eq(self.Rb)\n\t\t\t\t\tm.d.comb+=self.result.eq(self.Ra + self.immediate)\n\t\t\t\t\tm.d.comb += self.wmask.eq(0b1111)",
}

dicB = {
    "BEQ"	: "\t\t\t\twith m.If(self.inst_type2==self.BEQ):\n\t\t\t\t\twith m.If(self.Ra==self.Rb):\n\t\t\t\t\t\tm.d.comb+=self.branching.eq(0b1)\n\t\t\t\t\t\tm.d.comb+=self.result.eq(self.immediate)",
    "BNE" 	: "\t\t\t\twith m.If(self.inst_type2==self.BNE):\n\t\t\t\t\twith m.If(self.Ra!=self.Rb):\n\t\t\t\t\t\tm.d.comb+=self.branching.eq(0b1)\n\t\t\t\t\t\tm.d.comb+=self.result.eq(self.Ra + self.immediate)",
    "BLT" 	: "\t\t\t\twith m.If(self.inst_type2==self.BLT):\n\t\t\t\t\twith m.If(self.Ra<self.Rb):\n\t\t\t\t\t\tm.d.comb+=self.branching.eq(0b1)\n\t\t\t\t\t\tm.d.comb+=self.result.eq(self.immediate)",
    "BGE" 	: "\t\t\t\twith m.If(self.inst_type2==self.BGE):\n\t\t\t\t\twith m.If(self.Ra>=self.Rb):\n\t\t\t\t\t\tm.d.comb+=self.branching.eq(0b1)\n\t\t\t\t\t\tm.d.comb+=self.result.eq(self.immediate)",
    "BLTU" 	: "\t\t\t\twith m.If(self.inst_type2==self.BLTU):\n\t\t\t\t\twith m.If(self.Ra<self.Rb):\n\t\t\t\t\t\tm.d.comb+=self.branching.eq(0b1)\n\t\t\t\t\t\tm.d.comb+=self.result.eq(self.immediate)",
    "BGEU" 	: "\t\t\t\twith m.If(self.inst_type2==self.BGEU):\n\t\t\t\t\twith m.If(self.Ra>=self.Rb):\n\t\t\t\t\t\tm.d.comb+=self.branching.eq(0b1)\n\t\t\t\t\t\tm.d.comb+=self.result.eq(self.immediate)"
}

dicI1 = {
    "JALR"	:f"\t\t\t\twith m.If(self.inst_type2==self.JALR):\n\t\t\t\t\tm.d.comb += self.csb.eq(0b1)\n\t\t\t\t\tm.d.comb += self.web.eq(0b0)\n\t\t\t\t\tm.d.comb += self.wmask.eq(0b0000)\n\t\t\t\t\tm.d.comb += self.result.eq(self.pc+Const({d}))\n\t\t\t\t\tm.d.comb += self.jump.eq(Const(1))",
    "ADDI" 	:"\t\t\t\twith m.If(self.inst_type2==self.ADDI):\n\t\t\t\t\tm.d.comb += self.csb.eq(0b1)\n\t\t\t\t\tm.d.comb += self.web.eq(0b0)\n\t\t\t\t\tm.d.comb += self.wmask.eq(0b0000)\n\t\t\t\t\tm.d.comb += self.jump.eq(0b0)\n\t\t\t\t\tm.d.comb += self.result.eq(self.Ra+self.immediate)",
    "SLTI" 	:"\t\t\t\twith m.If(self.inst_type2==self.SLTI):\n\t\t\t\t\tm.d.comb += self.csb.eq(0b1)\n\t\t\t\t\tm.d.comb += self.web.eq(0b0)\n\t\t\t\t\tm.d.comb += self.wmask.eq(0b0000)\n\t\t\t\t\tm.d.comb += self.jump.eq(0b0)\n\t\t\t\t\twith m.If(self.Ra<self.immediate):\n\t\t\t\t\t\tm.d.comb+=self.result.eq(1)\n\t\t\t\t\twith m.Else():\n\t\t\t\t\t\tm.d.comb+=self.result.eq(0)",
    "SLTIU": "\t\t\t\twith m.If(self.inst_type2==self.SLTIU):\n\t\t\t\t\tm.d.comb += self.csb.eq(0b1)\n\t\t\t\t\tm.d.comb += self.web.eq(0b0)\n\t\t\t\t\tm.d.comb += self.wmask.eq(0b0000)\n\t\t\t\t\tm.d.comb += self.jump.eq(0b0)\n\t\t\t\t\twith m.If(self.Ra<self.immediate):\n\t\t\t\t\t\tm.d.comb+=self.result.eq(1)\n\t\t\t\t\twith m.Else():\n\t\t\t\t\t\tm.d.comb+=self.result.eq(0)",
    "XORI"	:"\t\t\t\twith m.If(self.inst_type2==self.XORI):\n\t\t\t\t\tm.d.comb += self.csb.eq(0b1)\n\t\t\t\t\tm.d.comb += self.web.eq(0b0)\n\t\t\t\t\tm.d.comb += self.wmask.eq(0b0000)\n\t\t\t\t\tm.d.comb += self.jump.eq(0b0)\n\t\t\t\t\tm.d.comb+=self.result.eq((self.Ra & (~self.immediate))|((~self.Ra) & self.immediate))",
    "ORI"	:"\t\t\t\twith m.If(self.inst_type2==self.ORI):\n\t\t\t\t\tm.d.comb += self.csb.eq(0b1)\n\t\t\t\t\tm.d.comb += self.web.eq(0b0)\n\t\t\t\t\tm.d.comb += self.wmask.eq(0b0000)\n\t\t\t\t\tm.d.comb += self.jump.eq(0b0)\n\t\t\t\t\tm.d.comb+=self.result.eq(self.Ra|self.immediate)",
    "ANDI"	:"\t\t\t\twith m.If(self.inst_type2==self.ANDI):\n\t\t\t\t\tm.d.comb += self.csb.eq(0b1)\n\t\t\t\t\tm.d.comb += self.web.eq(0b0)\n\t\t\t\t\tm.d.comb += self.wmask.eq(0b0000)\n\t\t\t\t\tm.d.comb += self.jump.eq(0b0)\n\t\t\t\t\tm.d.comb+=self.result.eq(self.Ra&self.immediate)",
    "SLLI" 	:"\t\t\t\twith m.If(self.inst_type1==self.SLLI):\n\t\t\t\t\tm.d.comb += self.csb.eq(0b1)\n\t\t\t\t\tm.d.comb += self.web.eq(0b0)\n\t\t\t\t\tm.d.comb += self.wmask.eq(0b0000)\n\t\t\t\t\tm.d.comb += self.jump.eq(0b0)\n\t\t\t\t\tm.d.comb+=self.result.eq(self.Ra << self.shamt)",
    "SRLI" 	:"\t\t\t\twith m.If(self.inst_type1==self.SRLI):\n\t\t\t\t\tm.d.comb += self.csb.eq(0b1)\n\t\t\t\t\tm.d.comb += self.web.eq(0b0)\n\t\t\t\t\tm.d.comb += self.wmask.eq(0b0000)\n\t\t\t\t\tm.d.comb += self.jump.eq(0b0)\n\t\t\t\t\tm.d.comb+=self.Ra_unsigned.eq(self.Ra)\n\t\t\t\t\tm.d.comb+=self.result.eq(self.Ra_unsigned >> self.shamt)",
    "SRAI" 	:"\t\t\t\twith m.If(self.inst_type1==self.SRAI):\n\t\t\t\t\tm.d.comb += self.csb.eq(0b1)\n\t\t\t\t\tm.d.comb += self.web.eq(0b0)\n\t\t\t\t\tm.d.comb += self.wmask.eq(0b0000)\n\t\t\t\t\tm.d.comb += self.jump.eq(0b0)\n\t\t\t\t\tm.d.comb+=self.result.eq(self.Ra >> self.shamt)",
    "LB"    :"\t\t\t\twith m.If(self.inst_type2==self.LB):\n\t\t\t\t\tm.d.comb+=self.result.eq(self.Ra + self.immediate)\n\t\t\t\t\tm.d.comb += self.csb.eq(0b0)\n\t\t\t\t\tm.d.comb += self.web.eq(0b1)\n\t\t\t\t\tm.d.comb += self.wmask.eq(0b0001)\n\t\t\t\t\tm.d.comb += self.jump.eq(0b0)",
    "LH":"\t\t\t\twith m.If(self.inst_type2==self.LH):\n\t\t\t\t\tm.d.comb+=self.result.eq(self.Ra + self.immediate)\n\t\t\t\t\tm.d.comb += self.csb.eq(0b0)\n\t\t\t\t\tm.d.comb += self.web.eq(0b1)\n\t\t\t\t\tm.d.comb += self.wmask.eq(0b0011)\n\t\t\t\t\tm.d.comb += self.jump.eq(0b0)",
    "LW":"\t\t\t\twith m.If(self.inst_type2==self.LW):\n\t\t\t\t\tm.d.comb+=self.result.eq(self.Ra + self.immediate)\n\t\t\t\t\tm.d.comb += self.csb.eq(0b0)\n\t\t\t\t\tm.d.comb += self.web.eq(0b1)\n\t\t\t\t\tm.d.comb += self.wmask.eq(0b1111)\n\t\t\t\t\tm.d.comb += self.jump.eq(0b0)",
    "LBU":"\t\t\t\twith m.If(self.inst_type2==self.LBU):\n\t\t\t\t\tm.d.comb+=self.result.eq(self.Ra + self.immediate)\n\t\t\t\t\tm.d.comb += self.csb.eq(0b0)\n\t\t\t\t\tm.d.comb += self.web.eq(0b1)\n\t\t\t\t\tm.d.comb += self.wmask.eq(0b0001)\n\t\t\t\t\tm.d.comb += self.jump.eq(0b0)",
    "LHU":"\t\t\t\twith m.If(self.inst_type2==self.LHU):\n\t\t\t\t\tm.d.comb+=self.result.eq(self.Ra + self.immediate)\n\t\t\t\t\tm.d.comb += self.csb.eq(0b0)\n\t\t\t\t\tm.d.comb += self.web.eq(0b1)\n\t\t\t\t\tm.d.comb += self.wmask.eq(0b0011)\n\t\t\t\t\tm.d.comb += self.jump.eq(0b0)",
}
if dic["R_type"]:
    s+='''
\t\t\twith m.If(self.inst_type==self.R_type):
\t\t\t\tm.d.comb += self.load_wb.eq(0b1)
\t\t\t\tm.d.comb += self.csb.eq(0b1)
\t\t\t\tm.d.comb += self.web.eq(0b1)
\t\t\t\tm.d.comb += self.wmask.eq(0b0000) 
\t\t\t\tm.d.comb += self.branching.eq(0b0)
\t\t\t\tm.d.comb += self.jump.eq(0b0)
'''
    for i in R:
        if dic[i]:
            s+=dicR[i]
            s+="\n"


if dic["M_type"]:
    s+='''
\t\t\twith m.If(self.inst_type==self.M_type):
\t\t\t\tm.d.comb += self.load_wb.eq(0b1)
\t\t\t\tm.d.comb += self.csb.eq(0b1)
\t\t\t\tm.d.comb += self.web.eq(0b0)
\t\t\t\tm.d.comb += self.wmask.eq(0b0000)
\t\t\t\tm.d.comb+=self.branching.eq(0b0)
'''
    for i in M:
        if dic[i]:
            s+=dicM[i]
            s+="\n"

if dic["JAL"]:
    s+=f'''
\t\t\twith m.If(self.inst_type==self.J_type):
\t\t\t\tm.d.comb += self.load_wb.eq(0b1)
\t\t\t\tm.d.comb += self.csb.eq(0b1)
\t\t\t\tm.d.comb += self.web.eq(0b0)
\t\t\t\tm.d.comb += self.wmask.eq(0b0000)
\t\t\t\tm.d.comb += self.jump.eq(0b0)
\t\t\t\twith m.If(self.inst_type3==self.JAL):
\t\t\t\t\tm.d.comb+=self.branching.eq(0b1)
\t\t\t\t\tm.d.comb+=self.result.eq(self.pc+Const({d}))
'''

if dic["U_type"]:
    s+='''
\t\t\twith m.If(self.inst_type==self.U_type):
\t\t\t\tm.d.comb += self.load_wb.eq(0b1)
\t\t\t\tm.d.comb += self.csb.eq(0b1)
\t\t\t\tm.d.comb += self.web.eq(0b0)
\t\t\t\tm.d.comb += self.branching.eq(0b0)
\t\t\t\tm.d.comb += self.wmask.eq(0b0000)
\t\t\t\tm.d.comb += self.jump.eq(0b0)
'''
    for i in U:
        if dic[i]:
            s+=dicU[i]
            s+="\n"


if dic["S_type"]:
    s+='''
\t\t\twith m.If(self.inst_type==self.S_type):
\t\t\t\tm.d.comb += self.load_wb.eq(0b0)
\t\t\t\tm.d.comb += self.csb.eq(0b0)
\t\t\t\tm.d.comb += self.web.eq(0b0)
\t\t\t\tm.d.comb += self.branching.eq(0b0)
\t\t\t\tm.d.comb += self.jump.eq(0b0)
'''
    
    for i in S:
        if dic[i]:
            s+=dicS[i]
            s+="\n"
if dic["B_type"]:
    s+='''
\t\t\twith m.If(self.inst_type==self.B_type):
\t\t\t\tm.d.comb += self.load_wb.eq(0b0)
\t\t\t\tm.d.comb += self.csb.eq(0b1)
\t\t\t\tm.d.comb += self.web.eq(0b0) 
\t\t\t\tm.d.comb += self.wmask.eq(0b0000)
\t\t\t\tm.d.comb += self.jump.eq(0b0)
'''
    for i in B:
        if dic[i]:
            s+=dicB[i]
            s+="\n"


    
if dic["I_type"]:
    s+='''\t\t\twith m.If(self.inst_type==self.I_type):
\t\t\t\tm.d.comb += self.load_wb.eq(0b1)
\t\t\t\tm.d.comb += self.branching.eq(0b0)    
'''
    for i in I1:
        if dic[i]:
            s+=dicI1[i]
            s+="\n"

s+='''
\t\t\treturn m
\t\tdef ports(self)->List[Signal]:
\t\t\treturn []
'''

f1=open('alu.py','w+')
f1.write(s)
