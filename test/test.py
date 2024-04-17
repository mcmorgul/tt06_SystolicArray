import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
import numpy as np

@cocotb.test()
async def matrix_multiply_test(dut):
    """Test the 4x4 matrix multiplier."""
    # Initialize the clock
    clock = Clock(dut.clk, 10, units="ns")  # 100 MHz clock
    cocotb.start_soon(clock.start())  # Start the clock generator

    # Reset the design
    dut.rst_n.value = 0
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1

    # Define the input matrix and the weight matrix
    input_matrix = np.random.randint(low=0, high=256, size=(4, 4), dtype=np.uint8)
    weight_matrix = np.random.randint(low=0, high=256, size=(4, 4), dtype=np.uint8)

    # Load the weights into the matrix multiplier (assuming conf=1 loads weights)
    for row in weight_matrix:
        for value in row:
            dut.ui_in.value = value
            dut.conf.value = 1
            await RisingEdge(dut.clk)

    # Feed the input matrix to the multiplier (conf=0 for normal operation)
    for row in input_matrix:
        for value in row:
            dut.ui_in.value = value
            dut.conf.value = 0
            await RisingEdge(dut.clk)

    # Optionally, wait for results to be processed and check them
    expected_result = np.dot(input_matrix, weight_matrix)
    for i in range(4):  # Assuming the results are output sequentially
        await RisingEdge(dut.clk)
        # Read output and compare with expected_result
        assert dut.uo_out.value == expected_result[i], f"Output mismatch at index {i}"
