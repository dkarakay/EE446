module datapath(
	input CLK,
	input ENABLE,
	input [1:0] OP,
    input [7:0] INP,
	output[7:0] REG_OUT,
	output reg[2:0] CYCLE,
	input RESET
	);
	
	reg WE;
	reg [7:0] mux1A,mux1B;
	reg [3:0] alu_ctrl;
	reg [1:0] shifter_ctrl;
	reg sel0,sel1,sel2;
	reg [4:0] shamt;
	wire [7:0] mux0_out, mux1_out, mux2_out;
	wire [7:0] alu_out,shifter_out;
	
	

	
	always @(posedge CLK)begin
		if(ENABLE)begin
			if(CYCLE == 5) CYCLE <=1;
			else CYCLE <= CYCLE +1;	
		end
	end
	
	always @(*)begin
		if(ENABLE)begin
			
			case(OP)
			
			//2s Complement
			0: begin
				// Cycles
				case(CYCLE)
				
				1:begin
					sel0 = 1;
					alu_ctrl = 4'b1111;
					WE = 1;
					end
					
				2:begin
					sel0 = 0;
					sel1 = 1;
					sel2 = 1;
					shifter_ctrl = 0;
					shamt = 0;
					alu_ctrl = 4'b0100;
					WE = 1;
					end
					
				default:	WE = 0;
				
				endcase
			end
			
			// Multiply by 10
			1:begin
				// Cycles
				case(CYCLE)
				
				1:begin
					sel0 = 1;
					alu_ctrl = 4'b1101;
					WE = 1;
					end
					
				2:begin
					sel0 = 0;
					sel1 = 0;
					shifter_ctrl = 0;
					shamt = 3;
					alu_ctrl = 4'b0100;
					WE = 1;
					end
					
				3:begin
					sel0 = 1;
					sel1 = 0;
					alu_ctrl = 4'b0100;
					WE = 1;
					end
				default:	WE = 0;
				
				endcase
			
			end
			
			// Duplicate the first 4 bit
			2:begin
				// Cycles
				case(CYCLE)
				
				1:begin
					sel0 = 1;
					alu_ctrl = 4'b1101;
					WE = 1;
					end
					
				2:begin
					sel0 = 0;
					sel1 = 0;
					shifter_ctrl = 1;
					shamt = 4;
					alu_ctrl = 4'b1101;
					WE = 1;
					end
					
				3:begin
					sel0 = 0;
					sel1 = 0;
					shamt = 4;
					shifter_ctrl = 0;
					alu_ctrl = 4'b1100;
					WE = 1;
					end
				default:	WE = 0;
				
				endcase
			
			end
			
			endcase
			
		end
	end

		// 8-bit register with reset and write enable
	register_with_reset_write #(8) reg8 (
		  .CLK(CLK),
		  .RESET(RESET),
		  .WE(WE),
		  .data(alu_out),
		  .OUT(REG_OUT)
	);

	// 8-bit multiplexer 0
	mux_two_to_one #(8) mux0(
        .select(sel0),
        .d0(shifter_out),
        .d1(INP),
        .OUT(mux0_out)
	);

	// 8-bit multiplexer 1
	mux_two_to_one #(8) mux1(
        .select(sel1),
        .d0(REG_OUT),
        .d1(mux2_out),
        .OUT(mux1_out)
	);
	
	// 8-bit multiplexer 2
	mux_two_to_one #(8) mux2(
        .select(sel2),
        .d0(0),
        .d1(1),
        .OUT(mux2_out)
	);

	// 8-bit ALU
	alu #(8) alu(
        .CTRL(alu_ctrl),
        .A(mux1_out),
        .B(mux0_out),
        .OUT(alu_out)
	);

   // 8-bit shifter
   shifter #(8) shifter(
		  .data(REG_OUT),
		  .CTRL(shifter_ctrl),
		  .shamt(shamt),
        .OUT(shifter_out)
   );
endmodule
