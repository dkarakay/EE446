module Controller(
	 input CLK,
	 input [1:0] OP,
	 input [3:0] COND,
	 input [5:0] FUNCT,
	 input [3:0] RD,
	 input FlagZ,
	 input RESET,
	 output reg PCWrite,
	 output reg AdSrc,
	 output reg MemWrite,
	 output reg IRWrite,
	 output reg [1:0]ResultSrc,
	 output reg [3:0] ALUControl,
	 output reg ALUSrcA,
	 output reg [1:0]ALUSrcB,
	 output reg [1:0]ImmSrc,
	 output reg RegWrite,
	 output reg [1:0]RegSrc,
	 output reg Sel14,
	 output reg CONDEX,
	 output reg[2:0] CYCLE
); 

//reg [2:0] CYCLE = 0;

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

	if(RESET) CYCLE <=0;
	else if(CYCLE == 4) CYCLE <= 0;
	else CYCLE <= CYCLE +1;	
end


always @(*) begin
	
	//case(CYCLE)
	
		// FETCH
		if(CYCLE == 0) begin
			PCWrite = 1;
			AdSrc = 0;
			MemWrite = 0;
			IRWrite = 1;
			ResultSrc = 2;
			ALUControl = 4;
			ALUSrcA = 1;
			ALUSrcB = 2;
			ImmSrc = 0;
			RegWrite = 0;
			RegSrc = 0;
			Sel14 = 0;
			
		
			// If branch
			if(OP == 2) RegSrc = 1;
		end
		
		// DECODE
		if(CYCLE == 1) begin
			PCWrite = 0;
			AdSrc = 0;
			MemWrite = 0;
			IRWrite = 0;
			ResultSrc = 2;
			ALUControl = 4;
			ALUSrcA = 1;
			ALUSrcB = 2;
			ImmSrc = 0;
			RegWrite = 0;
			RegSrc = 0;
			Sel14 = 0;
			
			// If branch
			if(OP == 2) RegSrc = 1;
			
		end

		// EXECUTE CYCLE 3
		if(CYCLE == 2) begin
			
			case(OP)
				// Data Processing
				2'b00: begin
					PCWrite = 0;
					AdSrc = 0;
					MemWrite = 0;
					IRWrite = 0;
					ResultSrc = 1;
					ALUSrcA = 0;
					ALUSrcB = 0;
					ImmSrc = 0;
					RegWrite = 0;
					RegSrc = 0;
					Sel14 = 0;

					case(FUNCT)

						// ADD 0100
						6'b001000: begin
							ALUControl = 4'b0100;
						end

						// SUB b0010
						6'b000100: begin
							ALUControl = 4'b0010;
						end

						// AND b0000
						6'b00000: begin
							ALUControl = 4'b0000;
						end

						// ORR b1100
						6'b011000: begin
							ALUControl = 4'b1100;
						end

						// MOV b1101
						6'b011010: begin
							ALUControl = 4'b1101;
						end

						// CMP b1010
						6'b010100: begin
							ALUControl = 4'b0010;
							RegWrite = 0;
						end

					endcase
					
				end

				// Memory
				2'b01:begin
					PCWrite = 0;
					AdSrc = 0;
					MemWrite = 0;
					IRWrite = 0;
					ResultSrc = 0;
					ALUControl = 4;
					ALUSrcA = 0;
					ALUSrcB = 1;
					ImmSrc = 1;
					RegWrite = 0;

					// LDR
				 	if (FUNCT == 6'b000001) RegSrc = 0;
					
					// STR
					else RegSrc = 2;

					Sel14 = 0;
				end

				// Branch
				2'b10:begin

					AdSrc = 0;
					IRWrite = 0;
					MemWrite = 0;
					ResultSrc = 2;
					ALUSrcA = 0;

					case(FUNCT[5:4])
						// BX LR
						2'b00: begin
							PCWrite = 1;
							ALUControl = 13;
							ALUSrcB = 0;
							ImmSrc = 0;
							RegWrite = 0;
							RegSrc = 0;
							Sel14 = 0;
						end

						// BEQ + B
						2'b10: begin
							PCWrite = CONDEX ? 1 : 0;
							ALUControl = 4;
							ALUSrcB = 1;
							ImmSrc = 2;
							RegWrite = 0;
							RegSrc = 1;
							Sel14 = 0;

						end

						// BL
						2'b11: begin
							PCWrite = 1;
							ALUControl = 4;
							ALUSrcB = 1;
							ImmSrc = 2;
							RegWrite = 1;
							RegSrc = 1;
							Sel14 = 1;
						end

					endcase
				end

				// Otherwise
			 	2'b11:begin
					PCWrite = 0;
					AdSrc = 0;
					MemWrite = 0;
					IRWrite = 0;
					ResultSrc = 0;
					ALUControl = 0;
					ALUSrcA = 0;
					ALUSrcB = 0;
					ImmSrc = 0;
					RegWrite = 0;
					RegSrc = 0;
					Sel14 = 0;
			 	end

			endcase
		
		end

		// MEMORY CYCLE 4
		if(CYCLE == 3) begin
			case(OP)
				// Data Processing
				2'b00: begin
					PCWrite = 0;
					AdSrc = 0;
					MemWrite = 0;
					IRWrite = 0;
					ResultSrc = 0;
					ALUControl = 0;
					ALUSrcA = 0;
					ALUSrcB = 0;
					ImmSrc = 0;
					RegWrite = 1;
					RegSrc = 0;
					Sel14 = 0;
				end
				
				// Memory
				2'b01: begin
					PCWrite = 0;
					AdSrc = 1;
					IRWrite = 0;
					ResultSrc = 0;
					ALUControl = 4;
					ALUSrcA = 0;
					ALUSrcB = 1;
					ImmSrc = 1;
					RegWrite = 0;
					RegSrc = 0;
					Sel14 = 0;

					// LDR
					if (FUNCT == 6'b000001) begin
						MemWrite = 0;
					end

					// STR
					else if (FUNCT == 6'b000000) begin
						MemWrite = 1;
					end
				end

				// Branch
				2'b10: begin
					PCWrite = 0;
					AdSrc = 0;
					MemWrite = 0;
					IRWrite = 0;
					ResultSrc = 0;
					ALUControl = 0;
					ALUSrcA = 0;
					ALUSrcB = 0;
					ImmSrc = 0;
					RegWrite = 0;
					RegSrc = 0;
					Sel14 = 0;
				end

				2'b11:begin
					PCWrite = 0;
					AdSrc = 0;
					MemWrite = 0;
					IRWrite = 0;
					ResultSrc = 0;
					ALUControl = 0;
					ALUSrcA = 0;
					ALUSrcB = 0;
					ImmSrc = 0;
					RegWrite = 0;
					RegSrc = 0;
					Sel14 = 0;
			 	end

			endcase

		end

		// CYCLE 5
		if(CYCLE == 4) begin
			// LDR
			if(OP == 2'b01 && FUNCT == 6'b000001) begin
				PCWrite = 0;
				AdSrc = 1;
				MemWrite = 0;
				IRWrite = 0;
				ResultSrc = 1;
				ALUControl = 4;
				ALUSrcA = 0;
				ALUSrcB = 1;
				ImmSrc = 1;
				RegWrite = 1;
				RegSrc = 0;
				Sel14 = 0;
			end
			
			else begin
				PCWrite = 0;
				AdSrc = 0;
				MemWrite = 0;
				IRWrite = 0;
				ResultSrc = 0;
				ALUControl = 0;
				ALUSrcA = 0;
				ALUSrcB = 0;
				ImmSrc = 0;
				RegWrite = 0;
				RegSrc = 0;
				Sel14 = 0;
			end
			
		end

		

end


endmodule