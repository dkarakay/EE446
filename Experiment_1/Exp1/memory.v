module memory #(parameter W = 4) (
  input wire CLK,
  input wire WE,
  input wire [W-1:0] INPUT,
  input wire [31:0] ADDR,
  output reg [W-1:0] OUT
);

  reg [31:0] mem [0:(1<<10)-1]; // 1MB memory
  
  always @(*) begin
    OUT = mem[ADDR];
  end
  
  always @(posedge CLK) begin
    if (WE) begin
      mem[ADDR] <= INPUT;
    end
  end
  
endmodule
