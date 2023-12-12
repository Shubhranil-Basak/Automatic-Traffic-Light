import json
f = open('All.json','r')
y=json.loads(f.read())

s1=f'''from typing import List
from nmigen import *
from nmigen.sim import *
from nmigen import Elaboratable,Module,Signal
from nmigen.build import Platform
from nmigen.cli import main_parser,main_runner

class ID(Elaboratable):
    
\tdef __init__(self):
\t\t#inputs
\t\tself.instruction = Signal({y['value_bit_width']}) 
\t\tself.s1_data_in = Signal(signed({y['value_bit_width']}))
\t\tself.s2_data_in = Signal(signed({y['value_bit_width']}))
\t\t#local variables
\t\tself.immediate = Signal({y['immediate']})
\t\t#outputs
\t\tself.des = Signal({y['address_size']})
\t\tself.s1 = Signal({y['address_size']})
\t\tself.s2 = Signal({y['address_size']})
\t\tself.s1data_out = Signal(signed({y['value_bit_width']}))
\t\tself.s2data_out = Signal(signed({y['value_bit_width']}))
\t\tself.signextended_immediate = Signal(signed({y['value_bit_width']}))
\t\tself.instruction_type = Signal(3)
\t\tself.it0 = Signal(17)
\t\tself.it1 = Signal(11)
\t\tself.it2 = Signal(11)
\t\tself.it3 = Signal(7)
\t\tself.ifload = Signal(1)
\t\tself.shamt = Signal({y['shamt']})
'''


dic=y['instructions']
d1={
    "LUI":"\t\tself.LUI 	=	0b0110111",
    "AUIPC":"\t\tself.AUIPC 	=	0b0010111",
    "JAL":"\t\tself.JAL 	=	0b1101111",
    "JALR":"\t\tself.JALR	=	0b0001100111",
    "BEQ":"\t\tself.BEQ	=	0b0001100011",
    "BNE":"\t\tself.BNE 	=	0b0011100011",
    "BLT":"\t\tself.BLT 	=	0b1001100011",
    "BGE":"\t\tself.BGE 	=	0b1011100011",
    "BLTU":"\t\tself.BLTU 	=	0b1101100011",
    "BGEU":"\t\tself.BGEU 	=	0b1111100011",
    "LB":"\t\tself.LB 	=	0b0000000011",
    "LH":"\t\tself.LH		=	0b0010000011",
    "LW":"\t\tself.LW		=	0b0100000011",
    "LBU":"\t\tself.LBU 	=	0b1000000011",
    "LHU":"\t\tself.LHU 	=	0b1010000011",
    "SB":"\t\tself.SB 	=	0b0000100011",
    "SH":"\t\tself.SH		=	0b0010100011",
    "SW":"\t\tself.SW		=	0b0100100011",
    "ADDI":"\t\tself.ADDI 	=	0b0000010011",
    "SLTI":"\t\tself.SLTI 	=	0b0100010011",
    "SLTIU":"\t\tself.SLTIU 	=	0b0110010011",
    "XORI":"\t\tself.XORI	=	0b1000010011",
    "ORI":"\t\tself.ORI	=	0b1100010011",
    "ANDI":"\t\tself.ANDI	=	0b1110010011",
    "SLLI":"\t\tself.SLLI 	=	0b00010010011",
    "SRLI":"\t\tself.SRLI 	=	0b01010010011",
    "SRAI":"\t\tself.SRAI 	=	0b11010010011",
    "ADD":"\t\tself.ADD 	=	0b00000110011",
    "SUB":"\t\tself.SUB 	=	0b10000110011",
    "SLL":"\t\tself.SLL 	=	0b00010110011",
    "SLT":"\t\tself.SLT 	=	0b00100110011",
    "SLTU":"\t\tself.SLTU 	=	0b00110110011",
    "XOR":"\t\tself.XOR 	=	0b01000110011",
    "SRL":"\t\tself.SRL 	=	0b01010110011",
    "SRA":"\t\tself.SRA 	=	0b11010110011",
    "OR":"\t\tself.OR 	=	0b01100110011",
    "AND":"\t\tself.AND 	=	0b01110110011",
    "MUL":"\t\tself.MUL    = 0b00000010000110011",
    "MULH":"\t\tself.MULH =   0b00000010010110011",
    "MULHSU":"\t\tself.MULHSU = 0b00000010100110011",
    "MULHU":"\t\tself.MULHU =  0b00000010110110011",
    "DIV":"\t\tself.DIV =  0b00000011000110011",
    "DIVU":"\t\tself.DIVU =   0b00000011010110011",
    "REM":"\t\tself.REM =    0b00000011100110011",
    "REMU":"\t\tself.REMU =   0b00000011110110011",
    "R_type":"\t\tself.R_type = 0b111",
    "I_type":"\t\tself.I_type = 0b001",
    "S_type":"\t\tself.S_type = 0b011",
    "B_type":"\t\tself.B_type = 0b100",
    "U_type":"\t\tself.U_type = 0b101",
    "J_type":"\t\tself.J_type = 0b110",
    "M_type":"\t\tself.M_type = 0b010",
}


