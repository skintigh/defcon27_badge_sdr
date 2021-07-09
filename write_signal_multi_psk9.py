#Search for the CRC value for a packet, first in groups of 32 at a time, then a binary search to identify the exact value
#This version uses "9psk" to turn off 3 symbols (nulls?) which I think is what the badge does. Constellation shows 3 nulls, wave form of undiffed signal shows 2... Yet 3 is working better with bytes 13-15. 2/15
#older notes:
#This should work, but works intermittently. Something odd about the 3 dead symbols and 1 mystery symbol. Or timing is slightly off. Or the encoding isn't right as it looks different. Or diff is wrong. Or mapping.
#just worked repeat=10 8,8,8,1  GRC map on diff on. badge had been sitting idle a few hours. then it failed next 6 times. Needs a new count number? Sanity check between?
#	played a good packet, that worked, then it failed 4 more times with this packet
#	Changed end to 8,8,8,2 and it failed twice then worked
#   8883 worked once with diff on. diff off: nope. diff off no map: nope.  diff on no map: nope. map and neg diff: nope.    <===  delay was off? no.  adding or bypassing diff and map does not change delay.
#	8883 map then diff encode then modulate no diff: nope. Shouldn't that be the same???
#	8883 map then diff on: nope???
#   8884 didn't in a short test
#2/15:
#	End 8,8,8,8 works very infrequently
#   start with N end with 8-N,8,8 worked okay
#	start with N end with 888 worked excellently

import serial
import guesser
import sys
import compute_experimental
from timeit import default_timer as timer
from datetime import timedelta
import subprocess
from time import sleep
#from crc_list import crcs_10_ordered_by_symbol as crcs
import crc_math
import math # for log

PRINT_ALL_PACKETS = True
BREAK_AFTER_FIRST_FIND = True
CRC_REPEAT = 16 #times to repeat a CRC in a packet when searching
NUMSEGS = 16*CRC_REPEAT
SEGLEN = 256//CRC_REPEAT  #256/8 = 32, 256/16=16 
SEGBITS = int(math.log(SEGLEN,2))
REPEAT = 12 #40 works? 20 seems reliable 15 too, 10 works 2/3rds of time?  15 missed 2 out of 4 after I removed the +2 wrap-around   missed 1 when I put it back... 25 still flaky with with [8,8] in packet, many hits with [8,8,8]
			#20: 5 hits with 888. 10: 2+, 2, fail, fail, fail, fail, 2,  15: 2, seems to be very reliable, 2,2,2,3,2, missed 64,0,0
			#30 could still miss, let's try 15 but with 16 CRC repeats
			#after switching to using crc bytes, repeat of 15 gave 4 hits.
PREAMBLE = [4, 4, 4, 0,  4, 0, 4, 0,  2, 4, 6, 0,  0, 0, 0, 0,  6, 4, 2, 0] # + [0, 0, 4, 4] + [2, 7, 7, 4,  6, 7, 5, 6]

#crcrepeat of 16, 256 segments, repeat of 15, long header: 15.8"*256= 67:25 (assuming no findings or glitches) 4 packets when it hit
#256 segs, repeat of 8, half header (271ms): 9" * 256 = 38:24  2 hits
#256 seg, repeat 6, quarter header (136ms): miss twice
#6 200ms miss
#8 200ms miss
#8 250ms miss x 2
#8 half: miss miss miss then 2 packets, now it's acting lke crap. wtf
#16 half, 8 hits, miss, 4 hits, 
'''
def badge_check(serial_output):
	if "[*] Exiting Interactive Mode" in serial_output:
		print("Manually reboot the badge")
		sys.exit(1)
'''

