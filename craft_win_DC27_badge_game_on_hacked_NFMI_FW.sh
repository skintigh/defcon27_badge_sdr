# This script creates creates the magic packets for SPEAKER VILLAGE CONTEST ARTIST GOON to win the badge game
# This script creates 10 packets which become 5 packets in badges with my NFMI firmware hack
# Note: the badge source code also indicates you need to pair with an UBER badge, but seems to set that game_flags bit the first time it pairs with *any* badge
# I haven't verified this wins the game yet.

set -e
HUMAN=0
GOON=1
SPEAKER=2
VENDOR=3
PRESS=4
VILLAGE=5
CONTEST=6
ARTIST=7
CFP=8
UBER=9

NOT_MAGIC=d0
MAGIC=d1

#needed for hacked NFMI FW to operate with normal badge FW
BEGIN=0x42
END=0x45

#stage 1: magic

echo -e Creating SPEAKER magic packets
#first 4 bytes of packet
python write_signal.py -q  1 0 0 0  9   $BEGIN   d0 d0  d0 d1  d0 d2  d0 d3   0 0
./craft_multipart_attack
#rename it
mv synthetic_signal.wav temp/part1.wav
#last 4 bytes of packet
python write_signal.py -q  1 0 0 0  9   0 $SPEAKER  0 $MAGIC  0 0  0 0   $END   0 0
./craft_multipart_attack

#concat them with delays
sox temp/part1.wav recordings/silence_1000ms.wav synthetic_signal.wav recordings/silence_1000ms.wav temp/out.wav
mv temp/out.wav synthetic_signal_win_DC27_game_on_hacked_NFMI_FW.wav


echo -e Creating VILLAGE magic packets
python write_signal.py -q  1 0 0 0  9   $BEGIN  d0 d0  d0 d1  d0 d2  d0 d3   0 0
./craft_multipart_attack
mv synthetic_signal.wav temp/part1.wav
python write_signal.py -q  1 0 0 0  9   0 $VILLAGE  0 $MAGIC  0 0  0 0   $END   0 0
./craft_multipart_attack

sox synthetic_signal_win_DC27_game_on_hacked_NFMI_FW.wav temp/part1.wav recordings/silence_1000ms.wav synthetic_signal.wav recordings/silence_1000ms.wav temp/out.wav
mv temp/out.wav synthetic_signal_win_DC27_game_on_hacked_NFMI_FW.wav



echo -e Creating CONTEST magic packets
python write_signal.py -q  1 0 0 0  9   $BEGIN  d0 d0  d0 d1  d0 d2  d0 d3   0 0
./craft_multipart_attack
mv synthetic_signal.wav temp/part1.wav
python write_signal.py -q  1 0 0 0  9   0 $CONTEST  0 $MAGIC  0 0  0 0   $END   0 0
./craft_multipart_attack

sox synthetic_signal_win_DC27_game_on_hacked_NFMI_FW.wav temp/part1.wav recordings/silence_1000ms.wav synthetic_signal.wav recordings/silence_1000ms.wav temp/out.wav
mv temp/out.wav synthetic_signal_win_DC27_game_on_hacked_NFMI_FW.wav



echo -e Creating ARTIST magic packets
python write_signal.py -q  1 0 0 0  9   $BEGIN  d0 d0  d0 d1  d0 d2  d0 d3   0 0
./craft_multipart_attack
mv synthetic_signal.wav temp/part1.wav
python write_signal.py -q  1 0 0 0  9   0 $ARTIST  0 $MAGIC  0 0  0 0   $END   0 0
./craft_multipart_attack

sox synthetic_signal_win_DC27_game_on_hacked_NFMI_FW.wav temp/part1.wav recordings/silence_1000ms.wav synthetic_signal.wav recordings/silence_1000ms.wav temp/out.wav
mv temp/out.wav synthetic_signal_win_DC27_game_on_hacked_NFMI_FW.wav



echo -e Creating GOON magic packets
python write_signal.py -q  1 0 0 0  9   $BEGIN  d0 d0  d0 d1  d0 d2  d0 d3   0 0
./craft_multipart_attack
mv synthetic_signal.wav temp/part1.wav
python write_signal.py -q  1 0 0 0  9   0 $GOON  0 $MAGIC  0 0  0 0   $END   0 0
./craft_multipart_attack

sox synthetic_signal_win_DC27_game_on_hacked_NFMI_FW.wav temp/part1.wav recordings/silence_1000ms.wav synthetic_signal.wav recordings/silence_1000ms.wav temp/out.wav
mv temp/out.wav synthetic_signal_win_DC27_game_on_hacked_NFMI_FW.wav


#stage 2: doesn't need to be magic

#VENDOR
echo -e Creating GOON magic packets
python write_signal.py -q  1 0 0 0  9   $BEGIN  d0 d0  d0 d1  d0 d2  d0 d3   0 0
./craft_multipart_attack
mv synthetic_signal.wav temp/part1.wav
python write_signal.py -q  1 0 0 0  9   0 $VENDOR  0 $NON-MAGIC  0 0  0 0   $END   0 0
./craft_multipart_attack

sox synthetic_signal_win_DC27_game_on_hacked_NFMI_FW.wav temp/part1.wav recordings/silence_1000ms.wav synthetic_signal.wav recordings/silence_1000ms.wav temp/out.wav
mv temp/out.wav synthetic_signal_win_DC27_game_on_hacked_NFMI_FW.wav


#PRESS
echo -e Creating GOON magic packets
python write_signal.py -q  1 0 0 0  9   $BEGIN  d0 d0  d0 d1  d0 d2  d0 d3   0 0
./craft_multipart_attack
mv synthetic_signal.wav temp/part1.wav
python write_signal.py -q  1 0 0 0  9   0 $PRESS  0 $NON-MAGIC  0 0  0 0   $END   0 0
./craft_multipart_attack

sox synthetic_signal_win_DC27_game_on_hacked_NFMI_FW.wav temp/part1.wav recordings/silence_1000ms.wav synthetic_signal.wav recordings/silence_1000ms.wav temp/out.wav
mv temp/out.wav synthetic_signal_win_DC27_game_on_hacked_NFMI_FW.wav

#add trailing silence if you want this to be a 1 shot attack instead of looped. Looping probably creates half packet that crash badges, better to play once and then hit "r"
# (really only needs to be 1281ms of silence with previous 1000ms already added)
sox synthetic_signal_win_DC27_game_on_hacked_NFMI_FW.wav recordings/silence_2281ms.wav temp/out.wav
mv temp/out.wav synthetic_signal_win_DC27_game_on_hacked_NFMI_FW.wav

