import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


def print_hex_dec(dut, val, name, cond=False, only_hex=False):
    if not str(val).__contains__("x") and not str(val).__contains__("z"):
        if only_hex:
            my = int(val)
            dut._log.info(f"{name}: H: {my:x}")
            return

        if cond or val != 0:
            my = int(val)
            dut._log.info(f"{name}: D: {my:d} H: {my:x} B: {val}")


## This function prints all the signals in the DUT except the ones that are zero
# @param dut: the DUT
def print_all(dut):
    print_hex_dec(dut, dut.InstructionF.value, name="InstructionF", only_hex=True)
    print_hex_dec(dut, dut.INSTR.value, name="INSTR", only_hex=True)

    print_hex_dec(dut, dut.PCPrime.value, name="PCPrime", cond=True)
    print_hex_dec(dut, dut.PCF.value, name="PCF", cond=True)

    print_hex_dec(dut, dut.BranchD.value, name="BranchD")
    print_hex_dec(dut, dut.BranchE.value, name="BranchE")

    # print_hex_dec(dut, dut.PCPlus4F.value, name="PCPlus4F")
    print_hex_dec(dut, dut.RESET.value, name="RESET")

    print_hex_dec(dut, dut.PCSrcD.value, name="PCSrcD")
    print_hex_dec(dut, dut.PCSrcE.value, name="PCSrcE")
    print_hex_dec(dut, dut.PCSrcM.value, name="PCSrcM")
    print_hex_dec(dut, dut.PCSrcW.value, name="PCSrcW")
    """

    print_hex_dec(dut, dut.Sel14.value, name="Sel14")
    print_hex_dec(dut, dut.Sel14E.value, name="Sel14E")
    print_hex_dec(dut, dut.Sel14M.value, name="Sel14M")
    print_hex_dec(dut, dut.Sel14W.value, name="Sel14W")
    """
    print_hex_dec(dut, dut.RegWriteD.value, name="RegWriteD")
    print_hex_dec(dut, dut.RegWriteE.value, name="RegWriteE")
    print_hex_dec(dut, dut.RegWriteM.value, name="RegWriteM")
    print_hex_dec(dut, dut.RegWriteW.value, name="RegWriteW")
    """
    print_hex_dec(dut, dut.MemWriteD.value, name="MemWriteD")
    print_hex_dec(dut, dut.MemWriteE.value, name="MemWriteE")
    print_hex_dec(dut, dut.MemWriteM.value, name="MemWriteM")

    print_hex_dec(dut, dut.MemtoRegD.value, name="MemtoRegD")
    print_hex_dec(dut, dut.MemtoRegE.value, name="MemtoRegE")
    print_hex_dec(dut, dut.MemtoRegM.value, name="MemtoRegM")
    print_hex_dec(dut, dut.MemtoRegW.value, name="MemtoRegW")
    
    print_hex_dec(dut, dut.ALUControlD.value, name="ALUControlD")
    """
    print_hex_dec(dut, dut.ALUControlE.value, name="ALUControlE")

    print_hex_dec(dut, dut.ALUSrcD.value, name="ALUSrcD")
    print_hex_dec(dut, dut.ALUSrcE.value, name="ALUSrcE")

    print_hex_dec(dut, dut.ShifterControl.value, name="ShifterControl")
    print_hex_dec(dut, dut.shamt.value, name="shamt")
    print_hex_dec(dut, dut.ExtImmD.value, name="ExtImmD")
    print_hex_dec(dut, dut.ShifterInput.value, name="ShifterInput")
    print_hex_dec(dut, dut.RD2_S.value, name="RD2_S")

    print_hex_dec(dut, dut.RegSrcD.value, name="RegSrcD")
    print_hex_dec(dut, dut.ImmSrcD.value, name="ImmSrcD")
    print_hex_dec(dut, dut.CondE.value, name="CondE")

    #    print_hex_dec(dut, dut.FlagZ.value, name="FlagZ")
    print_hex_dec(dut, dut.RA1D.value, name="RA1D")
    print_hex_dec(dut, dut.RA2D.value, name="RA2D")

    print_hex_dec(dut, dut.RA1E.value, name="RA1E")
    print_hex_dec(dut, dut.RA2E.value, name="RA2E")

    print_hex_dec(dut, dut.RD1.value, name="RD1")
    print_hex_dec(dut, dut.RD2.value, name="RD2")

    print_hex_dec(dut, dut.StallF.value, name="StallF")
    print_hex_dec(dut, dut.StallD.value, name="StallD")
    print_hex_dec(dut, dut.FlushD.value, name="FlushD")
    print_hex_dec(dut, dut.FlushE.value, name="FlushE")

    print_hex_dec(dut, dut.ForwardAE.value, name="ForwardAE")
    print_hex_dec(dut, dut.ForwardBE.value, name="ForwardBE")
    print_hex_dec(dut, dut.LDRstall.value, name="LDRstall")

    print_hex_dec(dut, dut.BranchTakenE.value, name="BranchTakenE")

    """
    print_hex_dec(dut, dut.RD1.value, name="RD1")
    print_hex_dec(dut, dut.RD2.value, name="RD2")
    print_hex_dec(dut, dut.RD1_OUT.value, name="RD1_OUT")
    print_hex_dec(dut, dut.RD2_OUT.value, name="RD2_OUT")
    """
    print_hex_dec(dut, dut.WA3E.value, name="WA3E")
    print_hex_dec(dut, dut.WA3M.value, name="WA3M")
    print_hex_dec(dut, dut.WA3W.value, name="WA3W")

    # print_hex_dec(dut, dut.ExtImmE.value, name="ExtImmE")
    print_hex_dec(dut, dut.SrcAE.value, name="SrcAE")
    print_hex_dec(dut, dut.SrcBE.value, name="SrcBE")

    print_hex_dec(dut, dut.ReadDataM.value, name="ReadDataM")
    print_hex_dec(dut, dut.ReadDataW.value, name="ReadDataW")
    print_hex_dec(dut, dut.WriteDataM.value, name="WriteDataM")

    print_hex_dec(dut, dut.ALUResultE.value, name="ALUResultE")
    print_hex_dec(dut, dut.MemtoRegE.value, name="MemtoRegE")
    print_hex_dec(dut, dut.ALUOutM.value, name="ALUOutM")
    print_hex_dec(dut, dut.ALUOutW.value, name="ALUOutW")

    print_hex_dec(dut, dut.OUT.value, name="OUT", cond=True)
    print("------------------")


