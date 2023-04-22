import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

'''
@cocotb.test()
async def datapath_general(dut):
    """Setup testbench and run a test."""
    # Generate the clock
    await cocotb.start(Clock(dut.CLK, 10, 'us').start(start_high=False))

    # set clkedge as the falling edge for triggers
    clkedge = FallingEdge(dut.CLK)
    # wait until the falling edge
    await clkedge

    for i in range(4):
        ALUResult = i * 4
        RD2 = 0
        MemWrite = 0
        dut.ALUResult.value = ALUResult
        dut.MemWrite.value = MemWrite
        dut.RD2.value = RD2
        await clkedge

        dut._log.info(f"ReadData {dut.ReadData.value}")
        dut._log.info(f"ALUResult {dut.ALUResult.value}")
        dut._log.info(f"MemWrite {dut.MemWrite.value}")
        dut._log.info(f"RD2 {dut.RD2.value}")

        print('------')

    hex_string = "00a00e00"  # a 32-bit hexadecimal value
    INSTR = int(hex_string, 16)  # convert the hexadecimal string to an integer
    RegWrite = 1
    OUT = 13
    dut.OUT.value = OUT
    dut.INSTR.value = INSTR
    dut.RegWrite.value = RegWrite

    await clkedge

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"INSTR {dut.INSTR.value}")
    dut._log.info(f"RegWrite {dut.RegWrite.value}")

    await clkedge

    print('------')

    hex_string = "00a01e00"  # a 32-bit hexadecimal value
    INSTR = int(hex_string, 16)  # convert the hexadecimal string to an integer
    RegWrite = 1
    OUT = 6
    dut.OUT.value = OUT
    dut.INSTR.value = INSTR
    dut.RegWrite.value = RegWrite

    await clkedge

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"INSTR {dut.INSTR.value}")
    dut._log.info(f"RegWrite {dut.RegWrite.value}")

    await clkedge

    print('------')

    RegWrite = 0
    RA1 = 0
    dut.RegWrite.value = RegWrite
    dut.RA1.value = RA1
    await clkedge

    dut._log.info(f"RegWrite {dut.RegWrite.value}")
    dut._log.info(f"RA1 {dut.RA1.value}")
    dut._log.info(f"RD1 {dut.RD1.value}")
    await clkedge

    print('------')

    RegWrite = 0
    RA1 = 1
    RA2 = 0
    ALUSrc = 0
    ALUControl = 4
    dut.RegWrite.value = RegWrite
    dut.RA1.value = RA1
    dut.RA2.value = RA2
    dut.ALUSrc.value = ALUSrc
    dut.ALUControl.value = ALUControl
    await clkedge

    dut._log.info(f"RD1 {dut.RD1.value}")
    dut._log.info(f"RD2 {dut.RD2.value}")
    dut._log.info(f"SrcB {dut.SrcB.value}")
    dut._log.info(f"ALUControl {dut.ALUControl.value}")
    dut._log.info(f"ALUSrc {dut.ALUSrc.value}")
    dut._log.info(f"ALUResult {dut.ALUResult.value}")
    print('-------  -------')
'''


