defcon27_badge_sdr Info and Setup
==================
Introduction
------------

The Defcon 27 badge communicates via NFMI bursts. Each burst has 4 sections. 
* Section 1 is 21 half-power bursts of 3 frequencie at the carrier and +/-150kHz followed by a null. I assume this is timing data for the PLL and maybe training for the D8PSK receiver. It's probably also used to set the amplifier on the antenna, hense it's half power to avoid damage.
* Section 2 is 2 copies of the datagram preamble with a pause inbetween: 
 > > 4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0  
 > > 4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 7 1 
 > > I think the last 12 or so symbols are the null/noise.
 > > However, in hald of the packets the preabmble is different:
 > > 4 4	4 0 4 0 4 0 2 4 6	0 0 0	0 0 6 4 2 0 0 0 4 **2 3 1 3 3 4 2 2 4**
 > > This preamble is curious because the section 4 preamble is:  
 > > 4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 **4 2 7 7 4 6 7 5 6**  
 > > This suggests this means... something.
 

* Section 3 is 4 square waves with pauses. 7 0 0 0 0 0 0 0 0 0 0 2 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 5 3 
* 4th is 271 (yes, 271...?!?) copies of the same datagram. These programs receive those signals, convert all 4 sections to symbols, and decode the datagrams from the 4th section only.

Each datagram consists of symbols. I'm going to refer to 4 symbols as a byte.

Each datagram consists of:
* 8 (or 5 + 3 of ???) bytes of preamble (or midamble/syncword/sync sequence?)
* 16 bytes of data
* 10 symbol that appear to be a 12-bit CRC
* 3 nulls
* 1 random symbol

The 16 bytes of data consist of:
* 4 bytes of some sort of counter increasing by 2. Sometimes it's even, sometimes odd, and it doesn't seem to start at 0 but close to 350,000.
* 1 byte for the length of Defcon data, set to 8
* 8 bytes of Defcon data
* 3 more bytes that can be used by the badge if you hack it.

# Install

You need to install GNURadio, which which can be a nightmare. 
The easiest way is probably on Pentoo. 
Another option is to compile everything from source, possible after editing and fixing bugs, but maybe that's fixed now.

## Pentoo

Install Pentoo on a physical machine, or VMWare may be an option. Common belief is SDR won't work on a VM. This seems true on Oracle Virtualbox, but earlier experiments of mine suggest VMWare might work... https://www.pentoo.ch/isos/Beta/

## Other OSes
Here are some other instructions. For Ubuntu? The vague instrucions for fixing things are clairified in the comments. https://gist.github.com/gbevan/8e583b9cf87aa3c58102251454fa48a6
(You may need to install libsoapysdr-dev, libiio-dev)
("avahi_service_browser_new() failed: Bad state" errors are fixed by... starting the daemon? reinstalling avahi?)
(XInitThreads errors fixed by installed x11 xauth dbus-x11)
(Qt session management errors fixed by: running as root)

# Using this Software
## Introduction
I have example scripts for crafting a packet in a .wav file and building multi-packet attacks attacks, GRC files for communication over the air, and various python files a few of which will be useful for things like deoding a recieved packet.

### Running Files

Scripts are run at the command line in the root dir

grc file are run in gnuradio_companion with a HackRF, or can be modified for other SDR hardware

py files are python 3 run at the command line.

### Some Files in this Repo

defcon_recv_and_decode.grc recieves signals from badges, converts them to symbols, and dumps them to symbols.txt

parse_symbols_long_crc.py parses that output file for unique symbol datagrams. Many will be corrupted by noise, so when a threshold of copies of one datagram is reached that is output as the valid datagram.
`python parse_symbols_long_crc.py > temp.txt`

guesser.py decodes those symbols by guessing at values and encoding those guesses and comparing them. (Not exactly efficient, but that made sense at the time when I was reverse engineering things.) It will automatically decode everything in temp.txt. 
`python guesser.py`

