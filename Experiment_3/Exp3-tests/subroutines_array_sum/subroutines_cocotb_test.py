import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


def print_all(dut):
    dut._log.info(f"INSTR {dut.INSTR.value}")

    my_signal_value = int(dut.INSTR.value)
    dut._log.info(f"INST (HEX): {my_signal_value:x}")

    dut._log.info(f"PCSrc {dut.PCSrc.value}")
    dut._log.info(f"RESET {dut.RESET.value}")
    dut._log.info(f"MemtoReg {dut.MemtoReg.value}")
    dut._log.info(f"MemWrite {dut.MemWrite.value}")
    dut._log.info(f"ALUControl {dut.ALUControl.value}")
    dut._log.info(f"ALUSrc {dut.ALUSrc.value}")
    dut._log.info(f"ImmSrc {dut.ImmSrc.value}")
    dut._log.info(f"RegWrite {dut.RegWrite.value}")
    dut._log.info(f"RegSrc {dut.RegSrc.value}")

    dut._log.info(f"------------------")
    dut._log.info(f"PC {dut.PC.value}")
    my_signal_value = int(dut.PC.value)
    dut._log.info(f"PC (DEC): {my_signal_value:d}")
    dut._log.info(f"RA1 {dut.RA1.value}")
    dut._log.info(f"RA2 {dut.RA2.value}")
    dut._log.info(f"RD1 {dut.RD1.value}")
    dut._log.info(f"RD2 {dut.RD2.value}")
    dut._log.info(f"FlagZ {dut.FlagZ.value}")
    dut._log.info(f"CONDEX {dut.CONDEX.value}")
    dut._log.info(f"OUT {dut.OUT.value}")
    my_signal_value = int(dut.OUT.value)
    dut._log.info(f"OUT (DEC): {my_signal_value:d}")
    dut._log.info(f"ALUResult {dut.ALUResult.value}")
    print('------------------')


@cocotb.test()
async def subroutine_2s_complement_using_branch(dut):
    """Setup testbench and run a test."""
    # Generate the clock
    await cocotb.start(Clock(dut.CLK, 10, 'us').start(start_high=False))

    # set clkedge as the rising edge of the clock
    clkedge = RisingEdge(dut.CLK)
    # wait until the clock edge

    dut.RESET.value = 1
    await clkedge

    dut.RESET.value = 0
    # print_all(dut)
    dut._log.info(f"Summing values at position 16, 20, 24 namely 04 (04), 2A (42), 37 (55) and 5C (92)")

    # Branch to subroutine at address 0x00000100
    # INSTR = 0xEA000004
    await clkedge
    dut._log.info(f"Branch to subroutine at address 0x00000010")
    print_all(dut)

    # Address 16
    # LDR R3, R0 => Load from memory location 0 to R3 <== 0x00000003 Array size
    # INSTR = 0xE4103000
    await clkedge
    dut._log.info(f"LDR R3, R0 => Load from memory location 0 to R3 <== 0x00000003 Array size")
    print_all(dut)

    # Address 20
    # LDR R2, R0 #4 => Load from memory location 4 to R2 <== 0x00000001
    # INST = 0xE4102004
    await clkedge
    dut._log.info(f"LD R2, R0 #4 => Load from memory location 4 to R2 <== 0x00000001")
    print_all(dut)

    # Address 24
    # LDR R5, R0 #12 => Load from memory location 12 to R5 <== 0x00000010 Base Address
    # INST = 0xE410500C
    await clkedge
    dut._log.info(f"LDR R5, R0 #12 => Load from memory location 12 to R5 <== 0x00000010 Base Address")
    print_all(dut)

    # Address 28
    # LDR R7 R0 #16 => Load from memory location 16 to R7 <== 0x0000000C
    # INST = 0xE4107010
    await clkedge
    dut._log.info(f"LDR R7 R0 #16 => Load from memory location 16 to R7 <== 0x0000000C")
    print_all(dut)

    # Address 32
    # LDR R4, R5 #0 => Load from memory location 0 to R4 <== 0x00000005 Start of array address
    # INST = 0xE4154000
    await clkedge
    dut._log.info(f"LDR R4, R5 #0 => Load from memory location 0 to R4 <== 0x00000005 Start of array address")
    print_all(dut)

    # Address 36
    # ADD R6, R4, R6 => R6 = R4 + R6 SUM
    # INSTR = 0xE0846006
    await clkedge   
    dut._log.info(f"ADD R6, R4, R6 => R6 = R4 + R6 SUM")
    print_all(dut)

    # Address 40
    # ADD R5. R5, R7 => R5 = R5 + R7
    # INSTR = 0xE0855007
    await clkedge
    dut._log.info(f"ADD R5. R5, R7 => R5 = R5 + R7")
    print_all(dut)

    # Address 44
    # SUB R3, R3, R2 => R3 - R2 and store in R3
    # INSTR = 0xE0433002
    await clkedge
    dut._log.info(f"SUB R3, R3, R2 => R3 - R2 and store in R3")
    print_all(dut)

    # Address 48
    # CMP R3, R1 => R3 - R1
    # INSTR = 0xE1430001
    await clkedge
    dut._log.info(f"CMP R3, R1 => R3 - R1")
    print_all(dut)

    # Address 52
    # BEQ Branch to subroutine at address 0x00000004 if Z flag is set
    # INSTR = 0x0A000001
    await clkedge
    dut._log.info(f"BEQ Branch to subroutine at address 0x00000004 if Z flag is set")
    print_all(dut)

    # Address 56
    # Branch to subroutine at address 0x0000001C
    # INSTR = 0xEA000008
    await clkedge
    dut._log.info(f"Branch to subroutine at address 0x00000010")
    print_all(dut)

    dut._log.info(f"############################################################################################################")

############################################################################################################
    for i in range(3):
        await clkedge
        dut._log.info(f"LDR R4, R5 #0 => Load from memory location 0 to R4 <== 0x00000005 Start of array address")
        print_all(dut)

        await clkedge
        dut._log.info(f"ADD R6, R4, R6 => R6 = R4 + R6 SUM")
        print_all(dut)

        await clkedge
        dut._log.info(f"ADD R5. R5, R7 => R5 = R5 + R7")
        print_all(dut)

        await clkedge
        dut._log.info(f"SUB R3, R3, R2 => R3 - R2 and store in R3")
        print_all(dut)

        await clkedge
        dut._log.info(f"CMP R3, R1 => R3 - R1")
        print_all(dut)

        await clkedge
        dut._log.info(f"BEQ Branch to subroutine at address 0x00000004 if Z flag is set")
        print_all(dut)

        if i == 0 or i == 1:
            await clkedge
            dut._log.info(f"Branch to subroutine at address 0x00000010")
            print_all(dut)
        else:
            await clkedge
            dut._log.info(f"Check PC value to see if it is 0x00000004 and result should be 193")
            print_all(dut)
            assert dut.OUT.value == 193





