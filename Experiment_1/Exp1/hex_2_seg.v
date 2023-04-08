module hex_2_seg (
  input [3:0] hex,
  output reg [6:0] OUT
);

always @(*) begin
  case (hex)
    4'h0: OUT = 7'b1000000; // 0
    4'h1: OUT = 7'b1111001; // 1
    4'h2: OUT = 7'b0100100; // 2
    4'h3: OUT = 7'b0110000; // 3
    4'h4: OUT = 7'b0011001; // 4
    4'h5: OUT = 7'b0010010; // 5
    4'h6: OUT = 7'b0000010; // 6
    4'h7: OUT = 7'b1111000; // 7
    4'h8: OUT = 7'b0000000; // 8
    4'h9: OUT = 7'b0011000; // 9
    4'ha: OUT = 7'b0001000; // A
    4'hb: OUT = 7'b0000011; // b
    4'hc: OUT = 7'b1000110; // C
    4'hd: OUT = 7'b0100001; // d
    4'he: OUT = 7'b0000110; // E
    4'hf: OUT = 7'b0001110; // F
    default: OUT = 7'b0000000; // blank
  endcase
end

endmodule