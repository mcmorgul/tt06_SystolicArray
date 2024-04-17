import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
from cocotb.regression import TestFactory

def matrix_mult(A, B):
    """ Manually multiply two 4x4 matrices A and B. """
    result = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                result[i][j] += A[i][k] * B[k][j]
    return result

@cocotb.test()
async def matrix_multiply_test(dut):
    """Test the 4x4 matrix multiplier."""
    # Initialize the clock
    clock = Clock(dut.clk, 10, units="ns")  # 100 MHz clock
    cocotb.start_soon(clock.start())  # Start the clock generator

    # Reset the device
    dut.rst_n.value = 0
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1

    # Prepare input and weight matrices
    input_matrix = [[random.randint(0, 255) for _ in range(4)] for _ in range(4)]
    weight_matrix = [[random.randint(0, 255) for _ in range(4)] for _ in range(4)]

    # Load the weights into the matrix multiplier
    for row in weight_matrix:
        for value in row:
            dut.ui_in.value = value
            dut.conf.value = 1  # Configure mode
            dut.key_valid.value = 1
            await RisingEdge(dut.clk)
            dut.key_valid.value = 0

    # Provide input to the multiplier
    for row in input_matrix:
        for value in row:
            dut.ui_in.value = value
            dut.conf.value = 0  # Normal operation mode
            dut.key_valid.value = 1
            await RisingEdge(dut.clk)
            dut.key_valid.value = 0

    # Wait for the results to be processed
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)  # Additional cycles for processing

    # Calculate the expected result manually
    expected_result = matrix_mult(input_matrix, weight_matrix)

    # Read the outputs and verify against expected results
    for i in range(4):
        for j in range(4):
            await RisingEdge(dut.clk)
            assert int(dut.uo_out.value) == expected_result[i][j], f"Output mismatch at index [{i}][{j}]: expected {expected_result[i][j]}, got {int(dut.uo_out.value)}"

import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
from cocotb.regression import TestFactory

def matrix_mult(A, B):
    """ Manually multiply two 4x4 matrices A and B. """
    result = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                result[i][j] += A[i][k] * B[k][j]
    return result

@cocotb.test()
async def matrix_multiply_test(dut):
    """Test the 4x4 matrix multiplier."""
    # Initialize the clock
    clock = Clock(dut.clk, 10, units="ns")  # 100 MHz clock
    cocotb.start_soon(clock.start())  # Start the clock generator

    # Reset the device
    dut.rst_n.value = 0
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1

    # Prepare input and weight matrices
    input_matrix = [[random.randint(0, 255) for _ in range(4)] for _ in range(4)]
    weight_matrix = [[random.randint(0, 255) for _ in range(4)] for _ in range(4)]

    # Load the weights into the matrix multiplier
    for row in weight_matrix:
        for value in row:
            dut.ui_in.value = value
            dut.conf.value = 1  # Configure mode
            dut.key_valid.value = 1
            await RisingEdge(dut.clk)
            dut.key_valid.value = 0

    # Provide input to the multiplier
    for row in input_matrix:
        for value in row:
            dut.ui_in.value = value
            dut.conf.value = 0  # Normal operation mode
            dut.key_valid.value = 1
            await RisingEdge(dut.clk)
            dut.key_valid.value = 0

    # Wait for the results to be processed
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)  # Additional cycles for processing

    # Calculate the expected result manually
    expected_result = matrix_mult(input_matrix, weight_matrix)

    # Read the outputs and verify against expected results
    for i in range(4):
        for j in range(4):
            await RisingEdge(dut.clk)
            assert int(dut.uo_out.value) == expected_result[i][j], f"Output mismatch at index [{i}][{j}]: expected {expected_result[i][j]}, got {int(dut.uo_out.value)}"

