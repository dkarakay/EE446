module Controller(
    input [1:0] OP,
    input [3:0] COND,
    input [5:0] FUNCT,
    input [3:0] RD,
    output reg PCSrc,
    output reg MemtoReg,
    output reg MemWrite,
    output reg [2:0] ALUControl,
    output reg ALUSrc,
    output reg [1:0]ImmSrc,
    output reg RegWrite,
	 output reg [1:0]RegSrc
); 

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
			RegWrite = 1;
			
			case(FUNCT)
			
				// ADD 0100
				6'b001000: begin
					ALUControl = 4'b0100;
				end
				
				// SUB b0010
				6'b00100: begin
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
				
				//
			
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
					RegWrite = 1;
					RegSrc = 0;

				end
				
				// STR
				6'b000000: begin
					RegSrc = 2;
					MemtoReg = 0;
					MemWrite = 1;
					ALUControl = 4'b0100;
					ALUSrc = 1;
					ImmSrc = 1;
					RegWrite = 0;
				end
				
			
			endcase
			
		end
		
		// Branch
		/*2'b10:begin
			PCSrc = 1;
			
			case(FUNCT)
			
				// LDR
				6'b000001: begin
					MemtoReg = 1;
					MemWrite = 0;
					ALUControl = 4'b0100;
					ALUSrc = 1;
					ImmSrc = 1;
					RegWrite = 1;
					RegSrc = 0;

				end
				
				// STR
				6'b000000: begin
					MemtoReg = 0;
					MemWrite = 1;
					ALUControl = 4'b0100;
					ALUSrc = 1;
					ImmSrc = 1;
					RegWrite = 0;
					RegSrc = 2;
				end
				
			
			endcase
			
		end*/
			
	endcase
end

endmodule