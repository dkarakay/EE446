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
async def fetch_and_decode(dut, clkedge, skip_print=False):
    # Cycle 1 - Fetch

    await clkedge
    if not skip_print:
        dut._log.info(f"Cycle 1 - Fetch")
        print_all(dut)
    # assert dut.ALUResult.value == dut.PC.value + 4
    # assert dut.OUT.value == dut.ALUResult.value

    # Cycle 2 - Decode
    await clkedge
    if not skip_print:
        dut._log.info(f"Cycle 2 - Decode")
        print_all(dut)
    # assert dut.ALUResult.value == dut.PC.value + 4
    # assert dut.OUT.value == dut.ALUResult.value


@cocotb.test()
async def main_cocotb_test(dut):
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
    # Check LDR
    # LDR R3, [R0, #124] => 17
    # 0xE410307C

    dut._log.info(f"LDR R3, [R0, #124] => 17")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - MemAddr
    await clkedge
    dut._log.info(f"Cycle 3 - MemAddr")
    print_all(dut)
    assert dut.ALUResult.value == 124
    assert dut.OUT.value == dut.PC.value + 4

    # Cycle 4 - MemRead
    await clkedge
    dut._log.info(f"Cycle 4 - MemRead")
    print_all(dut)
    assert dut.ALUResult.value == 124

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)
    assert dut.OUT.value == 17

    # Check LDR
    # Address 4
    # LDR R1, [R0, #128] => R1 = 5
    # 0xE4101080

    dut._log.info(f"LDR R1, [R0, #128] => R1 = 5")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - MemAddr
    await clkedge
    dut._log.info(f"Cycle 3 - MemAddr")
    print_all(dut)
    assert dut.ALUResult.value == 128

    # Cycle 4 - MemRead
    await clkedge
    dut._log.info(f"Cycle 4 - MemRead")
    print_all(dut)

    # Cycle 5 - WriteBack
    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)

    # Check ADD operation
    # Address 8
    # ADD R6, R3, R1 -> R6 = 22 (17 + 5)
    # 0xE0836001
    dut._log.info(f"ADD R6, R3, R1 -> R6 = 22 (17 + 5)")

    # Fetch and decode cycles
    await fetch_and_decode(dut, clkedge, skip_print=True)

    # Cycle 3 - Execute
    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE0836001

    # Cycle 4 - ALUWriteBack
    await clkedge
    dut._log.info(f"Cycle 4 - ALUWriteBack")
    print_all(dut)
    assert dut.OUT.value == 22

    # Cycle 5 - Wait
    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)

    # Check SUB operation
    # Address 12
    # SUB R7, R6, R3 -> R7 = 5 (22 - 17)
    # 0xE0467003
    dut._log.info(f"SUB R7, R6, R3 -> R7 = 5 (22 - 17)")

    # Fetch and decode cycles
    await fetch_and_decode(dut, clkedge, skip_print=True)

    # Cycle 3 - Execute
    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE0467003

    # Cycle 4 - ALUWriteBack
    await clkedge
    dut._log.info(f"Cycle 4 - ALUWriteBack")
    print_all(dut)
    assert dut.OUT.value == 5

    # Cycle 5 - Wait
    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)

    # Check AND operation
    # Address 16
    # AND R8, R3, R1 -> R8 = 1 (0001 & 10001)
    # 0xE0038001
    dut._log.info(f"AND R8, R3, R1 -> R8 = 1 (0001 & 10001)")

    # Fetch and decode cycles
    await fetch_and_decode(dut, clkedge, skip_print=True)

    # Cycle 3 - Execute
    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE0038001

    # Cycle 4 - ALUWriteBack
    await clkedge
    dut._log.info(f"Cycle 4 - ALUWriteBack")
    print_all(dut)
    assert dut.OUT.value == 1

    # Cycle 5 - Wait
    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)

    # Check ORR operation
    # Address 20
    # ORR R9, R3, R1 -> R9 = 21 (0001 | 10001)
    # 0xE1039001
    dut._log.info(f"ORR R9, R3, R1 -> R9 = 21 (0001 | 10001)")

    # Fetch and decode cycles
    await fetch_and_decode(dut, clkedge, skip_print=True)

    # Cycle 3 - Execute
    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE1039001

    # Cycle 4 - ALUWriteBack
    await clkedge
    dut._log.info(f"Cycle 4 - ALUWriteBack")
    print_all(dut)
    assert dut.OUT.value == 21

    # Cycle 5 - Wait
    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)

    # Check MOV operation
    # Address 24
    # MOV R10, R3 -> R10 = 17
    # 0xE400A003
    dut._log.info(f"MOV R10, R3 -> R10 = 17")

    # Fetch and decode cycles
    await fetch_and_decode(dut, clkedge, skip_print=True)

    # Cycle 3 - Execute
    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE400A003

    # Cycle 4 - ALUWriteBack
    await clkedge
    dut._log.info(f"Cycle 4 - ALUWriteBack")
    print_all(dut)
    assert dut.OUT.value == 17

    # Cycle 5 - Wait
    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)

    # Check STR operation
    # Address 28
    # STR R3, [R0, #132] -> MEM[132] = 17
    # 0xE4003084
    dut._log.info(f"STR R3, [R0, #132] -> MEM[132] = 17")

    # Fetch and decode cycles
    await fetch_and_decode(dut, clkedge, skip_print=True)

    # Cycle 3 - MemAdr
    await clkedge
    dut._log.info(f"Cycle 3 - MemAdr")
    print_all(dut)
    assert dut.INSTR.value == 0xE4003084

    # Cycle 4 - MemWrite
    await clkedge
    dut._log.info(f"Cycle 4 - MemWrite")
    print_all(dut)

    # Cycle 5 - Wait
    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)

    # Check LDR
    # Address 32
    # LDR R10, [R0, #132] -> R10 = 17
    # 0xE410A084

    dut._log.info(f"LDR R10, [R0, #132] -> R10 = 17")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - MemAddr

    await clkedge
    dut._log.info(f"Cycle 3 - MemAddr")
    print_all(dut)
    assert dut.ALUResult.value == 132
    assert dut.INSTR.value == 0xE410A084

    # Cycle 4 - MemRead

    await clkedge
    dut._log.info(f"Cycle 4 - MemRead")
    print_all(dut)

    # Cycle 5 - WriteBack

    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)
    """
    # Check B
    # Address 36
    # B 0x00000003 -> PC = (36 + 8) + 3*4 = 56
    # 0xEA000003

    dut._log.info(f"B 0x00000003 -> PC = (36 + 8) + 3*4 = 56")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge, branch=True, skip_print=False)

    # Cycle 3 - Branch
    ALUSrcB = 1
    ALUControl = 4
    ImmSrc = 2
    ResultSrc = 2
    RegSrc = 1
    PCWrite = 1

    write_data(
        dut,
        ALUSrcB=ALUSrcB,
        ALUControl=ALUControl,
        ImmSrc=ImmSrc,
        ResultSrc=ResultSrc,
        RegSrc=RegSrc,
        PCWrite=PCWrite,
    )

    await clkedge
    dut._log.info(f"Cycle 3 - Branch")
    print_all(dut)
    assert dut.INSTR.value == 0xEA000003

    # Cycle 4 - Branch
    write_data(dut)
    await clkedge
    dut._log.info(f"Cycle 4 - Branch")
    print_all(dut)

    # Cycle 5 - Branch
    write_data(dut)
    await clkedge
    dut._log.info(f"Cycle 5 - Branch")
    print_all(dut)

    # Check CMP
    # Address 56
    # CMP R3, R10 -> R3 - R10 = 0
    # 0xE143000A

    dut._log.info(f"CMP R3, R10 -> R3 - R10 = 0")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - Execute
    ResultSrc = 1
    ALUControl = 2

    write_data(dut, ResultSrc=ResultSrc, ALUControl=ALUControl)

    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE143000A

    write_data(dut, ResultSrc=ResultSrc, ALUControl=ALUControl)

    await clkedge
    dut._log.info(f"Cycle 4 - Wait")
    print_all(dut)
    assert dut.INSTR.value == 0xE143000A
    assert dut.FlagZ.value == 1

    write_data(dut, ResultSrc=ResultSrc, ALUControl=ALUControl)

    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)
    assert dut.INSTR.value == 0xE143000A

    # Check BL
    # Address 60
    # BL 0x00000002 -> PC = 60 + 8 + 2*4 = 76 R14 = 64
    # 0xEB000002

    dut._log.info(f"BL 0x00000002 -> PC = 60 + 8 + 2*4 = 76 R14 = 64")
    # Fetch and decode
    await fetch_and_decode(dut, clkedge, branch=True, skip_print=False)

    # Cycle 3 - Branch
    ALUSrcB = 1
    ALUControl = 4
    ImmSrc = 2
    ResultSrc = 2
    RegSrc = 1
    PCWrite = 1
    RegWrite = 1
    Sel14 = 1

    write_data(
        dut,
        ALUSrcB=ALUSrcB,
        ALUControl=ALUControl,
        ImmSrc=ImmSrc,
        ResultSrc=ResultSrc,
        RegSrc=RegSrc,
        PCWrite=PCWrite,
        RegWrite=RegWrite,
        Sel14=Sel14,
    )

    await clkedge
    dut._log.info(f"Cycle 3 - Branch")
    print_all(dut)
    assert dut.INSTR.value == 0xEB000002

    # Cycle 4 - Branch
    write_data(dut)
    await clkedge
    dut._log.info(f"Cycle 4 - Branch")
    print_all(dut)

    # Cycle 5 - Branch
    write_data(dut)
    await clkedge
    dut._log.info(f"Cycle 5 - Branch")
    print_all(dut)

    # Check BX LR
    # Address 76
    # BX LR -> PC = 64
    # 0xE800000E

    dut._log.info(f"BX LR -> PC = 64")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - Execute
    ResultSrc = 2
    ALUControl = 13
    PCWrite = 1

    write_data(dut, ResultSrc=ResultSrc, ALUControl=ALUControl, PCWrite=PCWrite)

    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE800000E

    write_data(dut, ResultSrc=ResultSrc, ALUControl=ALUControl)

    await clkedge
    dut._log.info(f"Cycle 4 - Wait")
    print_all(dut)

    write_data(dut, ResultSrc=ResultSrc, ALUControl=ALUControl)

    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)

    # Check ADD
    # Address 64
    # ADD R11, R6, R1 -> R11 = 22 + 5 = 27
    # 0xE086B001

    dut._log.info(f"ADD R11, R6, R1 -> R11 = 22 + 5 = 27")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - Execute
    ResultSrc = 1
    ALUControl = 4

    write_data(dut, ResultSrc=ResultSrc, ALUControl=ALUControl)

    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE086B001

    # Cycle 4 - ALUWriteBack
    RegWrite = 1
    write_data(dut, RegWrite=RegWrite)
    await clkedge
    dut._log.info(f"Cycle 4 - ALUWriteBack")
    print_all(dut)
    assert dut.OUT.value == 27

    # Cycle 5 - Wait
    write_data(dut)
    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)

    # Check BL
    # Address 68
    # BL 0x00000003 -> PC = 68 + 8 + 3*4 = 88 R14 = 72
    # 0xEB000003

    dut._log.info(f"BL 0x00000003 -> PC = 68 + 8 + 3*4 = 88 R14 = 72")
    # Fetch and decode
    await fetch_and_decode(dut, clkedge, branch=True)

    # Cycle 3 - Branch
    ALUSrcB = 1
    ALUControl = 4
    ImmSrc = 2
    ResultSrc = 2
    RegSrc = 1
    PCWrite = 1
    RegWrite = 1
    Sel14 = 1

    write_data(
        dut,
        ALUSrcB=ALUSrcB,
        ALUControl=ALUControl,
        ImmSrc=ImmSrc,
        ResultSrc=ResultSrc,
        RegSrc=RegSrc,
        PCWrite=PCWrite,
        RegWrite=RegWrite,
        Sel14=Sel14,
    )

    await clkedge
    dut._log.info(f"Cycle 3 - Branch")
    print_all(dut)
    assert dut.INSTR.value == 0xEB000003

    # Cycle 4 - Branch
    write_data(dut)
    await clkedge
    dut._log.info(f"Cycle 4 - Branch")
    print_all(dut)
    assert dut.PC.value == 88

    # Cycle 5 - Branch
    write_data(dut)
    await clkedge
    dut._log.info(f"Cycle 5 - Branch")
    print_all(dut)

    # Check ADD
    # Address 88
    # ADD R11, R6, R1 -> R11 = 22 + 5 = 27
    # 0xE086B001

    dut._log.info(f"ADD R11, R6, R1 -> R11 = 22 + 5 = 27")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - Execute
    ResultSrc = 1
    ALUControl = 4

    write_data(dut, ResultSrc=ResultSrc, ALUControl=ALUControl)

    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE086B001

    # Cycle 4 - ALUWriteBack
    RegWrite = 1
    write_data(dut, RegWrite=RegWrite)
    await clkedge
    dut._log.info(f"Cycle 4 - ALUWriteBack")
    print_all(dut)
    assert dut.OUT.value == 27

    # Cycle 5 - Wait
    write_data(dut)
    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)

    # Check BX LR
    # Address 76
    # BX LR -> PC = 72
    # 0xE800000E

    dut._log.info(f"BX LR -> PC = 72")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - Execute
    ResultSrc = 2
    ALUControl = 13
    PCWrite = 1

    write_data(dut, ResultSrc=ResultSrc, ALUControl=ALUControl, PCWrite=PCWrite)

    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE800000E

    write_data(dut, ResultSrc=ResultSrc, ALUControl=ALUControl)

    await clkedge
    dut._log.info(f"Cycle 4 - Wait")
    print_all(dut)
    assert dut.PC.value == 72

    write_data(dut, ResultSrc=ResultSrc, ALUControl=ALUControl)

    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)
    """
