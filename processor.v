


    module sky130_sram_2kbyte_1rw1r_32x256_8_inst(
    `ifdef USE_POWER_PINS
        vccd1,
        vssd1,
    `endif
    // Port 0: RW
        clk0,csb0,web0,wmask0,addr0,din0,dout0,
    // Port 1: R
        clk1,csb1,addr1,dout1
    );

    parameter NUM_WMASKS = 4 ;
    parameter DATA_WIDTH = 32 ;
    parameter ADDR_WIDTH = 8 ;
    parameter RAM_DEPTH = 1 << ADDR_WIDTH;
    // FIXME: This delay is arbitrary.
    parameter DELAY = 0 ;
    parameter VERBOSE = 0 ; //Set to 0 to only display warnings
    parameter T_HOLD = 0 ; //Delay to hold dout value after posedge. Value is arbitrary

    `ifdef USE_POWER_PINS
        inout vccd1;
        inout vssd1;
    `endif
    input  clk0; // clock
    input   csb0; // active low chip select
    input  web0; // active low write control
    input [NUM_WMASKS-1:0]   wmask0; // write mask
    input [ADDR_WIDTH-1:0]  addr0;
    input [DATA_WIDTH-1:0]  din0;
    output [DATA_WIDTH-1:0] dout0;
    input  clk1; // clock
    input   csb1; // active low chip select
    input [ADDR_WIDTH-1:0]  addr1;
    output [DATA_WIDTH-1:0] dout1;

    reg  csb0_reg;
    reg  web0_reg;
    reg [NUM_WMASKS-1:0]   wmask0_reg;
    reg [ADDR_WIDTH-1:0]  addr0_reg;
    reg [DATA_WIDTH-1:0]  din0_reg;
    reg [DATA_WIDTH-1:0]  dout0;

    // All inputs are registers
    always @(posedge clk0)
    begin
        csb0_reg = csb0;
        web0_reg = web0;
        wmask0_reg = wmask0;
        addr0_reg = addr0;
        din0_reg = din0;
        #(T_HOLD) dout0 = 32'bx;
        // if ( !csb0_reg && web0_reg && VERBOSE ) 
        //   $display($time," Reading %m addr0=%b dout0=%b",addr0_reg,mem[addr0_reg]);
        // if ( !csb0_reg && !web0_reg && VERBOSE )
        //   $display($time," Writing %m addr0=%b din0=%b wmask0=%b",addr0_reg,din0_reg,wmask0_reg);
    end

    reg  csb1_reg;
    reg [ADDR_WIDTH-1:0]  addr1_reg;
    reg [DATA_WIDTH-1:0]  dout1;

    // All inputs are registers
    always @(posedge clk1)
    begin
        csb1_reg = csb1;
        addr1_reg = addr1;
        // if (!csb0 && !web0 && !csb1 && (addr0 == addr1))
        //      $display($time," WARNING: Writing and reading addr0=%b and addr1=%b simultaneously!",addr0,addr1);
        #(T_HOLD) dout1 = 32'bx;
        // if ( !csb1_reg && VERBOSE ) 
        //   $display($time," Reading %m addr1=%b dout1=%b",addr1_reg,mem[addr1_reg]);
    end

    reg [DATA_WIDTH-1:0]    mem [0:RAM_DEPTH-1];

    // Memory Write Block Port 0
    // Write Operation : When web0 = 0, csb0 = 0
    always @ (negedge clk0)
    begin : MEM_WRITE0
        if ( !csb0_reg && !web0_reg ) begin
            if (wmask0_reg[0])
                    mem[addr0_reg][7:0] = din0_reg[7:0];
            if (wmask0_reg[1])
                    mem[addr0_reg][15:8] = din0_reg[15:8];
            if (wmask0_reg[2])
                    mem[addr0_reg][23:16] = din0_reg[23:16];
            if (wmask0_reg[3])
                    mem[addr0_reg][31:24] = din0_reg[31:24];
        end
    end

    // Memory Read Block Port 0
    // Read Operation : When web0 = 1, csb0 = 0
    always @ (negedge clk0)
    begin : MEM_READ0
        if (!csb0_reg && web0_reg)
        dout0 = #(DELAY) mem[addr0_reg];
    end

    // Memory Read Block Port 1
    // Read Operation : When web1 = 1, csb1 = 0
    always @ (negedge clk1)
    begin : MEM_READ1
        if (!csb1_reg)
        dout1 = #(DELAY) mem[addr1_reg];
    end

    endmodule


    module sky130_sram_2kbyte_1rw1r_32x256_8_data(
    `ifdef USE_POWER_PINS
        vccd1,
        vssd1,
    `endif
    // Port 0: RW
        clk0,csb0,web0,wmask0,addr0,din0,dout0,
    // Port 1: R
        clk1,csb1,addr1,dout1
    );

    parameter NUM_WMASKS = 4 ;
    parameter DATA_WIDTH = 32 ;
    parameter ADDR_WIDTH = 8 ;
    parameter RAM_DEPTH = 1 << ADDR_WIDTH;
    // FIXME: This delay is arbitrary.
    parameter DELAY = 0 ;
    parameter VERBOSE = 0 ; //Set to 0 to only display warnings
    parameter T_HOLD = 0 ; //Delay to hold dout value after posedge. Value is arbitrary

    `ifdef USE_POWER_PINS
        inout vccd1;
        inout vssd1;
    `endif
    input  clk0; // clock
    input   csb0; // active low chip select
    input  web0; // active low write control
    input [NUM_WMASKS-1:0]   wmask0; // write mask
    input [ADDR_WIDTH-1:0]  addr0;
    input [DATA_WIDTH-1:0]  din0;
    output [DATA_WIDTH-1:0] dout0;
    input  clk1; // clock
    input   csb1; // active low chip select
    input [ADDR_WIDTH-1:0]  addr1;
    output [DATA_WIDTH-1:0] dout1;

    reg  csb0_reg;
    reg  web0_reg;
    reg [NUM_WMASKS-1:0]   wmask0_reg;
    reg [ADDR_WIDTH-1:0]  addr0_reg;
    reg [DATA_WIDTH-1:0]  din0_reg;
    reg [DATA_WIDTH-1:0]  dout0;

    // All inputs are registers
    always @(posedge clk0)
    begin
        csb0_reg = csb0;
        web0_reg = web0;
        wmask0_reg = wmask0;
        addr0_reg = addr0;
        din0_reg = din0;
        #(T_HOLD) dout0 = 32'bx;
        // if ( !csb0_reg && web0_reg && VERBOSE ) 
        //   $display($time," Reading %m addr0=%b dout0=%b",addr0_reg,mem[addr0_reg]);
        // if ( !csb0_reg && !web0_reg && VERBOSE )
        //   $display($time," Writing %m addr0=%b din0=%b wmask0=%b",addr0_reg,din0_reg,wmask0_reg);
    end

    reg  csb1_reg;
    reg [ADDR_WIDTH-1:0]  addr1_reg;
    reg [DATA_WIDTH-1:0]  dout1;

    // All inputs are registers
    always @(posedge clk1)
    begin
        csb1_reg = csb1;
        addr1_reg = addr1;
        // if (!csb0 && !web0 && !csb1 && (addr0 == addr1))
        //      $display($time," WARNING: Writing and reading addr0=%b and addr1=%b simultaneously!",addr0,addr1);
        #(T_HOLD) dout1 = 32'bx;
        // if ( !csb1_reg && VERBOSE ) 
        //   $display($time," Reading %m addr1=%b dout1=%b",addr1_reg,mem[addr1_reg]);
    end

    reg [DATA_WIDTH-1:0]    mem [0:RAM_DEPTH-1];

    // Memory Write Block Port 0
    // Write Operation : When web0 = 0, csb0 = 0
    always @ (negedge clk0)
    begin : MEM_WRITE0
        if ( !csb0_reg && !web0_reg ) begin
            if (wmask0_reg[0])
                    mem[addr0_reg][7:0] = din0_reg[7:0];
            if (wmask0_reg[1])
                    mem[addr0_reg][15:8] = din0_reg[15:8];
            if (wmask0_reg[2])
                    mem[addr0_reg][23:16] = din0_reg[23:16];
            if (wmask0_reg[3])
                    mem[addr0_reg][31:24] = din0_reg[31:24];
        end
    end

    // Memory Read Block Port 0
    // Read Operation : When web0 = 1, csb0 = 0
    always @ (negedge clk0)
    begin : MEM_READ0
        if (!csb0_reg && web0_reg)
        dout0 = #(DELAY) mem[addr0_reg];
    end

    // Memory Read Block Port 1
    // Read Operation : When web1 = 1, csb1 = 0
    always @ (negedge clk1)
    begin : MEM_READ1
        if (!csb1_reg)
        dout1 = #(DELAY) mem[addr1_reg];
    end

    endmodule

    module uart_rx(
    input  wire       clk          , // Top level system clock input.
    input  wire       resetn       , // Asynchronous active low reset.
    input  wire       uart_rxd     , // UART Recieve pin.
    input  wire       uart_rx_en   , // Recieve enable
    output wire       uart_rx_break, // Did we get a BREAK message?
    output wire       uart_rx_valid, // Valid data recieved and available.
    output reg  [8-1:0] uart_rx_data   // The recieved data.
    );

    // --------------------------------------------------------------------------- 
    // External parameters.
    // 

    //
    // Input bit rate of the UART line.
    parameter   BIT_RATE        = 9600; // bits / sec
    localparam  BIT_P           = 1_000_000_000 * 1/BIT_RATE; // nanoseconds

    //
    // Clock frequency in hertz.
    parameter   CLK_HZ          =    50_000_000;
    localparam  CLK_P           = 1_000_000_000 * 1/CLK_HZ; // nanoseconds

    //
    // Number of data bits recieved per UART packet.
    parameter   PAYLOAD_BITS    = 8;

    //
    // Number of stop bits indicating the end of a packet.
    parameter   STOP_BITS       = 1;

    // -------------------------------------------------------------------------- 
    // Internal parameters.
    // 

    //
    // Number of clock cycles per uart bit.
    localparam       CYCLES_PER_BIT     = BIT_P / CLK_P;

    //
    // Size of the registers which store sample counts and bit durations.
    localparam       COUNT_REG_LEN      = 1+$clog2(CYCLES_PER_BIT);

    // -------------------------------------------------------------------------- 
    // Internal registers.
    // 

    //
    // Internally latched value of the uart_rxd line. Helps break long timing
    // paths from input pins into the logic.
    reg rxd_reg;
    reg rxd_reg_0;

    //
    // Storage for the recieved serial data.
    reg [PAYLOAD_BITS-1:0] recieved_data;

    //
    // Counter for the number of cycles over a packet bit.
    reg [COUNT_REG_LEN-1:0] cycle_counter;

    //
    // Counter for the number of recieved bits of the packet.
    reg [3:0] bit_counter;

    //
    // Sample of the UART input line whenever we are in the middle of a bit frame.
    reg bit_sample;

    //
    // Current and next states of the internal FSM.
    reg [2:0] fsm_state;
    reg [2:0] n_fsm_state;

    localparam FSM_IDLE = 0;
    localparam FSM_START= 1;
    localparam FSM_RECV = 2;
    localparam FSM_STOP = 3;

    // --------------------------------------------------------------------------- 
    // Output assignment
    // 

    assign uart_rx_break = uart_rx_valid && ~|recieved_data;
    assign uart_rx_valid = fsm_state == FSM_STOP && n_fsm_state == FSM_IDLE;

    always @(posedge clk) begin
        if(!resetn) begin
            uart_rx_data  <= {PAYLOAD_BITS{1'b0}};
        end else if (fsm_state == FSM_STOP) begin
            uart_rx_data  <= recieved_data;
        end
    end

    // --------------------------------------------------------------------------- 
    // FSM next state selection.
    // 

    wire next_bit     = cycle_counter == CYCLES_PER_BIT ||
                            fsm_state       == FSM_STOP && 
                            cycle_counter   == CYCLES_PER_BIT/2;
    wire payload_done = bit_counter   == PAYLOAD_BITS  ;

    //
    // Handle picking the next state.
    always @(*) begin : p_n_fsm_state
        case(fsm_state)
            FSM_IDLE : n_fsm_state = rxd_reg      ? FSM_IDLE : FSM_START;
            FSM_START: n_fsm_state = next_bit     ? FSM_RECV : FSM_START;
            FSM_RECV : n_fsm_state = payload_done ? FSM_STOP : FSM_RECV ;
            FSM_STOP : n_fsm_state = next_bit     ? FSM_IDLE : FSM_STOP ;
            default  : n_fsm_state = FSM_IDLE;
        endcase
    end

    // --------------------------------------------------------------------------- 
    // Internal register setting and re-setting.
    // 

    //
    // Handle updates to the recieved data register.
    integer i = 0;
    always @(posedge clk) begin : p_recieved_data
        if(!resetn) begin
            recieved_data <= {PAYLOAD_BITS{1'b0}};
        end else if(fsm_state == FSM_IDLE             ) begin
            recieved_data <= {PAYLOAD_BITS{1'b0}};
        end else if(fsm_state == FSM_RECV && next_bit ) begin
            recieved_data[PAYLOAD_BITS-1] <= bit_sample;
            for ( i = PAYLOAD_BITS-2; i >= 0; i = i - 1) begin
                recieved_data[i] <= recieved_data[i+1];
            end
        end
    end

    //
    // Increments the bit counter when recieving.
    always @(posedge clk) begin : p_bit_counter
        if(!resetn) begin
            bit_counter <= 4'b0;
        end else if(fsm_state != FSM_RECV) begin
            bit_counter <= {COUNT_REG_LEN{1'b0}};
        end else if(fsm_state == FSM_RECV && next_bit) begin
            bit_counter <= bit_counter + 1'b1;
        end
    end

    //
    // Sample the recieved bit when in the middle of a bit frame.
    always @(posedge clk) begin : p_bit_sample
        if(!resetn) begin
            bit_sample <= 1'b0;
        end else if (cycle_counter == CYCLES_PER_BIT/2) begin
            bit_sample <= rxd_reg;
        end
    end


    //
    // Increments the cycle counter when recieving.
    always @(posedge clk) begin : p_cycle_counter
        if(!resetn) begin
            cycle_counter <= {COUNT_REG_LEN{1'b0}};
        end else if(next_bit) begin
            cycle_counter <= {COUNT_REG_LEN{1'b0}};
        end else if(fsm_state == FSM_START || 
                    fsm_state == FSM_RECV  || 
                    fsm_state == FSM_STOP   ) begin
            cycle_counter <= cycle_counter + 1'b1;
        end
    end


    //
    // Progresses the next FSM state.
    always @(posedge clk) begin : p_fsm_state
        if(!resetn) begin
            fsm_state <= FSM_IDLE;
        end else begin
            fsm_state <= n_fsm_state;
        end
    end


    //
    // Responsible for updating the internal value of the rxd_reg.
    always @(posedge clk) begin : p_rxd_reg
        if(!resetn) begin
            rxd_reg     <= 1'b1;
            rxd_reg_0   <= 1'b1;
        end else if(uart_rx_en) begin
            rxd_reg     <= rxd_reg_0;
            rxd_reg_0   <= uart_rxd;
        end
    end


    endmodule

    module wrapper(clk,resetn,uart_rxd,uart_rx_en,uart_rx_break,uart_rx_valid,uart_rx_data, output_gpio_pins, input_gpio_pins, write_done, instructions);
    input clk;
    output reg write_done ; 
    output reg [2:0] instructions ; 
    input wire [7:0] input_gpio_pins;
    output reg [31:8] output_gpio_pins;  
    reg rst;
    reg neg_clk; 
    reg neg_rst; 
    input  resetn       ; // Asynchronous active low reset.
    input  uart_rxd     ; // UART Recieve pin.
    input  uart_rx_en   ; // Recieve enable
    output uart_rx_break; // Did we get a BREAK message?
    output uart_rx_valid; // Valid data recieved and available.
    output [7:0] uart_rx_data  ; // The recieved data.


    wire web;
    wire [7:0]inst_mem_addr;
    wire [7:0] data_mem_addr;
    wire [31:0]data_mem_wdata;
    wire [3:0]mem_wstrb;
    wire [31:0] inst_mem_rdata;
    wire [31:0] inst_mem_rdata_dummy;
    reg [31:0] inst_mem_rdata_reg;
    wire [31:0] data_mem_rdata; 
    wire [31:0] data_mem_rdata_dummy; 
    reg [31:0] data_mem_rdata_reg;

    wire [3:0] wmask; 
    wire csb_mem;
    wire csb_alu;

    reg temp_web;
    reg temp_csb;

    reg [31:0]instruction;

    parameter zero = 1'b0;
    parameter one = 1'b1;

    reg[7:0]write_inst_count;
    reg writing_inst_done;
    wire uart_rx_valid;
    wire [31:0] alu_result ; 

    wire [31:0] top_gpio_pins; 


    reg [1:0]inst_byte_count;
    reg inst_flag;// active low as write enable of sram is active low 

    always@(*)
    begin 
        neg_clk = ~clk; 
        rst = ~resetn ; 
        neg_rst = ~resetn; 
    end 

    // reg [2:0] count = 3'b0; // 3-bit counter to divide by 5
    // reg clk = 0; 

    reg [31:0] output_pins ; 

    always@(posedge clk)
    begin

        if(rst==1)
        begin 
            writing_inst_done=0;
            write_inst_count=0;
            instruction=0;
            inst_byte_count=0;
            inst_flag=1;
            
        end
        else 
        begin
            if(writing_inst_done==0)
            begin
                inst_flag=1;
                
                
                if(uart_rx_valid==1)
                begin
                    //inst_flag=1;
                    inst_byte_count = inst_byte_count+1;
                    if(inst_byte_count==1)
                    instruction[7:0]=uart_rx_data;
                    else if(inst_byte_count==2)
                    instruction[15:8]=uart_rx_data;
                    else if(inst_byte_count==3)
                    instruction[23:16]=uart_rx_data;
                    
                    // instruction = {o_Rx_Byte,instruction};
                    
                    else//byte count=4
                    begin
                        instruction[31:24]=uart_rx_data;
                        inst_flag=0;
                        inst_byte_count=0;
                        write_inst_count=write_inst_count+1;
                        if(instruction==32'b11111111111111111111111111111111)
                        begin
                        inst_flag=1;
                        writing_inst_done=1;
                        //write_inst_count<=inst_mem_addr;
                        end
                    end
                end
                temp_web=inst_flag;
                temp_csb=inst_flag;
            end
            else//(writing_inst_done==1)
            begin
                write_inst_count=inst_mem_addr;
                //starting to read 
                temp_web=1;//same as csb not proper 
                temp_csb=0;//csb from top module is not proper so hardwiring it to 0

                    
            end
        end
    end

    // (* blackbox *)
    top top_inst(.web(web), 
                .inst_mem_addr(inst_mem_addr), 
                .data_mem_addr(data_mem_addr),
                .data_mem_wdata(data_mem_wdata),
                .wmask(wmask), 
                .inst_mem_rdata(inst_mem_rdata_reg), 
                .data_mem_rdata(data_mem_rdata_reg),
                .neg_clk(neg_clk), 
                .neg_rst(neg_rst), 
                .clk(clk),
                .rst(rst), 
                .csb_mem(csb_mem),
                .csb_alu(csb_alu),
                .read_flag(writing_inst_done), 
                .alu_result(alu_result), 
                .gpio_pins(top_gpio_pins),  
                .output_pins(output_pins));


    // (* blackbox *)
    uart_rx uart_inst(.clk(clk)          , // Top level system clock input.
    .resetn(resetn)       , // Asynchronous active low reset.
    .uart_rxd(uart_rxd)     , // UART Recieve pin.
    .uart_rx_en(uart_rx_en)   , // Recieve enable
    .uart_rx_break(uart_rx_break), // Did we get a BREAK message?
    .uart_rx_valid(uart_rx_valid), // Valid data recieved and available.
    .uart_rx_data(uart_rx_data) );  // The recieved data.)



    // (* blackbox *)
    sky130_sram_2kbyte_1rw1r_32x256_8_inst inst_mem(
    .clk0(clk),// clock
    .csb0(temp_csb), // active low chip select
    .web0(temp_web), // active low write control
    .wmask0(4'b1111), // write mask
    .addr0(write_inst_count),
    .din0(instruction),
    .dout0(inst_mem_rdata),

    //not using 
    .clk1(1'b0), // clock
    .csb1(1'b1), // active low chip select
    .addr1(write_inst_count),
    .dout1(inst_mem_rdata_dummy)
    );

    //data mem
    // (* blackbox *)
    sky130_sram_2kbyte_1rw1r_32x256_8_data data_mem(
    .clk0(clk), // clock
    .csb0(csb_alu), // active low chip select
    .web0(web), // active low write control
    .wmask0(wmask), // write mask
    .addr0(data_mem_addr),
    .din0(data_mem_wdata),
    .dout0(data_mem_rdata),

    //not using 
    .clk1(1'b0), // clock
    .csb1(1'b1), // active low chip select
    .addr1(write_inst_count),
    .dout1(data_mem_rdata_dummy)
    );
    //sram_1rw0r0w_32_1024_sky130A_icache sram_instr_inst(.clk0(clk),.csb0(temp_csb),.web0(temp_web),.addr0(write_inst_count[9:0]),.din0(instruction),.dout0(inst_mem_rdata));
    //sram_1rw0r0w_32_1024_sky130A_dcache sram_data_inst(.clk0(clk),.csb0(csb),.web0(web),.addr0(data_mem_addr[9:0]),.din0(data_mem_wdata),.dout0(data_mem_rdata));

    always@(*) 
    begin 
        if(csb_mem == 0)
        begin 
            data_mem_rdata_reg = data_mem_rdata; 
        end 
        else 
        begin 
            data_mem_rdata_reg = alu_result; 
        end
    end 



    always@(posedge clk)
    begin 
        inst_mem_rdata_reg = inst_mem_rdata; 
        // data_mem_rdata_reg = data_mem_rdata;

    end 

    always @(posedge clk) 
    begin
    output_pins = {top_gpio_pins[31:8],  input_gpio_pins} ; 
    output_gpio_pins = top_gpio_pins[31:8]; 
    write_done = writing_inst_done ; 
    instructions = write_inst_count[2:0]; 

    end 

    endmodule
    
