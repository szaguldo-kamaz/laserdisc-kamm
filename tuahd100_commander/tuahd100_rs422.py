#
# Super simple class to communicate with the Panasonic TU-AHD100(N) via it's RS422 (System Control) port
#
# Author: David Vincze
# kamm@laserdisc.hu
#
# https://github.com/szaguldo-kamaz/
#

import serial


class TUAHD100_RS422:

    commandset = {
            'TV'                        : 0x04,
            'Video'                     : 0x05,
            'ScreenSwitch'              : 0x0A,  # 画面切換 (TV/Video)
            'NR'                        : 0x0C,
            'Position1'                 : 0x0D,
            'Position2'                 : 0x0E,
            'Position3'                 : 0x0F,
            'Position4'                 : 0x10,
            'Position5'                 : 0x11,
            'Position6'                 : 0x12,
            'Position7'                 : 0x13,
            'Position8'                 : 0x14,
            'Position9'                 : 0x15,
            'Position10'                : 0x16,
            'Position11'                : 0x17,
            'Position12'                : 0x18,
            'Position13'                : 0x19,
            'Position14'                : 0x1A,
            'Position15'                : 0x1B,
            'AudioSwitch'               : 0x1D,  # 音声切換
            'ChannelUp'                 : 0x1E,
            'ChannelDown'               : 0x1F,
            'OSD'                       : 0x20,  # 画面表示
            'Power'                     : 0x21,
            'PowerOn'                   : 0x22,
            'PowerOff'                  : 0x23,
            'CrossKey[]'                : 0x24,
            'CrossKeyUp'                : 0x25,
            'CrossKeyDown'              : 0x26,
            'CrossKeyRight'             : 0x27,
            'CrossKeyLeft'              : 0x28,
            'VideoMenu'                 : 0x29,
            'Standard'                  : 0x52,  # 標準
            'VideoStandard'             : 0x4E,
            'VideoDynamic'              : 0x4F,
            'VideoElegant'              : 0x50,  # 映像 エレガント
            'VideoChic'                 : 0x51,  # 映像 シック
            'Menu'                      : 0x2A,
            'AI'                        : 0x2B,
            'TV/Independent'            : 0x2C,  # 独立
            'BS-1'                      : 0x2D,
            'BS-3'                      : 0x2E,
            'BS-5'                      : 0x2F,
            'BS-7'                      : 0x30,
            'BS-9'                      : 0x31,
            'BS-11'                     : 0x32,
            'BS-13'                     : 0x33,
            'BS-15'                     : 0x34,
            'BSLevel'                   : 0x42,
            'Frame/Time'                : 0x35,
            'HD/MUSE'                   : 0x0B,  # Front panel "HD" button
            'Normal'                    : 0x36,
            'Cinema'                    : 0x37,
            'Zoom'                      : 0x38,
            'Full'                      : 0x39,
            'Subtitles'                 : 0x3A,
            'SubtitlesOn'               : 0x49,
            'SubtitlesOff'              : 0x4A,  # fixed in TU-AHD100N manual (TU-AHD100 manual says 0x50)
            'ScreenAlignment'           : 0x3B,  # 画面位置調整
            'ColorTemperatureHigh'      : 0x4B,
            'ColorTemperatureStandard'  : 0x4C,
            'ColorTemperatureLow'       : 0x4D,
            'HD'                        : 0x09,
            'MUSE1'                     : 0x06,
            'MUSE2'                     : 0x07,
            'MUSE3'                     : 0x08,
            'SurroundLevelUp'           : 0x3C,
            'SurroundLevelDown'         : 0x3D,

            # SystemApp
            'ProjectorPower'            : 0x3E,  # front panel green led
            'ProjectorPowerOn'          : 0x3F,  # front panel green led
            'ProjectorPowerOff'         : 0x40,  # front panel green led
            'HDMonitor4CH'              : 0x41,
            'DSPSwitch'                 : 0x1C,
            'DSP_OFF_DSP'               : 0x43,
            'SurroundDSPExpand'         : 0x44,
            'SurroundDSPCinema'         : 0x45,
            'SurroundDSPHall'           : 0x46,
            'SurroundDSPStadium'        : 0x47,
            'ProLogic'                  : 0x48,

            'ACK'                       : 0x00,
            'NAK'                       : 0x01,
            'STX'                       : 0x02,  # start transmit
            'ETX'                       : 0x03   # end transmit
        }


    def __init__(self, serialdev = '/dev/ttyUSB0', simplex = False):

        self.simplex = simplex;
        self.ser = serial.Serial(port = serialdev, baudrate = 4800, timeout = 0.2,
                                 bytesize = serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE,
                                 parity = serial.PARITY_ODD,
                                 xonxoff = False, rtscts = False);
        self.validcommandlist = list(self.commandset.keys());
        for badcomm in ['ACK', 'NAK', 'STX', 'ETX']:
            self.validcommandlist.remove(badcomm);


    def command_raw(self, commandtosend):

        commandstring = [ self.commandset['STX'], self.commandset[commandtosend], self.commandset['ETX'] ];
        self.ser.write(commandstring);
        self.ser.flush();

        if not self.simplex:
            # TU-AHD100 should reply within 1 sec (but 0.2s timeout seems to be OK)
            readbytes = list(self.ser.read(16));
            if len(readbytes) != 3:
                print("Invalid response from TU-AHD100:", readbytes);
                return -2
            if   readbytes == [ self.commandset['STX'], self.commandset['ACK'], self.commandset['ETX'] ]:
                return 0
            elif readbytes == [ self.commandset['STX'], self.commandset['NAK'], self.commandset['ETX'] ]:
                return 1
            else:
                return -3

        else:
            return 0


    def command(self, commandtosend):

        if commandtosend in self.validcommandlist:
            return self.command_raw(commandtosend);
        else:
            return -1

