import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


def print_hex_dec(dut, val, cond=False):
    if cond or val != 0:
        my_signal_value = int(val)
        dut._log.info(f"{val} (HEX): {my_signal_value:x} (DEC): {my_signal_value}")


## This function prints all the signals in the DUT except the ones that are zero
# @param dut: the DUT
def print_all(dut):
    print_hex_dec(dut, dut.INSTR.value, cond=True)

    print_hex_dec(dut, dut.RESET.value)
    print_hex_dec(dut, dut.PCWrite.value)
    print_hex_dec(dut, dut.AdSrc.value)
    print_hex_dec(dut, dut.MemWrite.value)
    print_hex_dec(dut, dut.IRWrite.value)
    print_hex_dec(dut, dut.ResultSrc.value)
    print_hex_dec(dut, dut.ALUControl.value)
    print_hex_dec(dut, dut.ALUSrcA.value)
    print_hex_dec(dut, dut.ALUSrcB.value)
    print_hex_dec(dut, dut.ImmSrc.value)
    print_hex_dec(dut, dut.RegWrite.value)
    print_hex_dec(dut, dut.RegSrc.value)
    print_hex_dec(dut, dut.Sel14.value)

    print_hex_dec(dut, dut.PC.value)
    print_hex_dec(dut, dut.ADR.value)
    print_hex_dec(dut, dut.ReadData.value)
    print_hex_dec(dut, dut.ReadDataOut.value)
    print_hex_dec(dut, dut.RA1.value)
    print_hex_dec(dut, dut.RA2.value)
    print_hex_dec(dut, dut.RA3.value)
    print_hex_dec(dut, dut.RD1.value)
    print_hex_dec(dut, dut.RD2.value)
    print_hex_dec(dut, dut.RD1_OUT.value)
    print_hex_dec(dut, dut.RD2_OUT.value)
    print_hex_dec(dut, dut.SrcA.value)
    print_hex_dec(dut, dut.SrcB.value)
    print_hex_dec(dut, dut.ALUResult.value)
    print_hex_dec(dut, dut.ALUOut.value)
    
    

    if dut.PCWrite.value != 0:
        dut._log.info(f"PCWrite {dut.PCWrite.value}")

    if dut.AdSrc.value != 0:
        dut._log.info(f"AdSrc {dut.AdSrc.value}")

    if dut.MemWrite.value != 0:
        dut._log.info(f"MemWrite {dut.MemWrite.value}")

    if dut.IRWrite.value != 0:
        dut._log.info(f"IRWrite {dut.IRWrite.value}")

    if dut.ResultSrc.value != 0:
        dut._log.info(f"ResultSrc {dut.ResultSrc.value}")

    if dut.ALUControl.value != 0:
        dut._log.info(f"ALUControl {dut.ALUControl.value}")

    if dut.ALUSrcA.value != 0:
        dut._log.info(f"ALUSrcA {dut.ALUSrcA.value}")

    if dut.ALUSrcB.value != 0:
        dut._log.info(f"ALUSrcB {dut.ALUSrcB.value}")

    if dut.ImmSrc.value != 0:
        dut._log.info(f"ImmSrc {dut.ImmSrc.value}")

    if dut.RegWrite.value != 0:
        dut._log.info(f"RegWrite {dut.RegWrite.value}")

    if dut.RegSrc.value != 0:
        dut._log.info(f"RegSrc {dut.RegSrc.value}")

    if dut.Sel14.value != 0:
        dut._log.info(f"Sel14 {dut.Sel14.value}")

    dut._log.info(f"------------------")
    my_signal_value = int(dut.PC.value)
    dut._log.info(f"PC {dut.PC.value} (HEX): {my_signal_value:x}")

    if dut.ADR.value != 0:
        my_signal_value = int(dut.ADR.value)
        dut._log.info(f"ADR {dut.ADR.value} (HEX): {my_signal_value:x}")

    if dut.ReadData.value != 0:
        my_signal_value = int(dut.ReadData.value)
        dut._log.info(
            f"ReadData {dut.ReadData.value} (HEX): {my_signal_value:x} (DEC): {my_signal_value}"
        )

    if dut.ReadDataOut.value != 0:
        my_signal_value = int(dut.ReadDataOut.value)
        dut._log.info(
            f"ReadDataOut {dut.ReadDataOut.value} (HEX): {my_signal_value:x} (DEC): {my_signal_value}"
        )

    if dut.RA1.value != 0:
        my_signal_value = int(dut.RA1.value)
        dut._log.info(f"RA1 {dut.RA1.value} (DEC): {my_signal_value}")

    if dut.RA2.value != 0:
        my_signal_value = int(dut.RA2.value)
        dut._log.info(f"RA2 {dut.RA2.value} (DEC): {my_signal_value}")

    if dut.RA3.value != 0:
        my_signal_value = int(dut.RA3.value)
        dut._log.info(f"RA3 {dut.RA3.value} (DEC): {my_signal_value}")

    if dut.RD1.value != 0:
        my_signal_value = int(dut.RD1.value)
        dut._log.info(
            f"RD1 {dut.RD1.value} (HEX): {my_signal_value:x} (DEC): {my_signal_value}"
        )

    if dut.RD2.value != 0:
        my_signal_value = int(dut.RD2.value)
        dut._log.info(
            f"RD2 {dut.RD2.value} (HEX): {my_signal_value:x} (DEC): {my_signal_value}"
        )

    if dut.RD1_OUT.value != 0:
        my_signal_value = int(dut.RD1_OUT.value)
        dut._log.info(
            f"RD1_OUT {dut.RD1_OUT.value} (HEX): {my_signal_value:x} (DEC): {my_signal_value}"
        )

    if dut.RD2_OUT.value != 0:
        my_signal_value = int(dut.RD2_OUT.value)
        dut._log.info(
            f"RD2_OUT {dut.RD2_OUT.value} (HEX): {my_signal_value:x} (DEC): {my_signal_value}"
        )

    if dut.SrcA.value != 0:
        my_signal_value = int(dut.SrcA.value)
        dut._log.info(
            f"SrcA {dut.SrcA.value} (HEX): {my_signal_value:x} (DEC): {my_signal_value}"
        )

    if dut.SrcB.value != 0:
        my_signal_value = int(dut.SrcB.value)
        dut._log.info(
            f"SrcB {dut.SrcB.value} (HEX): {my_signal_value:x}   (DEC): {my_signal_value}"
        )

    if dut.ALUResult.value != 0:
        my_signal_value = int(dut.ALUResult.value)
        dut._log.info(f"ALUResult {dut.ALUResult.value} (HEX): {my_signal_value:x}")

    if dut.ALUOut.value != 0:
        my_signal_value = int(dut.ALUOut.value)
        dut._log.info(f"ALUOut {dut.ALUOut.value} (HEX): {my_signal_value:x}")

    my_signal_value = int(dut.OUT.value)
    dut._log.info(
        f"OUT {dut.OUT.value} (HEX): {my_signal_value:x} (DEC): {my_signal_value:d}"
    )
    print("------------------")


