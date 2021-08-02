# This script creates creates the 5 magic packets for SPEAKER VILLAGE CONTEST ARTIST GOON to win the badge game
# Note: the badge source code also indicates you need to pair with an UBER badge, but seems to set that game_flags bit the first time it pairs with *any* badge

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


echo -e Creating SPEAKER magic packet
python write_signal.py -q  1 0 0 0  8   0 1 2 3  $SPEAKER $MAGIC 0 0   0 0 0
./craft_multipart_attack.sh
#concat with delay
#sox synthetic_signal.wav recordings/silence_1000ms.wav synthetic_signal_win_DC27_game.wav
sox synthetic_signal.wav synthetic_signal_win_DC27_game.wav


echo -e Creating VILLAGE magic packet
python write_signal.py -q  1 0 0 0  8   0 1 2 3  $VILLAGE $MAGIC 0 0   0 0 0
./craft_multipart_attack.sh
sox synthetic_signal_win_DC27_game.wav synthetic_signal.wav temp/out.wav #no delay
#sox synthetic_signal_win_DC27_game.wav synthetic_signal.wav recordings/silence_1000ms.wav temp/out.wav # 1s delay
mv temp/out.wav synthetic_signal_win_DC27_game.wav



echo -e Creating CONTEST magic packet
python write_signal.py -q  1 0 0 0  8   0 1 2 3  $CONTEST $MAGIC 0 0   0 0 0
./craft_multipart_attack.sh
sox synthetic_signal_win_DC27_game.wav synthetic_signal.wav temp/out.wav #no delay
#sox synthetic_signal_win_DC27_game.wav synthetic_signal.wav recordings/silence_1000ms.wav temp/out.wav # 1s delay
mv temp/out.wav synthetic_signal_win_DC27_game.wav



echo -e Creating ARTIST magic packet
python write_signal.py -q  1 0 0 0  8   0 1 2 3  $ARTIST $MAGIC 0 0   0 0 0
./craft_multipart_attack.sh
sox synthetic_signal_win_DC27_game.wav synthetic_signal.wav temp/out.wav #no delay
#sox synthetic_signal_win_DC27_game.wav synthetic_signal.wav recordings/silence_1000ms.wav temp/out.wav # 1s delay
mv temp/out.wav synthetic_signal_win_DC27_game.wav



echo -e Creating GOON magic packet
python write_signal.py -q  1 0 0 0  8   0 1 2 3  $GOON $MAGIC 0 0   0 0 0
./craft_multipart_attack.sh
sox synthetic_signal_win_DC27_game.wav synthetic_signal.wav temp/out.wav #no delay
#sox synthetic_signal_win_DC27_game.wav synthetic_signal.wav recordings/silence_1000ms.wav temp/out.wav # 1s delay
mv temp/out.wav synthetic_signal_win_DC27_game.wav


#This .wav is fine to play on repeat forever.
#Add trailing silence if you want to play this .wav once instead of looped.
# (really only needs to be 1281ms of silence with previous 1000ms already added)
#sox synthetic_signal_win_DC27_game.wav recordings/silence_2281ms.wav temp/out.wav
#mv temp/out.wav synthetic_signal_win_DC27_game.wav