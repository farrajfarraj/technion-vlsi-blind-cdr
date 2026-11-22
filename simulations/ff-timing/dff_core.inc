* Same transmission-gate master/slave circuit and device sizes as the starter.
.subckt INV A Y VDD VSS
MP Y A VDD VDD pmos L=16n W=64n
MN Y A VSS VSS nmos L=16n W=32n
.ends INV
.subckt TG A B EN ENB VDD VSS
MN B EN A VSS nmos L=16n W=32n
MP B ENB A VDD pmos L=16n W=64n
.ends TG
.subckt DFF D CLK Q VDD VSS MD MBAR
XCLKINV clk clkb vdd vss INV
XTGM_IN d md clkb clk vdd vss TG
XMINV md mbar vdd vss INV
XMFBINV mbar mfb vdd vss INV
XTGM_FB mfb md clk clkb vdd vss TG
XTGS_IN mbar sd clk clkb vdd vss TG
XSINV sd q vdd vss INV
XSFBINV q sfb vdd vss INV
XTGS_FB sfb sd clkb clk vdd vss TG
.ends DFF
