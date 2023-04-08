import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from cocotb.binary import BinaryValue



@cocotb.test()
async def alu_and_tests(dut):
    """Setup testbench and run a test."""
    # Generate the clock
    await cocotb.start(Clock(dut.CLK, 10, 'us').start(start_high=False))

    # set clkedge as the falling edge for triggers
    clkedge = FallingEdge(dut.CLK)
    # wait until the falling edge
    await clkedge

    # Check AND
    A1 = 0
    A2 = 1
    A3 = 5
    data = 7
    dut.A1.value = A1
    dut.A2.value = A2
    dut.A3.value = A3
    dut.data.value = data
    await clkedge
    dut._log.info(f"A1 {dut.A1.value}")
    dut._log.info(f"A2 {dut.A2.value}")
    dut._log.info(f"A3 {dut.A3.value}")
    dut._log.info(f"Data {dut.data.value}")
    dut._log.info(f"A3 {dut.A3.value}")
    dut._log.info(f"OUT1 {dut.OUT1.value}")
    await clkedge

    dut._log.info(f"A1 {dut.A1.value}")
    dut._log.info(f"A2 {dut.A2.value}")
    dut._log.info(f"A3 {dut.A3.value}")
    dut._log.info(f"Data {dut.data.value}")
    dut._log.info(f"A3 {dut.A3.value}")
    dut._log.info(f"OUT1 {dut.OUT1.value}")
    await clkedge

