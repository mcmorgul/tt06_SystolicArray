`include "defines.v"

`default_nettype none
module tt_um_haoyang_systolicarray(

    input  wire [7:0] ui_in,	// Dedicated inputs
	output wire [7:0] uo_out,	// Dedicated outputs
	input  wire [7:0] uio_in,	// IOs: Input path
	output wire [7:0] uio_out,	// IOs: Output path
	output wire [7:0] uio_oe,	// IOs: Enable path (active high: 0=input, 1=output)
	input  wire       ena,
	input  wire       clk,
	input  wire       rst_n
    );

    assign uio_oe = 8'hff;

    wire conf;
    wire key_valid;
    wire [`DATABUS] key_data;
    assign conf         =   ui_in[0];
    assign key_valid    =   ui_in[1];
    assign key_data     =   ui_in[3:2];

    assign uo_out       =  {mm_res0, mm_res1};
    assign uio_out      =  {mm_res2, mm_res3};


    wire[`DATABUS] buf_data1;
    wire[`DATABUS] buf_data2;
    wire[`DATABUS] buf_data3;
    wire[`DATABUS] buf_data4;
    wire buf_ready;
    inputbuf buf0(
        .clk(clk),
        .rst(rst_n),
        .data_in(key_data),
        .valid(key_valid),
        .ready(buf_ready),
        .data1(buf_data1),
        .data2(buf_data2),
        .data3(buf_data3),
        .data4(buf_data4)
    );

    wire[`RESBUS] mm_res0;
    wire[`RESBUS] mm_res1;
    wire[`RESBUS] mm_res2;
    wire[`RESBUS] mm_res3;
    MatrixMultiplier mm(
        .clk(clk),
        .rst(rst_n),
        .start(buf_ready),
        .conf(conf),
        .data_in0(buf_data1),
        .data_in1(buf_data2),
        .data_in2(buf_data3),
        .data_in3(buf_data4),
        .result0(mm_res0),
        .result1(mm_res1),
        .result2(mm_res2),
        .result3(mm_res3)
    );

    

endmodule
