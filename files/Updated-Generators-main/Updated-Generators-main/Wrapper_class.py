

from typing import List
import sys
from nmigen import *
from nmigen.sim import *
from nmigen import Elaboratable, Module, Signal, Const
from nmigen.build import Platform
from nmigen.cli import main_parser, main_runner
from nmigen.back import rtlil, verilog
from all_stages.id import ID
from all_stages.alu import ALU
from all_stages.reg_file import Register_file
from all_stages.ALU_M1_pipeline import ALU_M1_Pipeline
from all_stages.IF_ID_pipeline import IF_ID_Pipeline
from all_stages.M1_M2_pipeline import M1_M2_Pipeline
from all_stages.M2_WB_pipeline import M2_WB_Pipeline
from all_stages.forward_alu import Forwarding_ALU
from all_stages.forward_mem import Forwarding_Mem
from all_stages.Stall_unit import Stall_Unit
from all_stages.id_mux import ID_mux
from all_stages.pc_controller import PC_controller
import sys

#counter_branch keeps track of number of instructions

class Wrapper(Elaboratable):
    def __init__(self):
        self.pc = Signal(8)
        self.read_flag = Signal(1, reset=0x0)
        self.inst_mem_addr = Signal(8,reset=0x0)
        self.inst_mem_rdata = Signal(32, reset =0x0)
        self.wmask = Signal(4, reset=0x0)
        self.csb_alu = Signal(1, reset =0x0)
        self.csb_mem = Signal(1, reset =0x0)
        self.web = Signal(1, reset =0x0)
        self.data_mem_wdata = Signal(32, reset =0x0)
        self.data_mem_addr = Signal(8, reset =0x0)
        self.data_mem_rdata = Signal(32, reset = 0x0)
        self.alu_result = Signal(32, reset = 0x0)
        self.gpio_pins = Signal(32, reset = 0x0)
        self.output_pins = Signal(32, reset = 0x0)

        self.ID = ID()
        self.ALU = ALU()
        self.reg_file = Register_file()        
        self.id_mux = ID_mux()
        self.forwarding_alu = Forwarding_ALU()
        self.forwarding_mem = Forwarding_Mem()
        self.pc_controller = PC_controller()
        self.stall_unit = Stall_Unit()

        self.M1_M2_pipeline = M1_M2_Pipeline()
        self.M2_WB_pipeline = M2_WB_Pipeline()
        self.IF_ID_pipeline = IF_ID_Pipeline()
        self.ALU_M1_pipeline = ALU_M1_Pipeline()     


    def elaborate(self,platform:Platform) -> Module:
        m = Module()
        m.submodules.ID = self.ID
        m.submodules.ALU = self.ALU
        m.submodules.reg_file = self.reg_file
        m.submodules.pc_controller = self.pc_controller
        m.submodules.id_mux = self.id_mux
        m.submodules.forwarding_alu = self.forwarding_alu
        m.submodules.forwarding_mem = self.forwarding_mem
        m.submodules.stall_unit = self.stall_unit
        m.submodules.IF_ID_pipeline = self.IF_ID_pipeline
        m.submodules.M1_M2_pipeline = self.M1_M2_pipeline
        m.submodules.ALU_M1_pipeline = self.ALU_M1_pipeline
        m.submodules.M2_WB_pipeline = self.M2_WB_pipeline

        with m.If(self.read_flag == 0): 
            m.d.comb += self.pc.eq(Const(0))
        
        with m.Else(): 
            with m.If(self.pc < 6):

                with m.If(self.pc < 4):
                    m.d.comb += self.reg_file.csb_alu.eq(Const(0))
                    m.d.comb += self.reg_file.write_alu.eq(Const(0))  #pos->comb
                with m.Else(): 
                    m.d.comb += self.reg_file.csb_alu.eq(self.ALU_M1_pipeline.memory_csb)
                    m.d.comb += self.reg_file.write_alu.eq(self.ALU_M1_pipeline.memory_load_wb_in)  #pos->comb

                with m.If(self.pc < 3):
                    m.d.comb += self.IF_ID_pipeline.branch.eq(Const(0))
                    m.d.comb += self.IF_ID_pipeline.jump.eq(Const(0))
                    m.d.comb += self.IF_ID_pipeline.stall.eq(Const(0))
                    m.d.comb += self.pc_controller.stall.eq(Const(0))
                    m.d.comb += self.pc_controller.branch.eq(Const(0))
                    m.d.comb += self.pc_controller.jump.eq(Const(0))
                    m.d.comb += self.id_mux.stall.eq(Const(0))
                with m.Else(): 
                    m.d.comb += self.IF_ID_pipeline.branch.eq(self.ALU.branching)
                    m.d.comb += self.IF_ID_pipeline.jump.eq(self.ALU.jump)
                    m.d.comb += self.IF_ID_pipeline.stall.eq(self.stall_unit.stall)
                    m.d.comb += self.pc_controller.stall.eq(self.stall_unit.stall)
                    m.d.comb += self.pc_controller.branch.eq(self.ALU.branching)
                    m.d.comb += self.pc_controller.jump.eq(self.ALU.jump)
                    m.d.comb += self.id_mux.stall.eq(self.stall_unit.stall)

                m.d.comb += self.reg_file.csb_mem.eq(Const(0))
                m.d.comb += self.reg_file.web_mem.eq(Const(0))
                m.d.comb += self.reg_file.write_mem.eq(Const(0))

            with m.Else(): 
                m.d.comb += self.IF_ID_pipeline.branch.eq(self.ALU.branching)
                m.d.comb += self.IF_ID_pipeline.jump.eq(self.ALU.jump)
                m.d.comb += self.IF_ID_pipeline.stall.eq(self.stall_unit.stall)
                m.d.comb += self.pc_controller.stall.eq(self.stall_unit.stall)
                m.d.comb += self.pc_controller.branch.eq(self.ALU.branching)
                m.d.comb += self.pc_controller.jump.eq(self.ALU.jump)
                m.d.comb += self.id_mux.stall.eq(self.stall_unit.stall)
                m.d.comb += self.reg_file.csb_mem.eq(self.M2_WB_pipeline.csb_out)
                m.d.comb += self.reg_file.web_mem.eq(self.M2_WB_pipeline.web_out)  
                m.d.comb += self.reg_file.write_mem.eq(self.M2_WB_pipeline.reg_file_write_out)  #pos->comb
                m.d.comb += self.reg_file.csb_alu.eq(self.ALU_M1_pipeline.memory_csb)
                m.d.comb += self.reg_file.write_alu.eq(self.ALU_M1_pipeline.memory_load_wb_in)

        m.d.comb += self.inst_mem_addr.eq(self.pc)

        m.d.comb += self.IF_ID_pipeline.IF2_out.eq(self.inst_mem_rdata)
        m.d.comb += self.ID.instruction.eq(self.IF_ID_pipeline.inst_out)
        
        m.d.comb += self.stall_unit.csb0.eq(self.ALU_M1_pipeline.memory_csb)
        m.d.comb += self.stall_unit.web0.eq(self.ALU_M1_pipeline.memory_web)
        m.d.comb += self.stall_unit.csb1.eq(self.M1_M2_pipeline.csb_out)
        m.d.comb += self.stall_unit.web1.eq(self.M1_M2_pipeline.web_out)
        m.d.comb += self.stall_unit.ID_src1.eq(self.ID.s1)
        m.d.comb += self.stall_unit.ID_src2.eq(self.ID.s2)
        m.d.comb += self.stall_unit.next_dest0.eq(self.ALU_M1_pipeline.memory_reg_addr_out_in)
        m.d.comb += self.stall_unit.next_dest1.eq(self.M1_M2_pipeline.reg_file_write_addr_in)

        m.d.comb += self.pc_controller.pc_in.eq(self.pc)
        m.d.comb += self.pc_controller.ra.eq(self.ALU.Ra)
        m.d.comb += self.pc_controller.immediate.eq(self.ALU.immediate)
        m.d.comb += self.pc_controller.read_flag.eq(self.read_flag) 
        m.d.comb += self.reg_file.pc.eq(self.pc)
        m.d.comb += self.reg_file.load_Rs1_addr.eq(self.ID.s1)
        m.d.comb += self.reg_file.load_Rs2_addr.eq(self.ID.s2)
        m.d.comb += self.ID.s1_data_in.eq(self.reg_file.write_Rs1_data)
        m.d.comb += self.ID.s2_data_in.eq(self.reg_file.write_Rs2_data)

        m.d.comb += self.id_mux.des_id.eq(self.ID.des)
        m.d.comb += self.id_mux.s1_id.eq(self.ID.s1)
        m.d.comb += self.id_mux.s2_id.eq(self.ID.s2)
        m.d.comb += self.id_mux.s1data_out_id.eq(self.ID.s1data_out)
        m.d.comb += self.id_mux.s2data_out_id.eq(self.ID.s2data_out)
        m.d.comb += self.id_mux.signextended_immediate_id.eq(self.ID.signextended_immediate)
        m.d.comb += self.id_mux.instruction_type_id.eq(self.ID.instruction_type)
        m.d.comb += self.id_mux.it0_id.eq(self.ID.it0)
        m.d.comb += self.id_mux.it1_id.eq(self.ID.it1)
        m.d.comb += self.id_mux.it2_id.eq(self.ID.it2)
        m.d.comb += self.id_mux.it3_id.eq(self.ID.it3)
        m.d.comb += self.id_mux.ifload_id.eq(self.ID.ifload)
        m.d.comb += self.id_mux.shamt_id.eq(self.ID.shamt)

        m.d.comb += self.forwarding_alu.s1.eq(self.id_mux.s1)
        m.d.comb += self.forwarding_alu.s2.eq(self.id_mux.s2)
        m.d.comb += self.forwarding_alu.s1_data.eq(self.id_mux.s1data_out)
        m.d.comb += self.forwarding_alu.s2_data.eq(self.id_mux.s2data_out)
        m.d.comb += self.forwarding_alu.des0.eq(self.M2_WB_pipeline.reg_file_write_addr_in)
        m.d.comb += self.forwarding_alu.val0.eq(self.M2_WB_pipeline.reg_file_write_data_in)
        m.d.comb += self.forwarding_alu.csb0.eq(self.M2_WB_pipeline.csb_out)
        m.d.comb += self.forwarding_alu.web0.eq(self.M2_WB_pipeline.web_out)
        m.d.comb += self.forwarding_alu.des1.eq(self.ALU_M1_pipeline.memory_reg_addr_out_in)
        m.d.comb += self.forwarding_alu.val1.eq(self.ALU_M1_pipeline.memory_alu_result_in)
        m.d.comb += self.forwarding_alu.csb1.eq(self.ALU_M1_pipeline.memory_csb)
        m.d.comb += self.forwarding_alu.web1.eq(self.ALU_M1_pipeline.memory_web)

        m.d.comb += self.ALU.pc.eq(self.pc)

        m.d.comb += self.ALU.Ra.eq(self.forwarding_alu.ra)
        m.d.comb += self.ALU.Rb.eq(self.forwarding_alu.rb)
        m.d.comb += self.ALU.reg_addr_in.eq(self.id_mux.des)
        m.d.comb += self.ALU.immediate.eq(self.id_mux.signextended_immediate)
        m.d.comb += self.ALU.inst_type.eq(self.id_mux.instruction_type)
        m.d.comb += self.ALU.inst_type0.eq(self.id_mux.it0)
        m.d.comb += self.ALU.inst_type1.eq(self.id_mux.it1)
        m.d.comb += self.ALU.inst_type2.eq(self.id_mux.it2)
        m.d.comb += self.ALU.inst_type3.eq(self.id_mux.it3)
        m.d.comb += self.ALU.s1.eq(self.id_mux.s1)
        m.d.comb += self.ALU.s2.eq(self.id_mux.s2)
        m.d.comb += self.ALU.shamt.eq(self.id_mux.shamt)

        # this will take care of the condititon where add and store condition come consecutively and 
        # add hasn't completed it's writeback.

        m.d.comb += self.ALU_M1_pipeline.ALU_csb.eq(self.ALU.csb)
        m.d.comb += self.ALU_M1_pipeline.ALU_web.eq(self.ALU.web)
        m.d.comb += self.ALU_M1_pipeline.ALU_wmask.eq(self.ALU.wmask)
        m.d.comb += self.ALU_M1_pipeline.ALU_load_wb_out.eq(self.ALU.load_wb)
        m.d.comb += self.ALU_M1_pipeline.ALU_Rb_out.eq(self.ALU.Rb)
        m.d.comb += self.ALU_M1_pipeline.ALU_reg_addr_out_out.eq(self.ALU.reg_addr_out)
        m.d.comb += self.ALU_M1_pipeline.ALU_result_out.eq(self.ALU.result)
        m.d.comb += self.ALU_M1_pipeline.s1_in.eq(self.ALU.s1)
        m.d.comb += self.ALU_M1_pipeline.s2_in.eq(self.ALU.s2)

        m.d.comb += self.csb_alu.eq(self.ALU_M1_pipeline.memory_csb)
        m.d.comb += self.csb_mem.eq(self.M1_M2_pipeline.csb_out)
        m.d.comb += self.web.eq(self.ALU_M1_pipeline.memory_web)
        m.d.comb += self.wmask.eq(self.ALU_M1_pipeline.mem_wmask)
        m.d.comb += self.data_mem_addr.eq(self.ALU_M1_pipeline.memory_addr_in)
        m.d.comb += self.alu_result.eq(self.ALU_M1_pipeline.memory_alu_result_in)
        
        m.d.comb += self.forwarding_mem.des0.eq(self.M1_M2_pipeline.reg_file_write_addr_in)
        m.d.comb += self.forwarding_mem.val0.eq(self.data_mem_rdata)
        m.d.comb += self.forwarding_mem.csb0.eq(self.M1_M2_pipeline.csb_out)
        m.d.comb += self.forwarding_mem.web0.eq(self.M1_M2_pipeline.web_out)
        m.d.comb += self.forwarding_mem.src.eq(self.ID.s2)
        m.d.comb += self.forwarding_mem.src_data.eq(self.ID.s2data_out)

        m.d.comb += self.data_mem_wdata.eq(self.forwarding_mem.data_in)

        m.d.comb += self.M1_M2_pipeline.reg_file_write_in.eq(self.ALU_M1_pipeline.memory_load_wb_in)
        m.d.comb += self.M1_M2_pipeline.memory_reg_addr_out_out.eq(self.ALU_M1_pipeline.memory_reg_addr_out_in)
        m.d.comb += self.M1_M2_pipeline.s1_in.eq(self.ALU_M1_pipeline.s1_out)
        m.d.comb += self.M1_M2_pipeline.s2_in.eq(self.ALU_M1_pipeline.s2_out)
        m.d.comb += self.M1_M2_pipeline.csb_in.eq(self.ALU_M1_pipeline.memory_csb)
        m.d.comb += self.M1_M2_pipeline.web_in.eq(self.ALU_M1_pipeline.memory_web)

        m.d.comb += self.M2_WB_pipeline.reg_file_write_in.eq(self.M1_M2_pipeline.reg_file_write_out)
        m.d.comb += self.M2_WB_pipeline.memory_reg_addr_out_out.eq(self.M1_M2_pipeline.reg_file_write_addr_in)
        m.d.comb += self.M2_WB_pipeline.memory_data_out_out.eq(self.data_mem_rdata)
        m.d.comb += self.M2_WB_pipeline.s1_in.eq(self.M1_M2_pipeline.s1_out)
        m.d.comb += self.M2_WB_pipeline.s2_in.eq(self.M1_M2_pipeline.s2_out)
        m.d.comb += self.M2_WB_pipeline.csb_in.eq(self.M1_M2_pipeline.csb_out)
        m.d.comb += self.M2_WB_pipeline.web_in.eq(self.M1_M2_pipeline.web_out)

        m.d.comb += self.reg_file.write_addr_alu.eq(self.ALU_M1_pipeline.memory_reg_addr_out_in)
        m.d.comb += self.reg_file.write_data_alu.eq(self.ALU_M1_pipeline.memory_alu_result_in)

        m.d.comb += self.reg_file.write_addr_mem.eq(self.M2_WB_pipeline.reg_file_write_addr_in)
        m.d.comb += self.reg_file.write_data_mem.eq(self.M2_WB_pipeline.reg_file_write_data_in)
        m.d.comb += self.pc.eq(self.pc_controller.pc) 
        m.d.comb += self.gpio_pins.eq(self.reg_file.reg[31])
        m.d.comb += self.reg_file.gpio_input.eq(self.output_pins)
        return m

    def ports(self)->List[Signal]:
        return [self.read_flag,
            self.csb_alu,
            self.csb_mem,
            self.web,
            self.wmask, 
            self.alu_result,
            self.gpio_pins,
            self.output_pins,  
            self.inst_mem_addr,
            self.inst_mem_rdata, 
            self.data_mem_addr,
            self.data_mem_wdata,
            self.data_mem_rdata]
    
