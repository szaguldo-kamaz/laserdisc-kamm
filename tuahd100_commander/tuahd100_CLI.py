#
# Simple Command Line Interface using the TUAHD100_RS422 class
#
# Author: David Vincze
# kamm@laserdisc.hu
#
# https://github.com/szaguldo-kamaz/
#

from tuahd100_rs422 import TUAHD100_RS422
import time, os, platform



if platform.system() in [ 'Linux', 'macOS' ]:
    serialdev = '/dev/ttyUSB0';
elif platform.system() == 'Windows':
    serialdev = 'COM4';
else:
    print("Unknown platform/OS.");
    exit(1);

if not os.access(serialdev, os.R_OK + os.W_OK):
    print("Cannot access serial port: " + serialdev + "\nIs it correct? Driver loaded? Device connected? Permissions?");
    exit(2);

csirke = TUAHD100_RS422(serialdev);

if platform.system() in [ 'Linux', 'macOS' ]:
    import readline
    readline.parse_and_bind("tab: complete")

    def complete(text, state):
        validcommands = csirke.validcommandlist + ['Exit'];
        results = [x for x in validcommands if x.startswith(text)] + [None];
        return results[state]

    readline.set_completer(complete)


while True:

    try:
        cmd = input('TUAHD100> ');
    except EOFError as e:
        print();
        break

    if cmd == '':
        continue
    if cmd.lower() == 'exit':
        break

    cmdresult = csirke.command(cmd);

    if   cmdresult == 0:
        print('ACK');
    elif cmdresult == 1:
        print('NAK');
        print('Is the TU-AHD100(N) powered ON? Is it in the right mode?');
    elif cmdresult == -1:
        print('Unknown command.');
        print('Recognized commands: Exit,  ' + ',  '.join(csirke.validcommandlist));
    else:
        print("Error: ", cmdresult);

