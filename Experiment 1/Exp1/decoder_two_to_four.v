module decoder_two_to_four (
    input [1:0] inputs,
    output reg [3:0] outputs
);

always @(*) begin
    case (inputs)
        2'b00: outputs = 4'b0001;
        2'b01: outputs = 4'b0010;
        2'b10: outputs = 4'b0100;
        2'b11: outputs = 4'b1000;
    endcase
end

endmodule