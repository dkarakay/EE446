# Copyright (c) 2016 Technische Universitaet Dresden, Germany
# Chair for VLSI-Design, Diagnostic and Architecture
# Author: Martin Zabel
# All rights reserved.
#$(shell echo gol)

CWD=$(shell pwd)

SIM ?= icarus
TOPLEVEL_LANG ?=verilog


VERILOG_SOURCES =$(CWD)/../../Exp1/register_file.v
VERILOG_SOURCES +=$(CWD)/../../Exp1/decoder_four_to_sixteen.v
VERILOG_SOURCES +=$(CWD)/../../Exp1/register_with_reset_write.v

TOPLEVEL = register_file
MODULE := register_file_cocotb_test
COCOTB_HDL_TIMEUNIT=1us
COCOTB_HDL_TIMEPRECISION=1us

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
