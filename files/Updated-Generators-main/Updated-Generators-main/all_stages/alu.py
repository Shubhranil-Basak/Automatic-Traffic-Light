
from typing import List
from nmigen.back import rtlil, verilog
from nmigen import *
from nmigen.sim import *
from nmigen import Elaboratable,Module,Signal
from nmigen.build import Platform
from nmigen.cli import main_parser,main_runner

class ALU(Elaboratable):
		def __init__(self):
			self.Ra_unsigned = Signal(32)
			self.Rb_unsigned = Signal(32)
			self.Ra = Signal(signed(32))
			self.Rb= Signal(signed(32))
			self.result = Signal(32)
			self.result64 = Signal(signed(64))
			self.inst_type = Signal(3)
			self.inst_type0 = Signal(17)
			self.inst_type1 = Signal(11)
			self.inst_type2 = Signal(11)
			self.inst_type3 = Signal(7)
			self.reg_addr_in = Signal(5)
			self.immediate = Signal(signed(32))
			self.branching = Signal(1)
			self.data_to_mem = Signal(32)
			self.inst_type_out = Signal(3)
			self.inst_type1_out = Signal(11)
			self.inst_type2_out = Signal(11)
			self.inst_type3_out = Signal(7)
			self.reg_addr_out = Signal(5)
			self.jump = Signal(1)
			self.pc = Signal(8)
			self.shamt = Signal(5)
			self.shamt1 = Signal(5)
			self.csb = Signal(1)
			self.web = Signal(1)
			# self.load_mem = Signal(2)
			# self.write_mem = Signal(2)
			self.load_wb = Signal(1)
			self.wmask = Signal(4,reset = 0x0)
			self.s1 = Signal(5)
			self.s2 = Signal(5)
			self.LUI     =   0b0110111
			self.AUIPC   =   0b0010111
			self.JAL     =   0b1101111
			self.JALR	=	0b0001100111
			self.BEQ     =   0b0001100011
			self.BNE     =   0b0011100011
			self.BLT     =   0b1001100011
			self.BGE     =   0b1011100011
			self.BLTU    =   0b1101100011
			self.BGEU    =   0b1111100011
			self.LB 	=	0b0000000011
			self.LH		=	0b0010000011
			self.LW      =   0b0100000011
			self.LBU 	=	0b1000000011
			self.LHU 	=	0b1010000011
			self.SB 	=	0b0000100011
			self.SH		=	0b0010100011
			self.SW		=	0b0100100011
			self.ADDI    =   0b0000010011
			self.SLTI    =   0b0100010011
			self.SLTIU   =   0b0110010011
			self.XORI    =   0b1000010011
			self.ORI     =   0b1100010011
			self.ANDI    =   0b1110010011
			self.SLLI   =   0b00010010011
			self.SRLI   =   0b01010010011
			self.SRAI   =   0b11010010011
			self.ADD = 0b00000110011
			self.SUB = 0b10000110011
			self.SLL = 0b00010110011
			self.SLT = 0b00100110011
			self.SLTU = 0b00110110011
			self.XOR = 0b01000110011
			self.SRL = 0b01010110011
			self.SRA = 0b11010110011
			self.OR = 0b01100110011
			self.AND = 0b01110110011
			self.R_type = 0b111
			self.I_type = 0b001
			self.S_type = 0b011
			self.B_type = 0b100
			self.U_type = 0b101
			self.J_type = 0b110

		def elaborate(self,platform:Platform)->Module:
			m = Module()
			m.d.comb += self.inst_type_out.eq(self.inst_type)    
			m.d.comb += self.inst_type1_out.eq(self.inst_type1)
			m.d.comb += self.inst_type2_out.eq(self.inst_type2)
			m.d.comb += self.inst_type3_out.eq(self.inst_type3)
			m.d.comb += self.reg_addr_out.eq(self.reg_addr_in)
			m.d.comb += self.shamt1.eq(self.Rb[0:5])

			with m.If(self.inst_type==self.R_type):
				m.d.comb += self.load_wb.eq(0b1)
				m.d.comb += self.csb.eq(0b1)
				m.d.comb += self.web.eq(0b1)
				m.d.comb += self.wmask.eq(0b0000) 
				m.d.comb += self.branching.eq(0b0)
				m.d.comb += self.jump.eq(0b0)
				with m.If(self.inst_type1==self.ADD):
						m.d.comb += self.result.eq(self.Ra+self.Rb)
				with m.If(self.inst_type1==self.SUB):
						m.d.comb += self.result.eq(self.Ra-self.Rb)
				with m.If(self.inst_type1==self.SLL):
					m.d.comb += self.result.eq(self.Ra << self.shamt1)
				with m.If(self.inst_type1==self.SLTU):
					with m.If(self.Ra<self.Rb):
						m.d.comb+=self.result.eq(1)
					with m.Else():m.d.comb+=self.result.eq(0)
				with m.If(self.inst_type1==self.SLT):
					with m.If(self.Ra<self.Rb):
							m.d.comb+=self.result.eq(1)
					with m.Else():m.d.comb+=self.result.eq(0)
				with m.If(self.inst_type1==self.XOR):
					m.d.comb+=self.result.eq((self.Ra & (~self.Rb)))
				with m.Elif(self.inst_type1==self.SRL):
					m.d.comb += self.Ra_unsigned.eq(self.Ra)
					m.d.comb += self.result.eq(self.Ra_unsigned >> self.shamt1)
				with m.Elif(self.inst_type1==self.SRA):
					m.d.comb += self.result.eq(self.Ra >> self.shamt1)
				with m.If(self.inst_type1==self.OR):
					m.d.comb+=self.result.eq(self.Rb | self.Ra)
				with m.If(self.inst_type1==self.AND):
					m.d.comb+=self.result.eq(self.Rb & self.Ra)

			with m.If(self.inst_type==self.J_type):
				m.d.comb += self.load_wb.eq(0b1)
				m.d.comb += self.csb.eq(0b1)
				m.d.comb += self.web.eq(0b0)
				m.d.comb += self.wmask.eq(0b0000)
				m.d.comb += self.jump.eq(0b0)
				with m.If(self.inst_type3==self.JAL):
					m.d.comb+=self.branching.eq(0b1)
					m.d.comb+=self.result.eq(self.pc+Const(-2))

			with m.If(self.inst_type==self.U_type):
				m.d.comb += self.load_wb.eq(0b1)
				m.d.comb += self.csb.eq(0b1)
				m.d.comb += self.web.eq(0b0)
				m.d.comb += self.branching.eq(0b0)
				m.d.comb += self.wmask.eq(0b0000)
				m.d.comb += self.jump.eq(0b0)
				with m.If(self.inst_type3==self.LUI):
					m.d.comb+=self.result.eq(self.immediate)
				with m.If(self.inst_type3==self.AUIPC):
					m.d.comb+=self.result.eq(self.immediate+self.pc+-3) 

			with m.If(self.inst_type==self.S_type):
				m.d.comb += self.load_wb.eq(0b0)
				m.d.comb += self.csb.eq(0b0)
				m.d.comb += self.web.eq(0b0)
				m.d.comb += self.branching.eq(0b0)
				m.d.comb += self.jump.eq(0b0)
				with m.If(self.inst_type2==self.SB):
					m.d.comb += self.data_to_mem.eq(self.Rb)
					m.d.comb+=self.result.eq(self.Ra + self.immediate)
					m.d.comb += self.wmask.eq(0b0001)
				with m.If(self.inst_type2==self.SH):
					m.d.comb += self.data_to_mem.eq(self.Rb)
					m.d.comb+=self.result.eq(self.Ra + self.immediate)
					m.d.comb += self.wmask.eq(0b0011)
				with m.If(self.inst_type2==self.SW):
					m.d.comb += self.data_to_mem.eq(self.Rb)
					m.d.comb+=self.result.eq(self.Ra + self.immediate)
					m.d.comb += self.wmask.eq(0b1111)

			with m.If(self.inst_type==self.B_type):
				m.d.comb += self.load_wb.eq(0b0)
				m.d.comb += self.csb.eq(0b1)
				m.d.comb += self.web.eq(0b0) 
				m.d.comb += self.wmask.eq(0b0000)
				m.d.comb += self.jump.eq(0b0)
				with m.If(self.inst_type2==self.BEQ):
					with m.If(self.Ra==self.Rb):
						m.d.comb+=self.branching.eq(0b1)
						m.d.comb+=self.result.eq(self.immediate)
				with m.If(self.inst_type2==self.BNE):
					with m.If(self.Ra!=self.Rb):
						m.d.comb+=self.branching.eq(0b1)
						m.d.comb+=self.result.eq(self.Ra + self.immediate)
				with m.If(self.inst_type2==self.BLT):
					with m.If(self.Ra<self.Rb):
						m.d.comb+=self.branching.eq(0b1)
						m.d.comb+=self.result.eq(self.immediate)
				with m.If(self.inst_type2==self.BGE):
					with m.If(self.Ra>=self.Rb):
						m.d.comb+=self.branching.eq(0b1)
						m.d.comb+=self.result.eq(self.immediate)
				with m.If(self.inst_type2==self.BLTU):
					with m.If(self.Ra<self.Rb):
						m.d.comb+=self.branching.eq(0b1)
						m.d.comb+=self.result.eq(self.immediate)
				with m.If(self.inst_type2==self.BGEU):
					with m.If(self.Ra>=self.Rb):
						m.d.comb+=self.branching.eq(0b1)
						m.d.comb+=self.result.eq(self.immediate)
			with m.If(self.inst_type==self.I_type):
				m.d.comb += self.load_wb.eq(0b1)
				m.d.comb += self.branching.eq(0b0)    
				with m.If(self.inst_type2==self.ADDI):
					m.d.comb += self.csb.eq(0b1)
					m.d.comb += self.web.eq(0b0)
					m.d.comb += self.wmask.eq(0b0000)
					m.d.comb += self.jump.eq(0b0)
					m.d.comb += self.result.eq(self.Ra+self.immediate)
				with m.If(self.inst_type2==self.SLTI):
					m.d.comb += self.csb.eq(0b1)
					m.d.comb += self.web.eq(0b0)
					m.d.comb += self.wmask.eq(0b0000)
					m.d.comb += self.jump.eq(0b0)
					with m.If(self.Ra<self.immediate):
						m.d.comb+=self.result.eq(1)
					with m.Else():
						m.d.comb+=self.result.eq(0)
				with m.If(self.inst_type2==self.SLTIU):
					m.d.comb += self.csb.eq(0b1)
					m.d.comb += self.web.eq(0b0)
					m.d.comb += self.wmask.eq(0b0000)
					m.d.comb += self.jump.eq(0b0)
					with m.If(self.Ra<self.immediate):
						m.d.comb+=self.result.eq(1)
					with m.Else():
						m.d.comb+=self.result.eq(0)
				with m.If(self.inst_type2==self.XORI):
					m.d.comb += self.csb.eq(0b1)
					m.d.comb += self.web.eq(0b0)
					m.d.comb += self.wmask.eq(0b0000)
					m.d.comb += self.jump.eq(0b0)
					m.d.comb+=self.result.eq((self.Ra & (~self.immediate))|((~self.Ra) & self.immediate))
				with m.If(self.inst_type2==self.ORI):
					m.d.comb += self.csb.eq(0b1)
					m.d.comb += self.web.eq(0b0)
					m.d.comb += self.wmask.eq(0b0000)
					m.d.comb += self.jump.eq(0b0)
					m.d.comb+=self.result.eq(self.Ra|self.immediate)
				with m.If(self.inst_type2==self.ANDI):
					m.d.comb += self.csb.eq(0b1)
					m.d.comb += self.web.eq(0b0)
					m.d.comb += self.wmask.eq(0b0000)
					m.d.comb += self.jump.eq(0b0)
					m.d.comb+=self.result.eq(self.Ra&self.immediate)
				with m.If(self.inst_type2==self.JALR):
					m.d.comb += self.csb.eq(0b1)
					m.d.comb += self.web.eq(0b0)
					m.d.comb += self.wmask.eq(0b0000)
					m.d.comb += self.result.eq(self.pc+Const(-2))
					m.d.comb += self.jump.eq(Const(1))
				with m.If(self.inst_type1==self.SLLI):
					m.d.comb += self.csb.eq(0b1)
					m.d.comb += self.web.eq(0b0)
					m.d.comb += self.wmask.eq(0b0000)
					m.d.comb += self.jump.eq(0b0)
					m.d.comb+=self.result.eq(self.Ra << self.shamt)
				with m.If(self.inst_type1==self.SRLI):
					m.d.comb += self.csb.eq(0b1)
					m.d.comb += self.web.eq(0b0)
					m.d.comb += self.wmask.eq(0b0000)
					m.d.comb += self.jump.eq(0b0)
					m.d.comb+=self.Ra_unsigned.eq(self.Ra)
					m.d.comb+=self.result.eq(self.Ra_unsigned >> self.shamt)
				with m.If(self.inst_type1==self.SRAI):
					m.d.comb += self.csb.eq(0b1)
					m.d.comb += self.web.eq(0b0)
					m.d.comb += self.wmask.eq(0b0000)
					m.d.comb += self.jump.eq(0b0)
					m.d.comb+=self.result.eq(self.Ra >> self.shamt)
				with m.If(self.inst_type2==self.LB):
					m.d.comb+=self.result.eq(self.Ra + self.immediate)
					m.d.comb += self.csb.eq(0b0)
					m.d.comb += self.web.eq(0b1)
					m.d.comb += self.wmask.eq(0b0001)
					m.d.comb += self.jump.eq(0b0)
				with m.If(self.inst_type2==self.LH):
					m.d.comb+=self.result.eq(self.Ra + self.immediate)
					m.d.comb += self.csb.eq(0b0)
					m.d.comb += self.web.eq(0b1)
					m.d.comb += self.wmask.eq(0b0011)
					m.d.comb += self.jump.eq(0b0)
				with m.If(self.inst_type2==self.LW):
					m.d.comb+=self.result.eq(self.Ra + self.immediate)
					m.d.comb += self.csb.eq(0b0)
					m.d.comb += self.web.eq(0b1)
					m.d.comb += self.wmask.eq(0b1111)
					m.d.comb += self.jump.eq(0b0)
				with m.If(self.inst_type2==self.LBU):
					m.d.comb+=self.result.eq(self.Ra + self.immediate)
					m.d.comb += self.csb.eq(0b0)
					m.d.comb += self.web.eq(0b1)
					m.d.comb += self.wmask.eq(0b0001)
					m.d.comb += self.jump.eq(0b0)
				with m.If(self.inst_type2==self.LHU):
					m.d.comb+=self.result.eq(self.Ra + self.immediate)
					m.d.comb += self.csb.eq(0b0)
					m.d.comb += self.web.eq(0b1)
					m.d.comb += self.wmask.eq(0b0011)
					m.d.comb += self.jump.eq(0b0)

			return m
		def ports(self)->List[Signal]:
			return []
