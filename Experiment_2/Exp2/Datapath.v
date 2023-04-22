module Datapath(
input CLK,
input RESET,
input RegWrite, MemWrite, ImmSrc,
input [1:0] RegSrc,
output [31:0] OUT,
output FlagZ

);

wire [3:0] RA1, RA2, ALUControl;
wire [31:0] RD1, RD2, RD2_S, SrcB, R15, ALUResult, ReadData; 
wire [31:0] WriteData, ExtImm,NewPC;
wire [31:0] INSTR,PC_W,PCPlus4;

// Program Counter
wire [31:0] PC;


Register_file reg_file (
	.clk(CLK),
	.write_enable(RegWrite),
	.Source_select_0(RA1),
	.Source_select_1(RA2),
	.Destination_select(INSTR[15:12]),
	.out_0(RD1),
	.out_1(RD2),
	.DATA(OUT),
	.reset(RESET),
	.Reg_15(R15)
);


Memory data_memory(
	.clk(CLK),
	.WE(MemWrite),
	.ADDR(ALUResult),
	.RD(ReadData),
	.WD(RD2)
);

Instruction_memory instruction_mem(
	.ADDR(PC),
	.RD(INSTR)
);


ALU #(32) alu (
	.control(ALUControl),
	.DATA_A(RD1),
	.DATA_B(SrcB),
	.OUT(ALUResult),
	.Z(FlagZ)
);

 
// MUX for ALU input B
Mux_2to1 #(32) mux_b (
    .input_0(RD2_S),
    .input_1(ExtImm),
    .select(ALUSrc),
    .output_value(SrcB)
);

// MUX for Result
Mux_2to1 #(32) mux_result (
    .input_0(ALUResult),
    .input_1(ReadData),
    .select(MemtoReg),
    .output_value(OUT)
);

// MUX for Branch
Mux_2to1 #(32) mux_pc (
    .input_0(PCPlus4),
    .input_1(OUT),
    .select(PCSrc),
    .output_value(NewPC)
);


// MUX for RegSrc[0]
Mux_2to1 mux_reg (
    .input_0(INSTR[3:0]),
    .input_1(INSTR[15:12]),
    .select(RegSrc[1]),
    .output_value(RA2)
);

// MUX for RegSrc[1]
Mux_2to1 mux_reg_1 (
    .input_0(INSTR[19:16]),
    .input_1(4'b1111),
    .select(RegSrc[0]),
    .output_value(RA1)
);

Extender extend(
	.select(ImmSrc),
	.Q(ExtImm),
	.A(INSTR[23:0])
);

Adder add_pc_four(
	.DATA_A(PC),
	.DATA_B(4),
	.OUT(PCPlus4)
);

Adder add_pc_eight(
	.DATA_A(PCPlus4),
	.DATA_B(4),
	.OUT(R15)
);

Register_simple #(32) reg_pc(
	.clk(CLK),
	.DATA(NewPC),
	.reset(RESET),
	.OUT(PC)
);

shifter #(32) shift(
	.control(INSTR[6:5]),
	.shamt(INSTR[11:7]),
	.DATA(RD2),
	.OUT(RD2_S)
);

endmodule