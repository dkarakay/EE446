module mux_four_to_one #(parameter W = 4) (
    input [W-1:0] data_0,
    input [W-1:0] data_1,
    input [W-1:0] data_2,
    input [W-1:0] data_3,
    input [1:0] select,
    output reg [W-1:0] outputs
);

always @(*) begin
    case (select)
        2'b00: outputs = data_0;
        2'b01: outputs = data_1;
        2'b10: outputs = data_2;
        2'b11: outputs = data_3;
    endcase
end

endmodule