module PHT (
    input wire clk,
    input wire reset,
    input wire [2:0] ghr,
    input wire branch_taken,
    output reg OUT,
    output reg [7:0] pht
);


always @(posedge clk) begin
    if (reset) begin
        pht = 8'b00000000;
    end else begin
        pht[ghr] = branch_taken;
    end
end

always @(*) begin
    if (reset) begin
        OUT = 1'b0;
    end else begin
        OUT = pht[ghr];
    end
end

endmodule
 