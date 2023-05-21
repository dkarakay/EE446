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

    print_hex_dec(dut, dut.FlagWriteD.value, name="FlagWriteD", cond=True)
    print_hex_dec(dut, dut.FlagWriteE.value, name="FlagWriteE", cond=True)

    print_hex_dec(dut, dut.FlagZ.value, name="FlagZ", cond=True)
    print_hex_dec(dut, dut.OUT.value, name="OUT", cond=True)
    print("------------------")


@cocotb.test()
async def subroutine_2s_complement_using_branch(dut):
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

    # BL 0x0000000F -> PC = 0 + 8 + 15*4 = 68 R14 = 4
    # 0xEB00000F
    dut._log.info(f"Even parity of F = 1")
    dut._log.info(f"0 - BL 0x0000000F -> PC = 0 + 8 + 15*4 = 68 R14 = 4")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 4
    assert dut.InstructionF.value == 0xEB00000F

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
    assert dut.OUT.value == 68
    assert dut.PCPrime.value == 68
    assert dut.Sel14W.value == 1

    # LDR R3, [R0, #12] => F
    # 0xE410300C
    dut._log.info(f"68 - LDR R3, [R0, #12] => F")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE410300C
    assert dut.PCF.value == 68

    # LDR R2, [R0, #4] => 4
    # 0xE4102004
    dut._log.info(f"72 - LDR R2, [R0, #4] => 4")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE4102004
    assert dut.PCF.value == 72

    # LDR R1, [R0, 0] => 1
    # 0xE4101000
    dut._log.info(f"76 - LDR R1, [R0, 0] => 1")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE4101000
    assert dut.PCF.value == 76
    assert dut.ALUResultE.value == 12
    assert dut.WA3E.value == 3

    # NOP
    dut._log.info(f"80 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 80
    assert dut.WA3E.value == 2
    assert dut.ALUResultE.value == 4
    assert dut.ReadDataM.value == 14

    # NOP
    dut._log.info(f"84 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 84
    assert dut.WA3E.value == 1
    assert dut.ALUResultE.value == 0
    assert dut.ReadDataM.value == 4
    assert dut.OUT.value == 14

    """
    # Check LDR
    # Address 32
    # LDR R1, [R0, #128] => 1
    # 0xE4101080

    dut._log.info(f"LDR R1, [R0, #128] => 1")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - MemAddr
    await clkedge
    dut._log.info(f"Cycle 3 - MemAddr")
    print_all(dut)
    assert dut.INSTR.value == 0xE4101080

    # Cycle 4 - MemRead
    await clkedge
    dut._log.info(f"Cycle 4 - MemRead")
    print_all(dut)
    assert dut.ALUResult.value == 128

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)
    assert dut.OUT.value == 1

    # Check LDR
    # Address 36
    # LDR R3, [R0, #132] => 3 Load Array Size
    # 0xE4103084

    dut._log.info(f"LDR R3, [R0, #132] => 3 Load Array Size")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - MemAddr
    await clkedge
    dut._log.info(f"Cycle 3 - MemAddr")
    print_all(dut)
    assert dut.INSTR.value == 0xE4103084

    # Cycle 4 - MemRead
    await clkedge
    dut._log.info(f"Cycle 4 - MemRead")
    print_all(dut)
    assert dut.ALUResult.value == 132

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)
    assert dut.OUT.value == 3

    # Check LDR
    # Address 40
    # LDR R2, [R0, #136] => 4
    # 0xE4102088

    dut._log.info(f"LDR R2, [R0, #136] => 4")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - MemAddr
    await clkedge
    dut._log.info(f"Cycle 3 - MemAddr")
    print_all(dut)
    assert dut.INSTR.value == 0xE4102088

    # Cycle 4 - MemRead
    await clkedge
    dut._log.info(f"Cycle 4 - MemRead")
    print_all(dut)
    assert dut.ALUResult.value == 136

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)
    assert dut.OUT.value == 4

    # Check LDR
    # Address 44
    # LDR R4, [R0, #140] => 144
    # 0xE410408C

    dut._log.info(f"LDR R4, [R0, #140] => 144")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - MemAddr
    await clkedge
    dut._log.info(f"Cycle 3 - MemAddr")
    print_all(dut)
    assert dut.INSTR.value == 0xE410408C

    # Cycle 4 - MemRead
    await clkedge
    dut._log.info(f"Cycle 4 - MemRead")
    print_all(dut)
    assert dut.ALUResult.value == 140

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)
    assert dut.OUT.value == 144

    # Address 48
    # LDR R5, [R4] => 42
    # 0xE4145000

    dut._log.info(f"LDR R5, [R4] => 42")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - MemAddr
    await clkedge
    dut._log.info(f"Cycle 3 - MemAddr")
    print_all(dut)
    assert dut.INSTR.value == 0xE4145000

    # Cycle 4 - MemRead
    await clkedge
    dut._log.info(f"Cycle 4 - MemRead")
    print_all(dut)
    assert dut.ALUResult.value == 144

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)
    assert dut.OUT.value == 42

    # Address 52
    # ADD R4, R4, R2 => 148
    # 0xE0844002

    dut._log.info(f"ADD R4, R4, R2 => 148")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - Execute
    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE0844002

    # Cycle 4 - Execute
    await clkedge
    dut._log.info(f"Cycle 4 - Execute")
    print_all(dut)
    assert dut.OUT.value == 148

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)

    # Address 56
    # SUB R3, R3, R1 => 2
    # 0xE0433001

    dut._log.info(f"SUB R3, R3, R1 => 2")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - Execute
    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE0433001

    # Cycle 4 - Execute
    await clkedge
    dut._log.info(f"Cycle 4 - Execute")
    print_all(dut)
    assert dut.OUT.value == 2

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)

    # Address 60
    # ADD R10, R10, R5 => 42
    # 0xE08AA005

    dut._log.info(f"ADD R10, R10, R5 => 42")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - Execute
    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE08AA005

    # Cycle 4 - Execute
    await clkedge
    dut._log.info(f"Cycle 4 - Execute")
    print_all(dut)
    assert dut.OUT.value == 42

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)

    # Address 64
    # CMP R3, R0 => 0
    # 0xE1430000

    dut._log.info(f"CMP R3, R0 => 0")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - Execute
    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE1430000

    # Cycle 4 - Execute
    await clkedge
    dut._log.info(f"Cycle 4 - Execute")
    print_all(dut)

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)

    # Address 68
    # BEQ to dec 68+8 + 4*1 = 80
    # 0x0A000001

    dut._log.info(f"BEQ to dec 68+8 + 4*1 = 80")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - Execute
    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0x0A000001

    # Cycle 4 - Execute
    await clkedge
    dut._log.info(f"Cycle 4 - Execute")
    print_all(dut)

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)

    # Address 72
    # B to dec 72 + 8 - 4*8 = 48
    # 0xEAFFFFF8

    dut._log.info(f"B to dec 72 + 8 - 4*8 = 48")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - Execute
    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xEAFFFFF8

    # Cycle 4 - Execute
    await clkedge
    dut._log.info(f"Cycle 4 - Execute")
    print_all(dut)

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)

    dut._log.info(f"Wait for 2 loops")
    for i in range(0, 65):
        await clkedge
        #dut._log.info(f"Cycle {i} - Wait")
        # if dut.CYCLE.value != 0 and dut.CYCLE.value != 1 :

    print_all(dut)

    # Check BX LR
    # Address 80
    # BX LR -> PC = 4
    # 0xE800000E

    dut._log.info(f"BX LR -> PC = 4")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE800000E

    await clkedge
    dut._log.info(f"Cycle 4 - Wait")
    print_all(dut)
    assert dut.PC.value == 4

    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)

    # Address 4
    # ADD R10,R10,R0 => 189 (0xBD)
    # 0xE08AA000

    dut._log.info(f"ADD R10,R10,R0 => 189 (0xBD) Check the sum of the array")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE08AA000

    await clkedge
    dut._log.info(f"Cycle 4 - Execute")
    print_all(dut)
    assert dut.OUT.value == 189

    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)
    """