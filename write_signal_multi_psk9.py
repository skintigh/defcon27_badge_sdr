#brute force the CRC value for a packet.
#This version uses "9psk" to turn off 3 symbols which I think is what the badge does
#This should work, but works intermittently. Something odd about the 3 dead symbols and 1 mystery symbol. Or timing is slightly off. Or the encoding isn't right as it looks different. Or diff is wrong. Or mapping.
#just worked repeat=10 8,8,8,1  GRC map on diff on. badge had been sitting idle a few hours. then it failed next 6 times. Needs a new count number? Sanity check between?
#	played a good packet, that worked, then it failed 4 more times with this packet
#	Changed end to 8,8,8,2 and it failed twice then worked
#   8883 worked once with diff on. diff off: nope. diff off no map: nope.  diff on no map: nope. map and neg diff: nope.    <===  delay was off? no.  adding or bypassing diff and map does not change delay.
#	8883 map then diff encode then modulate no diff: nope. Shouldn't that be the same???
#	8883 map then diff on: nope???
#   8884 didn't in a short test
#	Enf 8,8,8,8 works very infrequently

import serial
import guesser
import sys
#import compute
import compute_experimental
from timeit import default_timer as timer
from datetime import timedelta
import subprocess
from time import sleep
from crc_list import crcs_10_ordered_by_symbol as crcs_10

'''
def badge_check(serial_output):
	if "[*] Exiting Interactive Mode" in serial_output:
		print("Manually reboot the badge")
		sys.exit(1)
'''

