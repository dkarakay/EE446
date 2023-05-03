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
    dut._log.info(f"RA1 {dut.RA1.value}")
    dut._log.info(f"RA2 {dut.RA2.value}")
    dut._log.info(f"RD1 {dut.RD1.value}")
    dut._log.info(f"RD2 {dut.RD2.value}")
    dut._log.info(f"OUT {dut.OUT.value}")
    print('------------------')


'''
@cocotb.test()
async def subroutine_2s_complement(dut):
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

    # LDR R3, R0 => Load from memory location 0 to R3 <== 0x0000000A
    # INSTR = 0xE4103000

    await clkedge
    dut._log.info(f"LDR R3, R0 => Load from memory location 0 to R3 <== 0x0000000A")
    print_all(dut)
    assert dut.INSTR.value == 0xE4103000
    assert dut.PCSrc.value == 0
    assert dut.MemtoReg.value == 1
    assert dut.MemWrite.value == 0
    assert dut.ALUControl.value == 4
    assert dut.ALUSrc.value == 1
    assert dut.ImmSrc.value == 1
    assert dut.RegWrite.value == 1
    assert dut.RegSrc.value == 0

    # SUB R5,R2,R3 => R2 - R3 and store in R5 R2=0 and R3=0x0000000A
    # INSTR = 0xE0425003
    PCSrc = 0
    MemtoReg = 0
    MemWrite = 0
    ALUControl = 2
    ALUSrc = 0
    ImmSrc = 0
    RegWrite = 1
    RegSrc = 0

    await clkedge
    dut._log.info(f"SUB R5,R2,R3 => R2 - R3 and store in R5")
    print_all(dut)
    assert dut.INSTR.value == 0xE0425003
    assert dut.PCSrc.value == PCSrc
    assert dut.MemtoReg.value == MemtoReg
    assert dut.MemWrite.value == MemWrite
    assert dut.ALUControl.value == ALUControl
    assert dut.ALUSrc.value == ALUSrc
    assert dut.ImmSrc.value == ImmSrc
    assert dut.RegWrite.value == RegWrite
    assert dut.RegSrc.value == RegSrc

    # STR R5,[R0,#8] => Store R5 to memory location 8
    # INSTR = 0xE4005008
    PCSrc = 0
    MemtoReg = 0
    MemWrite = 1
    ALUControl = 4
    ALUSrc = 1
    ImmSrc = 1
    RegWrite = 0
    RegSrc = 2

    await clkedge
    dut._log.info(f"STR R5,[R0,#8] => Store R5 to memory location 8")
    print_all(dut)
    assert dut.INSTR.value == 0xE4005008
    assert dut.PCSrc.value == PCSrc
    assert dut.MemtoReg.value == MemtoReg
    assert dut.MemWrite.value == MemWrite
    assert dut.ALUControl.value == ALUControl
    assert dut.ALUSrc.value == ALUSrc
    assert dut.ImmSrc.value == ImmSrc
    assert dut.RegWrite.value == RegWrite
    assert dut.RegSrc.value == RegSrc

    # LDR R2, R0, #8 => Load from memory location 8 to R3 <== 2's complement of 0x0000000A
    # INSTR = 0xE4102008
    PCSrc = 0
    MemtoReg = 1
    MemWrite = 0
    ALUControl = 4
    ALUSrc = 1
    ImmSrc = 1
    RegWrite = 1
    RegSrc = 0

    await clkedge
    dut._log.info(f"LDR R2, R0, #8 => Load from memory location 8 to R3 <== 2's complement of 0x0000000A")
    print_all(dut)
    assert dut.INSTR.value == 0xE4102008
    assert dut.PCSrc.value == PCSrc
    assert dut.MemtoReg.value == MemtoReg
    assert dut.MemWrite.value == MemWrite
    assert dut.ALUControl.value == ALUControl
    assert dut.ALUSrc.value == ALUSrc
    assert dut.ImmSrc.value == ImmSrc
    assert dut.RegWrite.value == RegWrite
    assert dut.RegSrc.value == RegSrc
'''


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

    # Branch to subroutine at address 0x00000100
    # INSTR = 0xEA000004

    await clkedge
    dut._log.info(f"Branch to subroutine at address 0x00000010")
    print_all(dut)

    await clkedge
    dut._log.info(f"LDR R3, R0 => Load from memory location 0 to R3 <== 0x0000000A")
    print_all(dut)

    # SUB R5,R2,R3 => R2 - R3 and store in R5 R2=0 and R3=0x0000000A
    # INSTR = 0xE0425003
    PCSrc = 0
    MemtoReg = 0
    MemWrite = 0
    ALUControl = 2
    ALUSrc = 0
    ImmSrc = 0
    RegWrite = 1
    RegSrc = 0

    await clkedge
    dut._log.info(f"SUB R5,R2,R3 => R2 - R3 and store in R5")
    print_all(dut)
    assert dut.INSTR.value == 0xE0425003
    assert dut.PCSrc.value == PCSrc
    assert dut.MemtoReg.value == MemtoReg
    assert dut.MemWrite.value == MemWrite
    assert dut.ALUControl.value == ALUControl
    assert dut.ALUSrc.value == ALUSrc
    assert dut.ImmSrc.value == ImmSrc
    assert dut.RegWrite.value == RegWrite
    assert dut.RegSrc.value == RegSrc

    # STR R5,[R0,#8] => Store R5 to memory location 8
    # INSTR = 0xE4005008
    PCSrc = 0
    MemtoReg = 0
    MemWrite = 1
    ALUControl = 4
    ALUSrc = 1
    ImmSrc = 1
    RegWrite = 0
    RegSrc = 2

    await clkedge
    dut._log.info(f"STR R5,[R0,#8] => Store R5 to memory location 8")
    print_all(dut)
    assert dut.INSTR.value == 0xE4005008
    assert dut.PCSrc.value == PCSrc
    assert dut.MemtoReg.value == MemtoReg
    assert dut.MemWrite.value == MemWrite
    assert dut.ALUControl.value == ALUControl
    assert dut.ALUSrc.value == ALUSrc
    assert dut.ImmSrc.value == ImmSrc
    assert dut.RegWrite.value == RegWrite
    assert dut.RegSrc.value == RegSrc
    assert dut.RD2.value == 0xFFFFFFF4

    # LDR R2, R0, #8 => Load from memory location 8 to R3 <== 2's complement of 0x0000000A
    # INSTR = 0xE4102008
    PCSrc = 0
    MemtoReg = 1
    MemWrite = 0
    ALUControl = 4
    ALUSrc = 1
    ImmSrc = 1
    RegWrite = 1
    RegSrc = 0

    await clkedge
    dut._log.info(f"LDR R2, R0, #8 => Load from memory location 8 to R3 <== 2's complement of 0x0000000A")
    print_all(dut)
    assert dut.INSTR.value == 0xE4102008
    assert dut.PCSrc.value == PCSrc
    assert dut.MemtoReg.value == MemtoReg
    assert dut.MemWrite.value == MemWrite
    assert dut.ALUControl.value == ALUControl
    assert dut.ALUSrc.value == ALUSrc
    assert dut.ImmSrc.value == ImmSrc
    assert dut.RegWrite.value == RegWrite
    assert dut.RegSrc.value == RegSrc
    assert dut.OUT.value == 0xFFFFFFF4
