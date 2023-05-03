module Datapath(
input CLK,
input RESET,
input RegWrite, MemWrite, ALUSrcA, PCWrite, AdSrc, Sel14,IRWrite,
input [1:0] RegSrc, ImmSrc, ALUSrcB, ResultSrc,
input [3:0] ALUControl,
output [31:0] INSTR, ALUOut,
output [31:0] OUT, PC, 
output [3:0] RA1, RA2, RA3,
output [31:0] RD1, RD2, ALUResult,
output FlagZ

);

wire [31:0] RD2_S, SrcB, SrcA, R15, ReadData, RD1_OUT, RD2_OUT; 
wire [31:0] WriteData, ExtImm, ReadDataOut, ADR;
wire ZIn;

// REG File
Register_file reg_file (
	.clk(CLK),
	.write_enable(RegWrite),
	.Source_select_0(RA1),
	.Source_select_1(RA2),
	.Destination_select(RA3),
	.out_0(RD1),
	.out_1(RD2),
	.DATA(OUT),
	.reset(RESET),
	.Reg_15(R15)
);

// MUX for BX LR
Mux_2to1 #(32) mux_alu_bx_lr (
    .input_0(INSTR[15:12]),
    .input_1(14),
    .select(Sel14),
    .output_value(RA3)
);

// Memory
Memory IDM(
	.clk(CLK),
	.WE(MemWrite),
	.ADDR(ADR),
	.RD(ReadData),
	.WD(RD2_OUT)
);


// ReadData
Register_simple #(32) reg_read_data(
	.clk(CLK),
	.DATA(ReadData),
	.reset(RESET),
	.OUT(ReadDataOut)
);

// INSTR
Register_sync_rw #(32) reg_instr(
	.clk(CLK),
	.DATA(ReadData),
	.reset(RESET),
	.we(IRWrite),
	.OUT(INSTR)
);


// RD1
Register_simple #(32) reg_rd1(
	.clk(CLK),
	.DATA(RD1),
	.reset(RESET),
	.OUT(RD1_OUT)
);

// RD2_S after shifter
Register_simple #(32) reg_rd2(
	.clk(CLK),
	.DATA(RD2_S),
	.reset(RESET),
	.OUT(RD2_OUT)
);


// MUX for ALU input A
Mux_2to1 #(32) mux_alu_a (
    .input_0(RD1_OUT),
    .input_1(PC),
    .select(ALUSrcA),
    .output_value(SrcA)
);

// MUX for ALU input B
Mux_4to1 #(32) mux_alu_b (
    .input_0(RD2_OUT),
    .input_1(ExtImm),
	 .input_2(4),
	 .input_3(0),
    .select(ALUSrcB),
    .output_value(SrcB)
);

// ALU
ALU #(32) alu (
	.control(ALUControl),
	.DATA_A(SrcA),
	.DATA_B(SrcB),
	.OUT(ALUResult),
	.Z(ZIn)
);

// After ALUResult
Register_simple #(32) reg_alu(
	.clk(CLK),
	.DATA(ALUResult),
	.reset(RESET),
	.OUT(ALUOut)
);


// MUX for Result
Mux_4to1 #(32) mux_result (
    .input_0(ALUOut),
    .input_1(ReadDataOut),
	 .input_2(ALUResult),
	 .input_3(0),
    .select(ResultSrc),
    .output_value(OUT)
);

// PC
Register_sync_rw #(32) reg_pc(
	.clk(CLK),
	.DATA(OUT),
	.reset(RESET),
	.we(PCWrite),
	.OUT(PC)
);


// MUX for Address
Mux_2to1 #(32) mux_pc (
    .input_0(PC),
    .input_1(OUT),
    .select(AdSrc),
    .output_value(ADR)
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


Register_simple #(1) reg_z(
	.clk(CLK),
	.DATA(ZIn),
	.reset(RESET),
	.OUT(FlagZ)
);

shifter #(32) shift(
	.control(INSTR[6:5]),
	.shamt(INSTR[11:7]),
	.DATA(RD2),
	.OUT(RD2_S)
);

endmodule