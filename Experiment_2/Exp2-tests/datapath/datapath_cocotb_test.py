import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

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
    #print_all(dut)

    # LDR R3, R0 => Load from memory location 0 to R3
    PCSrc = 0
    MemtoReg = 1
    MemWrite = 0
    ALUControl = 4
    ALUSrc = 1
    ImmSrc = 0b01
    RegWrite = 1
    RegSrc = 0b00

    dut.PCSrc.value = PCSrc
    dut.MemtoReg.value = MemtoReg
    dut.MemWrite.value = MemWrite
    dut.ALUControl.value = ALUControl
    dut.ALUSrc.value = ALUSrc
    dut.ImmSrc.value = ImmSrc
    dut.RegWrite.value = RegWrite
    dut.RegSrc.value = RegSrc
    await clkedge
    dut._log.info(f"LDR R3, R0 => Load from memory location 0 to R3")
    print_all(dut)

    # LDR R2, R0, #4 => Load from memory location 1 to R2
    PCSrc = 0
    MemtoReg = 1
    MemWrite = 0
    ALUControl = 4
    ALUSrc = 1
    ImmSrc = 0b01
    RegWrite = 1
    RegSrc = 0b00

    dut.PCSrc.value = PCSrc
    dut.MemtoReg.value = MemtoReg
    dut.MemWrite.value = MemWrite
    dut.ALUControl.value = ALUControl
    dut.ALUSrc.value = ALUSrc
    dut.ImmSrc.value = ImmSrc
    dut.RegWrite.value = RegWrite
    dut.RegSrc.value = RegSrc
    await clkedge
    dut._log.info(f"LDR R2, R0, #4 => Load from memory location 1 to R2")
    print_all(dut)

    # ADD R4,R2,R3 => Add R2 and R3 and store in R4
    PCSrc = 0
    MemtoReg = 0
    MemWrite = 0
    ALUControl = 4
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
    dut._log.info(f"ADD R4,R2,R3 => Add R2 and R3 and store in R4")
    print_all(dut)

    # Read R4 to check the result
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
    assert dut.OUT.value == 9
    await clkedge
    dut._log.info(f"Read R4 to check the result")
    print_all(dut)

    # SUB R5,R2,R3 => R2 - R3 and store in R5
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
    assert dut.OUT.value == 1
    await clkedge
    dut._log.info(f"Read R5 to check the result")
    print_all(dut)

    # AND R1,R2,R3 => R2 & R3 and store in R1
    # INSTR = 0xE4021003
    PCSrc = 0
    MemtoReg = 0
    MemWrite = 0
    ALUControl = 0
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
    dut._log.info(f"AND R1,R2,R3 => R2 & R3 and store in R1")
    print_all(dut)

    # Read R1 to check the result
    # INSTR = 0xE4010000
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
    assert dut.OUT.value == 4
    dut._log.info(f"Read R1 to check the result")
    print_all(dut)

    # ORR R6,R2,R3 => R2 | R3 and store in R6
    # INSTR = 0xE4026003
    PCSrc = 0
    MemtoReg = 0
    MemWrite = 0
    ALUControl = 12
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
    dut._log.info(f"ORR R6,R2,R3 => R2 | R3 and store in R6")
    print_all(dut)

    # Read R6 to check the result
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
    dut._log.info(f"Read R6 to check the result")
    print_all(dut)

    # STR R6,[R0] => Store R6 to memory location 0
    #INSTR = 0xE4006000
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
    dut._log.info(f"STR R6,[R0] => Store R6 to memory location 0")
    print_all(dut)

    # LDR R8, R0 => Load from memory location 0 to R8
    #INSTR = 0xE4008000
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
    dut._log.info(f"LDR R8, R0 => Load from memory location 0 to R8")
    print_all(dut)
    assert dut.OUT.value == 5

    # MOV R7, R8 => Move R8 to R7
    #INSTR = 0xE4007008
    PCSrc = 0
    MemtoReg = 0
    MemWrite = 0
    ALUControl = 13
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
    dut._log.info(f"MOV R7, R8 => Move R8 to R7")
    print_all(dut)

    # Read R7 to check the result
    #INSTR = 0xE4070000
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
    dut._log.info(f"Read R7 to check the result")
    assert dut.OUT.value == 5
    print_all(dut)

    # Branch Instruction to PC => 40
    #INSTR = 0xEA00000A
    PCSrc = 1
    MemtoReg = 0
    MemWrite = 0
    ALUControl = 13
    ALUSrc = 1
    ImmSrc = 2
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
    dut._log.info(f"Branch Instruction to PC => 40")
    print_all(dut)

    # Read R6 to check the result from instruction 36

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
    dut._log.info(f"Read R6 to check the result from instruction 36")

    print_all(dut)
