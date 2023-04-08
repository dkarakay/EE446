module alu #(parameter W = 4) (
	 input CLK,
    input CIN,
	 input [3:0] CTRL,
	 input [W-1:0] A,
    input [W-1:0] B,
    output reg CO,
    output reg OVF,
    output reg Z,
    output reg N,
	 output [W-1:0] OUT
);

reg [W:0] result;

always @(*) begin


    case (CTRL)
        4'b0000: result = A & B; //A and B
        4'b0001: result = A ^ B; //A
        4'b0010: result = A - B;
        4'b0011: result = B - A;
        4'b0100: result = A + B;
        4'b0101: result = A + B + CIN;
        4'b0110: result = A - B + CIN - 1;
        4'b0111: result = B - A + CIN - 1;
        4'b1100: result = A | B;
        4'b1101: result = B;
        4'b1110: result = A & ~B;
        4'b1111: result = ~B;
    endcase
	 
	
	 
	 if(CTRL[3:2] == 1 || CTRL == 0 || CTRL == 1)begin
		CO = 0;
		OVF = 0;
	 end
	 
	 
	 if(CTRL == 2 || CTRL == 3 || CTRL == 4 || CTRL == 5 || CTRL == 6 || CTRL == 7)begin
		if(result[W] == 1) CO = 1;
		else CO = 0;
		
	   OVF = (result[W-1] != A[W-1] && result[W-1] != B[W-1]) ? 1 : 0;
	 end
 
	 Z = (result == 0) ? 1 : 0;
	 N = (result[W-1] == 1) ? 1 : 0;
	 

end

assign OUT = result[W-1:0];
/*
always @(posedge clk) begin
    check_carry <= {CIN, resultt[W], resultt};
end*/

endmodule