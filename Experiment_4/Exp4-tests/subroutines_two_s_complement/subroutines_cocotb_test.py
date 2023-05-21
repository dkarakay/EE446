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
    # print_hex_dec(dut, dut.PCPlus4F.value, name="PCPlus4F")

    print_hex_dec(dut, dut.RESET.value, name="RESET")

    print_hex_dec(dut, dut.PCSrcD.value, name="PCSrcD")
    print_hex_dec(dut, dut.PCSrcE.value, name="PCSrcE")
    print_hex_dec(dut, dut.PCSrcM.value, name="PCSrcM")
    print_hex_dec(dut, dut.PCSrcW.value, name="PCSrcW")

    print_hex_dec(dut, dut.Sel14.value, name="Sel14")
    print_hex_dec(dut, dut.Sel14E.value, name="Sel14E")
    print_hex_dec(dut, dut.Sel14M.value, name="Sel14M")
    print_hex_dec(dut, dut.Sel14W.value, name="Sel14W")

    print_hex_dec(dut, dut.RegWriteD.value, name="RegWriteD")
    print_hex_dec(dut, dut.RegWriteE.value, name="RegWriteE")
    print_hex_dec(dut, dut.RegWriteM.value, name="RegWriteM")
    print_hex_dec(dut, dut.RegWriteW.value, name="RegWriteW")

    print_hex_dec(dut, dut.MemWriteD.value, name="MemWriteD")
    print_hex_dec(dut, dut.MemWriteE.value, name="MemWriteE")
    print_hex_dec(dut, dut.MemWriteM.value, name="MemWriteM")

    print_hex_dec(dut, dut.MemtoRegD.value, name="MemtoRegD")
    print_hex_dec(dut, dut.MemtoRegE.value, name="MemtoRegE")
    print_hex_dec(dut, dut.MemtoRegM.value, name="MemtoRegM")
    print_hex_dec(dut, dut.MemtoRegW.value, name="MemtoRegW")

    print_hex_dec(dut, dut.ALUControlD.value, name="ALUControlD")
    print_hex_dec(dut, dut.ALUControlE.value, name="ALUControlE")

    print_hex_dec(dut, dut.ALUSrcD.value, name="ALUSrcD")
    print_hex_dec(dut, dut.ALUSrcE.value, name="ALUSrcE")

    print_hex_dec(dut, dut.RegSrcD.value, name="RegSrcD")
    print_hex_dec(dut, dut.ImmSrcD.value, name="ImmSrcD")
    print_hex_dec(dut, dut.CondE.value, name="CondE")

    #    print_hex_dec(dut, dut.FlagZ.value, name="FlagZ")
    print_hex_dec(dut, dut.RA1D.value, name="RA1D")
    print_hex_dec(dut, dut.RA2D.value, name="RA2D")
    print_hex_dec(dut, dut.RD1.value, name="RD1")
    print_hex_dec(dut, dut.RD2.value, name="RD2")
    print_hex_dec(dut, dut.RD1_OUT.value, name="RD1_OUT")
    print_hex_dec(dut, dut.RD2_OUT.value, name="RD2_OUT")

    print_hex_dec(dut, dut.WA3E.value, name="WA3E")
    print_hex_dec(dut, dut.WA3M.value, name="WA3M")
    print_hex_dec(dut, dut.WA3W.value, name="WA3W")

    # print_hex_dec(dut, dut.ExtImmE.value, name="ExtImmE")
    print_hex_dec(dut, dut.SrcBE.value, name="SrcBE")

    print_hex_dec(dut, dut.ReadDataM.value, name="ReadDataM")
    print_hex_dec(dut, dut.ReadDataW.value, name="ReadDataW")
    print_hex_dec(dut, dut.WriteDataM.value, name="WriteDataM")

    print_hex_dec(dut, dut.ALUResultE.value, name="ALUResultE")
    print_hex_dec(dut, dut.ALUOutM.value, name="ALUOutM")
    print_hex_dec(dut, dut.ALUOutW.value, name="ALUOutW")

    print_hex_dec(dut, dut.OUT.value, name="OUT", cond=True)
    print("------------------")


@cocotb.test()
async def main_cocotb_test(dut):
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

    # BL 0x00000005 -> PC = 0 + 8 + 5*4 = 28 R14 = 4
    # 0xEB000005
    dut._log.info(f"2's complement of 0x00000007 = 0xFFFFFFF9")
    dut._log.info(f"0 - BL 0x00000002 -> PC = 0 + 8 + 2*4 = 28 R14 = 4")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 4
    assert dut.InstructionF.value == 0xEB000005

    # NOP
    dut._log.info(f"4 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCD.value == 4
    assert dut.WA3D.value == 14
    assert dut.Sel14.value == 1

    # NOP
    dut._log.info(f"8 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCE.value == 4
    assert dut.WA3E.value == 14
    assert dut.Sel14E.value == 1

    # NOP
    dut._log.info(f"12 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCM.value == 4
    assert dut.WA3M.value == 14
    assert dut.Sel14M.value == 1

    # NOP
    dut._log.info(f"16 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCW.value == 4
    assert dut.WA3W.value == 14
    assert dut.WD3.value == 4
    assert dut.OUT.value == 28
    assert dut.PCPrime.value == 28
    assert dut.Sel14W.value == 1

    # LDR R3, [R0, #8] => 7
    # 0xE4103008
    dut._log.info(f"28 - LDR R3, [R0, #8] => 7")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 32
    assert dut.InstructionF.value == 0xE4103008

    # NOP
    dut._log.info(f"32 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 36

    # NOP
    dut._log.info(f"36 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 40
    assert dut.ALUResultE.value == 8
    assert dut.WA3E.value == 3

    # NOP
    dut._log.info(f"40 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 44
    assert dut.ALUOutM.value == 8
    assert dut.ReadDataM.value == 7

    # SUB R4, R0, R3 => 0-7 = 0xFFFFFFF9
    # 0xE0404003
    dut._log.info(f"44 - SUB R4, R3, R0 => 7")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 48
    assert dut.InstructionF.value == 0xE0404003
    assert dut.OUT.value == 7

    # NOP
    dut._log.info(f"48 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 52

    # NOP
    dut._log.info(f"52 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 56
    assert dut.ALUResultE.value == 0xFFFFFFF9
    assert dut.WA3E.value == 4

    # NOP
    dut._log.info(f"56 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 60
    assert dut.ALUOutM.value == 0xFFFFFFF9
    assert dut.WA3M.value == 4

    # BX LR => PC = 4
    # 0xE800000E
    dut._log.info(f"60 - BX LR => PC = 4")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 64
    assert dut.InstructionF.value == 0xE800000E
    assert dut.OUT.value == 0xFFFFFFF9

    # NOP
    dut._log.info(f"64 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 68
    assert dut.RA2D.value == 14
    assert dut.RD2.value == 4

    # NOP
    dut._log.info(f"68 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 72
    assert dut.ALUResultE.value == 4

    # NOP
    dut._log.info(f"72 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 76
    assert dut.ALUOutM.value == 4

    # NOP
    dut._log.info(f"76 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 4
    assert dut.OUT.value == 4

    # NOP
    dut._log.info(f"4 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 8
    assert dut.PCF.value == 4

    """
   