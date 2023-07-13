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
    print_hex_dec(dut, dut.PCD.value, name="PCD")
    print_hex_dec(dut, dut.PCE.value, name="PCE")

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

    print_hex_dec(dut, dut.FlagZ.value, name="FlagZ")
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

    print_hex_dec(dut, dut.PredictionF.value, name="PredictionF")
    print_hex_dec(dut, dut.PredictionD.value, name="PredictionD")
    print_hex_dec(dut, dut.PredictionE.value, name="PredictionE")

    print_hex_dec(dut, dut.LRU.value, name="LRU")
    print_hex_dec(dut, dut.Hit.value, name="Hit")
    print_hex_dec(dut, dut.BTA.value, name="BTA")
    print_hex_dec(dut, dut.Match.value, name="Match")
    print_hex_dec(dut, dut.GHROut.value, name="GHROut")
    print_hex_dec(dut, dut.PHT.value, name="PHT")

    print_hex_dec(dut, dut.BTA.value, name="BTA")

    print_hex_dec(dut, dut.BTB_PC1.value, name="BTB_PC1")
    print_hex_dec(dut, dut.BTB_PC2.value, name="BTB_PC2")
    print_hex_dec(dut, dut.BTB_PC3.value, name="BTB_PC3")

    print_hex_dec(dut, dut.BTB_BTA1.value, name="BTB_BTA1")
    print_hex_dec(dut, dut.BTB_BTA2.value, name="BTB_BTA2")
    print_hex_dec(dut, dut.BTB_BTA3.value, name="BTB_BTA3")

    print_hex_dec(dut, dut.OUT.value, name="OUT", cond=True)
    print("------------------")


"""
@cocotb.test()
async def branch_predict_2(dut):
    # Generate the clock
    await cocotb.start(Clock(dut.CLK, 10, "us").start(start_high=False))

    # set clkedge as the rising edge of the clock
    clkedge = RisingEdge(dut.CLK)
    # wait until the clock edge
    dut.RESET.value = 1
    await clkedge
    print_all(dut)

    dut.RESET.value = 0

    # 0 - NOP
    # 0xF0000000
    dut._log.info(f"0 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 4 - LDR R3, [R0, #4] => 3
    # 0xE4103004
    dut._log.info(f"4 - LDR R3, [R0, #4] => 3")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE4103004

    # 8 - LDR R2, [R0] => 2
    # 0xE4102000
    dut._log.info(f"8 - LDR R2, [R0] => 2")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE4102000

    # 12 - LDR R1, [R0, #8] => 1
    # 0xE4101008
    dut._log.info(f"12 - LDR R1, [R0, #8] => 1")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE4101008

    # 16 - NOP
    # 0xF0000000
    dut._log.info(f"16 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 20 - NOP
    # 0xF0000000
    dut._log.info(f"20 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 24 - NOP
    # 0xF0000000
    dut._log.info(f"24 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 28 - NOP
    # 0xF0000000
    dut._log.info(f"28 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 32 - SUB R3, R3, R1 => 3 - 1 = 2
    # 0xE0433001
    dut._log.info(f"32 - SUB R3, R3, R1 => 3 - 1 = 2")
    await clkedge
    print_all(dut)

    # 36 - CMP R3, R2 => 2 - 2 = 0
    # 0xE1430002
    dut._log.info(f"36 - CMP R3, R2 => 2 - 2 = 0")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE1430002

    # 40 - BEQ 40 + 8 + 4 * (-4) = 32
    # 0x0AFFFFF6
    dut._log.info(f"40 - BEQ 40 + 8 + 4 * (-4) = 32")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0x0AFFFFFC

    # 44 - NOP
    # 0xF0000000
    dut._log.info(f"44 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 48 - NOP
    # 0xF0000000
    dut._log.info(f"48 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 52 - NOP
    # 0xF0000000
    dut._log.info(f"52 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 56 - NOP
    # 0xF0000000
    dut._log.info(f"56 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 60 - NOP
    # 0xF0000000
    dut._log.info(f"60 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

"""


@cocotb.test()
async def branch_predict_1(dut):
    # Generate the clock
    await cocotb.start(Clock(dut.CLK, 10, "us").start(start_high=False))

    # set clkedge as the rising edge of the clock
    clkedge = RisingEdge(dut.CLK)
    # wait until the clock edge
    dut.RESET.value = 1
    await clkedge
    print_all(dut)

    dut.RESET.value = 0

    # 0 - NOP
    # 0xF0000000
    dut._log.info(f"0 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 4 - Branch 4 + 8 + 4 * 3 = 24
    # 0xEA000003
    dut._log.info(f"4 - Branch 4 + 8 + 4 * 3 = 24")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xEA000003

    # 8 - NOP
    # 0xF0000000
    dut._log.info(f"8 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 12 - NOP
    # 0xF0000000
    dut._log.info(f"12 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000
    assert dut.BranchTakenE.value == 1
    assert dut.FlushE.value == 1
    assert dut.FlushD.value == 1

    # 24 - NOP
    # 0xF0000000
    dut._log.info(f"24 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 28 - NOP
    # 0xF0000000
    dut._log.info(f"28 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 32 - NOP
    # 0xF0000000
    dut._log.info(f"32 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 36 - Branch 36 + 8 + 4 * (-10) = 4
    # 0xEAFFFFF6
    dut._log.info(f"36 - Branch 36 + 8 + 4 * (-10) = 4")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xEAFFFFF6

    # 40 - NOP
    # 0xF0000000
    dut._log.info(f"40 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 44 - NOP
    # 0xF0000000
    dut._log.info(f"44 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000
    assert dut.BranchTakenE.value == 1

    # 4 - Branch 4 + 8 + 4 * 3 = 24
    # 0xEA000003
    dut._log.info(f"4 - Branch 4 + 8 + 4 * 3 = 24")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xEA000003

    # 8 - NOP
    # 0xF0000000
    dut._log.info(f"8 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000

    # 12 - NOP
    # 0xF0000000
    dut._log.info(f"12 - NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000
    assert dut.BranchTakenE.value == 1
    assert dut.FlushE.value == 1
    assert dut.FlushD.value == 1
