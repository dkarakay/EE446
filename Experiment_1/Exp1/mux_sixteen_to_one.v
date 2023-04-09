module mux_sixteen_to_one #(parameter W = 4) (
    input [W-1:0] d0,
    input [W-1:0] d1,
    input [W-1:0] d2,
    input [W-1:0] d3,
    input [W-1:0] d4,
    input [W-1:0] d5,
    input [W-1:0] d6,
    input [W-1:0] d7,
    input [W-1:0] d8,
    input [W-1:0] d9,
    input [W-1:0] d10,
    input [W-1:0] d11,
    input [W-1:0] d12,
    input [W-1:0] d13,
    input [W-1:0] d14,
    input [W-1:0] d15,
	 input [3:0] select,
    output reg [W-1:0] OUT
);

always @(*) begin
    case (select)
        4'b0000: OUT = d0;
        4'b0001: OUT = d1;
        4'b0010: OUT = d2;
        4'b0011: OUT = d3;
        4'b0100: OUT = d4;
        4'b0101: OUT = d5;
        4'b0110: OUT = d6;
        4'b0111: OUT = d7;
        4'b1000: OUT = d8;
        4'b1001: OUT = d9;
        4'b1010: OUT = d10;
        4'b1011: OUT = d11;
        4'b1100: OUT = d12;
        4'b1101: OUT = d13;
        4'b1110: OUT = d14;
        4'b1111: OUT = d15;
    endcase
end

endmodule