def print_all(dut):
    dut._log.info(f"INSTR {dut.INSTR.value}")
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
    dut._log.info(f"NewPC {dut.NewPC.value}")
    dut._log.info(f"PCPlus4 {dut.PCPlus4.value}")
    dut._log.info(f"R15 {dut.R15.value}")
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

    # set clkedge as the falling edge for triggers
    clkedge = FallingEdge(dut.CLK)
    # wait until the falling edge
    await clkedge

    dut.RESET.value = 1
    await clkedge
    dut.RESET.value = 0
    print_all(dut)

    # for i in range(4):
    #     ALUResult = i * 4
    #     RD2 = 0
    #     MemWrite = 0
    #     dut.ALUResult.value = ALUResult
    #     dut.MemWrite.value = MemWrite
    #     dut.RD2.value = RD2
    #     await clkedge
    #
    #     dut._log.info(f"ReadData {dut.ReadData.value}")
    #     dut._log.info(f"ALUResult {dut.ALUResult.value}")
    #     dut._log.info(f"MemWrite {dut.MemWrite.value}")
    #     dut._log.info(f"RD2 {dut.RD2.value}")
    #
    #     print('------')
    #
    await clkedge

    # Load from memory location 0 to R3
    dut._log.info(f"------------------")
    dut._log.info(f"Load from memory location 0 to R3")
    INSTR = 0xE4003000
    PCSrc = 0
    MemtoReg = 1
    MemWrite = 0
    ALUControl = 4
    ALUSrc = 1
    ImmSrc = 0b01
    RegWrite = 1
    RegSrc = 0b00

    dut.INSTR.value = INSTR
    dut.PCSrc.value = PCSrc
    dut.MemtoReg.value = MemtoReg
    dut.MemWrite.value = MemWrite
    dut.ALUControl.value = ALUControl
    dut.ALUSrc.value = ALUSrc
    dut.ImmSrc.value = ImmSrc
    dut.RegWrite.value = RegWrite
    dut.RegSrc.value = RegSrc
    await clkedge

    print_all(dut)

    # Load from memory location 1 to R2
    dut._log.info(f"------------------")
    dut._log.info(f"Load from memory location 1 to R2")
    INSTR = 0xE4002004
    PCSrc = 0
    MemtoReg = 1
    MemWrite = 0
    ALUControl = 4
    ALUSrc = 1
    ImmSrc = 0b01
    RegWrite = 1
    RegSrc = 0b00

    dut.INSTR.value = INSTR
    dut.PCSrc.value = PCSrc
    dut.MemtoReg.value = MemtoReg
    dut.MemWrite.value = MemWrite
    dut.ALUControl.value = ALUControl
    dut.ALUSrc.value = ALUSrc
    dut.ImmSrc.value = ImmSrc
    dut.RegWrite.value = RegWrite
    dut.RegSrc.value = RegSrc
    await clkedge

    print_all(dut)

    # Add R2 and R3 and store in R4
    dut._log.info(f"------------------")
    dut._log.info(f"Add R2 and R3 and store in R4")
    INSTR = 0xE4024003
    PCSrc = 0
    MemtoReg = 0
    MemWrite = 0
    ALUControl = 4
    ALUSrc = 0
    ImmSrc = 0
    RegWrite = 1
    RegSrc = 0

    dut.INSTR.value = INSTR
    dut.PCSrc.value = PCSrc
    dut.MemtoReg.value = MemtoReg
    dut.MemWrite.value = MemWrite
    dut.ALUControl.value = ALUControl
    dut.ALUSrc.value = ALUSrc
    dut.ImmSrc.value = ImmSrc
    dut.RegWrite.value = RegWrite
    dut.RegSrc.value = RegSrc
    await clkedge

    print_all(dut)

    # Read R4 to check the result
    dut._log.info(f"------------------")
    dut._log.info(f"Read R4 to check the result")
    INSTR = 0xE4040000
    PCSrc = 0
    MemtoReg = 0
    MemWrite = 0
    ALUControl = 4
    ALUSrc = 0
    ImmSrc = 0
    RegWrite = 0
    RegSrc = 0

    dut.INSTR.value = INSTR
    dut.PCSrc.value = PCSrc
    dut.MemtoReg.value = MemtoReg
    dut.MemWrite.value = MemWrite
    dut.ALUControl.value = ALUControl
    dut.ALUSrc.value = ALUSrc
    dut.ImmSrc.value = ImmSrc
    dut.RegWrite.value = RegWrite
    dut.RegSrc.value = RegSrc
    await clkedge

    print_all(dut)

