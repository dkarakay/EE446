module Extender(
input [11:0] A,
input select,
output [31:0] Q

);

assign Q = select ? {20'b0,A} : {24'b0,A[7:0]};

endmodule
