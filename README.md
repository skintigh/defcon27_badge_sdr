defcon27_badge_sdr
==================

Introduction
------------

The Defcon 27 badge communicates via NFMI bursts. Each burst has 4 sections. 
* Section 1 is 21 half-power clusters of 2 high frequency signals and a square wave with a short pause inbetween each cluster. I assume this is timing data for the PLL and maybe training for the D8PSK receiver. It's probably also used to set the amplifier on the antenna, hense it's half power to avoid damage.
* Section 2 is 2 copies of the datagram preamble with a pause inbetween: 
 > > 4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0  
 > > 4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 7 1  
 > > I think the last 12 or so symbols are the pause/noise. This is curious because the expected values are:  
 > > 4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6  
 > > This suggests those last 8 symbols are actually data of some sort...
* 3rd is 4 square waves with pauses. 7 0 0 0 0 0 0 0 0 0 0 2 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 5 3 
* 4th is 271 (yes, 271...?!?) copies of the same datagram. These program receive those signals, convert all 4 sections to symbols, and decode the datagrams from the 4th section only.

Each datagram consists of symbols. I'm going to refer to 4 symbols as a byte.

Each datagram consists of:
* 8 bytes of preamble (or 6 bytes of preample + 2 bytes of ?????)
* 16 bytes of data
* 2.5 bytes of something that seems random but is probably a CRC and maybe something else
* 1 byte of symbols that seem to be the signal decaying, as if a pause between datagrams. Maybe the half byte from the previous section belongs to this but it's not obvious.

For use by the badge, the 16 bytes of data consist of:
* 4 bytes of some sort of counter increasing by 2. Sometimes it's even, sometimes odd, and it doesn't seem to start at 0.
* 1 byte for the length of Defcon data, set to 8
* 8 bytes of Defcon data
* 3 more bytes that can be used by the badge if you hack it.

Install
-------

Install Pentoo on a physical machine. Common belief is SDR won't work on a VM. This seems true on Oracle Virtualbox, but earlier experiments of mine suggest VMWare might work.

Gnuradio-companion will timeout on UHD for 10 seconds every time you try to run a program. This is an annoying and very old bug in soapyplutosdr 0.2.0. It was fixed in 2018, to fix it you need to uninstall 0.2.0 and build the latest version:

> sudo emerge -Ca net-wireless/soapyplutosdr

Then follow the instructions at this repo, copied here but possibly out of date:  
 > git clone https://github.com/pothosware/SoapyPlutoSDR  
 > cd SoapyPlutoSDR  
 > mkdir build  
 > cd build  
 > cmake ..  
 > make  
 > sudo make install  

Files in this Repo
------------------

defcon_recv_and_decode.grc recieves these bursts and converts them to differential symbols.

parse_symbols.py parses that output file for unique symbol datagrams. Many will be corrupted by noise, so when a threshold of copies of one datagram is reached that is output as the valid datagram.

data_collector.py communicated with the badge via USB serial, updates the transmitted packet, then uses live output from the GRC file to collect the correcsponding datagram

recorder.grc records a wav file of the NFMI signal.

Running
-------

grc file are run in gnuradio_companion with a HackRF, or can be modified for other SDR hardware

py files are python 3 run at the command line
