#
# Simple Graphical User Interface using the TUAHD100_RS422 class
# Imitation the IR remote control
#
# Author: David Vincze
# kamm@laserdisc.hu
#
# https://github.com/szaguldo-kamaz/
#

from tuahd100_rs422 import TUAHD100_RS422
import time, os, platform
import PySimpleGUI as sg


if platform.system() in [ 'Linux', 'macOS' ]:
    serialdev = '/dev/ttyUSB0';
elif platform.system() == 'Windows':
    serialdev = 'COM3';
else:
    print("Unknown platform/OS.");
    exit(1);

if not os.access(serialdev, os.R_OK + os.W_OK):
    print("Cannot access serial port: " + serialdev + "\nIs it correct? Driver loaded? Device connected? Permissions?");
    exit(2);

csirke = TUAHD100_RS422(serialdev);


windowbackgroundcolor = '#000000';
buttonfont  = "Arial 9";

event_exit = (sg.WIN_CLOSED, "-EXIT-", 'Escape:9', 'Escape:27');

sg.theme('DarkGrey5');

graphsize = (500, 600);

buttonslayout = [
                 [sg.Text("TU-AHD100(N)\nRS422 Commander", font=("Verdana",15,'bold'), justification="center", background_color='black', pad=(50,10))],
                 [
                   sg.Button('VPPower', key="B-ProjectorPower", font=(buttonfont,8,'bold'), button_color=('#F0E000', '#404040'), size=(8,1)),
                   sg.Button('DSP ▲', key="B-SurroundLevelUp", font=(buttonfont,8,'bold'), button_color=('#F0E000', '#404040')),
                   sg.Button('Audio\nSwitch', key="B-AudioSwitch", font=(buttonfont,8,'bold'), button_color=('#F0E000', '#404040')),
                   sg.Button('NR', key="B-NR", font=(buttonfont,8,'bold'), button_color=('#F0E000', '#404040'), size=(4,1))
                 ],
                 [
                   sg.Button('DSP\nSurround', key="B-DSPSwitch", font=(buttonfont,8,'bold'), button_color=('#F0E000', '#404040'), size=(8,1)),
                   sg.Button('DSP ▼', key="B-SurroundLevelDown", font=(buttonfont,8,'bold'), button_color=('#F0E000', '#404040')),
                   sg.Button('TV\nIndep.', key="B-TV/Independent", font=(buttonfont,8,'bold'), button_color=('#F0E000', '#404040')),
                   sg.Button('Frame\nTime', key="B-Frame/Time", font=(buttonfont,8,'bold'), button_color=('#F0E000', '#404040'), size=(5,1))
                 ],
                 [
                   sg.Button('Full', key="B-Full", font=(buttonfont,8,'bold'), size=(5,1), button_color=('#F0F0F0', '#909090')),
                   sg.Button('Normal', key="B-Normal", font=(buttonfont,8,'bold'), size=(6,1), button_color=('#F0F0F0', '#909090')),
                   sg.Button('Cinema', key="B-Cinema", font=(buttonfont,8,'bold'), size=(6,1), button_color=('#F0F0F0', '#909090')),
                   sg.Button('Zoom', key="B-Zoom", font=(buttonfont,8,'bold'), size=(6,1), button_color=('#F0F0F0', '#909090'))
                 ],
                 [
                   sg.Button('Subtitles', key="B-Subtitles",   font=(buttonfont,8,'bold'), size=(7,1), pad=((5,0),(10,0)), button_color=('#F0F0F0', '#909090')),
                   sg.Button('▲', key="B-CrossKeyUp", font=(buttonfont,8,'bold'), size=(2,1), pad=((130,0),(10,0)), button_color=('#F0F0F0', '#909090'))
                 ],

                 [
                   sg.Button('Screen\nAlign', key="B-ScreenAlignment", font=(buttonfont,8,'bold'), size=(7,1), pad=((5,0),(3,0)), button_color=('#F0F0F0', '#909090')),
                   sg.Button('◀', key="B-CrossKeyLeft",   font=(buttonfont,8,'bold'), size=(2,1), pad=((83,0),(3,0)), button_color=('#F0F0F0', '#909090')),
                   sg.Button('■', key="B-CrossKey[]", font=(buttonfont,8,'bold'), size=(2,1), pad=((5,0),(3,0)), button_color=('#F0F0F0', '#909090')),
                   sg.Button('▶', key="B-CrossKeyRight",  font=(buttonfont,8,'bold'), size=(2,1), pad=((5,5),(3,0)), button_color=('#F0F0F0', '#909090'))
                 ],

                 [
                   sg.Button('Standard', key="B-Standard", font=(buttonfont,8,'bold'), size=(7,1), pad=((5,0),(3,10)), button_color=('#F0F0F0', '#909090')),
                   sg.Button('Menu', key="B-Menu", font=(buttonfont,8,'bold'), size=(5,1), pad=((5,0),(3,10)), button_color=('#F0F0F0', '#909090')),
                   sg.Button('▼', key="B-CrossKeyDown", font=(buttonfont,8,'bold'), size=(2,1), pad=((62,0),(3,10)), button_color=('#F0F0F0', '#909090'))
                 ],

                 [
                 ],

                 [
                   sg.Button('POWER', key="B-Power", font=(buttonfont,8,'bold'), button_color=('#FFFFFF', '#FF0000')),
                   sg.Button('HD', key="B-HD/MUSE", font=(buttonfont,8,'bold'), button_color=('#F0E000', '#404040')),
                   sg.Button('TV / Video', key="B-ScreenSwitch", font=(buttonfont,8,'bold'), button_color=('#F0E000', '#404040')),
                   sg.Button('OSD', key="B-OSD", font=(buttonfont,8,'bold'), button_color=('#F0E000', '#404040'))
                 ],

                 [
                   sg.Button('Channel ▼', key="B-ChannelDown", font=(buttonfont,8,'bold'), button_color=('#F0E000', '#404040')),
                   sg.Button('Channel ▲', key="B-ChannelUp", font=(buttonfont,8,'bold'), button_color=('#F0E000', '#404040')),
                   sg.Button('VideoMenu', key="B-VideoMenu", font=(buttonfont,8,'bold'), button_color=('#F0E000', '#404040'))
                 ],

                 [
                   sg.Button('1', key="B-Position1", font=(buttonfont,8,'bold'), size=(4,1), button_color=('#F0E000', '#404040'), pad=((25,5),(5,5)) ),
                   sg.Button('2', key="B-Position2", font=(buttonfont,8,'bold'), size=(4,1), button_color=('#F0E000', '#404040'), pad=((5,5),(5,5)) ),
                   sg.Button('3', key="B-Position3", font=(buttonfont,8,'bold'), size=(4,1), button_color=('#F0E000', '#404040'), pad=((5,5),(5,5)) ),
                   sg.Button('4', key="B-Position4", font=(buttonfont,8,'bold'), size=(4,1), button_color=('#F0E000', '#404040'), pad=((5,5),(5,5)) )
                 ],

                 [
                   sg.Button('5', key="B-Position5", font=(buttonfont,8,'bold'), size=(4,1), button_color=('#F0E000', '#404040'), pad=((25,5),(5,5)) ),
                   sg.Button('6', key="B-Position6", font=(buttonfont,8,'bold'), size=(4,1), button_color=('#F0E000', '#404040'), pad=((5,5),(5,5)) ),
                   sg.Button('7', key="B-Position7", font=(buttonfont,8,'bold'), size=(4,1), button_color=('#F0E000', '#404040'), pad=((5,5),(5,5)) ),
                   sg.Button('8', key="B-Position8", font=(buttonfont,8,'bold'), size=(4,1), button_color=('#F0E000', '#404040'), pad=((5,5),(5,5)) )
                 ],

                 [
                   sg.Button('9', key="B-Position9", font=(buttonfont,8,'bold'), size=(4,1), button_color=('#F0E000', '#404040'), pad=((25,5),(5,5)) ),
                   sg.Button('10/0', key="B-Position10", font=(buttonfont,8,'bold'), size=(4,1), button_color=('#F0E000', '#404040'), pad=((5,5),(5,5)) ),
                   sg.Button('11', key="B-Position11", font=(buttonfont,8,'bold'), size=(4,1), button_color=('#F0E000', '#404040'), pad=((5,5),(5,5)) ),
                   sg.Button('12', key="B-Position12", font=(buttonfont,8,'bold'), size=(4,1), button_color=('#F0E000', '#404040'), pad=((5,5),(5,5)) )
                 ],

                 [
                   sg.Button('BS-1', key="B-BS-1", font=(buttonfont,8,'bold'), button_color=('#FFFFFF', '#00A0D0'), size=(5,1), pad=((11,5),(5,5)) ),
                   sg.Button('BS-3', key="B-BS-3", font=(buttonfont,8,'bold'), button_color=('#FFFFFF', '#00A0D0'), size=(5,1)),
                   sg.Button('BS-5', key="B-BS-5", font=(buttonfont,8,'bold'), button_color=('#FFFFFF', '#00A0D0'), size=(5,1)),
                   sg.Button('BS-7', key="B-BS-7", font=(buttonfont,8,'bold'), button_color=('#FFFFFF', '#00A0D0'), size=(5,1)),
                 ],
                 [
                   sg.Button('BS-9', key="B-BS-9", font=(buttonfont,8,'bold'), button_color=('#FFFFFF', '#00A0D0'), size=(5,1), pad=((11,5),(5,5)) ),
                   sg.Button('BS-11', key="B-BS-11", font=(buttonfont,8,'bold'), button_color=('#FFFFFF', '#00A0D0'), size=(5,1)),
                   sg.Button('BS-13', key="B-BS-13", font=(buttonfont,8,'bold'), button_color=('#FFFFFF', '#00A0D0'), size=(5,1)),
                   sg.Button('BS-15', key="B-BS-15", font=(buttonfont,8,'bold'), button_color=('#FFFFFF', '#00A0D0'), size=(5,1)),
                 ],

                 [sg.Text("Panasonic", font=("Arial",11,'bold'), pad=((118,0),(10,0)), text_color='#F0E000', background_color='black' ) ],
                 [sg.Text("TV TUNER", font=("Arial",10,''), pad=((121,0),(0,20)), text_color='#F0E000', background_color='black' ) ],

                 [
                   sg.Button('MUSE1', key="B-MUSE1", font=(buttonfont,8,'bold'), size=(6,1), button_color=('#F0F0F0', '#A0A0A0')),
                   sg.Button('MUSE2', key="B-MUSE2", font=(buttonfont,8,'bold'), size=(6,1), button_color=('#F0F0F0', '#A0A0A0')),
                   sg.Button('MUSE3', key="B-MUSE3", font=(buttonfont,8,'bold'), size=(6,1), button_color=('#F0F0F0', '#A0A0A0')),
                   sg.Button('MUSE AI', key="B-AI", font=(buttonfont,8,'bold'), size=(6,1), button_color=('#F0F0F0', '#A0A0A0')),
                 ],

                 [
                   sg.Button('Video\nStandard', key="B-VideoStandard", font=(buttonfont,8,'bold'), size=(8,1), button_color=('#F0F0F0', '#A0A0A0')),
                   sg.Button('Video\nElegant', key="B-VideoElegant", font=(buttonfont,8,'bold'), size=(7,1), button_color=('#F0F0F0', '#A0A0A0')),
                   sg.Button('HDMonitor4CH', key="B-HDMonitor4CH", font=(buttonfont,8,'bold'), size=(14,1), button_color=('#F0F0F0', '#A0A0A0')),
                 ],

                 [
                   sg.Button('Video\nDynamic', key="B-VideoDynamic", font=(buttonfont,8,'bold'), size=(8,1), button_color=('#F0F0F0', '#A0A0A0')),
                   sg.Button('Video\nChic', key="B-VideoChic", font=(buttonfont,8,'bold'), size=(5,1), button_color=('#F0F0F0', '#A0A0A0')),
                   sg.Button('ProLogic', key="B-ProLogic", font=(buttonfont,8,'bold'), size=(7,1), button_color=('#F0F0F0', '#A0A0A0')),
                   sg.Button('DSP\nOFF', key="B-DSP_OFF_DSP", font=(buttonfont,8,'bold'), size=(4,1), button_color=('#F0F0F0', '#A0A0A0')),
                 ],

                 [
                   sg.Button('ColorTemp\nHigh', key="B-ColorTemperatureHigh", font=(buttonfont,8,'bold'), size=(10,1), button_color=('#F0F0F0', '#A0A0A0')),
                   sg.Button('ColorTemp\nStandard', key="B-ColorTemperatureStandard", font=(buttonfont,8,'bold'), size=(9,1), button_color=('#F0F0F0', '#A0A0A0')),
                   sg.Button('ColorTemp\nLow', key="B-ColorTemperatureLow", font=(buttonfont,8,'bold'), size=(10,1), button_color=('#F0F0F0', '#A0A0A0')),
                 ],

                 [sg.Text("github.com/szaguldo-kamaz", font=("Arial",9,'bold'), pad=((85,0),(10,0)), text_color='#F0E000', background_color='black' ) ],

            ];

commtextlayout = [ [ sg.Multiline('Command log:', size=(30, 54), key='textbox', background_color='#000000', text_color='white', autoscroll=True) ] ];

layout = [ [
             sg.pin(sg.Column(buttonslayout, key='-BUTTONSIDE-', size=(350, 780), background_color=windowbackgroundcolor, pad=(0, 0))),
             sg.pin(sg.Column(commtextlayout, key='-TEXTSIDE-', size=(250, 780), background_color=windowbackgroundcolor, pad=(0, 0)))
         ] ];

window = sg.Window('TU-AHD100(N) RS422 Commander by Kamm', layout, return_keyboard_events=True, finalize=True, use_default_focus=False, background_color=windowbackgroundcolor);


while True:

    [event, values] = window.read(100);

    if event in event_exit:
        break

    if event[:2] == 'B-':
        command = event[2:];
        logtext = values['textbox'] + "\n> " + command;

        cmdresult = csirke.command(command);

        if   cmdresult == 0:
            logtext += "\n< ACK";
        elif cmdresult == 1:
            logtext += "\n< NAK !";
        else:
            logtext += "\nError: " + str(cmdresult);

        window['textbox'].update(logtext);


window.close();
