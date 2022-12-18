# laserdisc-kamm - tuahd100_commander

# Panasonic TU-AHD100(N) RS422 commander

The Panasonic TU-AHD100(N), a well-known MUSE decoder and HD video processor, has a system control port on its back...
Which is actually a RS422 port as stated in its user's manual and can be used to do everything (and a bit more!) as its IR remote can do.
The necessary details on how to communicate with this device are described on pages 74-75.
Based on that, i prepared this simple python based tool to interface with the TU-AHD100.
Currently it's CLI only, maybe later i'll make some fancy GUI imitating its IR remote control.
You'll need python 3 and `pyserial`.
(And the necessary hardware to connect to its RS422 port from a PC...)
