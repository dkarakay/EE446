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
async def subroutine_array_sum_using_branch(dut):
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

    # NOP
    dut._log.info(f"0 - NOP")
    await clkedge
    assert dut.PCF.value == 0

    # NOP
    dut._log.info(f"4 - NOP")
    await clkedge
    assert dut.PCF.value == 4

    # BL 0x0000000F -> PC = 8 + 8 + 44*4 = 192 R14 = 12
    # 0xEB00002C
    dut._log.info("Array Sum Test for 3 elements in array")
    dut._log.info(f"(2A), (37), (5C) = 0xBD or in decimal 189")
    dut._log.info(f"8 - BL 0x0000000F -> PC = 8 + 8 + 44*4 = 192 R14 = 12")
    await clkedge
    print_all(dut)
    assert dut.PCPrime.value == 12
    assert dut.InstructionF.value == 0xEB00002C

    # NOP
    dut._log.info(f"12 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCD.value == 12
    assert dut.WA3D.value == 14
    assert dut.Sel14.value == 1

    # NOP
    dut._log.info(f"16 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCE.value == 12
    assert dut.WA3E.value == 14
    assert dut.Sel14E.value == 1

    # NOP
    dut._log.info(f"20 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCM.value == 12
    assert dut.WA3M.value == 14
    assert dut.Sel14M.value == 1

    # NOP
    dut._log.info(f"24 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCW.value == 12
    assert dut.WA3W.value == 14
    assert dut.WD3.value == 12
    assert dut.OUT.value == 192
    assert dut.PCPrime.value == 192
    assert dut.Sel14W.value == 1

    # LDR R3, [R0, #16] => 3 Array Size
    # 0xE4103010
    dut._log.info(f"192 - LDR R3, [R0, #16] => 3 Array Size")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE4103010
    assert dut.PCF.value == 192

    # LDR R4, [R0, #20] => 24
    # 0xE4104014
    dut._log.info(f"196 - LDR R4, [R0, #20] => 24")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE4104014
    assert dut.PCF.value == 196

    # LDR R2, [R0, #4] => 4
    # 0xE4102004
    dut._log.info(f"200 - LDR R2, [R0, #4] => 4")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE4102004
    assert dut.PCF.value == 200

    # LDR R1, [R0, 0] => 1
    # 0xE4101000
    dut._log.info(f"204 - LDR R1, [R0, 0] => 1")
    await clkedge
    print_all(dut)
    assert dut.InstructionF.value == 0xE4101000
    assert dut.PCF.value == 204

    # NOP
    dut._log.info(f"208 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 208
    assert dut.OUT.value == 3

    # NOP
    dut._log.info(f"212 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 212
    assert dut.OUT.value == 24

    # LDR R5, [R4] => 42 or 2A
    # 0xE4145000
    dut._log.info(f"216 - LDR R5, [R4] => 42 or 2A")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 216
    assert dut.InstructionF.value == 0xE4145000
    assert dut.OUT.value == 4

    # NOP
    dut._log.info(f"220 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 220
    assert dut.OUT.value == 1

    # NOP
    dut._log.info(f"224 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 224

    # ADD R4, R4, R2
    # 0xE0844002
    dut._log.info(f"228 - ADD R4, R4, R2")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 228
    assert dut.InstructionF.value == 0xE0844002

    # SUB R3, R3, #1
    # 0xE0433001
    dut._log.info(f"232 - SUB R3, R3, #1")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 232
    assert dut.InstructionF.value == 0xE0433001
    assert dut.OUT.value == 42

    # ADD R10, R10, R5
    # 0xE08AA005
    dut._log.info(f"236 - ADD R10, R10, R5")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 236
    assert dut.InstructionF.value == 0xE08AA005

    # NOP
    dut._log.info(f"240 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 240

    # NOP
    dut._log.info(f"244 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 244
    assert dut.OUT.value == 28

    # NOP
    dut._log.info(f"248 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 248
    assert dut.OUT.value == 2

    # CMP R3, R0
    # 0xE1430000
    dut._log.info(f"252 - CMP R3, R0")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 252
    assert dut.InstructionF.value == 0xE1430000
    assert dut.OUT.value == 42

    # NOP
    dut._log.info(f"256 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 256

    # NOP
    dut._log.info(f"260 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 260

    # NOP
    dut._log.info(f"264 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 264
    assert dut.ALUOutM.value == 2

    # BEQ to 268 + 8 + 4*7 = 304
    # 0x0A000007
    dut._log.info(f"268 - BEQ to 268 + 8 + 4*7 = 304")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 268
    assert dut.InstructionF.value == 0x0A000006

    # NOP
    dut._log.info(f"272 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 272

    # NOP
    dut._log.info(f"276 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 276

    # NOP
    dut._log.info(f"280 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 280

    # NOP
    dut._log.info(f"284 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 284

    # B to 288 + 8 + 4*-20 = 216
    # 0xEAFFFFEC
    dut._log.info(f"288 - B to 288 + 8 + 4*-20 = 216")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 288
    assert dut.InstructionF.value == 0xEAFFFFEC

    # NOP
    dut._log.info(f"292 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 292

    # NOP
    dut._log.info(f"296 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 296

    # NOP
    dut._log.info(f"300 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 300

    # NOP
    dut._log.info(f"304 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 304
    assert dut.PCPrime.value == 216

    for i in range(41):
        await clkedge
        # dut._log.info(f"PCF: {dut.PCF.value}")
        # print_all(dut)

    assert dut.PCPrime.value == 300

    # ADD R10, R10, R0
    # 0xE08AA000
    dut._log.info(f"300 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 300
    assert dut.InstructionF.value == 0xE08AA000

    # NOP
    dut._log.info(f"304 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 304

    # NOP
    dut._log.info(f"308 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 308

    # BX LR PC = 12
    # 0xE800000E
    dut._log.info(f"312 - BX LR PC = 12")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 312
    assert dut.InstructionF.value == 0xE800000E

    # NOP
    dut._log.info(f"316 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 316
    assert dut.OUT.value == 189

    # NOP
    dut._log.info(f"320 - NOP")
    await clkedge
    assert dut.PCF.value == 320

    # NOP
    dut._log.info(f"324 - NOP")
    await clkedge
    assert dut.PCF.value == 324

    # NOP
    await clkedge
    dut._log.info(f"328 - NOP")
    print_all(dut)
    assert dut.PCF.value == 328
    assert dut.PCPrime.value == 12

    # NOP
    dut._log.info(f"12 - NOP")
    await clkedge
    print_all(dut)
    assert dut.PCF.value == 12

    # NOP


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
