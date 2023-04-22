module Instruction_memory#(parameter BYTE_SIZE=4, parameter ADDR_WIDTH=32)(
	input [ADDR_WIDTH-1:0] ADDR,
	output [(BYTE_SIZE*8)-1:0] RD 
);

reg [7:0] mem [4095:0];

initial begin
/*mem[0]<=8'h01;
mem[1]<=8'h02;
mem[2]<=8'h03;
mem[3]<=8'h04;*/
//$readmemh("mem_data.txt", mem); // You will need this for real tests
end
genvar i;
generate
	for (i = 0; i < BYTE_SIZE; i = i + 1) begin: read_generate
		assign RD[8*i+:8] = mem[ADDR+i];
	end
endgenerate
endmodule