# This function writes data to the DUT
def write_data(
    dut,
    PCWrite=0,
    AdSrc=0,
    MemWrite=0,
    IRWrite=0,
    ResultSrc=0,
    ALUControl=0,
    ALUSrcA=0,
    ALUSrcB=0,
    ImmSrc=0,
    RegWrite=0,
    RegSrc=0,
    Sel14=0,
):
    dut.PCWrite.value = PCWrite
    dut.AdSrc.value = AdSrc
    dut.MemWrite.value = MemWrite
    dut.IRWrite.value = IRWrite
    dut.ResultSrc.value = ResultSrc
    dut.ALUControl.value = ALUControl
    dut.ALUSrcA.value = ALUSrcA
    dut.ALUSrcB.value = ALUSrcB
    dut.ImmSrc.value = ImmSrc
    dut.RegWrite.value = RegWrite
    dut.RegSrc.value = RegSrc
    dut.Sel14.value = Sel14


# Fetch and decode cycles
async def fetch_and_decode(dut, clkedge, skip_print=False):
    # Cycle 1 - Fetch
    PCWrite = 1
    IRWrite = 1
    ResultSrc = 2
    ALUControl = 4
    ALUSrcA = 1
    ALUSrcB = 2

    write_data(
        dut,
        PCWrite=PCWrite,
        IRWrite=IRWrite,
        ResultSrc=ResultSrc,
        ALUControl=ALUControl,
        ALUSrcA=ALUSrcA,
        ALUSrcB=ALUSrcB,
    )

    await clkedge
    if not skip_print:
        dut._log.info(f"Cycle 1 - Fetch")
        print_all(dut)
    assert dut.ALUResult.value == dut.PC.value + 4
    assert dut.OUT.value == dut.ALUResult.value

    # Cycle 2 - Decode
    ResultSrc = 2
    ALUSrcA = 1
    ALUSrcB = 2
    ALUControl = 4

    write_data(
        dut,
        ResultSrc=ResultSrc,
        ALUSrcA=ALUSrcA,
        ALUSrcB=ALUSrcB,
        ALUControl=ALUControl,
    )

    await clkedge
    if not skip_print:
        dut._log.info(f"Cycle 2 - Decode")
        print_all(dut)
    assert dut.ALUResult.value == dut.PC.value + 4
    assert dut.OUT.value == dut.ALUResult.value