for i in dic:
    if dic[i]==True:
        s1+=d1[i]
        s1+="\n"


s2=f'''
\tdef elaborate(self,platform:Platform)->Module:
\t\tm = Module()
\t\t
\t\tm.d.comb+=self.it3.eq(self.instruction[0:7])#self.instruction type
\t\tm.d.comb+=self.it2.eq(Cat(self.instruction[0:7],self.instruction[12:15]))#concatinate opcode and funct3
\t\tm.d.comb+=self.it1.eq(Cat(self.instruction[0:7],self.instruction[12:15],self.instruction[30]))# concatinate opcode, funct3, funct7
\t\tm.d.comb+=self.it0.eq(Cat(self.instruction[0:7],self.instruction[12:15],self.instruction[25:32]))
\t\t
\t\tm.d.comb+=self.s1.eq(self.instruction[15:20])
\t\tm.d.comb+=self.s2.eq(self.instruction[20:25])
'''
s1+=s2


R = ['ADD',"SUB","SLL","SLTU","SLT","XOR","SRL","SRA","OR","AND"]
if dic['R_type'] == True:
    s2 = '\t\twith m.If((Const(0)) '
    for i in R:
        if dic[i]==True:
            s2+=f'| (self.it1 == self.{i}) '
    s2+='):\n'
    s2+=f'''\t\t\tm.d.comb+=self.instruction_type.eq(self.R_type) #Inst_type.R_type
\t\t\tm.d.comb+=self.s1data_out.eq(self.s1_data_in) # passing input to output data as is
\t\t\tm.d.comb+=self.s2data_out.eq(self.s2_data_in)        
\t\t\tm.d.comb+=self.des.eq(self.instruction[7:12])
'''
    s1+=s2

M = ["MUL","MULH","MULHSU","MULHU","DIV","DIVU","REM","REMU"]
if dic['M_type'] == True:
    s2 = '\t\twith m.If((Const(0)) '
    for i in M:
        if dic[i]==True:
            s2+=f'| (self.it0 == self.{i}) '
    s2+='):\n'
    s2+=f'''\t\t\tm.d.comb+=self.instruction_type.eq(0b010)#Inst_type.M_type
\t\t\tm.d.comb+=self.s1data_out.eq(self.s1_data_in)
\t\t\tm.d.comb+=self.s2data_out.eq(self.s2_data_in)
\t\t\tm.d.comb+=self.des.eq(self.instruction[7:12])
'''
    s1+=s2



U = ["LUI","AUIPC"]
if dic['U_type'] == True:
    s2 = '\t\twith m.If((Const(0)) '
    for i in U:
        if dic[i]==True:
            s2+=f'| (self.it3 == self.{i}) '
    s2+='):\n'
    s2 +='''\t\t\tm.d.comb+=self.instruction_type.eq(0b101)#U type
\t\t\tm.d.comb+=self.signextended_immediate.eq(self.instruction[12:] << Const(12))#msb bits are immediate
\t\t\tm.d.comb+=self.des.eq(self.instruction[7:12])
'''
    s1+=s2


J = ["JAL"]
if dic['J_type']:
    s2='\t\twith m.If(self.it3==self.JAL):\n'
    s2+=f'''\t\t\tm.d.comb+=self.instruction_type.eq(0b110) #J type
\t\t\tm.d.comb+=self.des.eq(self.instruction[7:12])
\t\t\tm.d.comb+=self.signextended_immediate.eq(Cat(Const(0b0),self.instruction[21:31],self.instruction[20],self.instruction[12:20],self.instruction[31],Const(0b00000000000)))
'''
    s1+=s2


S=['SB','SH','SW']
B=['BEQ','BNE','BLT','BGE','BLTU',"BGEU"]
I1=['ADDI','SLTI','SLTIU','XORI','ORI','ANDI','JALR']
I2=['LB','LH','LW','LBU',"LHU"]
I3=['SLLI','SRLI','SRAI']
i1=False
i2=False
i3=False
i4=False
if dic['S_type']:
    s2 = '\t\twith m.If((Const(0)) '
    for i in S:
        if dic[i]==True:
            s2+=f'| (self.it2 == self.{i}) '
    s2+='):\n'
    s2+=f'''\t\t\tm.d.comb+=self.instruction_type.eq(0b011)#S type
\t\t\tm.d.comb+=self.s1data_out.eq(self.s1_data_in)
\t\t\tm.d.comb+=self.s2data_out.eq(self.s2_data_in)

\t\t\twith m.If(self.instruction[31]==Const(0)):
\t\t\t\tm.d.comb+=self.signextended_immediate.eq(Cat(self.instruction[7:12],self.instruction[25:],Const(0x00000)))
\t\t\twith m.Else():
\t\t\t\tm.d.comb+=self.signextended_immediate.eq(Cat(self.instruction[7:12],self.instruction[25:],Const(0xFFFFF)))
'''
    s1+=s2
