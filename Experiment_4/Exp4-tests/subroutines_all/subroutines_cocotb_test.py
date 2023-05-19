import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


def print_hex_dec(dut, val, name, cond=False, only_hex=False):
    if only_hex:
        my = int(val)
        dut._log.info(f"{name}: H: {my:x}")
        return

    if str(val) != "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx":
        if cond or val != 0:
            my = int(val)
            dut._log.info(f"{name}: D: {my:d} H: {my:x} B: {val}")


## This function prints all the signals in the DUT except the ones that are zero
# @param dut: the DUT
def print_all(dut):
    dut._log.info("CYCLE: " + str(dut.CYCLE.value))
    print_hex_dec(dut, dut.INSTR.value, name="INSTR", only_hex=True)

    print_hex_dec(dut, dut.RESET.value, name="RESET")
    print_hex_dec(dut, dut.PCWrite.value, name="PCWrite")
    print_hex_dec(dut, dut.AdSrc.value, name="AdSrc")
    print_hex_dec(dut, dut.MemWrite.value, name="MemWrite")
    print_hex_dec(dut, dut.IRWrite.value, name="IRWrite")
    print_hex_dec(dut, dut.ResultSrc.value, name="ResultSrc")
    print_hex_dec(dut, dut.ALUControl.value, name="ALUControl")
    print_hex_dec(dut, dut.ALUSrcA.value, name="ALUSrcA")
    print_hex_dec(dut, dut.ALUSrcB.value, name="ALUSrcB")
    print_hex_dec(dut, dut.ImmSrc.value, name="ImmSrc")
    print_hex_dec(dut, dut.RegWrite.value, name="RegWrite")
    print_hex_dec(dut, dut.RegSrc.value, name="RegSrc")
    print_hex_dec(dut, dut.Sel14.value, name="Sel14")

    print_hex_dec(dut, dut.PC.value, name="PC", cond=True)

    print_hex_dec(dut, dut.FlagZ.value, name="FlagZ")
    print_hex_dec(dut, dut.WD3.value, name="WD3")
    print_hex_dec(dut, dut.RA1.value, name="RA1")
    print_hex_dec(dut, dut.RA2.value, name="RA2")
    print_hex_dec(dut, dut.RA3.value, name="RA3")
    print_hex_dec(dut, dut.RD1.value, name="RD1")
    print_hex_dec(dut, dut.RD2.value, name="RD2")
    print_hex_dec(dut, dut.ALUResult.value, name="ALUResult")
    print_hex_dec(dut, dut.ALUOut.value, name="ALUOut")

    print_hex_dec(dut, dut.OUT.value, name="OUT", cond=True)
    print("------------------")


