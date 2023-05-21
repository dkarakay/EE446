module Controller(
	 input CLK,
	 input [1:0] OP,
	 input [3:0] COND,
	 input [5:0] FUNCT,
	 input [3:0] RD,
	 input FlagZ,
	 input RESET,
	 output reg PCSrcD,
	 output wire PCSrcE, PCSrcM,PCSrcW,
	 
	 output reg RegWriteD, 
	 output wire RegWriteE, RegWriteM, RegWriteW,
	 
	 output reg MemWriteD, 
	 output wire MemWriteE, MemWriteM,
	 
	 output reg FlagWriteD,
	 output wire FlagWriteE,

	 output reg MemtoRegD,
	 output wire MemtoRegE, MemtoRegM, MemtoRegW,

	 output reg [3:0] ALUControlD,
	 output wire [3:0] ALUControlE,
	 output reg ALUSrcD, 
	 output wire ALUSrcE,
	 output reg [1:0]RegSrcD,
	 output reg [1:0]ImmSrcD,
	 output wire [3:0]CondE,
	 output reg FlagZE,

	 output reg Sel14,
	 output reg CONDEX,
	 output reg[2:0] CYCLE
); 


always @(posedge CLK) begin 
	
	// Using only two LSB of CONDs
	case(COND)
		//EQ
		4'b0000: begin
			if(FlagZ ==1) CONDEX = 1;
			else CONDEX = 0;
		end
		//NE
		4'b0001: begin
			if(FlagZ ==1) CONDEX = 0;
			else CONDEX = 1;
		end
		// AL
		4'b1110: begin
			CONDEX = 1;
		end
		
		default: CONDEX = 1;
	endcase

	if(RESET) begin
		 PCSrcD=0;
		 RegWriteD=0;
		 MemWriteD=0;
		 MemtoRegD=0;
		 ALUControlD=0;
		 FlagWriteD=0;
		 ALUSrcD=0;
		 RegSrcD=0;
		 ImmSrcD=0;
		 Sel14=0;
	end	
