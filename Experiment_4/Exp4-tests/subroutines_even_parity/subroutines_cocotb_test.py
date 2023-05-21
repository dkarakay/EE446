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

    # CMP R3, R0 => R3-R0
    # 0xE1430000
    dut._log.info(f"88 - CMP R3, R0 => R3-R0")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 88
    assert dut.InstructionF.value == 0xE1430000
    assert dut.ReadDataM.value == 1
    assert dut.OUT.value == 4

    # NOP
    dut._log.info(f"92 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 92
    assert dut.RD1.value == 14
    assert dut.ALUControlD.value == 2
    assert dut.RegWriteD.value == 0

    # NOP
    dut._log.info(f"96 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 96
    assert dut.ALUResultE.value == 14

    # NOP
    dut._log.info(f"100 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 100
    assert dut.ALUOutM.value == 14

    # BEQ to 104 + 8 + 4*14 = 164
    # 0x0A00000E
    dut._log.info(f"104 - BEQ to 104 + 8 + 4*14 = 168")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 104
    assert dut.InstructionF.value == 0x0A00000E

    # AND R4, R1, R3
    # 0xE0014003
    dut._log.info(f"108 - AND R4, R1, R3")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 108
    assert dut.InstructionF.value == 0xE0014003

    # NOP
    dut._log.info(f"112 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 112

    # NOP
    dut._log.info(f"116 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 116
    assert dut.ALUResultE.value == 0
    assert dut.WA3E.value == 4

    # NOP
    dut._log.info(f"120 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 120
    assert dut.ALUOutM.value == 0
    assert dut.WA3M.value == 4

    # ADD R5, R5, R4
    # 0xE0855004
    dut._log.info(f"124 - ADD R5, R5, R4")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 124
    assert dut.InstructionF.value == 0xE0855004
    assert dut.OUT.value == 0

    # NOP
    dut._log.info(f"128 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 128

    # NOP
    dut._log.info(f"132 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 132
    assert dut.ALUResultE.value == 0

    # NOP
    dut._log.info(f"136 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 136
    assert dut.ALUOutM.value == 0

    # MOV R3, R3, LSR #1 => R3 >> 1
    # 0xE1A030A3
    dut._log.info(f"140 - MOV R3, R3, LSR #1 => R3 >> 1")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 140
    assert dut.InstructionF.value == 0xE1A030A3
    assert dut.OUT.value == 0

    # NOP
    dut._log.info(f"144 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 144

    # NOP
    dut._log.info(f"148 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 148
    assert dut.ALUResultE.value == 7
    assert dut.WA3E.value == 3

    # NOP
    dut._log.info(f"152 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 152
    assert dut.ALUOutM.value == 7
    assert dut.WA3M.value == 3

    # B to CMP 156 + 8 - 4 * 19 = 88
    # 0xEAFFFFED
    dut._log.info(f"156 - B to CMP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 156
    assert dut.InstructionF.value == 0xEAFFFFED
    assert dut.OUT.value == 7

    # NOP
    dut._log.info(f"160 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 160

    # NOP
    dut._log.info(f"164 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 164

    # NOP
    dut._log.info(f"168 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 168

    # NOP
    dut._log.info(f"172 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 172
    assert dut.OUT.value == 88
    assert dut.PCPrime.value == 88

    for i in range(0, 75):
        await clkedge
        dut._log.info(f"PCF: {dut.PCF.value}")
        print_all(dut)

    print_all(dut)
    assert dut.PCPrime.value == 168

    # AND R5, R5, R1
    # 0xE0055001
    dut._log.info(f"168 - AND R5, R5, R1")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 168
    assert dut.InstructionF.value == 0xE0055001

    # NOP
    dut._log.info(f"172 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 172

    # NOP
    dut._log.info(f"176 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 176
    assert dut.ALUResultE.value == 1
    assert dut.WA3E.value == 5

    # BX LR to 4
    # 0xE800000E
    dut._log.info(f"180 - BX LR to 4")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 180
    assert dut.InstructionF.value == 0xE800000E
    assert dut.ALUOutM.value == 1
    assert dut.WA3M.value == 5

    # NOP
    dut._log.info(f"184 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 184
    assert dut.OUT.value == 1


    # NOP
    dut._log.info(f"188 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 188
    assert dut.ALUResultE.value == 4

    # NOP
    dut._log.info(f"192 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 192

    # NOP
    dut._log.info(f"196 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 196
    assert dut.PCPrime.value == 4

    # NOP
    dut._log.info(f"4 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 8
    assert dut.PCF.value == 4

    # NOP

    """ 
    # Check LDR
    # Address 92
    # LDR R3, [R0, #188] => 7
    # 0xE41030BC

    dut._log.info(f"LDR R3, [R0, #188] => 7")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - MemAddr
    await clkedge
    dut._log.info(f"Cycle 3 - MemAddr")
    print_all(dut)
    assert dut.ALUResult.value == 188
    assert dut.OUT.value == dut.PC.value + 4

    # Cycle 4 - MemRead
    await clkedge
    dut._log.info(f"Cycle 4 - MemRead")
    print_all(dut)
    assert dut.ALUResult.value == 188

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)
    # assert dut.OUT.value == 7

    # Address 96
    # LDR R1 [R0, #192] => 1
    # 0xE41010C0

    dut._log.info(f"LDR R1 [R0, #192] => 1")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - MemAddr
    await clkedge
    dut._log.info(f"Cycle 3 - MemAddr")
    print_all(dut)
    assert dut.ALUResult.value == 192

    # Cycle 4 - MemRead
    await clkedge
    dut._log.info(f"Cycle 4 - MemRead")
    print_all(dut)
    assert dut.ALUResult.value == 192

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)
    assert dut.OUT.value == 1

    # Check LDR
    # Address 100
    # LDR R2, [R0, #200] => 4
    # 0xE41020C8

    dut._log.info(f"LDR R2, [R0, #200] => 4")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - MemAddr
    await clkedge
    dut._log.info(f"Cycle 3 - MemAddr")
    print_all(dut)
    assert dut.INSTR.value == 0xE41020C8

    # Cycle 4 - MemRead
    await clkedge
    dut._log.info(f"Cycle 4 - MemRead")
    print_all(dut)
    assert dut.ALUResult.value == 200

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)
    assert dut.OUT.value == 4

    # Check CMP
    # Address 104
    # CMP R3, R0 => R3 - R0
    # 0xE1430000

    dut._log.info(f"CMP R3, R0 => R3 - R0")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - ALU
    await clkedge
    dut._log.info(f"Cycle 3 - ALU")
    print_all(dut)
    assert dut.INSTR.value == 0xE1430000

    # Cycle 4 - ALUOut
    await clkedge
    dut._log.info(f"Cycle 4 - ALUOut")
    print_all(dut)

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)

    # Address 108
    # BEQ to dec 108+8 + 4*8 = 148
    # 0x0A000008

    dut._log.info(f"BEQ to dec 104+8 + 4*8 = 148")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - Execute
    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0x0A000008

    # Cycle 4 - Execute
    await clkedge
    dut._log.info(f"Cycle 4 - Execute")
    print_all(dut)

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)

    # Address 112
    # AND R4, R1, R3 => R4 = R1 & R3
    # 0xE0014003

    dut._log.info(f"AND R4, R1, R3 => R4 = R1 & R3")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - ALU
    await clkedge
    dut._log.info(f"Cycle 3 - ALU")
    print_all(dut)
    assert dut.INSTR.value == 0xE0014003

    # Cycle 4 - ALUOut
    await clkedge
    dut._log.info(f"Cycle 4 - ALUOut")
    print_all(dut)
    # assert dut.ALUResult.value == 1

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)

    # Address 116
    # ADD R5, R5, R4 => R5 = R5 + R4
    # 0xE0855004

    dut._log.info(f"ADD R5, R5, R4 => R5 = R5 + R4")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - ALU
    await clkedge
    dut._log.info(f"Cycle 3 - ALU")
    print_all(dut)
    assert dut.INSTR.value == 0xE0855004

    # Cycle 4 - ALUOut
    await clkedge
    dut._log.info(f"Cycle 4 - ALUOut")
    print_all(dut)

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)

    # Address 120
    # MOV R3, R3, LSR #1 => R3 = R3 >> 1
    # 0xE1A030A3

    dut._log.info(f"MOV R3, R3, LSR #1 => R3 = R3 >> 1")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - ALU
    await clkedge
    dut._log.info(f"Cycle 3 - ALU")
    print_all(dut)
    assert dut.INSTR.value == 0xE1A030A3

    # Cycle 4 - ALUOut
    await clkedge
    dut._log.info(f"Cycle 4 - ALUOut")
    print_all(dut)

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)

    # Address 124
    # B to dec 124+8 - 4*7 = 104
    # 0xEAFFFFF9

    dut._log.info(f"B to dec 124+8 - 4*7 = 104")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - Execute
    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xEAFFFFF9

    # Cycle 4 - Execute
    await clkedge
    dut._log.info(f"Cycle 4 - Execute")
    print_all(dut)
    assert dut.PC.value == 104

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)

    for i in range(100):
        await clkedge
        # print_all(dut)
        # dut._log.info(f"Cycle {i}")

    assert dut.PC.value == 148

    # Address 148
    # AND R5, R5, R1 => R5 = R5 & R1
    # 0xE0055001

    dut._log.info(f"AND R5, R5, R1 => R5 = R5 & R1")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - ALU
    await clkedge
    dut._log.info(f"Cycle 3 - ALU")
    print_all(dut)
    assert dut.INSTR.value == 0xE0055001

    # Cycle 4 - ALUOut
    await clkedge
    dut._log.info(f"Cycle 4 - ALUOut")
    print_all(dut)

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)
    dut._log.info(f"Result even Parity of 0x0000000F is {dut.OUT.value}")
    assert dut.OUT.value == 0

    # Address 152
    # BX LR => Branch to address in LR
    # 0xE800000E

    dut._log.info(f"BX LR => Branch to address in LR")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - Execute
    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE800000E

    # Cycle 4 - Execute
    await clkedge
    dut._log.info(f"Cycle 4 - Execute")
    print_all(dut)
    assert dut.PC.value == 4

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)
    """