# Fetch and decode cycles
async def fetch_and_decode(dut, clkedge, skip_print=True):
    # Cycle 1 - Fetch

    await clkedge
    if not skip_print:
        dut._log.info(f"Cycle 1 - Fetch")
        print_all(dut)

    # Cycle 2 - Decode
    await clkedge
    if not skip_print:
        dut._log.info(f"Cycle 2 - Decode")
        print_all(dut)


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
    dut.RESET.value = 1
    await clkedge
    print_all(dut)
    dut.RESET.value = 0

    ############################### 2's complement ###############################

    # Check BL
    # Address 00
    # BL 0x00000002 -> PC = 0 + 8 + 2*4 = 16 R14 = 4
    # 0xEB000002
    dut._log.info(f"2's complement of 7 in subroutine")
    dut._log.info(f"BL 0x00000002 -> PC = 0 + 8 + 2*4 = 16 R14 = 4")
    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - Branch

    await clkedge
    dut._log.info(f"Cycle 3 - Branch")
    print_all(dut)
    assert dut.INSTR.value == 0xEB000002

    # Cycle 4 - Branch
    await clkedge
    dut._log.info(f"Cycle 4 - Branch")
    print_all(dut)
    assert dut.PC.value == 16

    # Cycle 5 - Branch
    await clkedge
    dut._log.info(f"Cycle 5 - Branch")
    print_all(dut)

    # Check LDR
    # Address 16
    # LDR R3, [R0, #180] => 7
    # 0xE41030B4

    dut._log.info(f"LDR R3, [R0, #180] => 7")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - MemAddr
    await clkedge
    dut._log.info(f"Cycle 3 - MemAddr")
    print_all(dut)
    assert dut.ALUResult.value == 180
    assert dut.OUT.value == dut.PC.value + 4

    # Cycle 4 - MemRead
    await clkedge
    dut._log.info(f"Cycle 4 - MemRead")
    print_all(dut)
    assert dut.ALUResult.value == 180

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)
    assert dut.OUT.value == 7

    # Check SUB operation
    # Address 20
    # SUB R12, R0, R3 -> R12 = 0-7 = -7 in 2's complement = 0xFFFFFFF9
    # 0xE040C003
    dut._log.info(f"SUB R12, R0, R3 -> R12 = 0-7 = -7 in 2's complement = 0xFFFFFFF9")

    # Fetch and decode cycles
    await fetch_and_decode(dut, clkedge, skip_print=True)

    # Cycle 3 - Execute
    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE040C003

    # Cycle 4 - ALUWriteBack
    await clkedge
    dut._log.info(f"Cycle 4 - ALUWriteBack")
    print_all(dut)
    dut._log.info(f"2's complement of 7 = {dut.OUT.value}")
    assert dut.OUT.value == 0xFFFFFFF9

    # Cycle 5 - Wait
    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)

    # Check BX LR
    # Address 24
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

    ############################## Even Parity ##############################

    # Check BL
    # Address 0
    # BL 0x00000014 -> PC = 4 + 8 + 20*4 = 92 R14 = 8
    # 0xEB000014
    dut._log.info(f"Test Even Parity of 0x0000000E in subroutine")
    dut._log.info(f"BL 0x00000015 -> PC = 4 + 8 + 20*4 = 92 R14 = 8")
    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - Branch

    await clkedge
    dut._log.info(f"Cycle 3 - Branch")
    print_all(dut)
    assert dut.INSTR.value == 0xEB000014

    # Cycle 4 - Branch
    await clkedge
    dut._log.info(f"Cycle 4 - Branch")
    print_all(dut)
    assert dut.PC.value == 92

    # Cycle 5 - Branch
    await clkedge
    dut._log.info(f"Cycle 5 - Branch")
    print_all(dut)

    # Check LDR
    # Address 92
    # LDR R3, [R0, #188] => F
    # 0xE41030BC

    dut._log.info(f"LDR R3, [R0, #188] => F")

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
    assert dut.PC.value == 8

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)

    ############################## Array Sum #####################################

    # Check BL
    # Address 0
    # BL 0x00000004 -> PC = 8 + 8 + 4*4 = 32 R14 = 12
    # 0xEB000004
    dut._log.info("Array Sum Test for 3 elements in array")
    dut._log.info(f"(2A), (37), (5C) = 0xBD or in decimal 189")
    dut._log.info(f"BL 0x00000006 -> PC = 0 + 8 + 6*4 = 32 R14 = 4")
    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - Branch

    await clkedge
    dut._log.info(f"Cycle 3 - Branch")
    print_all(dut)
    assert dut.INSTR.value == 0xEB000004

    # Cycle 4 - Branch
    await clkedge
    dut._log.info(f"Cycle 4 - Branch")
    print_all(dut)
    assert dut.PC.value == 32

    # Cycle 5 - Branch
    await clkedge
    dut._log.info(f"Cycle 5 - Branch")
    print_all(dut)

    # Check LDR
    # Address 32
    # LDR R1, [R0, #192] => 1
    # 0xE41010C0

    dut._log.info(f"LDR R1, [R0, #192] => 1")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - MemAddr
    await clkedge
    dut._log.info(f"Cycle 3 - MemAddr")
    print_all(dut)
    assert dut.INSTR.value == 0xE41010C0

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
    # Address 36
    # LDR R3, [R0, #196] => 3 Load Array Size
    # 0xE41030C4

    dut._log.info(f"LDR R3, [R0, #196] => 3 Load Array Size")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - MemAddr
    await clkedge
    dut._log.info(f"Cycle 3 - MemAddr")
    print_all(dut)
    assert dut.INSTR.value == 0xE41030C4

    # Cycle 4 - MemRead
    await clkedge
    dut._log.info(f"Cycle 4 - MemRead")
    print_all(dut)
    assert dut.ALUResult.value == 196

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)
    assert dut.OUT.value == 3

    # Check LDR
    # Address 40
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

    # Check LDR
    # Address 44
    # LDR R4, [R0, #204] => 208
    # 0xE41040CC

    dut._log.info(f"LDR R4, [R0, #140] => 208")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - MemAddr
    await clkedge
    dut._log.info(f"Cycle 3 - MemAddr")
    print_all(dut)
    assert dut.INSTR.value == 0xE41040CC

    # Cycle 4 - MemRead
    await clkedge
    dut._log.info(f"Cycle 4 - MemRead")
    print_all(dut)
    assert dut.ALUResult.value == 204

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)
    assert dut.OUT.value == 208

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
    assert dut.ALUResult.value == 208

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)
    assert dut.OUT.value == 42

    # Address 52
    # ADD R4, R4, R2 => 212
    # 0xE0844002

    dut._log.info(f"ADD R4, R4, R2 => 212")

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
    assert dut.OUT.value == 212

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
        # dut._log.info(f"Cycle {i} - Wait")
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
    assert dut.PC.value == 12

    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)

    # Address 4
    # ADD R10,R10,R0 => 189 (0xBD)
    # 0xE08AA000


    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE08AA000

    await clkedge
    dut._log.info(f"Cycle 4 - Execute")
    print_all(dut)
    dut._log.info(f"ADD R10,R10,R0 => {dut.OUT.value} (0xBD) Check the sum of the array")
    assert dut.OUT.value == 189

    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)