def test_crc_range(crc_range_start, crc_range_len, data_bytes): #tests one range of CRCs          
	expected_symbols = [0]*4*(3+16+3)
	#compute packet to test groups of 8 CRCs
	#write binary packets for use by GNURadio
	with open("signal.bin","wb") as f:  #hardcoded filename...

		#test all CRCs in this chunk
		#for crc_inc in range(0,SEGLEN+2):  #was +2 to test wrap around nad use up extra space... A real packet is 272 long. With a repeat of 8 I was doing (32+2)*8 = 272. repeat of 16: (16+2)*16=288... yet that's working, but I should look into that
		for crc_inc in range(0,SEGLEN+(16//CRC_REPEAT)):  #was +2 to test wrap around nad use up extra space... A real packet is 272 long. With a repeat of 8 I was doing (32+2)*8 = 272. repeat of 16: (16+2)*16=288...
			crc_index = crc_inc%crc_range_len + crc_range_start
			crc_bytes = crc_math.crc_12bit_to_3bytes(crc_index)
			data_symbols = compute_experimental.compute(data_bytes+crc_bytes, expected_symbols, debug=False, ignore=8-3, print_error=False)[0:-2]
			diffed_packet = PREAMBLE + data_symbols

			#now that we have the diffed packet we need to undiff it for transmittion
			for n in range(0,CRC_REPEAT):  #global i guess

				#begin raw packet with a random number 0-7
				packet = [(1*n)%8]
				#packet = [(8-n)%8]

				#undiff the diffed packet
				for y in range(0,len(diffed_packet)):
					packet.append((packet[y]-diffed_packet[y])%8)
				
				#packet = packet + [(8-n)%8, 8, 8]  #reverse the start symbol because that's what I see in ground truth, then add 2 nulls
				#packet = packet + [(n)%8, 8, 8]  #reverse the start symbol because that's what I see in ground truth, then add 2 nulls
				packet = packet + [8, 8, 8]  #reverse the start symbol because that's what I see in ground truth, then add 2 nulls     waaaaaaaaaay more hits with [128, 135, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0] 

				assert(len(packet) == 110) #verify length is correct
				f.write(bytearray(packet))

		f.write(bytearray(20*[0]))   #padding to preserve end of last datagram



	#delete old wav to avoid confusion
	proc_ret = subprocess.run(["rm", "synthetic_signal.wav"])
	if proc_ret.returncode: print("Delete old signal .wav file exit code was: %d" % proc_ret.returncode)
		 
	#convert binary into 9PSK signal
	proc_ret = subprocess.run("grcc -r grc/d9psk_generator_no_gui_11905.grc".split(" "), stdout=subprocess.DEVNULL)
	if proc_ret.returncode: print("Generate new .wav exit code was: %d" % proc_ret.returncode)
	
	#trim extra samples
	proc_ret = subprocess.run("sox trans_output.wav trans_output_trim.wav trim 4s".split(" "))   #is this still correct?
	if proc_ret.returncode: print("Trim .wav exit code was: %d" % proc_ret.returncode)

	#concat header and signal
	#command = "sox " + REPEAT*"recordings/recorded_10.5551_PCsync_0PPM_119055_long_header.wav trans_output_trim.wav " + "synthetic_signal.wav"   #62 samples of 0   541ms
	command = "sox " + REPEAT*"recordings/recorded_10.5551_PCsync_0PPM_119055_long_header.wav trans_output_trim_327.5.wav " + "synthetic_signal.wav"
	#command = "sox " + REPEAT*"recordings/recorded_10.5551_PCsync_0PPM_119055_long_header_half.wav trans_output_trim.wav " + "synthetic_signal.wav"   # 271 ms hit
	#command = "sox " + REPEAT*"recordings/recorded_10.5551_PCsync_0PPM_119055_long_header_quarter.wav trans_output_trim.wav " + "synthetic_signal.wav"   #miss
	#command = "sox " + REPEAT*"recordings/recorded_10.5551_PCsync_0PPM_119055_long_header_200ms.wav trans_output_trim.wav " + "synthetic_signal.wav"   #
	#command = "sox " + REPEAT*"recordings/recorded_10.5551_PCsync_0PPM_119055_long_header_250ms.wav trans_output_trim.wav " + "synthetic_signal.wav"   #
	proc_ret = subprocess.run(command.split(" "))
	if proc_ret.returncode: print("Concat header and data files exit code was: %d" % proc_ret.returncode)
	

	# enter receive mode
	ser.write(b'R\r\n')
	sleep(1)
	serial_output = ser.read(100000)
	while serial_output:  	#read until there is no more output to prevent previous test from confusing this one
		#print('\nSetting RECEIVE mode output was "{}"'.format(serial_output.decode()))
		print('Setting RECEIVE mode output...')
		ser.write(b'R\r\n') #maybe this is needed but the sleep isn't?  or make timeout longer? put this before the sleep?
		sleep(2)  #needed? 1 didn't eat enough. I wonder if somehow the transmitter exits early...  2 didn't eat enough? added 1s above
		serial_output = ser.read(100000)
	#badge_check(serial_output.decode())


	#transmit the synthetic signal
	proc_ret = subprocess.run("grcc -r grc/player.grc".split(" "), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	if proc_ret.returncode: print("Player exit code was: %d" % proc_ret.returncode)

	#check if it was received
	found = False
	serial_output = ser.read(100000).decode()
	if serial_output: 
		#a packet was received!
		found = True

		#display the CRC segment and index/range
		if crc_range_len == 1: 
			print('CRC is in segment {} index {}'.format(crc_range_start//SEGLEN, crc_range_start),end="")
			print(diffed_packet)
		else: 
			print('CRC is in segment {} in range {} to {}'.format(crc_range_start//SEGLEN, crc_range_start,crc_range_start+crc_range_len-1),end="")

		if "length" in serial_output: #if there was data in the packet
			for line in serial_output.split("\r\n"): 
				if "length" in line: #find and print the line with the data
					print("\n"+line,end="")
					if PRINT_ALL_PACKETS: print()
					with open("multi_results.txt","a") as resf:
						resf.write("\n"+str(data_bytes)+"\n")
						resf.write('CRC is in range {} to {}\n'.format(crc_range_start,crc_range_start+crc_range_len-1))
						resf.write(line+"\n")
		ser.write(b'R\r\n') #badge usually exits receive mode after the first packet
		sleep(1)#was getting set receive mode msgs
		while serial_output: #eat all the responces			
			if PRINT_ALL_PACKETS:
				#sometimes the values are different!!!
				if "length" in serial_output: #if there was data in the packet
					for line in serial_output.split("\r\n"): 
						if "length" in line: #find and print the line with the data
							print(line)
			else:
				print(".",end="")


			serial_output = ser.read(100000).decode()
		print()
	return found



ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # open serial port
print("Connected to serial {}".format(ser.name))         	# check which port was really used
ser.write(b'H\r\n')     	# request the help menu   need a delay between commands or even \r\n ?
serial_output = ser.read(100000)
if "Ctrl-X: Exit interactive mode" not in serial_output.decode(): 
	print('Unexpected response from serial "{}" assuming the badge is already in receive mode'.format(serial_output.decode()))
else:
	ser.write(b'R\r\n')     	# enter receive mode
	serial_output = ser.read(100000)
	print(serial_output.decode())
#badge_check(serial_output.decode())  #obsolete with my hacked FW which ignores glitches on USB connection

seg_start = 0 +111
seg_end = NUMSEGS #last segment to test +1
for q in [128]*10 :
	new_seg = True
	#data_bytes = [0x80,0x87,0] + [0,0,0,0,11,0,0,0,0,0,0,0,0,] + q
	#data_bytes = [q,0x87,0] + [0,0,0,0,11] + 11*[0]
	#data_bytes = [0x80,0x87,0] + [0,0,0,0,11,0,0,0,0,0,0,0,0,0,0,pow(2,q)]
	#data_bytes = [0x80,0x87,0] + [0,0,0,0,11,0,0,0,0,0,0,0,0,0,pow(2,q),0]
	#data_bytes = [0x80,0x87,0] + [0,0,0,0,11,0,0,0,0,0,0,0,0,pow(2,q),0,0]
	data_bytes = [q,0x87, 0] + [0,0,0,0,11,0,0,0,0,0,0,0,0,0,0,0]

	print("\n\ndata_bytes =", data_bytes,"\n")
	assert(len(data_bytes)==19)

	#expected_symbols = [0]*4*len(data_bytes)
	#data_bytes = 16*[0]+[7,7,7,0,0,0]
	#data_symbols = compute_experimental.compute(data_bytes, expected_symbols, debug=False, ignore=8-3, print_error=False)
	#print(data_symbols)
	#sys.exit()
	#solution = guesser.solver([0]*(3+16), data_symbols, debug=False, ignore=5, print_error=False, print_result=False)
	#print(solution)
	#assert(solution == data_bytes) #verify it decodes to what I think it does. May not help if encoder is wrong in some sneaky way

	#iterate through possible CRCs in chunks
	seg = seg_start
	start = split = timer() #start timer
	while seg < seg_end:
		if new_seg:
			#print("Testing segment {} of {}".format(seg, NUMSEGS))
			print("Testing segment {}".format(seg),end = " ")
			sys.stdout.flush()
			new_seg = False
		else:
			print("{}".format(seg),end = " ")
			sys.stdout.flush()

		if test_crc_range(seg*SEGLEN, SEGLEN, data_bytes): #if in this batch of 16 or 32
			print("Found in range {} to {}".format(seg*SEGLEN,seg*SEGLEN+SEGLEN-1))  #1568 to 1599
			bits = 0

			for bitlevel in range(1,SEGBITS+1):
				div = 2**bitlevel
				bits = bits * 2
				#print("Testing range {} to {}".format(seg*SEGLEN+ bits*SEGLEN//div,  seg*SEGLEN+ bits*SEGLEN//div+ SEGLEN//div -1))
				if test_crc_range(seg*SEGLEN+ bits*SEGLEN//div, SEGLEN//div, data_bytes): 
					bits += 0
				else: 
					bits += 1 #assume!!! maybe I should double check all if it remains unreliable...

				print("bits = {:0{}b}{}".format(bits,bitlevel,'?'*(SEGBITS-bitlevel) ) )

			#if bits%2 == 1:  #verify only if last bit was a guess. That should be fine, except sometimes a positive result carries over from a previous test as I wasn't eating all of them...
			if True:
				print("Verifying CRC index {}... ".format(seg*SEGLEN+ bits*SEGLEN//div, end=""))
				if test_crc_range(seg*SEGLEN + bits*SEGLEN//div, SEGLEN//div, data_bytes):
					print("Success")
				else:
					print("FAILED!")
			
			seg += 1 #for timer math    assuming the find was succesful.........
			if BREAK_AFTER_FIRST_FIND: break #go to next data to test or exit program
			
		seg += 1
		end = timer()
		average = (end-start)/(seg-seg_start)
		print("Total elapse time: {} Segment split time {} Average segment time {} Remaining time {}".format(timedelta(seconds=end-start), timedelta(seconds=end-split), timedelta(seconds=average), timedelta(seconds=(NUMSEGS-seg)*average) ))
		split = end

	end = timer()
	average = (end-start)/(seg-seg_start)
	#print("\nTotal elapse time: {} Segment split time {} Average segment time {}".format(timedelta(seconds=end-start), timedelta(seconds=end-split), timedelta(seconds=average) ))

ser.close()             # close port