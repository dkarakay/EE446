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
    dut._log.info(f"ALUResult {dut.ALUResult.value}")
    dut._log.info(f"ReadData {dut.ReadData.value}")
    dut._log.info(f"OUT {dut.OUT.value}")
    print('------------------')


@cocotb.test()
async def datapath_load_from_memory_add(dut):
    """Setup testbench and run a test."""
    # Generate the clock
    await cocotb.start(Clock(dut.CLK, 10, 'us').start(start_high=False))

    # set clkedge as the rising edge of the clock
    clkedge = RisingEdge(dut.CLK)
    # wait until the clock edge
    dut.RESET.value = 1
    dut.PCSrc.value = 0
    await clkedge

    dut.RESET.value = 0
    # print_all(dut)

    # LDR R3, R0 => Load from memory location 0 to R3 <== 0x0000000A
    # INSTR = 0xE4003000
    PCSrc = 0
    MemtoReg = 1
    MemWrite = 0
    ALUControl = 4
    ALUSrc = 1
    ImmSrc = 1
    RegWrite = 1
    RegSrc = 0

    dut.PCSrc.value = PCSrc
    dut.MemtoReg.value = MemtoReg
    dut.MemWrite.value = MemWrite
    dut.ALUControl.value = ALUControl
    dut.ALUSrc.value = ALUSrc
    dut.ImmSrc.value = ImmSrc
    dut.RegWrite.value = RegWrite
    dut.RegSrc.value = RegSrc
    await clkedge
    dut._log.info(f"LDR R3, R0 => Load from memory location 0 to R3 <== 0x0000000A")
    print_all(dut)

    # SUB R5,R2,R3 => R2 - R3 and store in R5 R2=0 and R3=0x0000000A
    # INSTR = 0xE4025003
    PCSrc = 0
    MemtoReg = 0
    MemWrite = 0
    ALUControl = 2
    ALUSrc = 0
    ImmSrc = 0
    RegWrite = 1
    RegSrc = 0

    dut.PCSrc.value = PCSrc
    dut.MemtoReg.value = MemtoReg
    dut.MemWrite.value = MemWrite
    dut.ALUControl.value = ALUControl
    dut.ALUSrc.value = ALUSrc
    dut.ImmSrc.value = ImmSrc
    dut.RegWrite.value = RegWrite
    dut.RegSrc.value = RegSrc
    await clkedge
    dut._log.info(f"SUB R5,R2,R3 => R2 - R3 and store in R5")
    print_all(dut)

    # Read R5 to check the result
    # INSTR = 0xE4050000
    PCSrc = 0
    MemtoReg = 0
    MemWrite = 0
    ALUControl = 4
    ALUSrc = 0
    ImmSrc = 0
    RegWrite = 0
    RegSrc = 0

    dut.PCSrc.value = PCSrc
    dut.MemtoReg.value = MemtoReg
    dut.MemWrite.value = MemWrite
    dut.ALUControl.value = ALUControl
    dut.ALUSrc.value = ALUSrc
    dut.ImmSrc.value = ImmSrc
    dut.RegWrite.value = RegWrite
    dut.RegSrc.value = RegSrc
    await clkedge
    dut._log.info(f"Read R5 to check the result")
    print_all(dut)

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

    dut.PCSrc.value = PCSrc
    dut.MemtoReg.value = MemtoReg
    dut.MemWrite.value = MemWrite
    dut.ALUControl.value = ALUControl
    dut.ALUSrc.value = ALUSrc
    dut.ImmSrc.value = ImmSrc
    dut.RegWrite.value = RegWrite
    dut.RegSrc.value = RegSrc
    await clkedge
    dut._log.info(f"STR R5,[R0,#8] => Store R5 to memory location 8")
    print_all(dut)

    # LDR R2, R0, #8 => Load from memory location 8 to R3 <== 2's complement of 0x0000000A
    # INSTR = 0xE4002008
    PCSrc = 0
    MemtoReg = 1
    MemWrite = 0
    ALUControl = 4
    ALUSrc = 1
    ImmSrc = 1
    RegWrite = 1
    RegSrc = 0

    dut.PCSrc.value = PCSrc
    dut.MemtoReg.value = MemtoReg
    dut.MemWrite.value = MemWrite
    dut.ALUControl.value = ALUControl
    dut.ALUSrc.value = ALUSrc
    dut.ImmSrc.value = ImmSrc
    dut.RegWrite.value = RegWrite
    dut.RegSrc.value = RegSrc
    await clkedge
    dut._log.info(f"LDR R2, R0, #8 => Load from memory location 8 to R3 <== 2's complement of 0x0000000A")
    print_all(dut)

    # Read R2 to check the result
    # INSTR = 0xE4020000
    PCSrc = 0
    MemtoReg = 0
    MemWrite = 0
    ALUControl = 4
    ALUSrc = 0
    ImmSrc = 0
    RegWrite = 0
    RegSrc = 0

    dut.PCSrc.value = PCSrc
    dut.MemtoReg.value = MemtoReg
    dut.MemWrite.value = MemWrite
    dut.ALUControl.value = ALUControl
    dut.ALUSrc.value = ALUSrc
    dut.ImmSrc.value = ImmSrc
    dut.RegWrite.value = RegWrite
    dut.RegSrc.value = RegSrc
    await clkedge
    dut._log.info(f"Read R5 to check the result")
    print_all(dut)