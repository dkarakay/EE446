module Main(
	input CLK,
	input RESET,
	output [31:0] OUT,
	output FlagZ
);

wire [31:0] INSTR,PC, RD1, RD2, ALUResult;
wire PCSrc, MemtoReg, MemWrite, ALUSrc, RegWrite;
wire [3:0] ALUControl, RA1, RA2;
wire [1:0] ImmSrc,RegSrc;
wire CONDEX;

Controller controller (
	.CLK(CLK),
	.OP(INSTR[27:26]),
	.COND(INSTR[31:28]),
	.FUNCT(INSTR[25:20]),
	.RD(INSTR[15:12]),
	.FlagZ(FlagZ),
	.PCSrc(PCSrc),
	.MemtoReg(MemtoReg),
	.MemWrite(MemWrite),
	.ALUControl(ALUControl),
	.ALUSrc(ALUSrc),
	.ImmSrc(ImmSrc),
	.RegWrite(RegWrite),
	.RegSrc(RegSrc),
	.CONDEX(CONDEX)
	
);

Datapath datapath (
	.CLK(CLK),
	.RESET(RESET),
	.INSTR(INSTR),
	.PCSrc(PCSrc),
	.MemtoReg(MemtoReg),
	.MemWrite(MemWrite),
	.ALUControl(ALUControl),
	.ALUSrc(ALUSrc),
	.ImmSrc(ImmSrc),
	.RegWrite(RegWrite),
	.RegSrc(RegSrc),
	.OUT(OUT),
	.FlagZ(FlagZ),
	.PC(PC),
	.RD1(RD1),
	.RD2(RD2),
	.RA1(RA1),
	.RA2(RA2),
	.ALUResult(ALUResult)

);

endmodule