@cocotb.test()
async def datapath_load_from_memory_add(dut):
    """Setup testbench and run a test."""
    # Generate the clock
    await cocotb.start(Clock(dut.CLK, 10, 'us').start(start_high=False))

    # set clkedge as the falling edge for triggers
    clkedge = FallingEdge(dut.CLK)
    # wait until the falling edge
    await clkedge

    dut.RESET.value = 1
    await clkedge
    dut.RESET.value = 0
    print_all(dut)

    await clkedge
    dut.RESET.value = 1
    await clkedge
    dut.RESET.value = 0
    print_all(dut)

    # for i in range(4):
    #     ALUResult = i * 4
    #     RD2 = 0
    #     MemWrite = 0
    #     dut.ALUResult.value = ALUResult
    #     dut.MemWrite.value = MemWrite
    #     dut.RD2.value = RD2
    #     await clkedge
    #
    #     dut._log.info(f"ReadData {dut.ReadData.value}")
    #     dut._log.info(f"ALUResult {dut.ALUResult.value}")
    #     dut._log.info(f"MemWrite {dut.MemWrite.value}")
    #     dut._log.info(f"RD2 {dut.RD2.value}")
    #
    #     print('------')
    #
    await clkedge

    # LDR R3, R0 => Load from memory location 0 to R3
    dut._log.info(f"------------------")
    dut._log.info(f"LDR R3, R0 => Load from memory location 0 to R3")
    INSTR = 0xE4003000
    PCSrc = 0
    MemtoReg = 1
    MemWrite = 0
    ALUControl = 4
    ALUSrc = 1
    ImmSrc = 0b01
    RegWrite = 1
    RegSrc = 0b00

    dut.INSTR.value = INSTR
    dut.PCSrc.value = PCSrc
    dut.MemtoReg.value = MemtoReg
    dut.MemWrite.value = MemWrite
    dut.ALUControl.value = ALUControl
    dut.ALUSrc.value = ALUSrc
    dut.ImmSrc.value = ImmSrc
    dut.RegWrite.value = RegWrite
    dut.RegSrc.value = RegSrc
    await clkedge

    print_all(dut)

    # LDR R2, R0, #4 => Load from memory location 1 to R2
    dut._log.info(f"------------------")
    dut._log.info(f"LDR R2, R0, #4 => Load from memory location 1 to R2")
    INSTR = 0xE4002004
    PCSrc = 0
    MemtoReg = 1
    MemWrite = 0
    ALUControl = 4
    ALUSrc = 1
    ImmSrc = 0b01
    RegWrite = 1
    RegSrc = 0b00

    dut.INSTR.value = INSTR
    dut.PCSrc.value = PCSrc
    dut.MemtoReg.value = MemtoReg
    dut.MemWrite.value = MemWrite
    dut.ALUControl.value = ALUControl
    dut.ALUSrc.value = ALUSrc
    dut.ImmSrc.value = ImmSrc
    dut.RegWrite.value = RegWrite
    dut.RegSrc.value = RegSrc
    await clkedge

    print_all(dut)

    # ADD R4,R2,R3 => Add R2 and R3 and store in R4
    dut._log.info(f"------------------")
    dut._log.info(f"ADD R4,R2,R3 => Add R2 and R3 and store in R4")
    INSTR = 0xE4024003
    PCSrc = 0
    MemtoReg = 0
    MemWrite = 0
    ALUControl = 4
    ALUSrc = 0
    ImmSrc = 0
    RegWrite = 1
    RegSrc = 0

    dut.INSTR.value = INSTR
    dut.PCSrc.value = PCSrc
    dut.MemtoReg.value = MemtoReg
    dut.MemWrite.value = MemWrite
    dut.ALUControl.value = ALUControl
    dut.ALUSrc.value = ALUSrc
    dut.ImmSrc.value = ImmSrc
    dut.RegWrite.value = RegWrite
    dut.RegSrc.value = RegSrc
    await clkedge

    print_all(dut)

    # Read R4 to check the result
    dut._log.info(f"------------------")
    dut._log.info(f"Read R4 to check the result")
    INSTR = 0xE4040000
    PCSrc = 0
    MemtoReg = 0
    MemWrite = 0
    ALUControl = 4
    ALUSrc = 0
    ImmSrc = 0
    RegWrite = 0
    RegSrc = 0

    dut.INSTR.value = INSTR
    dut.PCSrc.value = PCSrc
    dut.MemtoReg.value = MemtoReg
    dut.MemWrite.value = MemWrite
    dut.ALUControl.value = ALUControl
    dut.ALUSrc.value = ALUSrc
    dut.ImmSrc.value = ImmSrc
    dut.RegWrite.value = RegWrite
    dut.RegSrc.value = RegSrc
    await clkedge

    print_all(dut)

    # SUB R5,R2,R3 => R2 - R3 and store in R5
    dut._log.info(f"------------------")
    dut._log.info(f"SUB R5,R2,R3 => R2 - R3 and store in R5")
    INSTR = 0xE4025003
    PCSrc = 0
    MemtoReg = 0
    MemWrite = 0
    ALUControl = 2
    ALUSrc = 0
    ImmSrc = 0
    RegWrite = 1
    RegSrc = 0

    dut.INSTR.value = INSTR
    dut.PCSrc.value = PCSrc
    dut.MemtoReg.value = MemtoReg
    dut.MemWrite.value = MemWrite
    dut.ALUControl.value = ALUControl
    dut.ALUSrc.value = ALUSrc
    dut.ImmSrc.value = ImmSrc
    dut.RegWrite.value = RegWrite
    dut.RegSrc.value = RegSrc
    await clkedge

    print_all(dut)

    # Read R4 to check the result
    dut._log.info(f"------------------")
    dut._log.info(f"Read R5 to check the result")
    INSTR = 0xE4050000
    PCSrc = 0
    MemtoReg = 0
    MemWrite = 0
    ALUControl = 4
    ALUSrc = 0
    ImmSrc = 0
    RegWrite = 0
    RegSrc = 0

    dut.INSTR.value = INSTR
    dut.PCSrc.value = PCSrc
    dut.MemtoReg.value = MemtoReg
    dut.MemWrite.value = MemWrite
    dut.ALUControl.value = ALUControl
    dut.ALUSrc.value = ALUSrc
    dut.ImmSrc.value = ImmSrc
    dut.RegWrite.value = RegWrite
    dut.RegSrc.value = RegSrc
    await clkedge

    print_all(dut)

    # Read R5 to check the result
    dut._log.info(f"------------------")
    dut._log.info(f"Read R5 to check the result")
    INSTR = 0xE4050000
    PCSrc = 0
    MemtoReg = 0
    MemWrite = 0
    ALUControl = 4
    ALUSrc = 0
    ImmSrc = 0
    RegWrite = 0
    RegSrc = 0

    dut.INSTR.value = INSTR
    dut.PCSrc.value = PCSrc
    dut.MemtoReg.value = MemtoReg
    dut.MemWrite.value = MemWrite
    dut.ALUControl.value = ALUControl
    dut.ALUSrc.value = ALUSrc
    dut.ImmSrc.value = ImmSrc
    dut.RegWrite.value = RegWrite
    dut.RegSrc.value = RegSrc
    await clkedge

    print_all(dut)

