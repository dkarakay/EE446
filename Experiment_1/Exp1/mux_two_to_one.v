module mux_two_to_one #(parameter W = 4) (
    input [W-1:0] d0,
    input [W-1:0] d1,
    input select,
    output reg [W-1:0] OUT
);

always @(*) begin
    if (select == 1'b0) begin
        OUT = d0;
    end else begin
        OUT = d1;
    end
end

endmodule