if dic['B_type']==True:
    
    s2 = '\t\twith m.If((Const(0)) '
    for i in B:
        if dic[i]==True:
            s2+=f'| (self.it2 == self.{i}) '
    s2+='):\n'
    
    s2+=f'''\t\t\tm.d.comb+=self.instruction_type.eq(0b100)#B type
\t\t\twith m.If(self.instruction[31]==Const(0)):
\t\t\t\tm.d.comb+=self.signextended_immediate.eq(Cat(Const(0b0),self.instruction[8:12],self.instruction[25:31],self.instruction[7],self.instruction[31],Const(0x0000),Const(0b000)))
\t\t\twith m.Else():
\t\t\t\tm.d.comb+=self.signextended_immediate.eq(Cat(Const(0b0),self.instruction[8:12],self.instruction[25:31],self.instruction[7],self.instruction[31],Const(0xFFFF),Const(0b111)))  
\t\t\tm.d.comb+=self.s1data_out.eq(self.s1_data_in)
\t\t\tm.d.comb+=self.s2data_out.eq(self.s2_data_in)
'''
    s1+=s2
if dic['I_type']:
    s2 = '\t\twith m.If((Const(0)) '
    for i in I1:
        if dic[i]==True:
            s2+=f'| (self.it2 == self.{i}) '
    s2+='):\n'
    s2+=f'''\t\t\tm.d.comb+=self.instruction_type.eq(self.I_type) #I type
\t\t\tm.d.comb+=self.s1data_out.eq(self.s1_data_in)
\t\t\tm.d.comb+=self.des.eq(self.instruction[7:12])
\t\t\tm.d.comb+=self.shamt.eq(self.instruction[20:25])
\t\t\twith m.If(self.instruction[31]==Const(0)):
\t\t\t\tm.d.comb+=self.signextended_immediate.eq(Cat(self.instruction[20:],Const(0x00000)))
\t\t\twith m.Else():
\t\t\t\tm.d.comb+=self.signextended_immediate.eq(Cat(self.instruction[20:],Const(0xFFFFF)))  
'''
    s1+=s2

    s2 = '\t\twith m.If((Const(0)) '
    for i in I3:
        if dic[i]==True:
            s2+=f'| (self.it1 == self.{i}) '
    s2+='):\n'
    s2+=f'''\t\t\tm.d.comb+=self.instruction_type.eq(self.I_type) #I type
\t\t\tm.d.comb+=self.s1data_out.eq(self.s1_data_in)
\t\t\tm.d.comb+=self.des.eq(self.instruction[7:12])
\t\t\tm.d.comb+=self.shamt.eq(self.instruction[20:25])
\t\t\twith m.If(self.instruction[31]==Const(0)):
\t\t\t\tm.d.comb+=self.signextended_immediate.eq(Cat(self.instruction[20:],Const(0x00000)))
\t\t\twith m.Else():
\t\t\t\tm.d.comb+=self.signextended_immediate.eq(Cat(self.instruction[20:],Const(0xFFFFF)))  
'''
    s1+=s2

    s2 = '\t\twith m.If((Const(0)) '
    for i in I2:
        if dic[i]==True:
            s2+=f'| (self.it2 == self.{i}) '
    s2+='):\n'
    s2+=f'''\t\t\tm.d.comb+=self.instruction_type.eq(self.I_type)#I type
\t\t\tm.d.comb+=self.s1data_out.eq(self.s1_data_in)
\t\t\tm.d.comb+=self.des.eq(self.instruction[7:12])
\t\t\twith m.If(self.instruction[31]==Const(0)):
\t\t\t\tm.d.comb+=self.signextended_immediate.eq(Cat(self.instruction[20:],Const(0x00000)))
\t\t\twith m.If(self.instruction[31]==Const(1)):
\t\t\t\tm.d.comb+=self.signextended_immediate.eq(Cat(self.instruction[20:],Const(0xFFFFF)))
\t\t\tm.d.comb += self.ifload.eq(Const(1))
'''
    s1+=s2

sfinal='''
\t\treturn m
\tdef ports(self)->List[Signal]:
\t\treturn []
'''
s1+=sfinal
f1=open('id.py','w+')
f1.write(s1)