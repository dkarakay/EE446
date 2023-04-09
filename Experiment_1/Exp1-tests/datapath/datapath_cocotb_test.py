import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from cocotb.binary import BinaryValue


def set_values(dut, INP, ENABLE, OP):
    dut.INP.value = INP
    dut.ENABLE.value = ENABLE
    dut.OP.value = OP

def print_values(dut):
    dut._log.info(f"INP {dut.INP.value}")
    dut._log.info(f"ENABLE {dut.ENABLE.value}")
    dut._log.info(f"OP {dut.OP.value}")
    dut._log.info(f"CYCLE {dut.CYCLE.value}")
    dut._log.info(f"REG_OUT {dut.REG_OUT.value}")
    dut._log.info(f"-----------------")


@cocotb.test()
async def register_file_tests(dut):
    """Setup testbench and run a test."""
    # Generate the clock
    await cocotb.start(Clock(dut.CLK, 10, 'us').start(start_high=False))
    clkedge = FallingEdge(dut.CLK)
    await clkedge

    # Wait till ENABLE is high
    dut._log.info("Wait till ENABLE is high")

    for i in range(10):
        INP = 5
        ENABLE = 1
        OP = 0
        set_values(dut, INP, ENABLE, OP)
        await clkedge
        print_values(dut)

    """
    # 2s complement Test
    dut._log.info("2s complement Test")

    INP = 5
    ENABLE = 1
    OP = 0
    set_values(dut, INP, ENABLE, OP)
    await clkedge

    print_values(dut)

    await clkedge
    await clkedge
    await clkedge
    await clkedge
    await clkedge

    print_values(dut)
    #assert dut.REG_OUT.value == BinaryValue(~(5)).integer + 1
    """


