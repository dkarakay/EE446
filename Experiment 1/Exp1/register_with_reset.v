module register_with_reset #(parameter W=4)(
	input clk,
	input reset, 
	input [W-1:0] data_input,
	output reg [W-1:0] data_output
);

always @(posedge clk) begin
    if (reset == 1) data_output <= 0; 
    else data_output <= data_input; 
   
end
endmodule