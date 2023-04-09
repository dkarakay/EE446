module register_file #(parameter W=4)(
	input CLK, RESET, WE,
   input [3:0] A1, A2, A3,
   input [W-1:0] data,
   output [W-1:0] RD1,RD2,
	output [16-1:0] dec

);
    wire [W-1:0] mux_out;
    wire [W-1:0] r0,r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15;

    // Instantiate decoder module for Write
    decoder_four_to_sixteen dec_1(A3, dec);
    
    // Instantiate register modules (16)
	 register_with_reset_write #(W) rg0(.CLK(CLK), .RESET(RESET), .WE(WE & dec[0]), .data(data), .OUT(r0));
	 register_with_reset_write #(W) rg1(.CLK(CLK), .RESET(RESET), .WE(WE & dec[1]), .data(data), .OUT(r1));
	 register_with_reset_write #(W) rg2(.CLK(CLK), .RESET(RESET), .WE(WE & dec[2]), .data(data), .OUT(r2));
	 register_with_reset_write #(W) rg3(.CLK(CLK), .RESET(RESET), .WE(WE & dec[3]), .data(data), .OUT(r3));
	 register_with_reset_write #(W) rg4(.CLK(CLK), .RESET(RESET), .WE(WE & dec[4]), .data(data), .OUT(r4));
	 register_with_reset_write #(W) rg5(.CLK(CLK), .RESET(RESET), .WE(WE & dec[5]), .data(data), .OUT(r5));
	 register_with_reset_write #(W) rg6(.CLK(CLK), .RESET(RESET), .WE(WE & dec[6]), .data(data), .OUT(r6));
	 register_with_reset_write #(W) rg7(.CLK(CLK), .RESET(RESET), .WE(WE & dec[7]), .data(data), .OUT(r7));
	 register_with_reset_write #(W) rg8(.CLK(CLK), .RESET(RESET), .WE(WE & dec[8]), .data(data), .OUT(r8));
	 register_with_reset_write #(W) rg9(.CLK(CLK), .RESET(RESET), .WE(WE & dec[9]), .data(data), .OUT(r9));
	 register_with_reset_write #(W) rg10(.CLK(CLK), .RESET(RESET), .WE(WE & dec[10]), .data(data), .OUT(r10));
	 register_with_reset_write #(W) rg11(.CLK(CLK), .RESET(RESET), .WE(WE & dec[11]), .data(data), .OUT(r11));
	 register_with_reset_write #(W) rg12(.CLK(CLK), .RESET(RESET), .WE(WE & dec[12]), .data(data), .OUT(r12));
	 register_with_reset_write #(W) rg13(.CLK(CLK), .RESET(RESET), .WE(WE & dec[13]), .data(data), .OUT(r13));
	 register_with_reset_write #(W) rg14(.CLK(CLK), .RESET(RESET), .WE(WE & dec[14]), .data(data), .OUT(r14));
	 register_with_reset_write #(W) rg15(.CLK(CLK), .RESET(RESET), .WE(WE & dec[15]), .data(data), .OUT(r15));
	 
	
	 mux_sixteen_to_one #(W) mux1(
	 .d0(r0),
	 .d1(r1),
	 .d2(r2),
	 .d3(r3),
	 .d4(r4),
	 .d5(r5),
	 .d6(r6),
	 .d7(r7),
	 .d8(r8),
	 .d9(r9),
	 .d10(r10),
	 .d11(r11),
	 .d12(r12),
	 .d13(r13),
	 .d14(r14),
	 .d15(r15),
	 .select(A1),
	 .OUT(RD1));

	  mux_sixteen_to_one #(W) mux2(
	 .d0(r0),
	 .d1(r1),
	 .d2(r2),
	 .d3(r3),
	 .d4(r4),
	 .d5(r5),
	 .d6(r6),
	 .d7(r7),
	 .d8(r8),
	 .d9(r9),
	 .d10(r10),
	 .d11(r11),
	 .d12(r12),
	 .d13(r13),
	 .d14(r14),
	 .d15(r15),
	 .select(A2),
	 .OUT(RD2));

 

endmodule
