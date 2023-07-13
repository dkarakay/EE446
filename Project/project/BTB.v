module BTB (
  input wire clk,        // Clock signal
  input wire reset,      // Reset signal
  input wire [31:0] PC,PCE,  // Current program counter
  input wire [31:0] branch_target,
  input wire branch_taken, BranchE,
  output reg hit,       // Hit flag
  output reg [31:0] BTA, // Branch target address
  output reg [1:0] lru,    // Least recently used counter
  output reg [2:0] match,
  output reg [31:0] btb_pc1, btb_pc2, btb_pc3,
  output reg [31:0] btb_bta1, btb_bta2, btb_bta3
);

// Comparator circuit
//assign match = {(btb_pc[0] == PC),(btb_pc[1] == PC),(btb_pc[2] == PC)};

// Find hit flag
//assign hit = |match;

// Find BTA
integer i;
always @(*) begin
  if(PC != 0)begin
    match = {(btb_pc3 == PC),(btb_pc2 == PC),(btb_pc1 == PC)};
  end else begin
    match = 0;
  end
  
  hit = match;

  if (match[0] == 1) begin
    BTA = btb_bta1;
  end else if (match[1] == 1) begin
    BTA = btb_bta2;
  end else if (match[2] == 1) begin
    BTA = btb_bta3;
  end else begin
    BTA = 0;
  end
end
  
always @(posedge clk) begin
  if (reset) begin
    btb_pc1 = 0;
    btb_pc2 = 0;
    btb_pc3 = 0;
    btb_bta1 = 0;
    btb_bta2 = 0;
    btb_bta3 = 0;
    lru = 0;
  end
  else if (BranchE && branch_taken) begin
    if (hit) begin
      // Update the BTA of the matching entry
      if(i == 0)begin
        btb_bta1 = branch_target;
      end
      if(i == 1)begin
        btb_bta2 = branch_target;
      end
      if(i == 2)begin
        btb_bta3 = branch_target;
      end
    end else if (BranchE) begin
      if (lru == 0) begin
        btb_pc1 = PCE;
        btb_bta1 = branch_target;
      end else if (lru == 1) begin
        btb_pc2 = PCE;
        btb_bta2 = branch_target;
      end else if (lru == 2) begin
        btb_pc3 = PCE;
        btb_bta3 = branch_target;
      end

      // Update the LRU counter
      lru = lru + 1;
      if (lru == 3) begin
        lru = 0;
      end
    end
  end
end 

endmodule
