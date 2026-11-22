* Rising-data setup sweep. The first edge captures zero and the second tests D.
.include "16nm_HP.pm"
.include "dff_core.inc"
.param VDD=0.7
Vpower vdd 0 {VDD}
Vclk clk 0 PULSE(0 {VDD} 1n 5p 5p 0.8n 3n)
Vdata d 0 PULSE(0 {VDD} {4n-delta} 5p 5p 1n 8n)
Xdut d clk q vdd 0 md mbar DFF
Cload q 0 1f
.tran 0 4.79n 3.4n {maxstep}
.options plotwinsize=0 numdgt=15
.meas tran tc WHEN V(clk)=0.35 RISE=1
.meas tran td50 WHEN V(d)=0.35 RISE=1
.meas tran tq WHEN V(q)=0.35 RISE=1
.meas tran separation PARAM tc-td50
.meas tran clk_to_q PARAM tq-tc
.save V(d) V(clk) V(q) V(md) V(mbar)
