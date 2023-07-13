module GHR (
    input wire clk,
    input wire reset,
    input wire branch_taken,
    output reg [2:0] OUT
);

always @(posedge clk) begin
    if (reset) begin
        OUT <= 3'b000;
    end else begin
        OUT <= {OUT[1:0], branch_taken};
    end
end

endmodule