recorder.grc records a wav file of the NFMI signal.
player_with_gui.grc plays a .wav file with a GUI output
player.grc plays a .wav file with no GUI

Other files you probbly won't need but I ought to document them all...:

data_collector.py communicates with the badge via USB serial, updates the transmitted packet, then uses live output from the GRC file to collect the correcsponding datagram

more...

## Understanding Firmware
There are 4 versions of firmware you can use [TODO: add to repo!!!]:
1. human.bin -- the original firmware, extracted by CoD_Segfault (original sounce: https://github.com/lowerrandom/CoD-Segfault-DefCon27badge)
2. stock_with_hacked_NFMI_FW.bin -- this is *almost* stock FW, but I removed the rickroll at reboot and fixed a bug that made the USB disconnect randomly. Then I added my hacked NFMI firmware which does not add "B" or "E" to packets and does not pad nibbles with 0xd, and it allows packet lengths up to 255 bytes (but only 11 bytes are real, the rest will output as 0s)
3. print_recv.bin -- the above version of "stock" plus I added debugging features that print all invalid attempts at reading the ringbuffer and prints the results of all valid packets read from the buffer.
4. print_recv_with_hacked_NFMI_fw.bin -- the above, plus the NFMI firmware hack

Code changes in those firmware versions cause some functions to change addresses, so attacks for one may not work on the other.
The exception to this is print_recv.bin and print_recv_with_hacked_NFMI_fw.bin as the only difference is the NFMI patch.
(Note: software breakpoints will also move addresses if you compile you own firmware, as will various optimizations.)

| Function \ Firmware:       | human.bin | stock_with... | print_recv* | Notes |
|---                         | ---       |     ---       |    ---      | --- |
| printf(R0...)              | 42d       | 42d           | 42d         | 0x42c + 1 for THUMB, set R0 to String Address below|
| MOVS R0,R4<BR/>POP {R4,PC} | 2de9, 418f, 6551 | 2ddb, 4A83, 6571 | 2e4f| KL_GetPacket pops R4-R6, so this address lets you control R0 while only adding 8 bytes to the attack |
| POP R0,R1,R2,R4,R5,PC      |           | 4c33          |             |       |
| ADDS R0,R4,0; POP{R4,R5,PC}|           | 6410          |             |       |
| SP and buf in KL_GetPacket | 20002F78  | 20002F78      | 20002F78    | |
|dataBlob in KL_GetPacket    | 20002F84  | 20002F84      | 20002F84    | Address of data excluding ‘B’ |
|Address of stack after PC   | 20002FA8  | 20002FA8      | 20002FA8    | dataBlob + (37-1=36=0x24) (based on the bytes I use before the string) |
| String Address             | 20002FB0  | 20002FB0      | 20002FB0    | 20002FA8 + 8 |
| control of R0 R1           |           | 6eb1		      |             | |
| “0x%08X]\n\r” 			          |           | 2B70          |             | format to print int |
| "-> Unique ID: 0x%08X"  	  |      	    | 75CC          |             | format to print int |
| "Speaker\0"                |      	    | 7538          |             | others near by |


