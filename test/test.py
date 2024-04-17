import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles

# 简单功能测试
@cocotb.test()
async def test_simple_functionality(dut):
    clock = Clock(dut.clk, 10, units="us")  # 设定时钟周期为10微秒
    cocotb.start_soon(clock.start())        # 开始时钟

    # 复位设备
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)           # 等待两个时钟周期
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)

    # 设定测试输入并检查输出
    dut.ui_in.value = 0x55                  # 设置一个简单的测试值
    await ClockCycles(dut.clk, 1)           # 等待一个时钟周期
    assert dut.uo_out.value == dut.ui_in.value, "Output should match input under simple conditions"
