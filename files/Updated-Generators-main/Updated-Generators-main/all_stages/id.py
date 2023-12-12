from typing import List
from nmigen import *
from nmigen.sim import *
from nmigen import Elaboratable,Module,Signal
from nmigen.build import Platform
from nmigen.cli import main_parser,main_runner

class ID(Elaboratable):
    
	def __init__(self):
		#inputs
		self.instruction = Signal(32) 
		self.s1_data_in = Signal(signed(32))
		self.s2_data_in = Signal(signed(32))
		#local variables
		self.immediate = Signal(12)
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
		self.LUI 	=	0b0110111
		self.AUIPC 	=	0b0010111
		self.JAL 	=	0b1101111
		self.JALR	=	0b0001100111
		self.BEQ	=	0b0001100011
		self.BNE 	=	0b0011100011
		self.BLT 	=	0b1001100011
		self.BGE 	=	0b1011100011
		self.BLTU 	=	0b1101100011
		self.BGEU 	=	0b1111100011
		self.LB 	=	0b0000000011
		self.LH		=	0b0010000011
		self.LW		=	0b0100000011
		self.LBU 	=	0b1000000011
		self.LHU 	=	0b1010000011
		self.SB 	=	0b0000100011
		self.SH		=	0b0010100011
		self.SW		=	0b0100100011
		self.ADDI 	=	0b0000010011
		self.SLTI 	=	0b0100010011
		self.SLTIU 	=	0b0110010011
		self.XORI	=	0b1000010011
		self.ORI	=	0b1100010011
		self.ANDI	=	0b1110010011
		self.SLLI 	=	0b00010010011
		self.SRLI 	=	0b01010010011
		self.SRAI 	=	0b11010010011
		self.ADD 	=	0b00000110011
		self.SUB 	=	0b10000110011
		self.SLL 	=	0b00010110011
		self.SLT 	=	0b00100110011
		self.SLTU 	=	0b00110110011
		self.XOR 	=	0b01000110011
		self.SRL 	=	0b01010110011
		self.SRA 	=	0b11010110011
		self.OR 	=	0b01100110011
		self.AND 	=	0b01110110011
		self.R_type = 0b111
		self.I_type = 0b001
		self.S_type = 0b011
		self.B_type = 0b100
		self.U_type = 0b101
		self.J_type = 0b110

	def elaborate(self,platform:Platform)->Module:
		m = Module()
		
		m.d.comb+=self.it3.eq(self.instruction[0:7])#self.instruction type
		m.d.comb+=self.it2.eq(Cat(self.instruction[0:7],self.instruction[12:15]))#concatinate opcode and funct3
		m.d.comb+=self.it1.eq(Cat(self.instruction[0:7],self.instruction[12:15],self.instruction[30]))# concatinate opcode, funct3, funct7
		m.d.comb+=self.it0.eq(Cat(self.instruction[0:7],self.instruction[12:15],self.instruction[25:32]))
		
		m.d.comb+=self.s1.eq(self.instruction[15:20])
		m.d.comb+=self.s2.eq(self.instruction[20:25])
		with m.If((Const(0)) | (self.it1 == self.ADD) | (self.it1 == self.SUB) | (self.it1 == self.SLL) | (self.it1 == self.SLTU) | (self.it1 == self.SLT) | (self.it1 == self.XOR) | (self.it1 == self.SRL) | (self.it1 == self.SRA) | (self.it1 == self.OR) | (self.it1 == self.AND) ):
			m.d.comb+=self.instruction_type.eq(self.R_type) #Inst_type.R_type
			m.d.comb+=self.s1data_out.eq(self.s1_data_in) # passing input to output data as is
			m.d.comb+=self.s2data_out.eq(self.s2_data_in)        
			m.d.comb+=self.des.eq(self.instruction[7:12])
		with m.If((Const(0)) | (self.it3 == self.LUI) | (self.it3 == self.AUIPC) ):
			m.d.comb+=self.instruction_type.eq(0b101)#U type
			m.d.comb+=self.signextended_immediate.eq(self.instruction[12:] << Const(12))#msb bits are immediate
			m.d.comb+=self.des.eq(self.instruction[7:12])
		with m.If(self.it3==self.JAL):
			m.d.comb+=self.instruction_type.eq(0b110) #J type
			m.d.comb+=self.des.eq(self.instruction[7:12])
			m.d.comb+=self.signextended_immediate.eq(Cat(Const(0b0),self.instruction[21:31],self.instruction[20],self.instruction[12:20],self.instruction[31],Const(0b00000000000)))
		with m.If((Const(0)) | (self.it2 == self.SB) | (self.it2 == self.SH) | (self.it2 == self.SW) ):
			m.d.comb+=self.instruction_type.eq(0b011)#S type
			m.d.comb+=self.s1data_out.eq(self.s1_data_in)
			m.d.comb+=self.s2data_out.eq(self.s2_data_in)

			with m.If(self.instruction[31]==Const(0)):
				m.d.comb+=self.signextended_immediate.eq(Cat(self.instruction[7:12],self.instruction[25:],Const(0x00000)))
			with m.Else():
				m.d.comb+=self.signextended_immediate.eq(Cat(self.instruction[7:12],self.instruction[25:],Const(0xFFFFF)))
		with m.If((Const(0)) | (self.it2 == self.BEQ) | (self.it2 == self.BNE) | (self.it2 == self.BLT) | (self.it2 == self.BGE) | (self.it2 == self.BLTU) | (self.it2 == self.BGEU) ):
			m.d.comb+=self.instruction_type.eq(0b100)#B type
			with m.If(self.instruction[31]==Const(0)):
				m.d.comb+=self.signextended_immediate.eq(Cat(Const(0b0),self.instruction[8:12],self.instruction[25:31],self.instruction[7],self.instruction[31],Const(0x0000),Const(0b000)))
			with m.Else():
				m.d.comb+=self.signextended_immediate.eq(Cat(Const(0b0),self.instruction[8:12],self.instruction[25:31],self.instruction[7],self.instruction[31],Const(0xFFFF),Const(0b111)))  
			m.d.comb+=self.s1data_out.eq(self.s1_data_in)
			m.d.comb+=self.s2data_out.eq(self.s2_data_in)
		with m.If((Const(0)) | (self.it2 == self.ADDI) | (self.it2 == self.SLTI) | (self.it2 == self.SLTIU) | (self.it2 == self.XORI) | (self.it2 == self.ORI) | (self.it2 == self.ANDI) | (self.it2 == self.JALR) ):
			m.d.comb+=self.instruction_type.eq(self.I_type) #I type
			m.d.comb+=self.s1data_out.eq(self.s1_data_in)
			m.d.comb+=self.des.eq(self.instruction[7:12])
			m.d.comb+=self.shamt.eq(self.instruction[20:25])
			with m.If(self.instruction[31]==Const(0)):
				m.d.comb+=self.signextended_immediate.eq(Cat(self.instruction[20:],Const(0x00000)))
			with m.Else():
				m.d.comb+=self.signextended_immediate.eq(Cat(self.instruction[20:],Const(0xFFFFF)))  
		with m.If((Const(0)) | (self.it1 == self.SLLI) | (self.it1 == self.SRLI) | (self.it1 == self.SRAI) ):
			m.d.comb+=self.instruction_type.eq(self.I_type) #I type
			m.d.comb+=self.s1data_out.eq(self.s1_data_in)
			m.d.comb+=self.des.eq(self.instruction[7:12])
			m.d.comb+=self.shamt.eq(self.instruction[20:25])
			with m.If(self.instruction[31]==Const(0)):
				m.d.comb+=self.signextended_immediate.eq(Cat(self.instruction[20:],Const(0x00000)))
			with m.Else():
				m.d.comb+=self.signextended_immediate.eq(Cat(self.instruction[20:],Const(0xFFFFF)))  
		with m.If((Const(0)) | (self.it2 == self.LB) | (self.it2 == self.LH) | (self.it2 == self.LW) | (self.it2 == self.LBU) | (self.it2 == self.LHU) ):
			m.d.comb+=self.instruction_type.eq(self.I_type)#I type
			m.d.comb+=self.s1data_out.eq(self.s1_data_in)
			m.d.comb+=self.des.eq(self.instruction[7:12])
			with m.If(self.instruction[31]==Const(0)):
				m.d.comb+=self.signextended_immediate.eq(Cat(self.instruction[20:],Const(0x00000)))
			with m.If(self.instruction[31]==Const(1)):
				m.d.comb+=self.signextended_immediate.eq(Cat(self.instruction[20:],Const(0xFFFFF)))
			m.d.comb += self.ifload.eq(Const(1))

		return m
	def ports(self)->List[Signal]:
		return []
