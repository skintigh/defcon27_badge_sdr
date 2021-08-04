# This script creates creates the 5 magic packets for SPEAKER VILLAGE CONTEST ARTIST GOON to win the badge game
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

#stage 1: magic
#case D  uber/any?
#case E
echo -e Creating SPEAKER magic packet
python write_signal.py -q  1 0 0 0  8   0 1 2 3  $SPEAKER $MAGIC 0 0   0 0 0
./craft_multipart_attack.sh
#concat with delay
#sox synthetic_signal.wav recordings/silence_1000ms.wav synthetic_signal_win_DC27_game.wav
sox synthetic_signal.wav synthetic_signal_win_DC27_game.wav

#case F
echo -e Creating VILLAGE magic packet
python write_signal.py -q  1 0 0 0  8   0 1 2 3  $VILLAGE $MAGIC 0 0   0 0 0
./craft_multipart_attack.sh
sox synthetic_signal_win_DC27_game.wav synthetic_signal.wav temp/out.wav #no delay
#sox synthetic_signal_win_DC27_game.wav synthetic_signal.wav recordings/silence_1000ms.wav temp/out.wav # 1s delay
mv temp/out.wav synthetic_signal_win_DC27_game.wav

#case C
echo -e Creating CONTEST magic packet
python write_signal.py -q  1 0 0 0  8   0 1 2 3  $CONTEST $MAGIC 0 0   0 0 0
./craft_multipart_attack.sh
sox synthetic_signal_win_DC27_game.wav synthetic_signal.wav temp/out.wav #no delay
#sox synthetic_signal_win_DC27_game.wav synthetic_signal.wav recordings/silence_1000ms.wav temp/out.wav # 1s delay
mv temp/out.wav synthetic_signal_win_DC27_game.wav

#case O
echo -e Creating ARTIST magic packet
python write_signal.py -q  1 0 0 0  8   0 1 2 3  $ARTIST $MAGIC 0 0   0 0 0
./craft_multipart_attack.sh
sox synthetic_signal_win_DC27_game.wav synthetic_signal.wav temp/out.wav #no delay
#sox synthetic_signal_win_DC27_game.wav synthetic_signal.wav recordings/silence_1000ms.wav temp/out.wav # 1s delay
mv temp/out.wav synthetic_signal_win_DC27_game.wav

#case N
echo -e Creating GOON magic packet
python write_signal.py -q  1 0 0 0  8   0 1 2 3  $GOON $MAGIC 0 0   0 0 0
./craft_multipart_attack.sh
sox synthetic_signal_win_DC27_game.wav synthetic_signal.wav temp/out.wav #no delay
#sox synthetic_signal_win_DC27_game.wav synthetic_signal.wav recordings/silence_1000ms.wav temp/out.wav # 1s delay
mv temp/out.wav synthetic_signal_win_DC27_game.wav


#stage 2: don't have to be magic (1 of each color?)
#human/contest/artist/cfp/uber x
#goon x
#speaker x
#vendor 
#press
echo -e Creating VENDOR NON-MAGIC packet
python write_signal.py -q  1 0 0 0  8   0 1 2 3  $VENDOR $NOT_MAGIC 0 0   0 0 0
./craft_multipart_attack.sh
sox synthetic_signal_win_DC27_game.wav synthetic_signal.wav temp/out.wav #no delay
#sox synthetic_signal_win_DC27_game.wav synthetic_signal.wav recordings/silence_1000ms.wav temp/out.wav # 1s delay
mv temp/out.wav synthetic_signal_win_DC27_game.wav

echo -e Creating PRESS NON-MAGIC packet
python write_signal.py -q  1 0 0 0  8   0 1 2 3  $PRESS $NOT_MAGIC 0 0   0 0 0
./craft_multipart_attack.sh
sox synthetic_signal_win_DC27_game.wav synthetic_signal.wav temp/out.wav #no delay
#sox synthetic_signal_win_DC27_game.wav synthetic_signal.wav recordings/silence_1000ms.wav temp/out.wav # 1s delay
mv temp/out.wav synthetic_signal_win_DC27_game.wav



#This .wav is fine to play on repeat forever.
#Add trailing silence if you want to play this .wav once instead of looped.
# (really only needs to be 1281ms of silence with previous 1000ms already added)
#sox synthetic_signal_win_DC27_game.wav recordings/silence_2281ms.wav temp/out.wav
#mv temp/out.wav synthetic_signal_win_DC27_game.wav