@cocotb.test()
async def hazard_unit(dut):
    """Setup testbench and run a test."""
    # Generate the clock
    await cocotb.start(Clock(dut.CLK, 10, "us").start(start_high=False))

    # set clkedge as the rising edge of the clock
    clkedge = RisingEdge(dut.CLK)
    # wait until the clock edge
    dut.RESET.value = 1
    await clkedge
    print_all(dut)

    dut.RESET.value = 0

    # LDR R3, [R0, #4] => 9
    # 0xE4103004
    dut._log.info(f"LDR R3, [R0, #4] => 9")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE4103004
    assert dut.PCPrime.value == 4

    # LDR R2, [R0] => 6
    # 0xE4102000
    dut._log.info(f"LDR R2, [R0] => 6")
    await clkedge
    print_all(dut)

    # LDR R1, [R0, #8] => 1
    # 0xE4101008
    dut._log.info(f"LDR R1, [R0, #8] => 1")
    dut._log.info(f"NOP")
    await clkedge

    # NOP
    await clkedge
    print_all(dut)

    # NOP
    await clkedge
    assert dut.OUT.value == 9
    print_all(dut)

    # ADD R7, R2, R1 (6 + 1 = 7)
    # 0xE0827001
    dut._log.info(f"ADD R7, R2, R1")
    await clkedge
    assert dut.OUT.value == 6
    print_all(dut)

    # ADD R8, R7, R1 (7 + 1 = 8)
    # 0xE0878001
    dut._log.info(f"ADD R8, R7, R1")
    await clkedge
    assert dut.OUT.value == 1
    print_all(dut)

    print("\n R1 = 1\n R2 = 6\n R3 = 9\n")

    # NOP
    await clkedge
    print_all(dut)

    # ADD R9, R1, R8 (1 + 8 = 7)
    # 0xE0819008
    dut._log.info(f"ADD R9, R1, R8")
    await clkedge
    print_all(dut)

    # NOP
    await clkedge
    assert dut.OUT.value == 7
    print_all(dut)
    print("\n R1 = 1\n R2 = 6\n R3 = 9\n R7 = 7\n")

    # NOP
    await clkedge
    assert dut.OUT.value == 8
    print_all(dut)
    print("\n R1 = 1\n R2 = 6\n R3 = 9\n R7 = 7\n R8 = 8\n")

    # NOP
    await clkedge
    print_all(dut)

    # NOP
    await clkedge
    assert dut.OUT.value == 9
    print_all(dut)
    print("\n R1 = 1\n R2 = 6\n R3 = 9\n R7 = 7\n R8 = 8\n R9 = 9\n")

    # LDR R2, [R0] => 2
    # 0xE410200C
    dut._log.info(f"LDR R2, [R0] => 2")
    await clkedge
    print_all(dut)

    # SUB R3, R3, R2 => (9 - 2) = 7
    # 0xE0433002
    dut._log.info(f"SUB R3, R3, R2 => (9 - 2) = 7")
    await clkedge
    print_all(dut)

    # NOP
    await clkedge
    print_all(dut)

    # NOP
    await clkedge
    print_all(dut)

    # NOP
    await clkedge
    print_all(dut)

    # NOP
    await clkedge
    print_all(dut)

    # NOP
    await clkedge
    print_all(dut)

    # NOP
    await clkedge
    print_all(dut)

    # NOP
    await clkedge
    print_all(dut)

    print("\n R1 = 1\n R2 = 2\n R3 = 7\n R7 = 7\n R8 = 8\n R9 = 9\n")

    # 84 - ADD R4, R3, R2 => (7 + 2) = 9
    # 0xE0834002
    dut._log.info(f"84 - ADD R4, R3, R2 => (7 + 2) = 9")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE0834002

    # 88 - LDR R5, [R0, #16] => 6
    # 0xE4105010
    dut._log.info(f"88 - LDR R5, [R0, #16] => 6")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE4105010

    # 92 - SUB R2, R4, R5 => (9 - 6) = 3
    # 0xE0442005
    dut._log.info(f"92 - SUB R6, R4, R5 => (9 - 6) = 3")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE0442005

    # 96 - AND R2, R5, R2 => (6 & 3) = 2
    # 0xE0052002
    dut._log.info(f"96 - AND R2, R5, R2 => (6 & 3) = 2")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE0052002
    assert dut.LDRstall.value == 1
    assert dut.StallF.value == 1
    assert dut.StallD.value == 1
    assert dut.FlushE.value == 1

    # 96 - AND R2, R5, R2 => (6 & 3) = 2
    # 0xE0052002
    dut._log.info(f"96 - AND R2, R5, R2 => (6 & 3) = 2")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE0052002
    assert dut.OUT.value == 9

    # 100 - NOP
    # 0xF0000000
    dut._log.info(f"100 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000
    assert dut.LDRstall.value == 0
    assert dut.StallF.value == 0
    assert dut.StallD.value == 0
    assert dut.FlushE.value == 0
    assert dut.ForwardBE.value == 1
    assert dut.OUT.value == 6

    # 104 - NOP
    # 0xF0000000
    dut._log.info(f"104 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000
    assert dut.ForwardBE.value == 2

    # 108 - NOP
    # 0xF0000000
    dut._log.info(f"108 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000
    assert dut.OUT.value == 3

    # 112 - NOP
    # 0xF0000000
    dut._log.info(f"112 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000
    assert dut.OUT.value == 2

    # 116 - NOP
    # 0xF0000000
    dut._log.info(f"116 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 120 - B 120 + 8 + 4 * 3 = 140
    # 0xEA000003
    dut._log.info(f"120 - B 120 + 8 + 4 * 3 = 140")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xEA000003
    assert dut.PCF.value == 120

    # 124 - NOP
    # 0xF0000000
    dut._log.info(f"124 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 128 - NOP
    # 0xF0000000
    dut._log.info(f"128 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000
    assert dut.BranchTakenE.value == 1
    assert dut.FlushE.value == 1
    assert dut.FlushD.value == 1

    # 140 BL 140 + 8 + 4 * 3 = 160, R14 = 144
    # 0xEB000003
    dut._log.info(f"140 BL 140 + 8 + 4 * 3 = 160")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xEB000003

    # 144 - NOP
    # 0xF0000000
    dut._log.info(f"144 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 148 - NOP
    # 0xF0000000
    dut._log.info(f"148 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 160 - MOV R6 rot-14 2 => 32
    # 0xE3B00E02
    dut._log.info(f"160 - MOV R6 rot-14 2 => 32")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE3B00E02

    # 164 - NOP
    # 0xF0000000
    dut._log.info(f"164 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000
    assert dut.ShifterControl.value == 3
    assert dut.RD2_S.value == 32

    # 168 - NOP
    # 0xF0000000
    dut._log.info(f"168 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 172 - NOP
    # 0xF0000000
    dut._log.info(f"172 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000
    assert dut.ALUOutM.value == 32

    # 176 - NOP
    # 0xF0000000
    dut._log.info(f"176 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000
    assert dut.OUT.value == 32

    # 180 - BX LR PC = 144
    # 0xE800000E
    dut._log.info(f"180 - BX LR PC = 144")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE800000E

    # 184 - NOP
    # 0xF0000000
    dut._log.info(f"184 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 188 - NOP
    # 0xF0000000
    dut._log.info(f"188 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 192 - NOP
    # 0xF0000000
    dut._log.info(f"192 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 196 - NOP
    # 0xF0000000
    dut._log.info(f"196 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000
    assert dut.PCPrime.value == 144

    # 144 - NOP
    # 0xF0000000
    dut._log.info(f"144 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000
    assert dut.PCF.value == 144

    # 148 - NOP
    # 0xF0000000
    dut._log.info(f"148 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000
