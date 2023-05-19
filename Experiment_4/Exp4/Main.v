module Main(
	input CLK,
	input RESET,
	output [31:0] OUT,
	output FlagZ
);

wire [31:0] INSTR, InstructionF;
wire [31:0] ALUOutM,ALUOutW;
wire [31:0] PCF,PCPlus4F,PCPrime;
wire [3:0] RA1D, RA2D;
wire [31:0] RD1, RD2, RD1_OUT, RD2_OUT, RD2_S;
wire [31:0] ALUResultE, ExtImmE, ExtImmD;
wire [3:0] WA3E, WA3M, WA3W;
wire [31:0] SrcBE, SrcBEIn, SrcAE, ReadDataM, ReadDataW, WriteDataM;

wire CONDEX;
wire [2:0] CYCLE;

wire PCSrcD,PCSrcE,PCSrcM,PCSrcW;
wire RegWriteD,RegWriteE,RegWriteM,RegWriteW;
wire MemWriteD,MemWriteE,MemWriteM;
wire MemtoRegD,MemtoRegE,MemtoRegM,MemtoRegW;
wire [3:0] ALUControlD,ALUControlE;
wire ALUSrcD,ALUSrcE;
wire [1:0] RegSrcD,ImmSrcD;
wire [3:0] CondE;

Controller controller (
	.CLK(CLK),
	.OP(INSTR[27:26]),
	.COND(INSTR[31:28]),
	.FUNCT(INSTR[25:20]),
	.RD(INSTR[15:12]),
	.FlagZ(FlagZ),
	.RESET(RESET),
	.PCSrcD(PCSrcD),
	.PCSrcE(PCSrcE),
	.PCSrcM(PCSrcM),
	.PCSrcW(PCSrcW),
	.RegWriteD(RegWriteD),
	.RegWriteE(RegWriteE),
	.RegWriteM(RegWriteM),
	.RegWriteW(RegWriteW),
	.MemWriteD(MemWriteD),
	.MemWriteE(MemWriteE),
	.MemWriteM(MemWriteM),
	.MemtoRegD(MemtoRegD),
	.MemtoRegE(MemtoRegE),
	.MemtoRegM(MemtoRegM),
	.MemtoRegW(MemtoRegW),
	.ALUControlD(ALUControlD),
	.ALUControlE(ALUControlE),
	.ALUSrcD(ALUSrcD),
	.ALUSrcE(ALUSrcE),
	.RegSrcD(RegSrcD),
	.ImmSrcD(ImmSrcD),
	.CondE(CondE)
);


Datapath dp (
	.CLK(CLK),
	.RESET(RESET),
	.RegWriteW(RegWriteW),
	.MemWriteM(MemWriteM),
	.MemtoRegW(MemtoRegW),
	.RegSrcD(RegSrcD),
	.ImmSrcD(ImmSrcD),
	.PCSrcW(PCSrcW),
	.ALUSrcE(ALUSrcE),
	.ALUControlE(ALUControlE),
	.INSTR(INSTR),
	.InstructionF(InstructionF),
	.ALUOutM(ALUOutM),
	.ALUOutW(ALUOutW),
	.PCPrime(PCPrime),
	.PCF(PCF),
	.PCPlus4F(PCPlus4F),
	.OUT(OUT),
	.RA1D(RA1D),
	.RA2D(RA2D),
	.RD1(RD1),
	.RD2(RD2),
	.RD1_OUT(RD1_OUT),
	.RD2_OUT(RD2_OUT),
	.RD2_S(RD2_S),
	.ALUResultE(ALUResultE),
	.WA3E(WA3E),
	.WA3M(WA3M),
	.WA3W(WA3W),
	.ExtImmD(ExtImmD),
	.ExtImmE(ExtImmE),
	.SrcBE(SrcBE),
	.ReadDataM(ReadDataM),
	.ReadDataW(ReadDataW),
	.WriteDataM(WriteDataM),
	.FlagZ(FlagZ)
);



endmodule