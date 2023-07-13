module Main(
	input CLK,
	input RESET,
	output [31:0] OUT,
	output FlagZ
);

wire [31:0] INSTR, InstructionF;
wire [31:0] ALUOutM,ALUOutW;
wire [31:0] PCF,PCPlus4F,PCPrime, PCD, PCE, PCM, PCW;
wire [3:0] RA1D, RA2D, RA1E, RA2E;
wire [31:0] RD1, RD2, RD1_OUT, RD2_OUT, RD2_S,ShifterInput;
wire [31:0] ALUResultE, ExtImmE, ExtImmD, WD3;
wire [3:0] WA3D, WA3E, WA3M, WA3W;
wire [31:0] SrcBE, SrcBEIn, ReadDataM, ReadDataW, WriteDataM;

wire CONDEX, Sel14, Sel14E, Sel14M, Sel14W, FlagWriteE, FlagWriteD;
wire [2:0] CYCLE, Match, GHROut;

wire PCSrcD,PCSrcE,PCSrcM,PCSrcW;
wire RegWriteD,RegWriteE,RegWriteM,RegWriteW;
wire MemWriteD,MemWriteE,MemWriteM;
wire MemtoRegD,MemtoRegE,MemtoRegM,MemtoRegW;
wire [3:0] ALUControlD,ALUControlE;
wire ALUSrcD,ALUSrcE;
wire [1:0] RegSrcD,ImmSrcD, ShifterControl;
wire [3:0] CondE;

wire BranchTakenE, BranchD, BranchE, LDRstall, PCWrPendingF;
wire [1:0] ForwardAE, ForwardBE;
wire [31:0] PCX, SrcAE, fBE_out;

wire [4:0] shamt;
wire [7:0] PHT;
wire [31:0] BTB_PC1, BTB_PC2, BTB_PC3;
wire [31:0] BTB_BTA1, BTB_BTA2, BTB_BTA3;

wire [31:0] BTA;
wire [1:0] LRU;
wire FlushE, FlushD, StallD, StallF, Hit;
wire PredictionF,PredictionD, PredictionE;

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
	.CondE(CondE),
	.Sel14(Sel14),
	.FlagWriteD(FlagWriteD),
	.BranchD(BranchD),
	.BranchE(BranchE),
	.BranchTakenE(BranchTakenE),
	.ForwardAE(ForwardAE), 
	.ForwardBE(ForwardBE),
	.WA3M(WA3M),
	.WA3W(WA3W),
	.RA1E(RA1E),
	.RA2E(RA2E),
	.WA3E(WA3E), 
	.RA1D(RA1D), 
	.RA2D(RA2D),
	.LDRstall(LDRstall),
	.PCWrPendingF(PCWrPendingF),
	.FlushE(FlushE),
	.FlushD(FlushD),
	.StallD(StallD),
	.StallF(StallF),
	.FlagWriteE(FlagWriteE)
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
	.PCD(PCD),
	.PCE(PCE),
	.PCM(PCM),
	.PCW(PCW),
	.OUT(OUT),
	.WD3(WD3),
	.RA1D(RA1D),
	.RA2D(RA2D),
	.RD1(RD1),
	.RD2(RD2),
	.RD1_OUT(RD1_OUT),
	.RD2_OUT(RD2_OUT),
	.RD2_S(RD2_S),
	.ALUResultE(ALUResultE),
	.WA3D(WA3D),
	.WA3E(WA3E),
	.WA3M(WA3M),
	.WA3W(WA3W),
	.ExtImmD(ExtImmD),
	.ExtImmE(ExtImmE),
	.SrcBE(SrcBE),
	.ReadDataM(ReadDataM),
	.ReadDataW(ReadDataW),
	.WriteDataM(WriteDataM),
	.Sel14(Sel14),
	.Sel14E(Sel14E),
	.Sel14M(Sel14M),
	.Sel14W(Sel14W),
	.FlagZ(FlagZ),
	.BranchTakenE(BranchTakenE),
	.ForwardAE(ForwardAE), 
	.ForwardBE(ForwardBE),
	.PCX(PCX),
	.SrcAE(SrcAE),
	.fBE_out(fBE_out),
	.RA1E(RA1E),
	.RA2E(RA2E),
    .FlushE(FlushE),
	.FlushD(FlushD),
	.StallD(StallD),
	.StallF(StallF),
	.FlagWriteE(FlagWriteE),
	.ShifterControl(ShifterControl),
	.shamt(shamt),
	.ShifterInput(ShifterInput),
	.BranchD(BranchD),
	.BranchE(BranchE),
	.BTA(BTA),
	.LRU(LRU),
	.PredictionD(PredictionD),
	.PredictionE(PredictionE),
	.PredictionF(PredictionF),
	.GHROut(GHROut),
	.BTB_PC1(BTB_PC1),
	.BTB_PC2(BTB_PC2),
	.BTB_PC3(BTB_PC3),
	.BTB_BTA1(BTB_BTA1),
	.BTB_BTA2(BTB_BTA2),
	.BTB_BTA3(BTB_BTA3),
	.Hit(Hit),
	.Match(Match),
	.PHT(PHT)
);



endmodule