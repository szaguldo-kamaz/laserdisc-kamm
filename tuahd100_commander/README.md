# laserdisc-kamm - tuahd100_commander

# Panasonic TU-AHD100(N) RS422 commander

The Panasonic TU-AHD100(N), a well-known MUSE decoder and HD video processor, has a system control port (システム コントロール) on its back...  
Which is actually a RS422 port as stated in its user's manual and can be used to do everything (and a bit more!) as its IR remote can do.
The necessary details on how to communicate with this device are described on pages 74-75.
Based on that, i prepared this simple python based tool to interface with the TU-AHD100.

I made a nice fancy GUI version imitating its IR remote control:

![tuahd100_commander_gui](https://user-images.githubusercontent.com/86873213/209506527-3961f15b-9997-4c6d-9a84-756336ecae69.png)

Also there's a CLI version, supporting all the commands the TU-AHD100 can understand:

![tuahd100_commander_cli](https://user-images.githubusercontent.com/86873213/208728692-02463820-91f1-4ccd-a1f8-347b2282d2e4.png)

You'll need python 3 and `pyserial`. And `pySimpleGUI` for the GUI version.  
(And the necessary hardware to connect to its RS422 port from a PC...)
