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
    # LDR R3, R0 => Load from memory location 0 to R3 Input Number
    # INSTR = 0xE4103000
    await clkedge
    dut._log.info(f"LDR R3, R0 => Load from memory location 0 to R3 Input Number")
    print_all(dut)

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