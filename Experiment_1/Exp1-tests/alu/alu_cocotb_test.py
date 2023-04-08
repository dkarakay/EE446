import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from cocotb.binary import BinaryValue


def convert_2_dec(bin_val):
    print(type(bin_val))
    dec_val = bin_val.integer
    if bin_val[0] == 1:
        dec_val = -(BinaryValue(~bin_val).integer + 1)
    return dec_val


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


@cocotb.test()
async def alu_subtraction_ba_tests(dut):
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
    dut.CTRL.value = 3
    print('Check Sub BA 4-3')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == B - A
    assert dut.OVF.value == 1
    assert dut.CO.value == 1
    assert dut.Z.value == 0
    assert dut.N.value == 1
    print('------')

    await clkedge

    # Check AND
    A = -6
    B = -7
    dut.A.value = A
    dut.B.value = B
    dut.CTRL.value = 3
    print('Check Sub BA -7 - -6')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert convert_2_dec(dut.OUT.value) == B - A
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 0
    assert dut.N.value == 1
    print('------')


@cocotb.test()
async def alu_addition_tests(dut):
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
    dut.CTRL.value = 4
    print('Check Add AB 4 + 3')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == A + B
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 0
    assert dut.N.value == 0
    print('------')

    await clkedge

    # Check AND
    A = -6
    B = 6
    dut.A.value = A
    dut.B.value = B
    dut.CTRL.value = 4
    print('Check Add AB -6 + 6')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == A + B
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 1
    assert dut.N.value == 0
    print('------')

    await clkedge

    # Check AND
    A = -7
    B = -3
    dut.A.value = A
    dut.B.value = B
    dut.CTRL.value = 4
    print('Check Add AB -7 + -3')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert convert_2_dec(dut.OUT.value) == A + B
    assert dut.OVF.value == 1
    assert dut.CO.value == 0
    assert dut.Z.value == 0
    assert dut.N.value == 1
    print('------')


@cocotb.test()
async def alu_addition_cin_tests(dut):
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
    CIN = 1
    dut.A.value = A
    dut.B.value = B
    dut.CIN.value = CIN
    dut.CTRL.value = 5
    print('Check Add AB 4 + 3 + CIN')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CIN {dut.CIN.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == A + B + CIN
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 0
    assert dut.N.value == 0
    print('------')

    await clkedge

    A = -5
    B = -2
    CIN = 1
    dut.A.value = A
    dut.B.value = B
    dut.CIN.value = CIN
    dut.CTRL.value = 5
    print('Check Add AB -5 + -2 + CIN')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CIN {dut.CIN.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == A + B + CIN
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 0
    assert dut.N.value == 1
    print('------')

    await clkedge

    A = 3
    B = -4
    CIN = 1
    dut.A.value = A
    dut.B.value = B
    dut.CIN.value = CIN
    dut.CTRL.value = 5
    print('Check Add AB 3 + -4 + CIN')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CIN {dut.CIN.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == A + B + CIN
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 1
    assert dut.N.value == 0
    print('------')

    A = 3
    B = -4
    CIN = 0
    dut.A.value = A
    dut.B.value = B
    dut.CIN.value = CIN
    dut.CTRL.value = 5
    print('Check Add AB 3 + -4 + CIN')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CIN {dut.CIN.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == A + B + CIN
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 0
    assert dut.N.value == 1
    print('------')


@cocotb.test()
async def alu_subtraction_ab_cin_tests(dut):
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
    CIN = 1
    dut.A.value = A
    dut.B.value = B
    dut.CIN.value = CIN
    dut.CTRL.value = 6
    print('Check Sub BA 4-3')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CIN {dut.CIN.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == A - B + CIN
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 1
    assert dut.N.value == 0
    print('------')

    await clkedge

    A = -4
    B = 3
    CIN = 1
    dut.A.value = A
    dut.B.value = B
    dut.CIN.value = CIN
    dut.CTRL.value = 6
    print('Check Sub BA 4-3')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CIN {dut.CIN.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == A - B + CIN
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 0
    assert dut.N.value == 1
    print('------')

    await clkedge

    A = 5
    B = 3
    CIN = 1
    dut.A.value = A
    dut.B.value = B
    dut.CIN.value = CIN
    dut.CTRL.value = 6
    print('Check Sub BA 4-3')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CIN {dut.CIN.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == A - B + CIN
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 0
    assert dut.N.value == 0
    print('------')

    await clkedge


@cocotb.test()
async def alu_subtraction_ba_cin_tests(dut):
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
    CIN = 1
    dut.A.value = A
    dut.B.value = B
    dut.CIN.value = CIN
    dut.CTRL.value = 7
    print('Check Sub BA 4-3')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CIN {dut.CIN.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == B - A + CIN
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 1
    assert dut.N.value == 0
    print('------')

    await clkedge

    A = -4
    B = 3
    CIN = 1
    dut.A.value = A
    dut.B.value = B
    dut.CIN.value = CIN
    dut.CTRL.value = 7
    print('Check Sub BA 4-3')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CIN {dut.CIN.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == B - A + CIN
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 0
    assert dut.N.value == 0
    print('------')

    await clkedge

    A = 5
    B = 3
    CIN = 1
    dut.A.value = A
    dut.B.value = B
    dut.CIN.value = CIN
    dut.CTRL.value = 7
    print('Check Sub BA 4-3')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CIN {dut.CIN.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == B - A + CIN
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 0
    assert dut.N.value == 0
    print('------')

    await clkedge


@cocotb.test()
async def alu_orr_tests(dut):
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
    dut.CTRL.value = 12
    print('Check ORR 0100 & 0011')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == A | B
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 0
    assert dut.N.value == 0
    print('------')

    await clkedge

    # Check AND
    A = 6
    B = -2
    dut.A.value = A
    dut.B.value = B
    dut.CTRL.value = 12
    print('Check ORR 0100 & 0011')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == A | B
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 0
    assert dut.N.value == 1
    print('------')


@cocotb.test()
async def alu_move_tests(dut):
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
    dut.CTRL.value = 13
    print('Check B')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == B
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 0
    assert dut.N.value == 0
    print('------')


@cocotb.test()
async def alu_a_and_b_not_tests(dut):
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
    dut.CTRL.value = 15
    print('Check A & B NOT')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == A & ~B
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 0
    assert dut.N.value == 0
    print('------')


@cocotb.test()
async def alu_move_not_tests(dut):
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
    dut.CTRL.value = 15
    print('Check B NOT')
    await clkedge
    dut._log.info(f"A {dut.A.value}")
    dut._log.info(f"B {dut.B.value}")
    dut._log.info(f"CTRL {dut.CTRL.value}")

    dut._log.info(f"OUT {dut.OUT.value}")
    dut._log.info(f"OVF {dut.OVF.value}")
    dut._log.info(f"CO {dut.CO.value}")
    dut._log.info(f"Z {dut.Z.value}")
    dut._log.info(f"N {dut.N.value}")

    assert dut.OUT.value == ~B
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    assert dut.Z.value == 0
    assert dut.N.value == 0
    print('------')
