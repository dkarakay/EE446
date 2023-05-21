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

    # Check LDR
    # LDR R3, [R0, #4] => 9
    # 0xE4103004
    dut._log.info(f"LDR R3, [R0, #4] => 9")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE4103004
    assert dut.PCPrime.value == 4

    # NOP
    dut._log.info(f"NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000
    assert dut.PCPrime.value == 8
    assert dut.INSTR.value == 0xE4103004
    assert dut.RegWriteD.value == 1
    assert dut.MemtoRegD.value == 1
    assert dut.ExtImmD.value == 4

    # NOP
    dut._log.info(f"NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000
    assert dut.PCPrime.value == 12
    assert dut.INSTR.value == 0xF0000000
    assert dut.ALUResultE.value == 4
    assert dut.WA3E.value == 3

    # NOP
    dut._log.info(f"NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000
    assert dut.PCPrime.value == 16
    assert dut.ALUOutM.value == 4
    assert dut.ReadDataM.value == 9

    # LDR R4, [R0, #0] => 6
    # 0xE4104000
    dut._log.info(f"LDR R4, [R0, #0] => 6")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE4104000
    assert dut.PCPrime.value == 20
    assert dut.INSTR.value == 0xF0000000
    assert dut.OUT.value == 9

    # NOP
    dut._log.info(f"NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000
    assert dut.PCPrime.value == 24

    # NOP
    dut._log.info(f"NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 28
    assert dut.ALUResultE.value == 0
    assert dut.WA3E.value == 4

    # NOP
    dut._log.info(f"NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 32
    assert dut.ALUOutM.value == 0
    assert dut.ReadDataM.value == 6

    # ADD R5, R3, R4 => 15
    # 0xE0835004
    dut._log.info(f"ADD R5, R3, R4 => 15")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE0835004
    assert dut.PCPrime.value == 36
    assert dut.OUT.value == 6

    # NOP
    dut._log.info(f"NOP")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xF0000000
    assert dut.PCPrime.value == 40
    assert dut.RegWriteD.value == 1
    assert dut.ALUControlD.value == 4
    assert dut.RA1D.value == 3
    assert dut.RA2D.value == 4
    assert dut.RD1.value == 9
    assert dut.RD2.value == 6

    # NOP
    dut._log.info(f"NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 44
    assert dut.ALUResultE.value == 15
    assert dut.WA3E.value == 5

    # NOP
    dut._log.info(f"NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 48
    assert dut.ALUOutM.value == 15
    assert dut.WA3M.value == 5

    # SUB R6, R3, R4 => 3
    # 0xE0436004
    dut._log.info(f"SUB R6, R3, R4 => 3")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE0436004
    assert dut.PCPrime.value == 52
    assert dut.OUT.value == 15

    # NOP
    dut._log.info(f"NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 56
    assert dut.RegWriteD.value == 1
    assert dut.ALUControlD.value == 2
    assert dut.RA1D.value == 3
    assert dut.RA2D.value == 4
    assert dut.RD1.value == 9
    assert dut.RD2.value == 6

    # NOP
    dut._log.info(f"NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 60
    assert dut.ALUResultE.value == 3
    assert dut.WA3E.value == 6

    # NOP
    dut._log.info(f"NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 64
    assert dut.ALUOutM.value == 3
    assert dut.WA3M.value == 6

    # AND R7, R3, R6 => (1001 & 0011) = 1
    # 0xE0037006
    dut._log.info(f"AND R7, R3, R6 => (1001 & 0011) = 1")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 68
    assert dut.OUT.value == 3
    assert dut.InstructionF.value == 0xE0037006

    # NOP
    dut._log.info(f"NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 72
    assert dut.RegWriteD.value == 1
    assert dut.ALUControlD.value == 0

    # NOP
    dut._log.info(f"NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 76
    assert dut.ALUResultE.value == 1
    assert dut.WA3E.value == 7

    # NOP
    dut._log.info(f"NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 80
    assert dut.ALUOutM.value == 1
    assert dut.WA3M.value == 7

    # MOV R10, R3 => 1001
    # 0xE1A0A003
    dut._log.info(f"MOV R10, R3 => 1001")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE1A0A003
    assert dut.PCPrime.value == 84
    assert dut.OUT.value == 1

    # NOP
    dut._log.info(f"NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 88
    assert dut.RegWriteD.value == 1
    assert dut.ALUControlD.value == 13

    # NOP
    dut._log.info(f"NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 92
    assert dut.ALUResultE.value == 9
    assert dut.WA3E.value == 10

    # NOP
    dut._log.info(f"NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 96
    assert dut.ALUOutM.value == 9
    assert dut.WA3M.value == 10

    # STR R7, [R0, #8] => 1
    # 0xE4007008
    dut._log.info(f"96 - STR R7, [R0, #8] => 1")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 100
    assert dut.OUT.value == 9
    assert dut.InstructionF.value == 0xE4007008

    # NOP
    dut._log.info(f"100 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 104
    assert dut.MemWriteD.value == 1
    assert dut.ALUSrcD.value == 1
    assert dut.ImmSrcD.value == 1

    # NOP
    dut._log.info(f"104 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 108
    assert dut.ALUResultE.value == 8
    assert dut.WA3E.value == 7

    # ORR R9, R3, R4 => (1001 | 1010) = 15
    # 0xE1039004
    dut._log.info(f"108 - ORR R9, R3, R4 => (1001 | 1010) = 15")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 112
    assert dut.ALUOutM.value == 8
    assert dut.WriteDataM.value == 1
    assert dut.WA3M.value == 7
    assert dut.InstructionF.value == 0xE1039004

    # NOP
    dut._log.info(f"112 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 116
    assert dut.RegWriteD.value == 1

    # NOP
    dut._log.info(f"116 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 120
    assert dut.ALUResultE.value == 15
    assert dut.WA3E.value == 9

    # NOP
    dut._log.info(f"120 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 124
    assert dut.ALUOutM.value == 15
    assert dut.WA3M.value == 9

    # B to dec 124 + 8 + 4 * 4 = 148
    # 0xEA000004
    dut._log.info(f"124 - B to dec 124 + 8 + 4 * 4 = 148")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 128
    assert dut.OUT.value == 15
    assert dut.InstructionF.value == 0xEA000004

    # NOP
    dut._log.info(f"128 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 132
    assert dut.RA1D.value == 15
    assert dut.RD1.value == 132

    # NOP
    dut._log.info(f"132 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 136
    assert dut.RD1_OUT.value == 132
    assert dut.ALUResultE.value == 148

    # NOP
    dut._log.info(f"136 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 140
    assert dut.ALUOutM.value == 148

    # NOP
    dut._log.info(f"140 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 148
    assert dut.OUT.value == 148

    # BL to dec 148 + 8 + 4 * 5 = 176, R14 = 152
    # 0xEB000005
    dut._log.info(f"148 - BL to dec 148 + 8 + 4 * 5 = 176, R14 = 152")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 152
    assert dut.InstructionF.value == 0xEB000005

    # NOP
    dut._log.info(f"152 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCD.value == 152
    assert dut.WA3D.value == 14
    assert dut.Sel14.value == 1

    # NOP
    dut._log.info(f"156 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCE.value == 152
    assert dut.WA3E.value == 14
    assert dut.Sel14E.value == 1

    # NOP
    dut._log.info(f"160 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCM.value == 152
    assert dut.WA3M.value == 14
    assert dut.Sel14M.value == 1

    # NOP
    dut._log.info(f"164 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCW.value == 152
    assert dut.WA3W.value == 14
    assert dut.WD3.value == 152
    assert dut.OUT.value == 176
    assert dut.PCPrime.value == 176
    assert dut.Sel14W.value == 1

    # NOP
    dut._log.info(f"176 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 180

    # BX LR => PC = 152
    # 0xE800000E
    dut._log.info(f"180 - BX LR => PC = 152")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 184
    assert dut.InstructionF.value == 0xE800000E

    # NOP
    dut._log.info(f"184 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 188
    assert dut.RA2D.value == 14
    assert dut.RD2.value == 152

    # NOP
    dut._log.info(f"188 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 192
    assert dut.RD2_OUT.value == 152
    assert dut.ALUResultE.value == 152

    # NOP
    dut._log.info(f"192 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 196
    assert dut.ALUOutM.value == 152

    # NOP
    dut._log.info(f"196 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 152
    assert dut.OUT.value == 152

    # NOP
    dut._log.info(f"152 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 156
    assert dut.PCF.value == 152

    