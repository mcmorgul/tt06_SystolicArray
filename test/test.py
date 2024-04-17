import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles

# 矩阵乘法测试
@cocotb.test()
async def matrix_multiplication_test(dut):
    # 创建时钟
    clock = Clock(dut.clk, 10, units="us")  # 设置时钟周期为10微秒
    cocotb.start_soon(clock.start())        # 启动时钟

    # 初始复位
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)

    # 输入矩阵A的数据
    matrix_A = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    # 输入矩阵B的数据，这里假设B矩阵每个元素都是1，简化计算
    matrix_B = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    # 配置矩阵A
    for i in range(16):
        dut.ui_in.value = matrix_A[i]
        dut.conf.value = 1  # 配置模式
        await RisingEdge(dut.clk)

    # 配置矩阵B并计算矩阵乘法
    for i in range(16):
        dut.ui_in.value = matrix_B[i]
        dut.conf.value = 0  # 执行模式
        await RisingEdge(dut.clk)

    # 计算预期的输出矩阵C
    expected_results = [
        10, 20, 30, 40,
        26, 52, 78, 104,
        42, 84, 126, 168,
        58, 116, 174, 232
    ]

    # 验证输出是否正确
    for i, expected in enumerate(expected_results):
        actual = int(dut.uo_out.value)
        assert actual == expected, f"Output {i}: Expected {expected}, got {actual}"

