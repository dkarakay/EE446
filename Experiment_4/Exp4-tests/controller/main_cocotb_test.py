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

    # NOP
    dut._log.info(f"NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 100
    assert dut.OUT.value == 9

    """
    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - MemAddr
    await clkedge
    dut._log.info(f"Cycle 3 - MemAddr")
    print_all(dut)
    assert dut.ALUResult.value == 124
    assert dut.OUT.value == dut.PC.value + 4

    # Cycle 4 - MemRead
    await clkedge
    dut._log.info(f"Cycle 4 - MemRead")
    print_all(dut)
    assert dut.ALUResult.value == 124

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)
    assert dut.OUT.value == 17

    # Check LDR
    # Address 4
    # LDR R1, [R0, #128] => R1 = 5
    # 0xE4101080

    dut._log.info(f"LDR R1, [R0, #128] => R1 = 5")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - MemAddr
    await clkedge
    dut._log.info(f"Cycle 3 - MemAddr")
    print_all(dut)
    assert dut.ALUResult.value == 128

    # Cycle 4 - MemRead
    await clkedge
    dut._log.info(f"Cycle 4 - MemRead")
    print_all(dut)

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)

    # Check ADD operation
    # Address 8
    # ADD R6, R3, R1 -> R6 = 22 (17 + 5)
    # 0xE0836001
    dut._log.info(f"ADD R6, R3, R1 -> R6 = 22 (17 + 5)")

    # Fetch and decode cycles
    await fetch_and_decode(dut, clkedge, skip_print=True)

    # Cycle 3 - Execute
    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE0836001

    # Cycle 4 - ALUWriteBack
    await clkedge
    dut._log.info(f"Cycle 4 - ALUWriteBack")
    print_all(dut)
    assert dut.OUT.value == 22

    # Cycle 5 - Wait
    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)

    # Check SUB operation
    # Address 12
    # SUB R7, R6, R3 -> R7 = 5 (22 - 17)
    # 0xE0467003
    dut._log.info(f"SUB R7, R6, R3 -> R7 = 5 (22 - 17)")

    # Fetch and decode cycles
    await fetch_and_decode(dut, clkedge, skip_print=True)

    # Cycle 3 - Execute
    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE0467003

    # Cycle 4 - ALUWriteBack
    await clkedge
    dut._log.info(f"Cycle 4 - ALUWriteBack")
    print_all(dut)
    assert dut.OUT.value == 5

    # Cycle 5 - Wait
    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)

    # Check AND operation
    # Address 16
    # AND R8, R3, R1 -> R8 = 1 (0001 & 10001)
    # 0xE0038001
    dut._log.info(f"AND R8, R3, R1 -> R8 = 1 (0001 & 10001)")

    # Fetch and decode cycles
    await fetch_and_decode(dut, clkedge, skip_print=True)

    # Cycle 3 - Execute
    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE0038001

    # Cycle 4 - ALUWriteBack
    await clkedge
    dut._log.info(f"Cycle 4 - ALUWriteBack")
    print_all(dut)
    assert dut.OUT.value == 1

    # Cycle 5 - Wait
    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)

    # Check ORR operation
    # Address 20
    # ORR R9, R3, R1 -> R9 = 21 (0001 | 10001)
    # 0xE1039001
    dut._log.info(f"ORR R9, R3, R1 -> R9 = 21 (0001 | 10001)")

    # Fetch and decode cycles
    await fetch_and_decode(dut, clkedge, skip_print=True)

    # Cycle 3 - Execute
    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE1039001

    # Cycle 4 - ALUWriteBack
    await clkedge
    dut._log.info(f"Cycle 4 - ALUWriteBack")
    print_all(dut)
    assert dut.OUT.value == 21

    # Cycle 5 - Wait
    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)

    # Check MOV operation
    # Address 24
    # MOV R10, R3 -> R10 = 17
    # 0xE400A003
    dut._log.info(f"MOV R10, R3 -> R10 = 17")

    # Fetch and decode cycles
    await fetch_and_decode(dut, clkedge, skip_print=True)

    # Cycle 3 - Execute
    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE400A003

    # Cycle 4 - ALUWriteBack
    await clkedge
    dut._log.info(f"Cycle 4 - ALUWriteBack")
    print_all(dut)
    assert dut.OUT.value == 17

    # Cycle 5 - Wait
    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)

    # Check STR operation
    # Address 28
    # STR R3, [R0, #132] -> MEM[132] = 17
    # 0xE4003084
    dut._log.info(f"STR R3, [R0, #132] -> MEM[132] = 17")

    # Fetch and decode cycles
    await fetch_and_decode(dut, clkedge, skip_print=True)

    # Cycle 3 - MemAdr
    await clkedge
    dut._log.info(f"Cycle 3 - MemAdr")
    print_all(dut)
    assert dut.INSTR.value == 0xE4003084

    # Cycle 4 - MemWrite
    await clkedge
    dut._log.info(f"Cycle 4 - MemWrite")
    print_all(dut)

    # Cycle 5 - Wait
    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)

    # Check LDR
    # Address 32
    # LDR R10, [R0, #132] -> R10 = 17
    # 0xE410A084

    dut._log.info(f"LDR R10, [R0, #132] -> R10 = 17")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - MemAddr

    await clkedge
    dut._log.info(f"Cycle 3 - MemAddr")
    print_all(dut)
    assert dut.ALUResult.value == 132
    assert dut.INSTR.value == 0xE410A084

    # Cycle 4 - MemRead

    await clkedge
    dut._log.info(f"Cycle 4 - MemRead")
    print_all(dut)

    # Cycle 5 - WriteBack

    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)
"""
