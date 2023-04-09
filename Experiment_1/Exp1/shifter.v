module shifter #(parameter W = 4) (
	input wire signed [W-1:0] data,
	input [4:0] shamt,
   input [1:0] CTRL,
   output reg signed [W-1:0] OUT
);

integer i;
always @(*) begin
   case(CTRL)
        2'b00: OUT = data << shamt;
        2'b01: OUT = data >> shamt;
		  2'b10: OUT = data >>>	shamt;
        2'b11: begin
		  OUT = data;
		   for (i = 0; i < shamt; i = i + 1) begin
			OUT = {OUT[0], OUT[W-1:1]};
			end
		  end
    endcase
end

endmodule