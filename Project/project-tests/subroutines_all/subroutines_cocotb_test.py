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
    print_hex_dec(dut, dut.WD3.value, name="WD3")

    # print_hex_dec(dut, dut.ExtImmE.value, name="ExtImmE")
    print_hex_dec(dut, dut.SrcBE.value, name="SrcBE")

    print_hex_dec(dut, dut.ReadDataM.value, name="ReadDataM")
    print_hex_dec(dut, dut.ReadDataW.value, name="ReadDataW")
    print_hex_dec(dut, dut.WriteDataM.value, name="WriteDataM")

    print_hex_dec(dut, dut.ALUResultE.value, name="ALUResultE")
    print_hex_dec(dut, dut.ALUOutM.value, name="ALUOutM")
    print_hex_dec(dut, dut.ALUOutW.value, name="ALUOutW")

    print_hex_dec(dut, dut.FlagWriteD.value, name="FlagWriteD")
    print_hex_dec(dut, dut.FlagWriteE.value, name="FlagWriteE")

    print_hex_dec(dut, dut.FlagZ.value, name="FlagZ", cond=True)
    print_hex_dec(dut, dut.OUT.value, name="OUT", cond=True)
    print("------------------")


@cocotb.test()
async def subroutine_all(dut):
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

    ############################### 2's complement ###############################
    dut._log.info(f"####################### 2's complement #######################")

    # BL 0x00000010 -> PC = 0 + 8 + 16*4 = 72 R14 = 4
    # 0xEB000010
    dut._log.info(f"2's complement of 0x00000007 = 0xFFFFFFF9")
    dut._log.info(f"0 - BL 0x00000010 -> PC = 0 + 8 + 16*4 = 72 R14 = 4")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 4
    assert dut.InstructionF.value == 0xEB000010

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
    assert dut.PCE.value == 4
    assert dut.WA3E.value == 14
    assert dut.Sel14E.value == 1

    # NOP
    dut._log.info(f"12 - NOP")
    await clkedge
    assert dut.PCM.value == 4
    assert dut.WA3M.value == 14
    assert dut.Sel14M.value == 1

    # NOP
    dut._log.info(f"16 - NOP")
    await clkedge
    assert dut.PCW.value == 4
    assert dut.WA3W.value == 14
    assert dut.WD3.value == 4
    assert dut.OUT.value == 72
    assert dut.PCPrime.value == 72
    assert dut.Sel14W.value == 1

    # LDR R3, [R0, #8] => 7
    # 0xE4103008
    dut._log.info(f"72 - LDR R3, [R0, #8] => 7")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 76
    assert dut.InstructionF.value == 0xE4103008

    # NOP
    dut._log.info(f"76 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 80

    # NOP
    dut._log.info(f"80 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 84
    assert dut.ALUResultE.value == 8
    assert dut.WA3E.value == 3

    # NOP
    dut._log.info(f"84 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 88
    assert dut.ALUOutM.value == 8
    assert dut.ReadDataM.value == 7

    # SUB R4, R0, R3 => 0-7 = 0xFFFFFFF9
    # 0xE0404003
    dut._log.info(f"88 - SUB R4, R0, R3 => 0-7 = 0xFFFFFFF9")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 92
    assert dut.InstructionF.value == 0xE0404003
    assert dut.OUT.value == 7

    # NOP
    dut._log.info(f"92 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 96

    # NOP
    dut._log.info(f"96 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 100
    assert dut.ALUResultE.value == 0xFFFFFFF9
    assert dut.WA3E.value == 4

    # NOP
    dut._log.info(f"100 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 104
    assert dut.ALUOutM.value == 0xFFFFFFF9
    assert dut.WA3M.value == 4

    # BX LR => PC = 4
    # 0xE800000E
    dut._log.info(f"104 - BX LR => PC = 4")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 108
    assert dut.InstructionF.value == 0xE800000E
    assert dut.OUT.value == 0xFFFFFFF9

    # NOP
    dut._log.info(f"108 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 112
    assert dut.RA2D.value == 14
    assert dut.RD2.value == 4

    # NOP
    dut._log.info(f"112 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 116
    assert dut.ALUResultE.value == 4

    # NOP
    dut._log.info(f"116 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 120
    assert dut.ALUOutM.value == 4

    # NOP
    dut._log.info(f"120 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 4
    assert dut.OUT.value == 4

    # NOP
    dut._log.info(f"4 - NOP")
    await clkedge
    assert dut.PCPrime.value == 8

    # NOP
    dut._log.info(f"8 - NOP")
    await clkedge
    assert dut.PCPrime.value == 12

    # NOP
    dut._log.info(f"12 - NOP")
    await clkedge
    assert dut.PCPrime.value == 16

    # NOP
    dut._log.info(f"16 - NOP")
    await clkedge
    assert dut.PCPrime.value == 20

    # NOP
    dut._log.info(f"20 - NOP")
    await clkedge
    assert dut.PCPrime.value == 24

    ############################## Even Parity ##############################
    dut._log.info(
        "############################## Even Parity ##############################"
    )

    # BL 0x00000018 -> PC = 24 + 8 + 24*4 = 128 R14 = 28
    # 0xEB000018
    dut._log.info(f"Even parity of E = 1")
    dut._log.info(f"24 - BL 0x00000018 -> PC = 24 + 8 + 24*4 = 128 R14 = 28")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 24
    assert dut.InstructionF.value == 0xEB000018

    # NOP
    dut._log.info(f"28 - NOP")
    await clkedge
    assert dut.PCF.value == 28
    assert dut.WA3D.value == 14
    assert dut.Sel14.value == 1

    # NOP
    dut._log.info(f"32 - NOP")
    await clkedge
    assert dut.PCF.value == 32
    assert dut.WA3E.value == 14
    assert dut.Sel14E.value == 1

    # NOP
    dut._log.info(f"36 - NOP")
    await clkedge
    assert dut.PCF.value == 36
    assert dut.WA3M.value == 14
    assert dut.Sel14M.value == 1

    # NOP
    dut._log.info(f"40 - NOP")
    await clkedge
    assert dut.PCW.value == 28
    assert dut.WA3W.value == 14
    assert dut.WD3.value == 28
    assert dut.OUT.value == 128
    assert dut.PCPrime.value == 128
    assert dut.Sel14W.value == 1

    # LDR R3, [R0, #12] => F
    # 0xE410300C
    dut._log.info(f"128 - LDR R3, [R0, #12] => F")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE410300C
    assert dut.PCF.value == 128

    # LDR R2, [R0, #4] => 4
    # 0xE4102004
    dut._log.info(f"132 - LDR R2, [R0, #4] => 4")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE4102004
    assert dut.PCF.value == 132

    # LDR R1, [R0, 0] => 1
    # 0xE4101000
    dut._log.info(f"136 - LDR R1, [R0, 0] => 1")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE4101000
    assert dut.PCF.value == 136
    assert dut.ALUResultE.value == 12
    assert dut.WA3E.value == 3

    # NOP
    dut._log.info(f"140 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 140
    assert dut.WA3E.value == 2
    assert dut.ALUResultE.value == 4
    assert dut.ReadDataM.value == 14

    # NOP
    dut._log.info(f"144 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 144
    assert dut.WA3E.value == 1
    assert dut.ALUResultE.value == 0
    assert dut.ReadDataM.value == 4
    assert dut.OUT.value == 14

    # CMP R3, R0 => R3-R0
    # 0xE1430000
    dut._log.info(f"148 - CMP R3, R0 => R3-R0")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 148
    assert dut.InstructionF.value == 0xE1430000
    assert dut.ReadDataM.value == 1
    assert dut.OUT.value == 4

    # NOP
    dut._log.info(f"152 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 152
    assert dut.RD1.value == 14
    assert dut.ALUControlD.value == 2
    assert dut.RegWriteD.value == 0

    # NOP
    dut._log.info(f"156 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 156
    assert dut.ALUResultE.value == 14

    # NOP
    dut._log.info(f"160 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 160
    assert dut.ALUOutM.value == 14

    # BEQ to 164 + 8 + 4*14 = 228
    # 0x0A00000E
    dut._log.info(f"164 - BEQ to 164 + 8 + 4*14 = 228")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 164
    assert dut.InstructionF.value == 0x0A00000E

    # AND R4, R1, R3
    # 0xE0014003
    dut._log.info(f"168 - AND R4, R1, R3")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 168
    assert dut.InstructionF.value == 0xE0014003

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
    assert dut.ALUResultE.value == 0
    assert dut.WA3E.value == 4

    # NOP
    dut._log.info(f"180 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 180
    assert dut.ALUOutM.value == 0
    assert dut.WA3M.value == 4

    # ADD R5, R5, R4
    # 0xE0855004
    dut._log.info(f"184 - ADD R5, R5, R4")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 184
    assert dut.InstructionF.value == 0xE0855004
    assert dut.OUT.value == 0

    # NOP
    dut._log.info(f"188 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 188

    # NOP
    dut._log.info(f"192 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 192
    assert dut.ALUResultE.value == 0

    # NOP
    dut._log.info(f"196 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 196
    assert dut.ALUOutM.value == 0

    # MOV R3, R3, LSR #1 => R3 >> 1
    # 0xE1A030A3
    dut._log.info(f"200 - MOV R3, R3, LSR #1 => R3 >> 1")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 200
    assert dut.InstructionF.value == 0xE1A030A3
    assert dut.OUT.value == 0

    # NOP
    dut._log.info(f"204 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 204

    # NOP
    dut._log.info(f"208 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 208
    assert dut.ALUResultE.value == 7
    assert dut.WA3E.value == 3

    # NOP
    dut._log.info(f"212 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 212
    assert dut.ALUOutM.value == 7
    assert dut.WA3M.value == 3

    # B to CMP 216 + 8 - 4 * 19 = 148
    # 0xEAFFFFED
    dut._log.info(f"216 - B to CMP 216 + 8 - 4 * 19 = 148")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 216
    assert dut.InstructionF.value == 0xEAFFFFED
    assert dut.OUT.value == 7

    # NOP
    dut._log.info(f"220 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 220

    # NOP
    dut._log.info(f"224 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 224

    # NOP
    dut._log.info(f"228 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 228

    # NOP
    dut._log.info(f"232 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 232
    assert dut.OUT.value == 148
    assert dut.PCPrime.value == 148

    for i in range(0, 75):
        await clkedge

    print_all(dut)
    assert dut.PCPrime.value == 228

    # AND R5, R5, R1
    # 0xE0055001
    dut._log.info(f"228 - AND R5, R5, R1")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 228
    assert dut.InstructionF.value == 0xE0055001

    # NOP
    dut._log.info(f"232 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 232

    # NOP
    dut._log.info(f"236 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 236
    assert dut.ALUResultE.value == 1
    assert dut.WA3E.value == 5

    # BX LR to 28
    # 0xE800000E
    dut._log.info(f"240 - BX LR to 28")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 240
    assert dut.InstructionF.value == 0xE800000E
    assert dut.ALUOutM.value == 1
    assert dut.WA3M.value == 5

    # NOP
    dut._log.info(f"244 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 244
    assert dut.OUT.value == 1

    # NOP
    dut._log.info(f"248 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 248
    assert dut.ALUResultE.value == 28

    # NOP
    dut._log.info(f"252 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 252

    # NOP
    dut._log.info(f"256 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 256
    assert dut.PCPrime.value == 28

    # NOP
    dut._log.info(f"28 - NOP")
    await clkedge
    assert dut.PCPrime.value == 32
    assert dut.PCF.value == 28

    # NOP
    dut._log.info(f"32 - NOP")
    await clkedge
    assert dut.PCF.value == 32

    # NOP
    dut._log.info(f"36 - NOP")
    await clkedge
    assert dut.PCF.value == 36

    # NOP
    dut._log.info(f"40 - NOP")
    await clkedge
    assert dut.PCF.value == 40

    # NOP
    dut._log.info(f"44 - NOP")
    await clkedge
    assert dut.PCF.value == 44

    ############################## Array Sum #####################################
    dut._log.info(
        "############################## Array Sum #####################################"
    )

    # BL 0x00000033 -> PC = 48 + 8 + 51*4 = 260 R14 = 52
    # 0xEB000033
    dut._log.info("Array Sum Test for 3 elements in array")
    dut._log.info(f"(2A), (37), (5C) = 0xBD or in decimal 189")
    dut._log.info(f"48 - BL 0x00000033 -> PC = 48 + 8 + 51*4 = 260 R14 = 52")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 48
    assert dut.InstructionF.value == 0xEB000033

    # NOP
    dut._log.info(f"52 - NOP")
    await clkedge
    assert dut.PCF.value == 52
    assert dut.WA3D.value == 14
    assert dut.Sel14.value == 1

    # NOP
    dut._log.info(f"56 - NOP")
    await clkedge
    assert dut.PCF.value == 56
    assert dut.WA3E.value == 14
    assert dut.Sel14E.value == 1

    # NOP
    dut._log.info(f"60 - NOP")
    await clkedge
    assert dut.PCF.value == 60
    assert dut.WA3M.value == 14
    assert dut.Sel14M.value == 1

    # NOP
    dut._log.info(f"64 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCW.value == 52
    assert dut.WA3W.value == 14
    assert dut.WD3.value == 52
    assert dut.OUT.value == 260
    assert dut.PCPrime.value == 260
    assert dut.Sel14W.value == 1

    # LDR R3, [R0, #16] => 3 Array Size
    # 0xE4103010
    dut._log.info(f"260 - LDR R3, [R0, #16] => 3 Array Size")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE4103010
    assert dut.PCF.value == 260

    # LDR R4, [R0, #20] => 24
    # 0xE4104014
    dut._log.info(f"264 - LDR R4, [R0, #20] => 24")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE4104014
    assert dut.PCF.value == 264

    # LDR R2, [R0, #4] => 4
    # 0xE4102004
    dut._log.info(f"268 - LDR R2, [R0, #4] => 4")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE4102004
    assert dut.PCF.value == 268

    # LDR R1, [R0, 0] => 1
    # 0xE4101000
    dut._log.info(f"272 - LDR R1, [R0, 0] => 1")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE4101000
    assert dut.PCF.value == 272

    # NOP
    dut._log.info(f"276 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 276
    assert dut.OUT.value == 3

    # NOP
    dut._log.info(f"280 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 280
    assert dut.OUT.value == 24

    # LDR R5, [R4] => 42 or 2A
    # 0xE4145000
    dut._log.info(f"284 - LDR R5, [R4] => 42 or 2A")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 284
    assert dut.InstructionF.value == 0xE4145000
    assert dut.OUT.value == 4

    # NOP
    dut._log.info(f"288 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 288
    assert dut.OUT.value == 1

    # NOP
    dut._log.info(f"292 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 292

    # ADD R4, R4, R2
    # 0xE0844002
    dut._log.info(f"296 - ADD R4, R4, R2")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 296
    assert dut.InstructionF.value == 0xE0844002

    # SUB R3, R3, #1
    # 0xE0433001
    dut._log.info(f"300 - SUB R3, R3, #1")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 300
    assert dut.InstructionF.value == 0xE0433001
    assert dut.OUT.value == 42

    # ADD R10, R10, R5
    # 0xE08AA005
    dut._log.info(f"304 - ADD R10, R10, R5")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 304
    assert dut.InstructionF.value == 0xE08AA005

    # NOP
    dut._log.info(f"308 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 308

    # NOP
    dut._log.info(f"312 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 312
    assert dut.OUT.value == 28

    # NOP
    dut._log.info(f"316 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 316
    assert dut.OUT.value == 2

    # CMP R3, R0
    # 0xE1430000
    dut._log.info(f"320 - CMP R3, R0")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 320
    assert dut.InstructionF.value == 0xE1430000
    assert dut.OUT.value == 42

    # NOP
    dut._log.info(f"324 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 324

    # NOP
    dut._log.info(f"328 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 328

    # NOP
    dut._log.info(f"332 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 332
    assert dut.ALUOutM.value == 2

    # BEQ to 336 + 8 + 4*7 = 372
    # 0x0A000007
    dut._log.info(f"336 - BEQ to 372")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 336
    assert dut.InstructionF.value == 0x0A000006

    # NOP
    dut._log.info(f"340 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 340

    # NOP
    dut._log.info(f"344 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 344

    # NOP
    dut._log.info(f"348 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 348

    # NOP
    dut._log.info(f"352 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 352

    # B to 356 + 8 + 4*-20 = 284
    # 0xEAFFFFEC
    dut._log.info(f"356 - B to 284")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 356
    assert dut.InstructionF.value == 0xEAFFFFEC

    # NOP
    dut._log.info(f"360 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 360

    # NOP
    dut._log.info(f"364 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 364

    # NOP
    dut._log.info(f"368 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 368

    # NOP
    dut._log.info(f"372 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 372
    assert dut.PCPrime.value == 284

    for i in range(41):
        await clkedge

    assert dut.PCPrime.value == 368

    # ADD R10, R10, R0
    # 0xE08AA000
    dut._log.info(f"368 - ADD R10, R10, R0")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 368
    assert dut.InstructionF.value == 0xE08AA000

    # NOP
    dut._log.info(f"372 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 372

    # NOP
    dut._log.info(f"376 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 376

    # BX LR PC = 52
    # 0xE800000E
    dut._log.info(f"380 - BX LR PC = 52")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 380
    assert dut.InstructionF.value == 0xE800000E

    # NOP
    dut._log.info(f"384 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 384
    assert dut.OUT.value == 189

    # NOP
    dut._log.info(f"388 - NOP")
    await clkedge
    assert dut.PCF.value == 388

    # NOP
    dut._log.info(f"392 - NOP")
    await clkedge
    assert dut.PCF.value == 392

    # NOP
    await clkedge
    dut._log.info(f"396 - NOP")
    print_all(dut)
    assert dut.PCF.value == 396
    assert dut.PCPrime.value == 52

    # NOP
    dut._log.info(f"52 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 52


