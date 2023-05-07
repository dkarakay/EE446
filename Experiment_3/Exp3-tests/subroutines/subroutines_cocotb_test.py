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

    # Check BL
    # Address 60
    # BL 0x00000002 -> PC = 0 + 8 + 2*4 = 16 R14 = 4
    # 0xEB000002

    dut._log.info(f"BL 0x00000002 -> PC = 0 + 8 + 2*4 = 16 R14 = 4")
    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    # Cycle 3 - Branch

    await clkedge
    dut._log.info(f"Cycle 3 - Branch")
    print_all(dut)
    assert dut.INSTR.value == 0xEB000002

    # Cycle 4 - Branch
    await clkedge
    dut._log.info(f"Cycle 4 - Branch")
    print_all(dut)
    assert dut.PC.value == 16

    # Cycle 5 - Branch
    await clkedge
    dut._log.info(f"Cycle 5 - Branch")
    print_all(dut)

    # Check LDR
    # Address 16
    # LDR R3, [R0, #124] => 7
    # 0xE410307C

    dut._log.info(f"LDR R3, [R0, #124] => 7")

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
    assert dut.OUT.value == 7

    # Check SUB operation
    # Address 20
    # SUB R5, R0, R3 -> R5 = 0-7 = -7 in 2's complement = 0xFFFFFFF9
    # 0xE0405003
    dut._log.info(f"SUB R5, R0, R3 -> R5 = 0-7 = -7 in 2's complement = 0xFFFFFFF9")

    # Fetch and decode cycles
    await fetch_and_decode(dut, clkedge, skip_print=True)

    # Cycle 3 - Execute
    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE0405003

    # Cycle 4 - ALUWriteBack
    await clkedge
    dut._log.info(f"Cycle 4 - ALUWriteBack")
    print_all(dut)
    assert dut.OUT.value == 0xFFFFFFF9

    # Cycle 5 - Wait
    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)

    # Check BX LR
    # Address 24
    # BX LR -> PC = 4
    # 0xE800000E

    dut._log.info(f"BX LR -> PC = 4")

    # Fetch and decode
    await fetch_and_decode(dut, clkedge)

    await clkedge
    dut._log.info(f"Cycle 3 - Execute")
    print_all(dut)
    assert dut.INSTR.value == 0xE800000E

    await clkedge
    dut._log.info(f"Cycle 4 - Wait")
    print_all(dut)
    assert dut.PC.value == 4

    await clkedge
    dut._log.info(f"Cycle 5 - Wait")
    print_all(dut)
