echo -e This script crafts a single, stand-alone packet

rm synthetic_signal.wav

set -e

#convert data to symbols in signal.bin
#python write_signal.py

echo -e \\n1: Convert signal.bin into a .wav
cd grc #so generated .py files stay in that dir
grcc -r d8psk_generator_no_gui.grc
cd ..

echo -e \\n2: Trim beginning of generated signal
sox temp/trans_output.wav temp/trans_output_trim.wav trim 76s

echo -e \\n3: Resample it to 1.2MHz
sox temp/trans_output_trim.wav -r 1200000 temp/trans_output_trim_resamp.wav

echo -e \\n4: Concat it onto a recording of a header
sox recordings/recorded_header_long_3_327.5.wav temp/trans_output_trim_resamp.wav temp/trans_output_trim_resamp_header_long.wav

echo -e \\n5: Concat 2.281 seconds of silence onto the end
sox temp/trans_output_trim_resamp_header_long.wav recordings/silence_2281ms.wav synthetic_signal.wav

echo -e \\nOutput: synthetic_signal.wav
