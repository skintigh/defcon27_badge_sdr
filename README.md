# defcon27_badge_sdr

Install

Install Pentoo on a physical machine. Common belief is it SDR won't work on a VM. This seems correct on Oracle Virtualbox, but earlier experiments of mine indicated VMWare might work.

Gnuradio-companion will timeout on UHD for 10 seconds every time you try to run a program. This is a very old bug in 0.2.0. It was fixed in 2018, to fix it you need to uninstall 0.2.0 and build the latest version. Directions...

Intro

Defcon 27 badge communicates via NFMI bursts. Each burst has 4 sections -- first 2 seem to be timing, 3rd might be data of unknown importance, 4th is many (100s?) copies of the same datagram.

Files
defcon_recv_and_decode.grc recieves these bursts and converts them to differential symbols.

parse_symbols.py parses that output file for unique symbol datagrams. Many will be corrupted by noise, so when a threshold of copies of one datagram is reached that is output as the valid datagram.

data_collector.py communicated with the badge via USB serial, updates the transmitted packet, then uses live output from the GRC file to collect the correcsponding datagram

recorder.grc records a wav file of the NFMI signal.
