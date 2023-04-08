module mux_two_to_one #(parameter W = 4) (
    input [W-1:0] data_0,
    input [W-1:0] data_1,
    input select,
    output reg [W-1:0] outputs
);

always @(*) begin
    if (select == 1'b0) begin
        outputs = data_0;
    end else begin
        outputs = data_1;
    end
end

endmodule