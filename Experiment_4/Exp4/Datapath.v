module Datapath(
	input CLK,
	input RESET,
	input RegWriteW, MemWriteM, MemtoRegW, ALUSrcE,PCSrcW,
	input [1:0] RegSrcD, ImmSrcD, 
	input [3:0] ALUControlE,
	output [31:0] INSTR, InstructionF,
	output [31:0] ALUOutM,ALUOutW,
	output [31:0] PCPrime, PCF,PCPlus4F,
	output [31:0] OUT, 
	output [3:0] RA1D, RA2D,
	output [3:0] WA3E, WA3M, WA3W,
	output [31:0] RD1, RD2, RD1_OUT, RD2_OUT, RD2_S,
	output [31:0] ALUResultE, ExtImmE,ExtImmD,
	output [31:0] SrcBE, ReadDataM, ReadDataW, WriteDataM,
	output FlagZ
	//input StallD, FlushD, FlushE, ForwardAE, ForwardBE,
	//output [31:0] SrcAE, SrcBE,SrcBEIn
	//output [31:0] PCWait,
);

wire ZIn;
wire [4:0] shamt5;

// REG File
Register_file reg_file (
	.clk(CLK),
	.write_enable(RegWriteW),
	.Source_select_0(RA1D),
	.Source_select_1(RA2D),
	.Destination_select(WA3W),
	.out_0(RD1),
	.out_1(RD2),
	.DATA(OUT),
	.reset(RESET),
	.Reg_15(PCPlus4F)
);


// FETCH STAGE

// MUX for PCSrcW
Mux_2to1 #(32) mux_pc(
	.input_0(PCPlus4F),
	.input_1(OUT),
	.select(PCSrcW),
	.output_value(PCPrime)
);

// Register for PC_prime to PCF
Register_simple #(32) reg_pc(
	.clk(CLK),
	.DATA(PCPrime),
	.reset(RESET),
	.OUT(PCF)
);

// Instruction memory
Instruction_memory instruction_mem(
	.ADDR(PCF),
	.RD(InstructionF)
);

// Register InstructionF tp InstructionD
Register_sync_rw #(32) reg_instr(
	.clk(CLK),
	.DATA(InstructionF),
	.reset(FlushD),
	.we(1),
	.OUT(INSTR)
);

// PC Adder
Adder add_pc_four(
	.DATA_A(PCF),
	.DATA_B(4),
	.OUT(PCPlus4F)
);

// DECODE STAGE

// MUX for RegSrcD[1]
Mux_2to1 mux_reg (
    .input_0(INSTR[3:0]),
    .input_1(INSTR[15:12]),
    .select(RegSrcD[1]),
    .output_value(RA2D)
);

// MUX for RegSrcD[0]
Mux_2to1 mux_reg_1 (
    .input_0(INSTR[19:16]),
    .input_1(4'b1111),
    .select(RegSrcD[0]),
    .output_value(RA1D)
);

// Extender
Extender extend(
	.select(ImmSrcD),
	.Q(ExtImmD),
	.A(INSTR[23:0])
);

assign shamt5 = (INSTR[27:26] == 2'b00) ? INSTR[11:7] : 0; 

shifter #(32) shift(
	.control(INSTR[6:5]),
	.shamt(shamt5),
	.DATA(RD2),
	.OUT(RD2_S)
);

// EXECUTE STAGE

// Register for ExtImmD to ExtImmE with FlushE
Register_sync_rw #(32) reg_ext(
	.clk(CLK),
	.DATA(ExtImmD),
	.reset(FlushE),
	.we(1'b1),
	.OUT(ExtImmE)
);

// Register for RD1 to RD1_OUT with FlushE
Register_sync_rw #(32) reg_rd1(
	.clk(CLK),
	.DATA(RD1),
	.reset(FlushE),
	.we(1'b1),
	.OUT(RD1_OUT)
);

// Register for INSTR[15:12] to WA3E with FlushE
Register_sync_rw #(4) reg_wa3(
	.clk(CLK),
	.DATA(INSTR[15:12]),
	.reset(FlushE),
	.we(1'b1),
	.OUT(WA3E)
);

// Register for RD2 to RD2_OUT with FlushE
Register_sync_rw #(32) reg_rd2(
	.clk(CLK),
	.DATA(RD2_S),
	.reset(FlushE),
	.we(1'b1),
	.OUT(RD2_OUT)
);

/*
// MUX for RD1
Mux_4to1 #(32) mux_rd1(
	.input_0(RD1_OUT),
	.input_1(OUT),
	.input_2(ALUOutM),
	.input_3(0),
	.select(ForwardAE),
	.output_value(SrcAE)
);*/

/*// MUX for RD2
Mux_4to1 #(32) mux_rd2 (
	.input_0(RD2_OUT),
	.input_1(OUT),
	.input_2(ALUOutM),
	.input_3(0),
	.select(ForwardBE),
	.output_value(SrcBEIn)
);*/

// MUX for SrcBE
Mux_2to1 #(32) mux_src_be(
	.input_0(RD2_OUT),
	.input_1(ExtImmE),
	.select(ALUSrcE),
	.output_value(SrcBE)
);

// ALU
ALU #(32) alu (
	.control(ALUControlE),
	.DATA_A(RD1_OUT),
	.DATA_B(SrcBE),
	.OUT(ALUResultE),
	.Z(ZIn)
);


// MEMORY

// Register for ALUResultE to ALUResultM
Register_sync_rw #(32) reg_alu(
	.clk(CLK),
	.DATA(ALUResultE),
	.reset(RESET),
	.we(1'b1),
	.OUT(ALUOutM)
);

// Register for RD2_OUT to WriteDataM
Register_sync_rw #(32) reg_wd(
	.clk(CLK),
	.DATA(RD2_OUT),
	.reset(RESET),
	.we(1'b1),
	.OUT(WriteDataM)
);

// Register for WA3E to WA3M
Register_sync_rw #(4) reg_wa3m(
	.clk(CLK),
	.DATA(WA3E),
	.reset(RESET),
	.we(1'b1),
	.OUT(WA3M)
);

// Data Memory
Memory DM(
	.clk(CLK),
	.WE(MemWriteM),
	.ADDR(ALUOutM),
	.RD(ReadDataM),
	.WD(WriteDataM)
);

// WRITE BACK

// Register ReadDataM to ReadDataW
Register_sync_rw #(32) reg_read_data(
	.clk(CLK),
	.DATA(ReadDataM),
	.reset(RESET),
	.we(1'b1),
	.OUT(ReadDataW)
);

// Register for WA3M to WA3W
Register_sync_rw #(4) reg_wa3w(
	.clk(CLK),
	.DATA(WA3M),
	.reset(RESET),
	.we(1'b1),
	.OUT(WA3W)
);

// Register for ALUOutM to ALUOutW
Register_sync_rw #(32) reg_alu_out(
	.clk(CLK),
	.DATA(ALUOutM),
	.reset(RESET),
	.we(1'b1),
	.OUT(ALUOutW)
);

// MUX for ReadDataW
Mux_2to1 #(32) mux_read_data(
	.input_0(ALUOutW),
	.input_1(ReadDataW),
	.select(MemtoRegW),
	.output_value(OUT)
);






endmodule