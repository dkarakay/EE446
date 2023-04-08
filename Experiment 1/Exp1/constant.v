module constant #(parameter W=4, parameter VALUE=1) (
    output reg [W-1:0] data
);

always @(*) begin
    data = VALUE;
end

endmodule