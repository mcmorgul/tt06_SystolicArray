import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles
import numpy as np

@cocotb.test()
async def matrix_multiply_test(dut):
    """Test the 4x4 systolic array matrix multiplier."""
    # Initialize the clock
    clock = Clock(dut.clk, 10, units="ns")  # 100 MHz clock
    cocotb.start_soon(clock.start())  # Start the clock generator

    # Reset the device
    dut.rst_n.value = 0
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1

    # Prepare input and weight matrices
    input_matrix = np.random.randint(0, 256, (4, 4), dtype=np.uint8)
    weight_matrix = np.random.randint(0, 256, (4, 4), dtype=np.uint8)

    # Load the weights into the matrix multiplier
    for value in weight_matrix.flatten():
        dut.ui_in.value = value
        dut.conf.value = 1  # Configure mode
        dut.key_valid.value = 1
        await RisingEdge(dut.clk)
        dut.key_valid.value = 0

    # Provide input to the multiplier
    for value in input_matrix.flatten():
        dut.ui_in.value = value
        dut.conf.value = 0  # Normal operation mode
        dut.key_valid.value = 1
        await RisingEdge(dut.clk)
        dut.key_valid.value = 0

    # Wait for the results to be processed
    await ClockCycles(dut.clk, 20)

    # Read the outputs and verify against expected results
    expected_result = np.matmul(input_matrix, weight_matrix)
    result = []
    for _ in range(4):  # Assuming the results are available in consecutive cycles
        await RisingEdge(dut.clk)
        result.append(dut.uo_out.value.integer)

    # Reshape result for comparison
    result_matrix = np.array(result).reshape((4, 4))
    assert np.array_equal(result_matrix, expected_result), f"Output mismatch: expected {expected_result}, got {result_matrix}"
