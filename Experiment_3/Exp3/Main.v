module Main(
	input CLK,
	input RESET,
	output [31:0] OUT,
	output FlagZ
);

wire [31:0] INSTR,PC, RD1, RD2, ALUResult,ALUOut, WD3;
wire RegWrite, MemWrite, ALUSrcA, PCWrite, AdSrc, Sel14,IRWrite;
wire [3:0] ALUControl, RA1, RA2, RA3;
wire [1:0] RegSrc, ImmSrc, ALUSrcB, ResultSrc;
wire CONDEX;
wire [2:0] CYCLE;

Controller controller (
	.CLK(CLK),
	.OP(INSTR[27:26]),
	.COND(INSTR[31:28]),
	.FUNCT(INSTR[25:20]),
	.RD(INSTR[15:12]),
	.FlagZ(FlagZ),
	.PCWrite(PCWrite),
	.AdSrc(AdSrc),
	.MemWrite(MemWrite),
	.IRWrite(IRWrite),
	.ALUControl(ALUControl),
	.ALUSrcA(ALUSrcA),
	.ALUSrcB(ALUSrcB),
	.ImmSrc(ImmSrc),
	.RegWrite(RegWrite),
	.RegSrc(RegSrc),
	.ResultSrc(ResultSrc),
	.Sel14(Sel14),
	.CONDEX(CONDEX),
	.CYCLE(CYCLE),
	.RESET(RESET)
);

Datapath datapath (
	.CLK(CLK),
	.RESET(RESET),
	.INSTR(INSTR),
	.CYCLE(CYCLE),
	.PCWrite(PCWrite),
	.AdSrc(AdSrc),
	.MemWrite(MemWrite),
	.IRWrite(IRWrite),
	.ALUControl(ALUControl),
	.ALUSrcA(ALUSrcA),
	.ALUSrcB(ALUSrcB),
	.ImmSrc(ImmSrc),
	.RegWrite(RegWrite),
	.RegSrc(RegSrc),
	.ResultSrc(ResultSrc),
	.Sel14(Sel14),
	.OUT(OUT),
	.FlagZ(FlagZ),
	.PC(PC),
	.RD1(RD1),
	.RD2(RD2),
	.RA1(RA1),
	.RA2(RA2),
	.RA3(RA3),
	.ALUResult(ALUResult),
	.ALUOut(ALUOut),
	.WD3(WD3)
);

endmodule