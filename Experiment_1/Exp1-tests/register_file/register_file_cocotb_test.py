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
    clkedge = FallingEdge(dut.CLK)
    await clkedge

    # Write Data to Register 1 and show the value in RD1
    dut._log.info("Write Data to RD1")
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

    # Replace data in Register 1
    dut._log.info("Replace Data in RD1")
    A1 = 0
    data = 3
    WE = 1
    set_values(dut, A1, A2, A3, data, WE, RESET)
    await clkedge
    print_values(dut)
    assert dut.RD1.value == 3, "RD1 should be 3"
    await clkedge

    # Write Data to Register3 and Read data from RD1 and RD2
    dut._log.info("Write Data to RD3 and Read RD1 and RD2")
    A1 = 0
    A2 = 3
    A3 = 3
    data = 9
    WE = 1
    set_values(dut, A1, A2, A3, data, WE, RESET)
    await clkedge
    print_values(dut)
    assert dut.RD1.value == 3, "RD1 should be 3"
    assert dut.RD2.value == 9, "RD2 should be 9"
    await clkedge

    # Test WE = 0
    dut._log.info("Test WE = 0")
    A1 = 0
    A2 = 3
    A3 = 3
    data = 11
    WE = 0
    set_values(dut, A1, A2, A3, data, WE, RESET)
    await clkedge
    print_values(dut)
    assert dut.RD1.value == 3, "RD1 should be 3"
    assert dut.RD2.value == 9, "RD2 should be 9"
    await clkedge

    # Test RESET = 1
    dut._log.info("Test RESET = 1")
    RESET = 1
    set_values(dut, A1, A2, A3, data, WE, RESET)
    await clkedge
    print_values(dut)
    assert dut.RD1.value == 0, "RD1 should be 0"
    assert dut.RD2.value == 0, "RD2 should be 0"
    await clkedge