def test_crc_range(crc_range_start, crc_range_len, data_bytes): #tests one range of CRCs           # TO DO: I could probably reduce repeats
	#compute packet to test groups of 8 CRCs
	#write binary packets for use by GNURadio
	with open("signal.bin","wb") as f:  #hardcoded filename

		#test all CRCs in this chunk
		#for crc_inc in range(0,SEGLEN+2):  #lets send 256 instead of 271 for now... lets not and sent 272...
		#for crc_inc in range(0,crc_range_len):  #was +2 to test wrap around nad use up extra space...
		for crc_inc in range(0,SEGLEN+2):  #was +2 to test wrap around nad use up extra space...

			crc_index = crc_inc%crc_range_len + crc_range_start
			crc_str = crcs[crc_index]
			#print(crc_str, end = " ")				#this just adds clutter
			#print(crc_index, end = " ")				#this just adds clutter

			
			crc_symbols = [int(c) for c in str(crc_str)]

			diffed_packet = preamble + data_symbols + crc_symbols

			#now that we have the diffed packet we need to undiff it for transmittion
			for n in range(0,CRC_REPEAT):  #global i guess

				#begin raw packet with a random number 0-7
				packet = [n]

				#undiff the diffed packet
				for y in range(0,len(diffed_packet)):
					packet.append((packet[y]-diffed_packet[y])%8)
				
				packet = packet + [(8-n)%8, 8, 8]  #reverse the start symbol because that's what I see in ground truth, then add 2 nulls

				assert(len(packet) == 110) #verify length is correct
				f.write(bytearray(packet))

		f.write(bytearray(20*[0]))   #padding to preserve end of last datagram



	#delete old wav to avoid confusion
	proc_ret = subprocess.run(["rm", "synthetic_signal.wav"])
	if proc_ret.returncode: print("Delete old signal .wav file exit code was: %d" % proc_ret.returncode)
		 
	#convert binary into 9PSK signal
	proc_ret = subprocess.run("grcc -r d9psk_generator_no_gui_11905.grc".split(" "), stdout=subprocess.DEVNULL)
	if proc_ret.returncode: print("Generate new .wav exit code was: %d" % proc_ret.returncode)
	
	#trim extra samples
	proc_ret = subprocess.run("sox trans_output.wav trans_output_trim.wav trim 4s".split(" "))   #is this still correct?
	if proc_ret.returncode: print("Trim .wav exit code was: %d" % proc_ret.returncode)

	#concat header and signal
	command = "sox " + REPEAT*"recordings/recorded_10.5551_PCsync_0PPM_119055_long_header.wav trans_output_trim.wav " + "synthetic_signal.wav"   #62 samples of 0
	proc_ret = subprocess.run(command.split(" "))
	if proc_ret.returncode: print("Concat header and data files exit code was: %d" % proc_ret.returncode)
	

	# enter receive mode
	ser.write(b'R\r\n')     	
	serial_output = ser.read(100000)
	while serial_output:  	#read until there is no more output to prevent previous test from confusing this one
		#print('\nSetting RECEIVE mode output was "{}"'.format(serial_output.decode()))
		print('Setting RECEIVE mode output...')
		ser.write(b'R\r\n') #maybe this is needed but the sleep isn't?  or make timeout longer? put this before the sleep?
		sleep(1)  #needed?
		serial_output = ser.read(100000)
	#badge_check(serial_output.decode())


	#transmit the synthetic signal
	proc_ret = subprocess.run("grcc -r player.grc".split(" "), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	if proc_ret.returncode: print("Player exit code was: %d" % proc_ret.returncode)


	serial_output = ser.read(100000).decode()
	while serial_output:
		print('\nReceived PACKET:\n"{}"'.format(serial_output))
		if "Unique" in serial_output or "Badge thinks USB-to-serial adapter is removed, ignoring" not in serial_output:
			print('CRC segment is', crc_range_start/SEGLEN)
			print('CRC is in range {} to {}'.format(crc_range_start,crc_range_start+crc_range_len-1))
			with open("multi_results.txt","a") as resf:
				resf.write(str(data_bytes))
				resf.write("\tsegment: "+str(crc_range_start/SEGLEN)+"\n")
				resf.write('CRC is in range {} to {}'.format(crc_range_start,crc_range_start+crc_range_len-1))
				resf.write(serial_output+"\n\n")
				#seg += 1 #for timer math
			return True
		#adge_check(serial_output)	#obsolete
		sleep(1)
		ser.write(b'R\r\n') #will this help? longer sleep? before sleep 2 didn't eat everything, after? maybe sleep 1 before and after?
		sleep(1)
		serial_output = ser.read(100000).decode()
	return False


#I thought using a CRC of length 11 was much more reliable than using 10. Not sure I took notes on it. might be some weird interaction before I used nulls
#4096 = min NUMSEGS 16*256 max SEGLEN

seg_start = 0


crcs = crcs_10
CRC_REPEAT = 8
NUMSEGS = 16*CRC_REPEAT
SEGLEN = 256//CRC_REPEAT
REPEAT = 20  #40 works? 20 seems reliable 15 too, 10 works 2/3rds of time?  15 missed 2 out of 4 after I removed the +2 wrap-around   missed 1 when I put it back...

#preamble 5+3 not 6+2?
#preamble = [4, 4, 4, 0,  4, 0, 4, 0,  2, 4, 6, 0,  0, 0, 0, 0,  6, 4, 2, 0,  0, 0, 4, 4] + [2, 7, 7, 4,  6, 7, 5, 6]
preamble = [4, 4, 4, 0,  4, 0, 4, 0,  2, 4, 6, 0,  0, 0, 0, 0,  6, 4, 2, 0,]#  0, 0, 4, 4] + [2, 7, 7, 4,  6, 7, 5, 6]

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # open serial port
#ser = serial.Serial('/tmp/ttyV0', 115200, timeout=1)  # open serial port
print("Connected to serial {}".format(ser.name))         	# check which port was really used
ser.write(b'H\r\n')     	# request the help menu   need a delay between commands or even \r\n ?
serial_output = ser.read(100000)
if "Ctrl-X: Exit interactive mode" not in serial_output.decode(): 
	print('Unexpected response from serial "{}" assuming the badge is already in receive mode'.format(serial_output.decode()))
else:
	ser.write(b'R\r\n')     	# enter receive mode
	serial_output = ser.read(100000)
	print(serial_output.decode())
	#""Waiting for Packet(s)...""

#badge_check(serial_output.decode())  #obsolete with my hacked FW

#zeroes with count
#data = [2,5,2,2, 6,6,2,7, 4,4,2,4, 4,1,6,7, 0,7,3,2,           5,4,3,5, 7,0,3,6, 4,0,7,3, 0,4,1,4, 4,2,7,4, 6,2,0,2, 0,7,6,6, 1,6,4,1, 3,1,4,4, 0,7,7,3, 5,2,7,7,]#,7,7,3, 0,3,1,6, 4,4])]  7773031644  #1/6 recording
#Trying segment 15 #Packet received: "0x0000000000000000

# now test all CRCs in segments
print()



data_bytes = [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0] #fail 2x
data_bytes = [1,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0] #failed once
data_bytes = [1,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0] #segment 118 0x0000000000014F00 once, failed 4 times after
data_bytes = [1,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0] #segment 16! 0x0000000000004F00, failed, reboot and fail, fail
data_bytes = [1,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0] #fail                                                I guess the count can't be that low, weird.

data_bytes = [10,10,10,0,0,0,0,0,0,0,0,0,0,0,0,0] #fail 2x
data_bytes = [10,10,10,0,1,0,0,0,0,0,0,0,0,0,0,0] # failx1.5 
data_bytes = [10,10,10,0,2,0,0,0,0,0,0,0,0,0,0,0] #segemnt 7    0x0000A30000014F00 3x
data_bytes = [10,10,10,0,3,0,0,0,0,0,0,0,0,0,0,0] #fail, seg 54 0x0000000000014F00 2x
data_bytes = [10,10,10,0,4,0,0,0,0,0,0,0,0,0,0,0] #0x0000000000014F00 107   worked twice! 3x!
data_bytes = [12,10,10,0,4,0,0,0,0,0,0,0,0,0,0,0] #seg 68 0x0000000000014F00		
data_bytes = [10,10,10,0,8,0,0,0,0,0,0,0,0,0,0,0] #0x0000000000000000 segment 121
data_bytes = [10,10,10,0,11,0,0,0,0,0,0,0,0,0,0,0] # seg 38 0x0000000000000000
data_bytes = [10,10,10,0,12,0,0,0,0,0,0,0,0,0,0,0] # failed 2x
data_bytes = [10,10,10,0,132,0,0,0,0,0,0,0,0,0,0,0] #128+4 failx3
data_bytes = [10,10,10,0,250,0,0,0,0,0,0,0,0,0,0,0] #fail
data_bytes = [10,10,10,0,255,0,0,0,0,0,0,0,0,0,0,0] #fail x3, all 3 with no restarts needed which is weird
data_bytes = [10,10,10,0,254,0,0,0,0,0,0,0,0,0,0,0] #fail x2
data_bytes = [0,0,1,0,2,0,0,0,0,0,0,0,0,0,0,0] #fail
data_bytes = [0,0,8,0,2,0,0,0,0,0,0,0,0,0,0,0] #seg 23 B d0 d0 d0 d0 E -- length = 4   0x0000C30000014F00
data_bytes = [0,0,4,0,2,0,0,0,0,0,0,0,0,0,0,0] #fail?
data_bytes = [0,0,6,0,2,0,0,0,0,0,0,0,0,0,0,0] #fail
data_bytes = [0,0,7,0,2,0,0,0,0,0,0,0,0,0,0,0] #fail
data_bytes = [255,255,7,0,2,0,0,0,0,0,0,0,0,0,0,0] #seg 81 0x0000C30000014F00
data_bytes = [255,255,7,0,1,0,0,0,0,0,0,0,0,0,0,0] #fail

data_bytes = [11,10,10,0,4,0,0,0,0,0,0,0,0,0,0,0] #2*10-2->18->segemnt 7. dumbass it's + not - ...  fail!?
data_bytes = [9 ,10,10,0,4,0,0,0,0,0,0,0,0,0,0,0] #2*10+2=22->segemnt 7. 2*9+4=22->  fail, wtf!?!
data_bytes = [128,32,8,0,8,0,0,0,0,0,0,0,0,0,0,0] #fail
data_bytes = [10,10,10,0,2,0,0,0,0,0,0,0,0,0,0,0] #segment 7 0x0000230000014F00
data_bytes = [11,10,10,0,4,0,0,0,0,0,0,0,0,0,0,0] #fail
data_bytes = [8 ,10,10,0,4,0,0,0,0,0,0,0,0,0,0,0] #fail with 3 glitches   maybe becaues compute is wrong I'm not making the expected packet?
data_bytes = [32,128,8,0,4,0,0,0,0,0,0,0,0,0,0,0] #seg 74 0x0000000000014F00
data_bytes = [28,128,8,0,6,0,0,0,0,0,0,0,0,0,0,0] #fail

#using new compute
#data_bytes = [8,10,10,0,4,0,0,0,0,0,0,0,0,0,0,0] 
data_bytes = [0x80,0x87,0, 10,10,10,0,2,0,0,0,0,0,0,0,0,0,0,0] #seg 7, B d0 d0 d0 d0 E -- length = 4 0x0000230000014F00
data_bytes = [0x80,0x87,0, 6,10,10,0,4,0,0,0,0,0,0,0,0,0,0,0] #fail 2x
data_bytes = [0x80,0x87,0, 4,10,10,0,8,0,0,0,0,0,0,0,0,0,0,0] #fail 3x
data_bytes = [10,10,10,0,3,0,0,0,0,0,0,0,0,0,0,0] #fail
data_bytes = [10,10,10,0,2,0,0,0,0,0,0,0,0,0,0,0] #seg 7, B d0 d0 d0 d0 E              -- length = 4 0x0000230000014F00 work x2, fail, work x2 , fail, work --- at repeat of 10.
data_bytes = [10,10,10,0,4,0,0,0,0,0,0,0,0,0,0,0] #seg 107 B d0 d0 d0 d0 d0 d0 d0 d0 E -- length = 8 0x0000000000014F00
data_bytes = [10,10,10,0,8,0,0,0,0,0,0,0,0,0,0,0] #seg 121 data_bytes = [10,10,10,0,4,0,0,0,0,0,0,0,0,0,0,0]
data_bytes = [10,10,10,0,10,0,0,0,0,0,0,0,0,0,0,0] #fail
data_bytes = [10,10,10,0,11,0,0,0,0,0,0,0,0,0,0,0] #seg 38 B d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d7 d0 d7 d0 d7 E -- length = 22  0x0000000000000000  070707?? workx4
#data_bytes = [10,10,10,0,9,0,0,0,0,0,0,0,0,0,0,0] #fail x2
#data_bytes = [0,0,16,0,10,0,0,0,0,0,0,0,0,0,0,0] #fail
data_bytes = [1,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0] #seg 16 fail shortx2
#0 failed
data_bytes = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #seg 49  B d0 d0 E -- length = 2 0x0000E30000014F00 0x0000FF003500FF00  failx2 worked 0x0000230000014F00 0x0000FF003500FF00 fail 0x0000230000014F00
#fail 0x0000230000014F00  0x0000230000014F00 0x0000FF003500FF00

#0, 1 failed
#[128, 135, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]	segment: 107  0x0000E30000014F00 0x0000FF003500FF00
#3 failed
#[128, 135, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]	segment: 7     0x0000000000014F00              so 3 times count 0 0 0 had same crc as 10 10 10  0x000000003500FF00 0x00000000990001FF
#5, 6 failed
#[128, 135, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]	segment: 72 0x0000000000000000
#[128, 135, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]	segment: 17 0x0000000000000000
#9 failed

#[128, 135, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] segment: 91 B d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d7 d0 d7 d0 d7 E -- length = 22 0x0000000000000000
#[128, 135, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] segment: 0  B d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d7 d0 d7 d0 d7 E -- length = 22 0x0000000000000000

#seg_start = 118
#for q in [65]+[qq for qq in range(71,256)]:
for q in [] + [qq for qq in range(171,256)]:
	new_seg = True
	data_bytes = [0,0,0,0,q,0,0,0,0,0,0,0,0,0,0,0]
	data_bytes = [1,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0]
	#prepend mutable preambls
	data_bytes = [0x80,0x87,0] + data_bytes
	print("data_bytes =", data_bytes,"\n")
	assert(len(data_bytes)==19)

	expected_symbols = [0]*4*len(data_bytes)
	data_symbols = compute_experimental.compute(data_bytes, expected_symbols, debug=False, ignore=8-3, print_error=False)
	#print(data_symbols)

	solution = guesser.solver([0]*(3+16), data_symbols, debug=False, ignore=5, print_error=False, print_result=False)
	#print(solution)
	assert(solution == data_bytes) #verify it decodes to what I think it does. May not help if encoder is wrong in some sneaky way

	#iterate through possible CRCs in chunks
	seg = seg_start
	start = split = timer() #start timer
	while seg < NUMSEGS:
		if new_seg:
			#print("Testing segment {} of {}".format(seg, NUMSEGS))
			print("Testing segment {}".format(seg),end = " ")
			sys.stdout.flush()
			new_seg = False
		else:
			print("{}".format(seg),end = " ")
			sys.stdout.flush()

		#run a test of 32 CRCs
		#if True:
		if test_crc_range(seg*SEGLEN, SEGLEN, data_bytes): #if in this batch of 32
			print("Found in range {} to {}".format(seg*SEGLEN,seg*SEGLEN+SEGLEN-1))  #1568 to 1599
			bits = 0
			for bitlevel in range(1,6):
				div = 2**bitlevel
				bits = bits * 2
				print("Testing range {} to {}".format(seg*SEGLEN+ bits*SEGLEN//div,  seg*SEGLEN+ bits*SEGLEN//div+ SEGLEN//div -1))
				if test_crc_range(seg*SEGLEN+ bits*SEGLEN//div, SEGLEN//div, data_bytes): 
					bits += 0
				else: 
					bits += 1 #assume!!!
				print("################")
				print("# bits = {:0{}b}{} #".format(bits,bitlevel,'?'*(5-bitlevel)))
				print("################")

			#if bits%2 == 1:
			if True:
				print("verifying assumed bits...")
				print("Testing range {} to {}".format(seg*SEGLEN+ bits*SEGLEN//div,  seg*SEGLEN+ bits*SEGLEN//div+ SEGLEN//div -1))
				if test_crc_range(seg*SEGLEN + bits*SEGLEN//div, SEGLEN//div, data_bytes):
					print("Verification successful")
				else:
					print("Failure to verify CRC!\n # bits = {:05b}".format(bits))

			'''
			#16
			div = 2
			bits = 0
			if test_crc_range(seg*SEGLEN+ bits*SEGLEN//div, SEGLEN//div, data_bytes): bits = bite + 0
			else: bits = 1 #assume!!!

			#8
			div *= 2
			bits *= 2
			if test_crc_range(seg*SEGLEN + bits*SEGLEN//div, SEGLEN//div, data_bytes): bits = bits + 0
			else: bits = bits + 1 #assume!!!

			#4
			div *= 2
			bits *= 2			
			if test_crc_range(seg*SEGLEN + bits*SEGLEN//div, SEGLEN//div, data_bytes): bits = bits + 0
			else: bits = bits + 1 #assume!!!

			#2
			div *= 2
			bits *= 2			
			if test_crc_range(seg*SEGLEN + bits*SEGLEN//div, SEGLEN//div, data_bytes): bits = bits + 0
			else: bits = bits + 1 #assume!!!

			#1
			div *= 2
			bits *= 2		
			if test_crc_range(seg*SEGLEN + bits*SEGLEN//div, SEGLEN//div, data_bytes): bits = bits + 0
			else: #
				bits = bits + 1 #assume!!! this bit is assumes, maybe wrong, maybe earlier assumption wrong
				if not test_crc_range(seg*SEGLEN + bits*SEGLEN//div, SEGLEN//div, data_bytes):
					printf("Failure to verify CRC!\n bits = {:05b}".format(bits))
			'''					
			'''
			if bit2*bit2*bit0: #if all bits are assumed, better double check
				if not test_crc_range(seg*SEGLEN+bit2*SEGLEN//2+bit1*SEGLEN//4,bit0*SEGLEN//8, SEGLEN//8, data_bytes):
					printf("Failure to verify CRC!")
			'''
			seg += 1 #for timer math    assuming the find was succesful.........
			break
			


		'''
		#compute back to test groups of 8 CRCs

		#write binary packets for use by GNURadio
		with open("signal.bin","wb") as f:

			#test all CRCs in this chunk
			for crc_inc in range(0,SEGLEN+2):  #lets send 256 instead of 271 for now... lets not and sent 272...

				crc_index = crc_inc%SEGLEN + seg*SEGLEN
				crc_str = crcs[crc_index]
				#print(crc_str, end = " ")				#this just adds clutter
				#print(crc_index, end = " ")				#this just adds clutter

				
				crc_symbols = [int(c) for c in str(crc_str)]

				diffed_packet = preamble + data_symbols + crc_symbols

				#now that we have the diffed packet we need to undiff it for transmittion
				for n in range(0,CRC_REPEAT):

					#begin raw packet with a random number 0-7
					packet = [n]

					#undiff the diffed packet
					for y in range(0,len(diffed_packet)):
						packet.append((packet[y]-diffed_packet[y])%8)
					
					packet = packet + [(8-n)%8, 8, 8]  #reverse the start symbol because that's what I see in ground truth, then add 2 nulls

					assert(len(packet) == 110) #verify length is correct
					f.write(bytearray(packet))

			f.write(bytearray(20*[0]))   #padding to preserve end of last datagram

		


		#delete old wav to avoid confusion
		proc_ret = subprocess.run(["rm", "synthetic_signal.wav"])
		if proc_ret.returncode: print("Delete old signal .wav file exit code was: %d" % proc_ret.returncode)
			 
		#convert binary into 9PSK signal
		proc_ret = subprocess.run("grcc -r d9psk_generator_no_gui_11905.grc".split(" "), stdout=subprocess.DEVNULL)
		if proc_ret.returncode: print("Generate new .wav exit code was: %d" % proc_ret.returncode)
		
		#trim extra samples
		proc_ret = subprocess.run("sox trans_output.wav trans_output_trim.wav trim 4s".split(" "))   #is this still correct?
		if proc_ret.returncode: print("Trim .wav exit code was: %d" % proc_ret.returncode)

		#concat header and signal
		command = "sox " + REPEAT*"recordings/recorded_10.5551_PCsync_0PPM_119055_long_header.wav trans_output_trim.wav " + "synthetic_signal.wav"   #62 samples of 0
		proc_ret = subprocess.run(command.split(" "))
		if proc_ret.returncode: print("Concat header and data files exit code was: %d" % proc_ret.returncode)
		


		# enter receive mode
		ser.write(b'R\r\n')     	
		serial_output = ser.read(10000)
		if serial_output: print('\nSetting rec mode output was "{}"'.format(serial_output.decode()))
		badge_check(serial_output.decode())

		

		#transmit the synthetic signal
		proc_ret = subprocess.run("grcc -r player.grc".split(" "), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		if proc_ret.returncode: print("Player exit code was: %d" % proc_ret.returncode)


		serial_output = ser.read(10000).decode()
		if serial_output:
			print('\nReceived:\n"{}"'.format(serial_output))
			if "Unique" in serial_output or "Badge thinks USB-to-serial adapter is removed, ignoring" not in serial_output:
				print('CRC segment is', seg)
				with open("multi_results.txt","a") as resf:
					resf.write(str(data_bytes))
					resf.write("\tsegment: "+str(seg)+"\n")
					resf.write(serial_output+"\n\n")
					seg += 1 #for timer math
				break;
			badge_check(serial_output)

		'''

		seg += 1
		end = timer()
		average = (end-start)/(seg-seg_start)
		#print("Total elapse time: {} Segment split time {} Average segment time {} Remaining time {}".format(timedelta(seconds=end-start), timedelta(seconds=end-split), timedelta(seconds=average), timedelta(seconds=(NUMSEGS-seg)*average) ))
		split = end



	end = timer()
	average = (end-start)/(seg-seg_start)
	#print("\nTotal elapse time: {} Segment split time {} Average segment time {}".format(timedelta(seconds=end-start), timedelta(seconds=end-split), timedelta(seconds=average) ))
ser.close()             # close port