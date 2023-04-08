module alu #(parameter W = 4) (
    input c_in,
	 input [3:0] ctrl,
	 input [W-1:0] A,
    input [W-1:0] B,
    output reg CO,
    output reg OVF,
    output reg Z,
    output reg N,
	 output [W-1:0] result
);

reg [W:0] p_result;

always @(*) begin


    case (ctrl)
        4'b0000: p_result = A & B; //A and B
        4'b0001: p_result = A ^ B; //A
        4'b0010: p_result = A - B;
        4'b0011: p_result = B - A;
        4'b0100: p_result = A + B;
        4'b0101: p_result = A + B + c_in;
        4'b0110: p_result = A - B + c_in - 1;
        4'b0111: p_result = B - A + c_in - 1;
        4'b1100: p_result = A | B;
        4'b1101: p_result = B;
        4'b1110: p_result = A & ~B;
        4'b1111: p_result = ~B;
    endcase
	 
	
	 
	 if(ctrl[3:2] == 1 || ctrl == 0 || ctrl == 1)begin
		CO = 0;
		OVF = 0;
	 end
	 
	 
	 if(ctrl == 2 || ctrl == 3 || ctrl == 4 || ctrl == 5 || ctrl == 6 || ctrl == 7)begin
		if(p_result[W] == 1) CO = 1;
		else CO = 0;
		
	   OVF = (p_result[W-1] != A[W-1] && p_result[W-1] != B[W-1]) ? 1 : 0;
	 end
 
	 Z = (p_result == 0) ? 1 : 0;
	 N = (p_result[W-1] == 1) ? 1 : 0;
	 

end

assign result = p_result[W-1:0];
/*
always @(posedge clk) begin
    check_carry <= {c_in, result[W], result};
end*/

endmodule