import cocotb
from cocotb.triggers import RisingEdge, ClockCycles
from cocotb.regression import TestFactory
from cocotb import Clock, fork
import numpy as np

# Define the input matrix and the weight matrix
input_matrix = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
weight_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])  # Identity matrix for simplicity

# Expected result is the product of input_matrix and weight_matrix
expected_result = np.dot(input_matrix, weight_matrix)

@cocotb.test()
async def matrix_multiply_test(dut):
    # Setup clock
    clock = Clock(dut.clk, 10, units="ns")  # 100MHz clock
    fork(clock.start())  # Start the clock
    
    # Reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)

    # Configure weights in the PEs
    for i in range(16):
        dut.ui_in.value = weight_matrix.flatten()[i]
        dut.conf.value = 1
        dut.key_valid.value = 1
        await RisingEdge(dut.clk)

    # Feed input matrix
    for i in range(16):
        dut.ui_in.value = input_matrix.flatten()[i]
        dut.conf.value = 0
        dut.key_valid.value = 1
        await RisingEdge(dut.clk)

    # Wait for the results to be computed
    await ClockCycles(dut.clk, 20)

    # Read the output results
    output_results = []
    for _ in range(4):
        output_results.append(int(dut.uo_out.value))
        await RisingEdge(dut.clk)

    # Check the results
    assert np.array_equal(output_results, expected_result.flatten()), f"Test failed: {output_results} != {expected_result.flatten()}"

# Create the test
tf = TestFactory(matrix_multiply_test)
tf.generate_tests()