if __name__ == "__main__":
    parser = main_parser()
    args = parser.parse_args()

    m = Module()
    m.domains.sync = sync = ClockDomain("sync", async_reset=True)
    
    pos = ClockDomain("pos", async_reset=True)
    neg = ClockDomain("neg",clk_edge="neg",async_reset=True)
    neg.clk = pos.clk
    m.domains += [neg,pos]
    m.submodules.wrapper = wrapper = Wrapper()

    instructions = []
    #reading instructions into the memory
    f = open("./assembly_hex.txt", "r")
    inst = f.readlines()

    for i in range(2**8):

        if(i<len(inst)):
            instruction = "0x"+inst[i]
            instructions.append(Signal(32,reset=int(instruction,16)))

        else:
            instructions.append(Signal(32,reset=0))

    InstMemory = Array(instructions) #IM + DM
    DataMemory = Memory(width = 32, depth = 1024, init = [0 for i in range(1024)])

    Inst_mem_rdata = Signal(32) #input to the wrapper
    Data_mem_rdata = Signal(32)
    data_mem_wdata = Signal(32)

    inst_mem_addr = Signal(8)
    data_mem_addr = Signal(8)
    alu_result = Signal(32)
    csb = Signal(1)
    web = Signal(1)
    wmask = Signal(4)

    m.d.comb += wrapper.read_flag.eq(0b1)
    m.d.sync += inst_mem_addr.eq(wrapper.inst_mem_addr)
    m.d.comb += csb.eq(wrapper.csb_mem)
    m.d.sync += web.eq(wrapper.web)
    m.d.sync += wmask.eq(wrapper.wmask)
    m.d.sync += alu_result.eq(wrapper.alu_result)
    m.d.sync += data_mem_addr.eq(wrapper.data_mem_addr)
    m.d.sync += data_mem_wdata.eq(wrapper.data_mem_wdata)

    m.d.sync += Inst_mem_rdata.eq(InstMemory[inst_mem_addr])
    m.d.sync += wrapper.inst_mem_rdata.eq(Inst_mem_rdata)

    with m.If(csb == 0b0):
        with m.If(web == 0b0):
            with m.If(wmask == 0b1111):
                m.d.neg += DataMemory[data_mem_addr].eq(data_mem_wdata)
            with m.Elif(wmask == 0b1100):
                m.d.neg += DataMemory[data_mem_addr].eq(data_mem_wdata[16:])
            with m.Elif(wmask == 0b0011):
                m.d.neg += DataMemory[data_mem_addr].eq(data_mem_wdata[0:16])
            with m.Elif(wmask == 0b1000):
                m.d.neg += DataMemory[data_mem_addr].eq(data_mem_wdata[24:])
            with m.Elif(wmask == 0b0100):
                m.d.neg += DataMemory[data_mem_addr].eq(data_mem_wdata[16:24])
            with m.Elif(wmask == 0b0010):
                m.d.neg += DataMemory[data_mem_addr].eq(data_mem_wdata[8:16])
            with m.Elif(wmask == 0b0001):
                m.d.neg += DataMemory[data_mem_addr].eq(data_mem_wdata[:8])
        
        with m.Else():
            with m.If(wmask == 0b0000):
                m.d.comb += Data_mem_rdata.eq(alu_result)
            with m.Elif(wmask == 0b0001):
                m.d.comb += Data_mem_rdata.eq(DataMemory[data_mem_addr][0:8])
            with m.Elif(wmask == 0b0010):
                m.d.comb += Data_mem_rdata.eq(DataMemory[data_mem_addr][8:16])
            with m.Elif(wmask == 0b0100):
                m.d.comb += Data_mem_rdata.eq(DataMemory[data_mem_addr][16:24])
            with m.Elif(wmask == 0b1000):
                m.d.comb += Data_mem_rdata.eq(DataMemory[data_mem_addr][24:32])
            with m.Elif(wmask == 0b0011):
                m.d.comb += Data_mem_rdata.eq(DataMemory[data_mem_addr][0:16])
            with m.Elif(wmask == 0b1100):
                m.d.comb += Data_mem_rdata.eq(DataMemory[data_mem_addr][16:32])
            with m.Else():
                m.d.comb += Data_mem_rdata.eq(DataMemory[data_mem_addr]) 
    with m.Else():
        m.d.comb += Data_mem_rdata.eq(alu_result)

    m.d.neg += wrapper.data_mem_rdata.eq(Data_mem_rdata)


    sim = Simulator(m)
    sim.add_clock(1e-6, domain="sync")

    sim.add_clock(1e-6,domain="pos")
    sim.add_clock(1e-6,domain = "neg")

    def process():

        yield

    # commment in these lines for simulations

    sim.add_sync_process(process, domain="sync")
    with sim.write_vcd("code.vcd", "code.gtkw", traces=[]+wrapper.ports()):
        sim.run_until(10000e-6, run_passive=True)

    # comment in these lines for verilog generation
    Wrapper  = Wrapper()
    frag = Wrapper.elaborate(platform=None)
    print(verilog.convert(frag, ports =Wrapper.ports()))

