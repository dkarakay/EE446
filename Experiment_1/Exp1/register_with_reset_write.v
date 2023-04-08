module register_with_reset_write #(parameter W=4)(
	input CLK,
	input RESET, 
	input WE, 
	input [W-1:0] data,
	output reg [W-1:0] OUT
);

always @(posedge CLK) begin
    if (RESET == 1) OUT <= 0; 
	 else if(RESET == 0 && WE == 1) OUT <= data; 
   
end

endmodule
  