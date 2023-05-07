module Controller(
	 input CLK,
    input [1:0] OP,
    input [3:0] COND,
    input [5:0] FUNCT,
    input [3:0] RD,
	 input FlagZ,
    output reg PCSrc,
    output reg MemtoReg,
    output reg MemWrite,
    output reg [3:0] ALUControl,
    output reg ALUSrc,
    output reg [1:0]ImmSrc,
    output reg RegWrite,
	 output reg [1:0]RegSrc,
	 output reg CONDEX
); 


always @(CLK) begin 
	
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
	endcase
end

always @(*) begin
	
	case(OP)
	
		// Data Processing
		2'b00:begin
			PCSrc = 0;
			MemtoReg = 0;
			MemWrite = 0;
			ALUSrc = 0;
			ImmSrc = 0;
			RegSrc = 0;
			RegWrite = CONDEX ? 1 : 0;
			
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
			PCSrc = 0;
			
			case(FUNCT)
			
				// LDR
				6'b000001: begin
					MemtoReg = 1;
					MemWrite = 0;
					ALUControl = 4'b0100;
					ALUSrc = 1;
					ImmSrc = 1;
					RegWrite = CONDEX ? 1 : 0;
					RegSrc = 0;

				end
				
				// STR
				6'b000000: begin
					RegSrc = 2;
					MemtoReg = 0;
					MemWrite = CONDEX ? 1 : 0;
					ALUControl = 4'b0100;
					ALUSrc = 1;
					ImmSrc = 1;
					RegWrite = 0;
				end
				
			
			endcase
			
		end
		
		// Branch
		2'b10:begin
			PCSrc = CONDEX ? 1 : 0;
			MemtoReg = 0;
			MemWrite = 0;
			ALUControl = 4'b1101;
			ImmSrc = 2'b10;
			RegWrite = 0;

			case(FUNCT[5:4])
			
				// B + BEQ
				2'b10: begin
					ALUSrc = 1;
					RegSrc = 0;
					
					
				end
				
				// BL
				2'b11: begin
					ALUSrc = 1;
					RegSrc = 1;

				end
				
			endcase
			
		end
			
	endcase
end

endmodule