python3 assembly_hex.py
python3 ALU_generator.py
python3 Forward_ALU_generator.py
python3 Forward_mem_generator.py
python3 ID_generator.py
python3 ID_controller.py
python3 PC_generator.py
python3 Pipeline_generator.py
python3 Reg_File_generator.py
python3 Stall_generator.py
python3 Wrapper_generator.py
[ ! -d all_stages ] || rm -Rf all_stages
mkdir all_stages
[ ! -f alu.py ] || mv alu.py ./all_stages/alu.py
[ ! -f forward_alu.py ] || mv forward_alu.py ./all_stages/forward_alu.py
[ ! -f forward_mem.py ] || mv forward_mem.py ./all_stages/forward_mem.py
[ ! -f id_mux.py ] || mv id_mux.py ./all_stages/id_mux.py
[ ! -f id.py ] || mv id.py ./all_stages/id.py
[ ! -f IF_ID_pipeline.py ] || mv IF_ID_pipeline.py ./all_stages/IF_ID_pipeline.py
[ ! -f ID_ALU_pipeline.py ] || mv ID_ALU_pipeline.py ./all_stages/ID_ALU_pipeline.py
[ ! -f ALU_M1_pipeline.py ] || mv ALU_M1_pipeline.py ./all_stages/ALU_M1_pipeline.py
[ ! -f M1_M2_pipeline.py ] || mv M1_M2_pipeline.py ./all_stages/M1_M2_pipeline.py
[ ! -f M2_WB_pipeline.py ] || mv M2_WB_pipeline.py ./all_stages/M2_WB_pipeline.py
[ ! -f pc_controller.py ] || mv pc_controller.py ./all_stages/pc_controller.py
[ ! -f reg_file.py ] || mv reg_file.py ./all_stages/reg_file.py
[ ! -f Stall_unit.py ] || mv Stall_unit.py ./all_stages/Stall_unit.py
python3 assembly_hex.py
python3 Wrapper_class.py > processor.v
python3 testbench_generator.py
python3 processor_appendor.py
cat temp.txt >> processor.v
# iverilog -o test testbench.v processor.v
# ./test