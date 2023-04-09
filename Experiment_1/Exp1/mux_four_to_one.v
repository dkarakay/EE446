module mux_four_to_one #(parameter W = 4) (
    input [W-1:0] d0,
    input [W-1:0] d1,
    input [W-1:0] d2,
    input [W-1:0] d3,
    input [1:0] select,
    output reg [W-1:0] OUT
);

always @(*) begin
    case (select)
        2'b00: OUT = d0;
        2'b01: OUT = d1;
        2'b10: OUT = d2;
        2'b11: OUT = d3;
    endcase
end

endmodule