end 
always @(*) begin

	if (COND != 4'b1111) begin
		case(OP) 
			// Data Processing
			2'b00: begin
				ALUSrcD = 0;
				ImmSrcD = 0;
				PCSrcD = 0;
				MemWriteD = 0;
				MemtoRegD = 0;
				RegSrcD = 0;
				RegWriteD = 1;			
				
				case(FUNCT)
					// ADD 0100
					6'b001000: begin
						ALUControlD = 4'b0100;
					end

					// SUB b0010
					6'b000100: begin
						ALUControlD = 4'b0010;
					end

					// AND b0000
					6'b00000: begin
						ALUControlD = 4'b0000;
					end

					// ORR b1100
					6'b011000: begin
						ALUControlD = 4'b1100;
					end

					// MOV b1101
					6'b011010: begin
						ALUControlD = 4'b1101;
					end

					// CMP b1010
					6'b010100: begin
						ALUControlD = 4'b0010;
						RegWriteD = 0;
						FlagWriteD = 1;
					end

					endcase
			end

			// Memory
			2'b01:begin

				case(FUNCT)

					// LDR
					6'b000001: begin
						ALUControlD = 4'b0100;
						ALUSrcD = 1;
						ImmSrcD = 1;
						RegSrcD = 0;
						RegWriteD = 1;
						PCSrcD = 0;
						MemWriteD = 0;
						MemtoRegD = 1;
					end

					// STR
					6'b000000: begin
						ALUControlD = 4'b0100;
						ALUSrcD = 1;
						ImmSrcD = 1;
						RegSrcD = 2;
						RegWriteD = 0;
						PCSrcD = 0;
						MemWriteD = 1;
						MemtoRegD = 0;
					end
				endcase
			end

			// Branch
			2'b10: begin
				case (FUNCT[5:4])

					// BX LR
					2'b00: begin
						PCSrcD = 1;
						RegWriteD = 0;
						MemtoRegD = 0;
						ALUSrcD = 0;
						ImmSrcD = 0;
						RegSrcD = 0;
						ALUControlD = 13;
						Sel14 = 0;
					end
					
					// B + BEQ
					2'b10: begin
						PCSrcD = 1;
						RegWriteD = 0;
						MemtoRegD = 0;
						MemWriteD = 0;
						ALUSrcD = 1;
						ImmSrcD = 2;
						RegSrcD = 1;
						ALUControlD = 4;
						Sel14 = 0;
					end

					// BL
					2'b11: begin
						PCSrcD = 1;
						RegWriteD = 1;
						MemtoRegD = 0;
						MemWriteD = 0;
						ALUSrcD = 1;
						ImmSrcD = 2;
						RegSrcD = 1;
						ALUControlD = 4;
						Sel14 = 1;
					end
				endcase
			end


		endcase
	end
	else begin
		PCSrcD = 0;
		Sel14 = 0;
		RegWriteD=0;
		MemWriteD=0;
		MemtoRegD=0;
		ALUControlD=4;
		ALUSrcD=0;
		RegSrcD=0;
		FlagWriteD=0;
	end
end




// Define register for PCSrcD to PCSrcE
Register_sync_rw #(1) PCSrcD2E(
	.clk(CLK),
	.reset(RESET),
	.DATA(PCSrcD),
	.we(1'b1),
	.OUT(PCSrcE)
);

// PCSrcE to PCSrcM
Register_sync_rw #(1) PCSrcE2M(
	.clk(CLK),
	.reset(RESET),
	.DATA(PCSrcE & CONDEX),
	.we(1'b1),
	.OUT(PCSrcM)
);

// PCSrcM to PCSrcW
Register_sync_rw #(1) PCSrcM2W(
	.clk(CLK),
	.reset(RESET),
	.DATA(PCSrcM),
	.we(1'b1),
	.OUT(PCSrcW)
);

// Define register for RegWriteD to RegWriteE
Register_sync_rw #(1) RegWriteD2E(
	.clk(CLK),
	.reset(RESET),
	.DATA(RegWriteD),
	.we(1'b1),
	.OUT(RegWriteE)
);

// RegWriteE to RegWriteM
Register_sync_rw #(1) RegWriteE2M(
	.clk(CLK),
	.reset(RESET),
	.DATA(RegWriteE & CONDEX),
	.we(1'b1),
	.OUT(RegWriteM)
);

// RegWriteM to RegWriteW
Register_sync_rw #(1) RegWriteM2W(
	.clk(CLK),
	.reset(RESET),
	.DATA(RegWriteM),
	.we(1'b1),
	.OUT(RegWriteW)
);

// MemWriteD to MemWriteE
Register_sync_rw #(1) MemWriteD2E(
	.clk(CLK),
	.reset(RESET),
	.DATA(MemWriteD),
	.we(1'b1),
	.OUT(MemWriteE)
);

// MemWriteE to MemWriteM
Register_sync_rw #(1) MemWriteE2M(
	.clk(CLK),
	.reset(RESET),
	.DATA(MemWriteE & CONDEX),
	.we(1'b1),
	.OUT(MemWriteM)
);

// MemtoRegD to MemtoRegE
Register_sync_rw #(1) MemtoRegD2E(
	.clk(CLK),
	.reset(RESET),
	.DATA(MemtoRegD),
	.we(1'b1),
	.OUT(MemtoRegE)
);

// MemtoRegE to MemtoRegM
Register_sync_rw #(1) MemtoRegE2M(
	.clk(CLK),
	.reset(RESET),
	.DATA(MemtoRegE),
	.we(1'b1),
	.OUT(MemtoRegM)
);

// MemtoRegM to MemtoRegW
Register_sync_rw #(1) MemtoRegM2W(
	.clk(CLK),
	.reset(RESET),
	.DATA(MemtoRegM),
	.we(1'b1),
	.OUT(MemtoRegW)
);

// ALUControlD to ALUControlE
Register_sync_rw #(4) ALUControlD2E(
	.clk(CLK),
	.reset(RESET),
	.DATA(ALUControlD),
	.we(1'b1),
	.OUT(ALUControlE)
);

// ALUSrcD to ALUSrcE
Register_sync_rw #(1) ALUSrcD2E(
	.clk(CLK),
	.reset(RESET),
	.DATA(ALUSrcD),
	.we(1'b1),
	.OUT(ALUSrcE)
);

// COND to CondE
Register_sync_rw #(4) COND2E(
	.clk(CLK),
	.reset(RESET),
	.DATA(COND),
	.we(1'b1),
	.OUT(CondE)
);

// FlagWriteD to FlagWriteE
Register_sync_rw #(1) FlagWriteD2E(
	.clk(CLK),
	.reset(RESET),
	.DATA(FlagWriteD),
	.we(1'b1),
	.OUT(FlagWriteE)
);


endmodule