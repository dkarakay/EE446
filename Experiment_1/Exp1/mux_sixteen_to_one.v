module mux_sixteen_to_one #(parameter W = 4) (
    input [W-1:0] data_0,
    input [W-1:0] data_1,
    input [W-1:0] data_2,
    input [W-1:0] data_3,
    input [W-1:0] data_4,
    input [W-1:0] data_5,
    input [W-1:0] data_6,
    input [W-1:0] data_7,
    input [W-1:0] data_8,
    input [W-1:0] data_9,
    input [W-1:0] data_10,
    input [W-1:0] data_11,
    input [W-1:0] data_12,
    input [W-1:0] data_13,
    input [W-1:0] data_14,
    input [W-1:0] data_15,
	 input [3:0] select,
    output reg [W-1:0] outputs
);

always @(*) begin
    case (select)
        4'b0000: outputs = data_0;
        4'b0001: outputs = data_1;
        4'b0010: outputs = data_2;
        4'b0011: outputs = data_3;
        4'b0100: outputs = data_4;
        4'b0101: outputs = data_5;
        4'b0110: outputs = data_6;
        4'b0111: outputs = data_7;
        4'b1000: outputs = data_8;
        4'b1001: outputs = data_9;
        4'b1010: outputs = data_10;
        4'b1011: outputs = data_11;
        4'b1100: outputs = data_12;
        4'b1101: outputs = data_13;
        4'b1110: outputs = data_14;
        4'b1111: outputs = data_15;
    endcase
end

endmodule