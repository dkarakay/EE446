module register_file #(parameter W=4)(
	input CLK, RESET, WE,
   input [3:0] A1, A2, A3,
   input [W-1:0] data,
   output [W-1:0] OUT1,OUT2,
	output [N-1:0] dec1,dec2,dec3,
   output [W-1:0] rg11

);
    parameter N = 16;
    wire [W-1:0] mux_out;
    wire [W-1:0] reg_out1, reg_out2;
    // Instantiate decoder module
    decoder_four_to_sixteen dec_1(A1, dec1);
    decoder_four_to_sixteen dec_2(A2, dec2);
    decoder_four_to_sixteen dec_3(A3, dec3);
    
    // Instantiate register modules

	 register_with_reset_write #(W) rg1(.CLK(CLK), .RESET(RESET), .WE(WE), .data(data), .OUT(OUT1));
	 
    /*genvar i;
    generate
        for (i = 0; i < N; i = i + 1) begin : gen_regs
            register_with_reset_write #(W) rg(CLK, RESET, dec_1[i], data, reg_out1);
        end
    endgenerate
*/

endmodule
