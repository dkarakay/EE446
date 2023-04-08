import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge


@cocotb.test()
async def alu_basic_test(dut):
    """Setup testbench and run a test."""
    # Generate the clock
    await cocotb.start(Clock(dut.CLK, 10, 'us').start(start_high=False))

    # set clkedge as the falling edge for triggers
    clkedge = FallingEdge(dut.CLK)
    # wait until the falling edge
    await clkedge

    # Check Add
    A = 10
    B = 5
    dut.A.value = A
    dut.Bls\
        .value = B
    dut.SEL.value = 0
    await clkedge
    print('Check add: 10 + 5 ')
    print(f'AC: {dut.AC.value}')
    print(f'DR: {dut.DR.value}')
    print(f'OUT: {dut.OUT.value}')
    print(f'OVF: {dut.OVF.value}')
    print(f'CO: {dut.CO.value}')
    assert dut.OUT.value == AC + DR
    assert dut.OVF.value == 0
    assert dut.CO.value == 0
    print('------')

    #
    # # Check Add
    # AC = -15
    # DR = -14
    # dut.AC.value = AC
    # dut.DR.value = DR
    # dut.SEL.value = 0
    # await clkedge
    # print('Check add: -15 -14')
    # print(f'AC: {dut.AC.value}')
    # print(f'DR: {dut.DR.value}')
    # print(f'OUT: {dut.OUT.value}')
    # print(f'OVF: {dut.OVF.value}')
    # print(f'CO: {dut.CO.value}')
    # assert dut.OUT.value != AC + DR
    # assert dut.OVF.value == 1
    # assert dut.CO.value == 0
    # print('------')
    #
    # # Check Add
    # AC = 7
    # DR = 7
    # dut.AC.value = AC
    # dut.DR.value = DR
    # dut.SEL.value = 0
    # await clkedge
    # print('Check add: 7 + 7')
    # print(f'AC: {dut.AC.value}')
    # print(f'DR: {dut.DR.value}')
    # print(f'OUT: {dut.OUT.value}')
    # print(f'OVF: {dut.OVF.value}')
    # print(f'CO: {dut.CO.value}')
    # assert dut.OUT.value == AC + DR
    # assert dut.OVF.value == 0
    # assert dut.CO.value == 1
    # print('------')
    #
    # # Check Add
    # AC = 0
    # DR = 1
    # dut.AC.value = AC
    # dut.DR.value = DR
    # dut.SEL.value = 1
    # await clkedge
    # print('Check and: 0 & 1')
    # print(f'AC: {dut.AC.value}')
    # print(f'DR: {dut.DR.value}')
    # print(f'OUT: {dut.OUT.value}')
    # print(f'OVF: {dut.OVF.value}')
    # print(f'CO: {dut.CO.value}')
    # print(f'Z: {dut.Z.value}')
    # print(f'N: {dut.N.value}')
    # assert dut.OUT.value == AC & DR
    # assert dut.OVF.value == 0
    # assert dut.CO.value == 0
    # print('------')
    #
    # # Check Load
    # AC = 0
    # DR = 23
    # dut.AC.value = AC
    # dut.DR.value = DR
    # dut.SEL.value = 2
    # await clkedge
    # print('Load: DR 23')
    # print(f'AC: {dut.AC.value}')
    # print(f'DR: {dut.DR.value}')
    # print(f'OUT: {dut.OUT.value}')
    # print(f'OVF: {dut.OVF.value}')
    # print(f'CO: {dut.CO.value}')
    # assert dut.OUT.value == DR
    # assert dut.OVF.value == 0
    # assert dut.CO.value == 0
    # print('------')
    #
    # # Check Complement
    # AC = 6
    # DR = 1
    # dut.AC.value = AC
    # dut.DR.value = DR
    # dut.SEL.value = 3
    # await clkedge
    # print('Complement of AC:4')
    # print(f'AC: {dut.AC.value}')
    # print(f'DR: {dut.DR.value}')
    # print(f'OUT: {dut.OUT.value}')
    # print(f'OVF: {dut.OVF.value}')
    # print(f'CO: {dut.CO.value}')
    # # assert dut.OUT.value == ~AC
    # assert dut.OVF.value == 0
    # assert dut.CO.value == 0
    # print('------')
    #
    # # Check Shift right
    # AC = 12
    # DR = 1
    # dut.AC.value = AC
    # dut.DR.value = DR
    # dut.SEL.value = 4
    # dut.E.value = 0
    # await clkedge
    # print('Shift right of AC:12')
    # print(f'AC: {dut.AC.value}')
    # print(f'DR: {dut.DR.value}')
    # print(f'OUT: {dut.OUT.value}')
    # print(f'OVF: {dut.OVF.value}')
    # print(f'CO: {dut.CO.value}')
    # assert dut.OUT.value == AC / 2
    # assert dut.OVF.value == 0
    # assert dut.CO.value == 0
    # print('------')
    #
    # # Check Shift Left
    # AC = 5
    # DR = 1
    # dut.AC.value = AC
    # dut.DR.value = DR
    # dut.SEL.value = 5
    # dut.E.value = 0
    # await clkedge
    # print('Shift right of AC:5')
    # print(f'AC: {dut.AC.value}')
    # print(f'DR: {dut.DR.value}')
    # print(f'OUT: {dut.OUT.value}')
    # print(f'OVF: {dut.OVF.value}')
    # print(f'CO: {dut.CO.value}')
    # assert dut.OUT.value == AC * 2
    # assert dut.OVF.value == 0
    # assert dut.CO.value == 0
    # print('------')