## Example Scripts
There are several craft_* scripts to build attacks for specific firmware versions.
Example usage for the **original** firmware on badges: **human.bin**:
1. Run .\craft_win_DC27_badge_game.sh which creates synthetic_signal_win_DC27_game.wav 
2. Run gnuradio_companion
3. Load grc/player_with_gui.grc
4. Change the file name in the "wav source file" block to  synthetic_signal_win_DC27_game.wav if necessary
5. Set reepeat = yes in the "wav source file" block
6. Click the "play" button 
7. In the intereactive window for the badge, type "r" at any time to recieve packets. This will tell the badge to process any packet it has already recieved until the buffer is empty. You may have to do this a few times to get every packet required to win the game (assuming I didn't leave any out...)

Exmample for both **print_recv** versions for the badge firmware.
1. Run craft_print_hack_the_planet_for_print_recv_FW.sh
2. That will create the file synthetic_hack_the_planet_for_print_recv.wav
3. Run gnuradio_companion
4. Load grc/player_with_gui.grc
5. Change the file name in the "wav source file" block if necessary
6. Click "play" (wait for it to complete if using attacks for hacked NFMI)
7. On the badge, type "r" ro recieve the packet(s)
8. It will rarely work the first time, you'll need to futz with amplification setting, distance of the antenna, etc. and resetting the badge a lot if it gets stuck (or even if it looks fine it could be in a corrupt state.)

## How to Craft and Transmit a Single Packet
1. Convert your desired packet into symbols in signal.bin 
   1. 4 counter bytes, 1 data length byte, 11 data bytes, all in hexidecimal:
      ```
      python write_signal.py 0 0 0 0  8  1 2 3 4 5 6 7 8 0 0 0
      ```
   2. **Or** count and length are still in hex, but 11 data bytes in ASCII:
      ```
      python write_signal.py -a 0 0 0 0  b  h e l l o ' ' w o r l d
      ```

2. Convert those symbols into synthetic_signal.wav
./make_signal

3. Transmit it
   1. Open gnuradio-companion  
   2. load grc/player_wit_gui.grc 
   3. play synthetic_signal.wav
  

How to Craft and Transmit Multiple Packets:
-------------------------------------------
See example scripts, or you could cut and paste .wavs of single packets together in Audacity. 
**Do not** cut off the trailing 2281ms of silence from the last packet, that's there to trick GNURadio into operating correctly and transmitting the entire .wav, if you remove it you won't transmit everything in your .wav. (For all I know you may need a longer silence on your setup...)


Recieve Packets:
----------------
1) Launch the receiver
Open gnuradio-companion
load grc/d8psk_recv_and_decode.grc
Run it

2) Adjust the receiver
Adjust the RF gain and LPF gain so a constelation of 8 clusters of dots fits in the Costas Loop Output window.
Now the waveform in the Rational Resampler window should fit in the window and not be cut off by the top of the window.
And the color bars in the bottom left window, which represent data, should be orderly and consistant, with very little noise or randomess.
Raw symbols captures are now being dumped to symbols.txt

3) Pull one packet per burst of 271 packets, save it to a file
python parse_symbols_long_crc.py > temp.txt

4) Decode the packets

# Debugging
## Install issues
See the notes under "other OSes" above fr=or the issues I ran into

## Possible HackRF Issues
### 10 Second Timeouts
Gnuradio-companion will timeout on UHD for 10 seconds every time you try to run a program. It's doing a DND lookup of a non-existant server for no reason, every time. This is an annoying and very old bug in soapyplutosdr 0.2.0. It was fixed in 2018, to fix it you need to uninstall 0.2.0 and build the latest version:

> sudo emerge -Ca net-wireless/soapyplutosdr

Then follow the instructions at this repo, copied here but possibly out of date:  
 > git clone https://github.com/pothosware/SoapyPlutoSDR  
 > cd SoapyPlutoSDR  
 > mkdir build  
 > cd build  
 > cmake ..  
 > make  
 > sudo make install  

Then download and run this repo.

### HackRF works once, hen needs to be reset to work a second time
You may be running 2018 firmware and 2021 libraries. Upgrade the HackRF firmware.

### Minute+ Timeouts
Soapy is still probably being idiotic and doing DNS queeries for non-existant things for no reason, and the DNS service is down. Best you can do may be to make sure the avahi-daemon is running so the pointless lookup is faster. In pentoo: sudo avahi-daemon. On other OSes: sudo service avahi restart

### Transmit Block Errors
To broadcast in 2019, I had to rebuild osmosdr_sink.blobk.yml with gen_osmosdr_blocks.py Instructions and files here:
https://gist.github.com/gbevan/8e583b9cf87aa3c58102251454fa48a6
https://github.com/osmocom/gr-osmosdr/blob/master/grc/gen_osmosdr_blocks.py
But I didn't seem to have to do that in 2021.