@cocotb.test()
async def datapath_operations(dut):
    """Setup testbench and run a test."""
    # Generate the clock
    await cocotb.start(Clock(dut.CLK, 10, "us").start(start_high=False))

    # set clkedge as the rising edge of the clock
    clkedge = RisingEdge(dut.CLK)
    # wait until the clock edge
    dut.RESET.value = 1
    await clkedge

    dut.RESET.value = 0
    await clkedge

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - MemAddr
    ALUSrcB = 1
    ImmSrc = 1
    ALUControl = 4

    write_data(dut, ALUSrcB=ALUSrcB, ImmSrc=ImmSrc, ALUControl=ALUControl)

    await clkedge
    dut._log.info(f"Cycle 3 - MemAddr")
    print_all(dut)
    assert dut.ALUResult.value == 60
    assert dut.OUT.value == dut.PC.value + 4

    # Cycle 4 - MemRead
    AdSrc = 1
    ImmSrc = 1
    ALUSrcB = 1
    ALUControl = 4

    write_data(dut, AdSrc=AdSrc, ImmSrc=ImmSrc, ALUSrcB=ALUSrcB, ALUControl=ALUControl)

    await clkedge
    dut._log.info(f"Cycle 4 - MemRead")
    print_all(dut)
    assert dut.ALUResult.value == 60
    assert dut.ADR.value == 60
    assert dut.ReadData.value == 17

    # Cycle 5 - WriteBack
    AdSrc = 1
    ImmSrc = 1
    ALUSrcB = 1
    RegWrite = 1
    ResultSrc = 1
    ALUControl = 4

    write_data(
        dut,
        AdSrc=AdSrc,
        ImmSrc=ImmSrc,
        ALUSrcB=ALUSrcB,
        RegWrite=RegWrite,
        ResultSrc=ResultSrc,
        ALUControl=ALUControl,
    )

    await clkedge
    dut._log.info(f"Cycle 5 - WriteBack")
    print_all(dut)
    assert dut.ALUResult.value == 60
    assert dut.ReadDataOut.value == 17
    assert dut.OUT.value == 17

    # Check ADD operation
    dut._log.info(f"Check ADD operation")

    # Fetch and decode cycles
    await fetch_and_decode(dut, clkedge, skip_print=True)

    # Cycle 3 - Execute
    ResultSrc = 1
    ALUControl = 4

    write_data(dut, ResultSrc=ResultSrc, ALUControl=ALUControl)
    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)

    # Cycle 4 - ALUWriteBack
    RegWrite = 1
    write_data(dut, RegWrite=RegWrite)
    await clkedge
    dut._log.info(f"Cycle 4 - Wait")
    print_all(dut)

    # Cycle 5 - Wait
    write_data(dut)
    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)
