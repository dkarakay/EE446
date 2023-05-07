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

    # Check BL
    # Address 0
    # BL 0x00000015 -> PC = 0 + 8 + 21*4 = 92 R14 = 4
    # 0xEB000015
    dut._log.info(f"Test Even Parity of 0x0000000E is 1")
    dut._log.info(f"BL 0x00000015 -> PC = 0 + 8 + 21*4 = 92 R14 = 4")
    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - Branch

    await clkedge
    dut._log.info(f"Cycle 3 - Branch")
    print_all(dut)
    assert dut.INSTR.value == 0xEB000015

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
    dut._log.info(f"Result even Parity of 0x0000000E is {dut.OUT.value}")
    assert dut.OUT.value == 1

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

    # Address 20
    # LDR R2, R0 #4 => Load from memory location 4 to R2 <== 0x00000001
    # INST = 0xE4102004
    await clkedge
    dut._log.info(f"LD R2, R0 #4 => Load from memory location 4 to R2 <== 0x00000001")
    print_all(dut)

    # Address 24
    # CMP R3, R1 => R3 - R1
    # INSTR = 0xE1430001
    await clkedge
    dut._log.info(f"CMP R3, R1 => R3 - R1")
    print_all(dut)

    # Address 28
    # BEQ Branch to subroutine at address 48 if Z flag is set
    # INSTR = 0x0A00000C
    await clkedge
    dut._log.info(f"BEQ Branch to subroutine at address 48 if Z flag is set")
    print_all(dut)

    # Address 32
    # AND R4,R2,R3 => R4 = R2 & R3
    # INSTR = 0xE0024003
    await clkedge
    dut._log.info(f"AND R4,R2,R3 => R4 = R2 & R3")
    print_all(dut)

    # Address 36
    # ADD R5,R5,R4 => R5 = R5 + R4
    # INSTR = 0xE0855004
    await clkedge
    dut._log.info(f"ADD R5,R5,R4 => R5 = R5 + R4")
    print_all(dut)

    # Address 40
    # MOV R3, R3, LSR #1 => R3 = R3 >> 1
    # INSTR = 0xE1A030A3
    await clkedge
    dut._log.info(f"MOV R3, R3, R2 LSL #1 => R3 = R3 << R2")
    print_all(dut)

    # Address 44
    # Branch to subroutine at address 24
    # INSTR = 0xEA000006
    await clkedge
    dut._log.info(f"Branch to subroutine at address 24")
    print_all(dut)

    dut._log.info(
        f"############################################################################################################")

    ############################################################################################################
    for i in range(4):
        await clkedge
        dut._log.info(f"CMP R3, R1 => R3 - R1")
        print_all(dut)

        await clkedge
        dut._log.info(f"BEQ Branch to subroutine at address 48 if Z flag is set")
        print_all(dut)

        if(i == 3):
            # Address 48
            # AND R5,R5,R2 => R5 = R5 & R2
            # INSTR = 0xE0055002
            await clkedge
            dut._log.info(f"AND R5,R5,R2 => R5 = R5 & R2")
            print_all(dut)

            # Address 52
            # STR R5,[R0,#12] => Store R5 to memory location 12
            # INSTR = 0xE400500C
            await clkedge
            dut._log.info(f"STR R5,[R0,#8] => Store R5 to memory location 8")
            print_all(dut)
        else:
            await clkedge
            dut._log.info(f"AND R4,R2,R3 => R4 = R2 & R3")
            print_all(dut)

            await clkedge
            dut._log.info(f"ADD R5,R5,R4 => R5 = R5 + R4")
            print_all(dut)

            await clkedge
            dut._log.info(f"MOV R3, R3, R2 LSL #1 => R3 = R3 << R2")
            print_all(dut)

            await clkedge
            dut._log.info(f"Branch to subroutine at address 24")
            print_all(dut)

    # Address 16
    # LDR R8, R0,12 => Load from memory location 0 to R3 Input Number
    # INSTR = 0xE410800C
    await clkedge
    dut._log.info(f"LDR R8, R0,12 => Load from memory location 0 to R3 Input Number")
    print_all(dut)
    """
