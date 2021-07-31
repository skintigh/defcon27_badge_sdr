# This script makes the beginning or middle packet of a multi-packet attack ONLY. Use make_one_shot_signal for a single, stand-alone crafted packet
# Output: synthetic_signal.wav


rm -f synthetic_signal.wav 
set -e
#python write_signal.py

#echo -e \1: Convert signal.bin into a .wav
cd grc #so generated .py files stay there
grcc -r d8psk_generator_no_gui.grc > /dev/null
cd ..

#echo -e \2: Trim beginning of generated signal
sox temp/trans_output.wav temp/trans_output_trim.wav trim 76s

#echo -e \3: Resample it to 1.2MHz
sox temp/trans_output_trim.wav -r 1200000 temp/trans_output_trim_resamp.wav

#echo -e \4: Concat it onto a recording of a header
sox recordings/recorded_header_long_3_327.5.wav temp/trans_output_trim_resamp.wav synthetic_signal.wav
#sox recordings/recorded_header_long_3_484.wav temp/trans_output_trim_resamp.wav synthetic_signal.wav

