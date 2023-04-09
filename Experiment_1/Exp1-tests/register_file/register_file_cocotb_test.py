import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from cocotb.binary import BinaryValue


def set_values(dut, A1, A2, A3, data, WE, RESET):
    dut.A1.value = A1
    dut.A2.value = A2
    dut.A3.value = A3
    dut.data.value = data
    dut.WE.value = WE
    dut.RESET.value = RESET


def print_values(dut):
    dut._log.info(f"A1 {dut.A1.value}")
    dut._log.info(f"A2 {dut.A2.value}")
    dut._log.info(f"A3 {dut.A3.value}")
    dut._log.info(f"Data {dut.data.value}")
    dut._log.info(f"WE {dut.WE.value}")
    dut._log.info(f"RESET {dut.RESET.value}")
    dut._log.info(f"RD1 {dut.RD1.value}")
    dut._log.info(f"RD2 {dut.RD2.value}")
    dut._log.info(f"-----------------")


@cocotb.test()
async def register_file_tests(dut):
    """Setup testbench and run a test."""
    # Generate the clock
    await cocotb.start(Clock(dut.CLK, 10, 'us').start(start_high=False))

    # set clkedge as the falling edge for triggers
    clkedge = FallingEdge(dut.CLK)
    # wait until the falling edge
    await clkedge

    # Write Data to RD1
    A1 = 0
    A2 = 1
    A3 = 0
    data = 7
    WE = 1
    RESET = 0
    set_values(dut, A1, A2, A3, data, WE, RESET)
    await clkedge

    print_values(dut)
    assert dut.RD1.value == 7, "RD1 should be 7"
    await clkedge

    A1 = 0
    data = 3
    WE = 1
    set_values(dut, A1, A2, A3, data, WE, RESET)
    await clkedge

    A1 = 0
    WE = 0
    set_values(dut, A1, A2, A3, data, WE, RESET)
    await clkedge
    print_values(dut)
