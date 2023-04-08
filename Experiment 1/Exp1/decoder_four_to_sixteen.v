module decoder_four_to_sixteen (
    input [3:0] inputs,
    output [15:0] outputs
);

assign outputs = (1 << inputs);

endmodule