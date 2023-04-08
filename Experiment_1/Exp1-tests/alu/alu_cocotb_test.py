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
    A = 4
    B = 3
    dut.A.value = A
    dut.B.value = B
    dut.CTRL.value = 0
    print('Check AND 0100 & 0011')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == A & B
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 1
    assert dut.N.value == 0
    print('------')

    await clkedge

    # Check AND
    A = 6
    B = 7
    dut.A.value = A
    dut.B.value = B
    dut.CTRL.value = 0
    dut._log.info('Check AND 0110 & 0111')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == A & B
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 0
    assert dut.N.value == 0
    print('------')


@cocotb.test()
async def alu_xor_tests(dut):
    """Setup testbench and run a test."""
    # Generate the clock
    await cocotb.start(Clock(dut.CLK, 10, 'us').start(start_high=False))

    # set clkedge as the falling edge for triggers
    clkedge = FallingEdge(dut.CLK)
    # wait until the falling edge
    await clkedge

    # Check AND
    A = 4
    B = 3
    dut.A.value = A
    dut.B.value = B
    dut.CTRL.value = 1
    print('Check XOR 0100 & 0011')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == A ^ B
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 0
    assert dut.N.value == 0
    print('------')

    await clkedge

    # Check AND
    A = 6
    B = 7
    dut.A.value = A
    dut.B.value = B
    dut.CTRL.value = 1
    dut._log.info('Check XOR 0110 & 0111')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == A ^ B
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 0
    assert dut.N.value == 0
    print('------')


@cocotb.test()
async def alu_subtraction_ab_tests(dut):
    """Setup testbench and run a test."""
    # Generate the clock
    await cocotb.start(Clock(dut.CLK, 10, 'us').start(start_high=False))

    # set clkedge as the falling edge for triggers
    clkedge = FallingEdge(dut.CLK)
    # wait until the falling edge
    await clkedge

    # Check AND
    A = 4
    B = 3
    dut.A.value = A
    dut.B.value = B
    dut.CTRL.value = 2
    print('Check Sub AB 4-3')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == A - B
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 0
    assert dut.N.value == 0
    print('------')

    await clkedge

    # Check AND
    A = 6
    B = 7
    dut.A.value = A
    dut.B.value = B
    dut.CTRL.value = 2
    print('Check Sub AB 6-7')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert convert_2_dec(dut.OUT.value) == A - B
    assert dut.OVF.value == 1
    assert dut.CO.value == 1
    assert dut.Z.value == 0
    assert dut.N.value == 1
    print('------')


def convert_2_dec(bin_val):
    print(type(bin_val))
    dec_val = bin_val.integer
    if bin_val[0] == 1:
        dec_val = -(BinaryValue(~bin_val).integer + 1)
    return dec_val
