###########################################################################################
#This program guesses data bits to match a known/given zero-state and an known output value

sanity_debug = False
import sys, ast
#from compute import compute
from compute_experimental import compute
import compute_experimental
divider = "-"*120


def solver(in_data_orig, expected_orig, debug=False, ignore=0, print_error=False, print_result=False, default=True, zeros_symbols=False, delta_1347=False, delta_2=False, delta_6=False):  #in_data_orig and expected are ONLY the values to be computed, ignore sets the pos in zero_symbols
	in_data = in_data_orig.copy()# prevent modification of data
	expected = expected_orig.copy()#+8*[0]
	if debug:# and False:
		print("solver() debug:")
		print("in_data",in_data)
		print("len",len(in_data)*4)
		print("expected",expected)
		print("len",len(expected))

	#removed for experimental_compute
	#if not default or zeros_symbols or delta_1347 or delta_2 or delta_6:
	#	assert(zeros_symbols and delta_1347 and delta_2 and delta_6)

	if default: sum = compute(in_data, expected+8*[0], debug, ignore, print_error)
	else: 
		#print("not default1")
		sum = compute(in_data, expected+8*[0], debug, ignore, print_error, zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)
	#L = (len(in_data) - ignore)*4
	L = (len(in_data))*4
	#while sum[0:L] != expected[0:L]:
	#while sum[4*ignore:L+4*ignore] != expected[4*ignore:L+4*ignore]:
	while sum[0:L] != expected[0:L]:
		if debug: 
			print()
			print("solver debug")
			print("sum", sum)
			print("exp", expected)
		#print(ignore, L)

		for x in range(0,L):
			if sum[x] != expected[x]:
				in_data[x//4] += 1<<2*(x%4)	
				if (in_data[x//4] // (1<<2*(x%4))) > 3: 
					if print_error:
						print("solver print_error:")
						print("sum", sum)
						print("exp", expected)					#sys.exit(1)
						print("Impossible at symbol", x)
					return "Impossible"
				if default: sum = compute(in_data, expected, debug, ignore, print_error)
				else: 
					#print("not default2")
					sum = compute(in_data, expected, debug, ignore, print_error,zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)
				break	
		
	if print_result:
		print("solver results:")
		#print("Sum          :",sum)
		#print("Expected     :",expected[4*ignore:])
		print("Found:        ", end="")
		for c in in_data: 	print("{:3d}".format(c),end=" ")
		print("\nHex:          ", end="")
		for c in in_data: 	print("x{:02x}".format(c),end=" ")
		print("\nASCII:          ", end="")
		for c in in_data: 
			if c<16 or c >= 0x80: print("?",end="   ")
			else: print(chr(c),end="   ")   #printing 9e or 9e 6e kills python???
		'''
		print("\nRev hex:      ", end="")
		for c in in_data: 		
			print(hex(c%16*16+c//16),end=" ")
		print("\nrev hex ASCII ", end="")
		for c in in_data:
			if c >= 0x80: print("?",end=" ")
			else: print(chr(c%16*16+c//16),end=" ")
		'''
		print()

	return in_data

if __name__ == "__main__":   #only run if this file is run as main script

	if sanity_debug: print("Sanity check: some value that I guess was tricky... ", end="")
	solution = solver([4,4], [2, 1, 2, 0, 5, 5, 6, 1], debug=False, ignore=8, print_result=False)#, print_error=False, print_result=False)
	if solution == "Impossible": 
		print("\n*** Failed sanity check")
		sys.exit(1)
	if sanity_debug: print("Pass")

	lowest_count_seen_symbols = [4,0,0,6, 1,4,5,1, 4,3,1,2, 3,3,6,7, 0,3,3,2]
	solution = solver([0,0,0], lowest_count_seen_symbols, debug=False, ignore=8, print_error=False, print_result=False)		#lowest count seen [45, 74, 5] 346669 (or [45, 74, 197]   0x2d 0x4a 0xc5  - J ?)
	if solution == "Impossible": 
		print("*** Failed to computer lowest count sanity check")
		sys.exit(1)
	count = solution[0]+256*solution[1]+256*256*solution[2]
	if sanity_debug: print("Sanity check: Computed lowest count seen:", solution, count, end="... ")
	#should probably check the value is correct, now that I (think) I know the correct value
	if count != 346637:
		print("\n*** Failed sanity check: expected [13, 74, 5] 346637")
		sys.exit(1)
	if sanity_debug:print("Pass")
	if sanity_debug:print(divider)


	#guess all in file *with* preamble
	if 1: 
		print("guess/solve values for all packets in file *including* last 3 bytes of preamble")# (and manually verify second count digit no longer vascilates by 8)")
		filename = "temp.txt"
		with open(filename, "r") as infile:	
			print("using file:", filename)
			line = infile.readline()
			while line:
				#with preamble and crc
				symbols = [0,0,4,4, 2,7,7,4, 6,7,5,6] + [int(n) for n in line.split(' ')[0:-2]] #drop the count at end, 
				solution = solver([0]*(16+3+3), symbols+[0,0], debug=False, ignore=8-3, print_error=False, print_result=False)

				#print in decimal					
				#print (solution) 

				crc = solution[-1]*65536 +solution[-2]*256 + solution[-3]
				print(solution[0:],"    \t{:05x}".format(crc))
				#print in hex
				#for c in solution: 	print("x{:02x}".format(c),end=" ")
				#print()



				line = infile.readline()
		if sanity_debug: print(divider)

	#similar CRCs, from when I was trying to reverse engineer the CRC
	if 0:
		print("these 2 have the same crc:")
		packet = [4,2,1,0,7,0,6,1,3,2,4,2,2,2,7,5,6,2,5,6,4,7,2,5,5,7,1,0,1,5,6,1,2,5,3,2,4,1,5,4,6,2,0,2,0,7,6,6,1,6,4,1,5,2,3,4,4,7,5,1,1,2,5,5  ,1,4,4,0,6,1,1,1,2,4,4  ,0]
		solution = solver(len(packet)//4*[0], packet, ignore=8, debug=False, print_error=False, print_result=False)  #ignore preamble
		for x in solution: print("%.2x"%x,end="")
		print(" {:05x}".format(solution[-1]*65536 + solution[-2]*256 + solution[-3]))
		packet = [4,2,1,0,7,0,6,1,3,2,4,2,2,2,7,5,2,4,0,0,2,1,6,0,5,5,2,5,3,5,6,1,2,5,3,2,4,1,5,4,6,2,0,2,0,7,6,6,1,6,4,1,5,2,3,4,4,7,5,1,1,2,5,5  ,1,4,4,0,6,1,1,1,2,4,4 ,0]
		solution = solver(len(packet)//4*[0], packet, ignore=8, debug=False, print_error=False, print_result=False)  #ignore preamble
		for x in solution: print("%.2x"%x,end="")
		print(" {:05x}".format(solution[-1]*65536 + solution[-2]*256 + solution[-3]))
		print()

		print("these have similar crcs:")
		#packet = [4,2,1,0,7,0,6,1,3,2,4,2,2,2,7,5,2,6,5,4,1,7,7,6,6,7,2,5,3,5,6,1,2,5,3,2,4,1,5,4,6,2,0,2,0,7,6,6,1,6,4,1,5,2,3,4,4,7,5,1,1,2,5,5  ,5,4,4,0,6,1,1,1,2,4,3 ,0]
		packet = [4,2,1,0,7,0,6,1,3,2,4,2,2,2,7,5,2,6,5,4,1,7,7,6,6,7,2,5,3,5,6,1,2,5,3,2,4,1,5,4,6,2,0,2,0,7,6,6,1,6,4,1,5,2,3,4,4,7,5,1,1,2,5,5  ,5,4,4,0,6,1,1,1,2,4, 4 ,0]
		solution = solver(len(packet)//4*[0], packet, ignore=8, debug=False, print_error=False, print_result=False)  #ignore preamble
		for x in solution: print("%.2x"%x,end="")
		print(" {:05x}".format(solution[-1]*65536 + solution[-2]*256 + solution[-3]))

		packet = [4,2,1,0,7,0,6,1,3,2,4,2,2,2,7,5,2,6,3,1,1,4,5,7,0,0,4,5,3,5,6,1,2,5,3,2,4,1,5,4,6,2,0,2,0,7,6,6,1,6,4,1,5,2,3,4,4,7,5,1,1,2,5,5  ,1,4,4,0,6,1,1,1,6,0,4 ,0]
		solution = solver(len(packet)//4*[0], packet, ignore=8, debug=False, print_error=False, print_result=False)  #ignore preamble
		for x in solution: print("%.2x"%x,end="")
		print(" {:05x}".format(solution[-1]*65536 + solution[-2]*256 + solution[-3]))
		
		packet = [4,2,1,0,7,0,6,1,3,2,4,2,2,2,7,5,2,4,2,5,2,6,0,5,7,6,4,5,3,5,6,1,2,5,3,2,4,1,5,4,6,2,0,2,0,7,6,6,1,6,4,1,5,2,3,4,4,7,5,1,1,2,5,5  ,5,4,4,0,6,1,1,1,6,0,4 ,0]
		solution = solver(len(packet)//4*[0], packet, ignore=8, debug=False, print_error=False, print_result=False)  #ignore preamble
		for x in solution: print("%.2x"%x,end="")
		print(" {:05x}".format(solution[-1]*65536 + solution[-2]*256 + solution[-3]))




		print("\nAgain but with 00 after 10 crc symbols")
		print("these 2 have the same crc:")
		packet = [4,2,1,0,7,0,6,1,3,2,4,2,2,2,7,5,6,2,5,6,4,7,2,5,5,7,1,0,1,5,6,1,2,5,3,2,4,1,5,4,6,2,0,2,0,7,6,6,1,6,4,1,5,2,3,4,4,7,5,1,1,2,5,5  ,1,4,4,0,6,1,1,1,2,4,0  ,0]
		solution = solver(len(packet)//4*[0], packet, ignore=8, debug=False, print_error=False, print_result=False)  #ignore preamble
		for x in solution: print("%.2x"%x,end="")
		print(" {:05x}".format(solution[-1]*65536 + solution[-2]*256 + solution[-3]))

		packet = [4,2,1,0,7,0,6,1,3,2,4,2,2,2,7,5,2,4,0,0,2,1,6,0,5,5,2,5,3,5,6,1,2,5,3,2,4,1,5,4,6,2,0,2,0,7,6,6,1,6,4,1,5,2,3,4,4,7,5,1,1,2,5,5  ,1,4,4,0,6,1,1,1,2,4,0 ,0]
		solution = solver(len(packet)//4*[0], packet, ignore=8, debug=False, print_error=False, print_result=False)  #ignore preamble
		for x in solution: print("%.2x"%x,end="")
		print(" {:05x}".format(solution[-1]*65536 + solution[-2]*256 + solution[-3]))
		print()

		print("these have similar crcs:")
		#packet = [4,2,1,0,7,0,6,1,3,2,4,2,2,2,7,5,2,6,5,4,1,7,7,6,6,7,2,5,3,5,6,1,2,5,3,2,4,1,5,4,6,2,0,2,0,7,6,6,1,6,4,1,5,2,3,4,4,7,5,1,1,2,5,5  ,5,4,4,0,6,1,1,1,2,4,3 ,0]
		packet = [4,2,1,0,7,0,6,1,3,2,4,2,2,2,7,5,2,6,5,4,1,7,7,6,6,7,2,5,3,5,6,1,2,5,3,2,4,1,5,4,6,2,0,2,0,7,6,6,1,6,4,1,5,2,3,4,4,7,5,1,1,2,5,5  ,5,4,4,0,6,1,1,1,2,4, 0 ,0]
		solution = solver(len(packet)//4*[0], packet, ignore=8, debug=False, print_error=False, print_result=False)  #ignore preamble
		for x in solution: print("%.2x"%x,end="")
		print(" {:05x}".format(solution[-1]*65536 + solution[-2]*256 + solution[-3]))

		packet = [4,2,1,0,7,0,6,1,3,2,4,2,2,2,7,5,2,6,3,1,1,4,5,7,0,0,4,5,3,5,6,1,2,5,3,2,4,1,5,4,6,2,0,2,0,7,6,6,1,6,4,1,5,2,3,4,4,7,5,1,1,2,5,5  ,1,4,4,0,6,1,1,1,6,0,0 ,0]
		solution = solver(len(packet)//4*[0], packet, ignore=8, debug=False, print_error=False, print_result=False)  #ignore preamble
		for x in solution: print("%.2x"%x,end="")
		print(" {:05x}".format(solution[-1]*65536 + solution[-2]*256 + solution[-3]))
		
		packet = [4,2,1,0,7,0,6,1,3,2,4,2,2,2,7,5,2,4,2,5,2,6,0,5,7,6,4,5,3,5,6,1,2,5,3,2,4,1,5,4,6,2,0,2,0,7,6,6,1,6,4,1,5,2,3,4,4,7,5,1,1,2,5,5  ,5,4,4,0,6,1,1,1,6,0,0 ,0]
		solution = solver(len(packet)//4*[0], packet, ignore=8, debug=False, print_error=False, print_result=False)  #ignore preamble
		for x in solution: print("%.2x"%x,end="")
		print(" {:05x}".format(solution[-1]*65536 + solution[-2]*256 + solution[-3]))
		print(divider)
		sys.exit()

	#test with a startup data packet.        #correct value is ?!?!?
	if 0:
		print("Test with a startup data packet of (I think) NFMI buffer address")
		#startup #1
		packet = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6,6,1,4,1,5,0,5,2,3,0,0,0,2,1,5,5,0,3,3,2,5,4,5,0,5,0,0,6,2,6,2,3,2,3,5,4,2,4,6,1,7,3,1,1,5,5,1,6,1,7,6,1,1,4,1,1,6,7,7,3,5,2,7,7]#, 5,0,0,3,6,0,4,4,0,0, 4,0,7,7] startup #1
		packet = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6, 6,1,4,1,5,0,5,2,3,0,0,0,2,1,5,5,0,3,3,2, 5,4,5,0,5,0,0,6,2,6,2,3,2,3,5,4,2,4,6,1,7,3,1,1,5,5,1,6,1,7,6,1,1,4,1,1,6,7,7,3,5,2,7,7, 5,0,0,3,6,0,4,4,0,0, 0,0]#4,0,7,7]
		#packet =                                                                 [6,1,4,1,5,0,5,2,3,0,0,0,2,1,5,5,0,3,3,2,5,4,5,0,5,0,0,6,2,6,2,3,2,3,5,4,2,4,6,1,7,3,1,1,5,5,1,6,1,7,6,1,1,4,1,1,6,7,7,3,5,2,7,7]#, 5,0,0,3,6,0,4,4,0,0, 4,0,7,7]
		print("length in symbols =", len(packet))
		solution = solver(len(packet)//4*[0], packet, ignore=0, debug=False, print_error=False, print_result=True)  #ignore preamble
		print("badge recieves 0xC0005A0081FF4F00   0x7300E30000014F00 0xD500FF003500FF00 3x 0x0000C000990001FF 0x7300230000014F00   0xD500FF003500FF00 then 5x 0x0000C000990001FF")
		print('But now I know that since the packet length is "0" the badge is just printing uninitialized buffer, so I shouldn\'t expect the values to match.')
		'''
		Found:        [150, 1, 169, 0, 2, 48, 180, 48, 179, 77, 48, 52, 53, 0, 0, 0]
		Hex:          0x96 0x1 0xa9 0x0 0x2    0x30 0xb4 0x30 0xb3 0x4d 0x30 0x34 0x35 0x0 0x0 0x0 
		ASCII:        ?  ?   0 ? 0 ? M 0 4 5   
		
		new compute:                   !!! length 0
		Found:        150   1 169   0   0  48  52  48  51  69  48  52  53   0   0   0 
		Hex:          x96 x01 xa9 x00 x00 x30 x34 x30 x33 x45 x30 x34 x35 x00 x00 x00 
		ASCII:          ?   ?   ?   ?   ?   0   4   0   3   E   0   4   5   ?   ?   ?  
		badge recieves 0xC0005A0081FF4F00
		'''
		

		print("\nTest another startup packet")
		startup3 = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6,  
					2, 7, 3, 4,  2, 7, 3, 5,  3, 4, 4, 2,  3, 4, 0, 7,  0, 7, 3, 2, 
		            5, 4, 5, 0,  5, 0, 0, 6,  2, 6, 2, 3,  2, 3, 5, 4,  2, 4, 6, 1,  7, 3, 1, 1,  5, 5, 1, 6,  1, 7, 6, 1,  1, 4, 1, 1,  6, 7, 7, 3,  5, 2, 7, 7,  
		            7, 1, 2, 5,  2, 7, 2, 4, 0, 0,   0,0]
		startup3=[4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6,2,7,3,4,2,7,3,5,3,4,4,2,3,4,0,7,0,7,3,2,5,4,5,0,5,0,0,6,2,6,2,3,2,3,5,4,2,4,6,1,7,3,1,1,5,5,1,6,1,7,6,1,1,4,1,1,6,7,7,3,5,2,7,7, 7,1,2,5,2,7,2,4,0,0,0,0]		
		#This test used to fail on symbol 16, probably because symbols 12-19 were (still basically are) guesses
		solution = solver(len(startup3)//4*[0], startup3, ignore=0, debug=False, print_error=False, print_result=True)  #ignore preamble

		'''
		badge actually receives 0x3034303345303435

		Found:          0   0   0   0   0 128 135   0 200 230   4   0   8  48  52  48  51  69  48  52  53   0   0   0 172 138  10 
		Hex:          x00 x00 x00 x00 x00 x80 x87 x00 xc8 xe6 x04 x00 x08 x30 x34 x30 x33 x45 x30 x34 x35 x00 x00 x00 xac x8a x0a 
		ASCII:          ?   ?   ?   ?   ?   ?   ?   ?   ?   ?   ?   ?   ?   0   4   0   3   E   0   4   5   ?   ?   ?   ?   ?   ?   
		'''


		#old results
		# Found: [0, 0, 0, 0, 0, 0, 0, 0, 51, 51, 13, 0, 0, 48, 52, 176, 51, 69, 48, 52, 149, 0, 0, 0, 129, 170]
		# 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x33 0x33 0xd 0x0 0x0 0x30 0x34 0xb0 0x33 0x45 0x30 0x34 0x95 0x0 0x0 0x0 0x81 0xaa 
	    # 3 3 \d   0 4 ° 3 E 0 4      ª  

		print("\nPacket of 8 0s, source is ??")
		packet = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6,2,5,2,2,6,6,2,7,4,4,2,4,4,1,6,7,0,7,3,2,5,4,3,5,7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7, 7,7,7,3,0,3,1,6,4,4  ,0,0]
		solution = solver(len(packet)//4*[0], packet, ignore=0, debug=False, print_error=False, print_result=True)  #ignore preamble
		print(divider)
	
	#potential sanity check, didn't end up needing it
	#startup transmit packet [*] Loading Data: 0xD7D6DCD8D7D2DFDBD0D0D0D0D7DFD0D0
	#0x76C872FB00007F00
	if 0:
		packet = [2,1,2,2,2,6,0,2,0,7,4,1,2,2,0,7,0,7,3,2,1,2,0,0,6,4,2,1,0,0,3,4,2,7,7,6,2,3,7,3,7,4,0,2,2,4,3,5,4,5,3,4,2,3,4,4,0,7,7,3,5,2,7,7]#,5,2,7,0,6,2,3,1,6,0]
		solution = solver( len(packet)//4*[0], packet, ignore=8, debug=False, print_error=False, print_result=False)  #ignore preamble
		print("Expected\n          76c872fb00007f00") 
		for x in solution: print("%.2x"%x,end="")
		print()
		packet = [6,1,2,2,2,6,0,2,0,7,4,1,2,2,0,7,0,7,3,2,1,2,0,0,6,4,2,1,0,0,3,4,2,7,7,6,2,3,7,3,7,4,0,2,2,4,3,5,4,5,3,4,2,3,4,4,0,7,7,3,5,2,7,7,1,4,4,3,]#6,0,4,4,]#4,4]
		solution = solver( len(packet)//4*[0], packet, ignore=8, debug=False, print_error=False, print_result=False)  #ignore preamble
		print("Expected\n          76C872FB00007F00")
		for x in solution: print("%.2x"%x,end="")
		print(divider)
		sys.exit()

	#mini tests with sequential rollover values
	if 0:  
		print("Mini tests with sequential rollover values")
		before = [6,5,0,3, 4,4,4,7, 5,0,2,2, 3,1,6,0, 4,6,1,4]# ,3,1,5,7,0,3,6,4,0 7 3 0 4 1 4 4 2 7 4 6 2 0 2 0 7 6 6 1 6 4 1 5 2 3 4 4 7 5 1 1 2 5 5 1 0 4 4 6 5 1 5 6 0 3  146
		after =  [2,3,3,6, 7,7,0,1, 3,2,0,2, 2,2,7,5, 2,6,1,4]  #,3,1,5,7,0,3,6,4,0 7 3 0 4 1 4 4 2 7 4 6 2 0 2 0 7 6 6 1 6 4 1 5 2 3 4 4 7 5 1 1 2 5 5 7 1 4 7 0 4 3 2 0 0 4  152	
		t3=[6,5,0,3,4,0,0,5,0,6,4,2,4,3,6,0,4,6,1,4]#,5,3,1,5,7,0,3,6,4,0,7,3,0,4 1 4 4 2 7 4 6 2 0 2 0 7 6 6 1 6 4 1 5 2 3 4 4 7 5 1 1 2 5 5 5 2 5 2 4 5 6 7 2 4 1  43
		t4=[2,3,3,6,7,3,6,0,7,7,1,4,4,3,6,0,4,6,1,4] #,5,3,1,5,7,0,3,6,4,0,7 3 0 4 1 4 4 2 7 4 6 2 0 2 0 7 6 6 1 6 4 1 5 2 3 4 4 7 5 1 1 2 5 5 1 0 4 4 2 5 1 1 6 0 3  95

		t5=[2, 7, 5, 1, 2, 4, 5, 6, 6, 0, 4, 1, 2, 3, 6, 0]
		t6=[2, 7, 5, 1, 0, 7, 0, 7, 6, 5, 1, 4, 4, 3, 6, 0]

		solution1 = solver([0,0,0], before, debug=False, ignore=8)#, print_error=False, print_result=False)
		print(solution1) #Found: [254, 255, 119]
		solution2 = solver([0,0,0], after, debug=False, ignore=8, print_error=False)#, print_result=False)
		print(solution2)
		if (solution1[0]+256*solution1[1]+256*256*solution1[2] + 2) != solution2[0]+256*solution2[1]+256*256*solution2[2]:
			print("*** fail rollover test 1")
			sys.exit(1)
		#could assert coorect values
		'''
		[254, 255, 223]
		[0, 0, 224]
		[254, 151, 223]
		[0, 152, 223]
		'''
		solution1 = solver([0,0,0], t3, debug=False, ignore=8, print_error=False, print_result=False) 
		print(solution1)
		solution2 = solver([0,0,0], t4, debug=False, ignore=8, print_error=False, print_result=False)
		print(solution2)
		if (solution1[0]+256*solution1[1]+256*256*solution1[2] + 2) != solution2[0]+256*solution2[1]+256*256*solution2[2]:
			print("*** fail rollover test 2")
			sys.exit(1)

		solution5 = solver([0,0,0], t5, debug=False, ignore=8, print_error=False, print_result=False) 
		print(solution5) #[248, 143, 223] odd_100010   : [0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 2, 0]
		solution6 = solver([0,0,0], t6, debug=False, ignore=8, print_error=False, print_result=False) 
		print(solution6) #[248, 16, 255]  odd_100010   : [0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 6]
		#assert solution5 == [248, 143, 223]
		#assert solution6 == [248, 144, 223]  off by 192?
		assert solution5 == [248, 143, 31]
		assert solution6 == [248, 144, 31]
		print(divider)

	#guess at byte 2 zero symbols    find 3240 42 44 46
	if 0:
		print("guess at byte 2 zero symbols    find 3240 42 44 46")
		before = [6,5,0,3, 4,4,4,7, 5,0,2,2, 3,1,6,0, 4,6,1,4]# ,3,1,5,7,0,3,6,4,0 7 3 0 4 1 4 4 2 7 4 6 2 0 2 0 7 6 6 1 6 4 1 5 2 3 4 4 7 5 1 1 2 5 5 1 0 4 4 6 5 1 5 6 0 3  146
		after =  [2,3,3,6, 7,7,0,1, 3,2,0,2, 2,2,7,5, 2,6,1,4]  #,3,1,5,7,0,3,6,4,0 7 3 0 4 1 4 4 2 7 4 6 2 0 2 0 7 6 6 1 6 4 1 5 2 3 4 4 7 5 1 1 2 5 5 7 1 4 7 0 4 3 2 0 0 4  152	
		t3=[6,5,0,3,4,0,0,5,0,6,4,2,4,3,6,0,4,6,1,4]#,5,3,1,5,7,0,3,6,4,0,7,3,0,4 1 4 4 2 7 4 6 2 0 2 0 7 6 6 1 6 4 1 5 2 3 4 4 7 5 1 1 2 5 5 5 2 5 2 4 5 6 7 2 4 1  43
		t4=[2,3,3,6,7,3,6,0,7,7,1,4,4,3,6,0,4,6,1,4] #,5,3,1,5,7,0,3,6,4,0,7 3 0 4 1 4 4 2 7 4 6 2 0 2 0 7 6 6 1 6 4 1 5 2 3 4 4 7 5 1 1 2 5 5 1 0 4 4 2 5 1 1 6 0 3  95

		t5=[2, 7, 5, 1, 2, 4, 5, 6, 6, 0, 4, 1, 2, 3, 6, 0]
		t6=[2, 7, 5, 1, 0, 7, 0, 7, 6, 5, 1, 4, 4, 3, 6, 0]
		for x in range(0,8):
			for y in range(0,8):
				zeros_symbols = [2,3,3,6, 7,7,0,1, 3,2,x,y]# ,2,2,7,5]  #known 0
				delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in zeros_symbols]   # 001 010 101 110 
				delta_2 = [(x*2+3)%8 for x in zeros_symbols]
				delta_6 = [1 + 6 * (x & 1) for x in zeros_symbols]
				solution1 = solver([0,0,0], before, debug=False, ignore=0, print_error=False, print_result=False,default=False,zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)   #startup
				solution2 = solver([0,0,0], after, debug=False, ignore=0, print_error=False, print_result=False,default=False,zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)   #startup
				solution3 = solver([0,0,0], t3, debug=False, ignore=0, print_error=False, print_result=False,default=False,zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6) 	  #startup
				solution4 = solver([0,0,0], t4, debug=False, ignore=0, print_error=False, print_result=False,default=False,zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)   #startup
				if solution1 != "Impossible" and solution2 != "Impossible" and (solution1[2]+1 == solution2[2]):# and (solution3[2]+1 == solution4[2]):  
					print(zeros_symbols)
					print(solution1)
					print(solution2)
					print(solution3)
					print(solution4)
					print()
		sys.exit()
		
	#try to brute force  byte 3 to get length of 8 or byte3=0, guess zero symbols
	#found byte3=0:
	#[2, 3, 3, 6,  7, 7, 0, 1,  3, 2, 4,  6,  2, 2, 7, 5]
	#[2, 3, 3, 6,  7, 7, 0, 1,  3, 2, 4,  2,  2, 2, 7, 5]
	if 0:
		print("Brute force symbol 11..15 of the mask symbols/zero_symbols, with my guess of the length mask and counter mask symbols known from testing")
		print("I now know the correct answer is: 2, 3, 3, 6,  7, 7, 0, 1,  3, 2, 4,*2,  2, 2, 7, 5,* 0, 3, 3, 2.  (did I ever verify the 4th byte really is 0 somehow?)")
		for a in range(0,8):
			print("%d/8..."%a)
			for b in range(0,8):
				for c in range(0,8):
					for d in range(0,8):
						for e in range(0,8):
							zeros_symbols = [2,3,3,6, 7,7,0,1, 3,2,4,a, b,c,d,e, 0,3,3,2]   #2,3,3,6,   7,7,0,1,   3,2,4, 0,  3,2,4,3 ,0,7,3,2,
							delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in zeros_symbols]   # 001 010 101 110 
							delta_2 = [(x*2+3)%8 for x in zeros_symbols]
							delta_6 = [1 + 6 * (x & 1) for x in zeros_symbols]
							solution = solver([0,0,0,0,0], lowest_count_seen_symbols, debug=False, ignore=0, print_error=False, print_result=False,default=False,zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)   #startup
							#print(solution)
							if solution != "Impossible": print(zeros_symbols[11:])
							if solution[4] == 8:
								print(8, zeros_symbols)
							if solution[3] == 0: #I guessed the 4th byte will be 0
								print(0, zeros_symbols)							
		sys.exit()

	#brute forces zero symbols for
	#8 [2, 3, 3, 6, 7, 7, 0, 1, 3, 2, 4, 2, 2, 2, 7, 5, 0, 7, 3, 2] [45, 74, 5, 0, 8]
	#8 [2, 3, 3, 6, 7, 7, 0, 1, 3, 2, 4, 6, 2, 2, 7, 5, 0, 7, 3, 2] [45, 74, 133, 0, 8]
	#but is 3,2,4,6 even possible? yes! so far anyway, need longer counts
	if 0:
		print("brute force test of last counter symbol and of length")
		print("I now know the correct answer for different lengths are:\n0:[2, 3, 3, 6, 7, 7, 0, 1, 3, 2, 4, 2  2, 2, 7, 5, 0, 3, 3, 2]\n8:[2, 3, 3, 6, 7, 7, 0, 1, 3, 2, 4,*2* 2, 2, 7, 5,*0, 7, 3, 2*]\n") 
		for a in range(2,8,4):
			for b in range(0,8):
				for c in range(0,8):
					for d in range(0,8):
						for e in range(0,8):
							zeros_symbols = [2,3,3,6, 7,7,0,1, 3,2,4,a, 2,2,7,5, b,c,d,e]
							delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in zeros_symbols]   # 001 010 101 110 
							delta_2 = [(x*2+3)%8 for x in zeros_symbols]
							delta_6 = [1 + 6 * (x & 1) for x in zeros_symbols]
							solution = solver([0,0,0,0,0], lowest_count_seen_symbols, debug=False, ignore=0, print_error=False, print_result=False,default=False,zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)   #startup
							if solution[4] == 8: #length should be 8
								print(8, zeros_symbols, solution)

		sys.exit()

	#prints transitions that occur in long capture files
	if 0:
		print("Transitions that occur in long capture files, to help me reverse engineer the symbol math")
		for filename in ["test_0s_20_70_147_symbols.txt", "test_0s_100_40_11_symbols_3.txt", "test_0s_50_40_11_symbols_4.txt", "test_0s_50_40_11_symbols_5.txt", 
			"test_0s_50_40_11_symbols_6.txt", "test_0s_50_40_11_symbols_7.txt", "test_0s_50_40_11_symbols_8.txt"]:
			with open("data_captures/"+filename, "r") as infile:	
				print("Using:", filename)
				#print batches at transitions to help figure out math
				#num = 5+256*2
				p = False
				x = -1
				count = 0
				line = infile.readline()
				while line:
					x+=1
					#if line[0:7] == '2 7 5 1':  #[248, *, *] - 6
					#	count = 8
					#	p = True
					if line[0:15] == '2 7 5 1 2 4 3 5': #[248, 255] - [6,0]
					#if line[0:17] == '2 7 5 1 2 4 3 5 5': #[248, 255] - [6,0 4 bit]
						count = 8
						p = True
					#if line[0:7] == '2 3 3 6': count = 1  #[0, *]
					#if line[0:17] == '2 3 3 6 7 7 0 1 3': count = 1  #[0, *]

					#if line[0:31] == '6 1 2 0 5 7 5 6 7 7 1 4 4 3 6 0':
					#	count = 256
					if count:
						symbols = [int(n) for n in line.split(' ')[0:20]]
						solution = solver([0,0,0], symbols, debug=False, ignore=8, print_error=False, print_result=False)
						print
						print("{:6}: {} [{:3}, {:3}, {:3}] [{:08b}, {:08b}, {:08b}]".format(x, symbols[0:20], solution[0], solution[1],solution[2], solution[0], solution[1],solution[2]))
						count -= 1
						if not count and p: print()
					#if (x-64)%(128*256) == 10: print()
					line = infile.readline()
					#if not x % 1000: input("Press any key to continue...")			
		print(divider)

	#guess all in file *without* preamble -- fail!
	if 0:
		print("guess all packet values in file *without* preamble. First digit vascilates by 32 without preamble")
		filename = "temp.txt"
		with open(filename, "r") as infile:	
			print("Using {}".format(filename))	
			line = infile.readline()
			while line:
				symbols =  [int(n) for n in line.split(' ')[0:-2]] #drop the count at end, 
				solution = solver([0]*16, symbols, debug=False, ignore=8, print_error=False, print_result=False)
				print (solution)
				line = infile.readline()
		print(divider)

	#verify vs recorded counts
	if 0:
		print("VSerify vs recorded counts. Check every packet against the next, report dropped packets and impossible values. Very slow.")
		filename = "test_0s_20_70_147_symbols.txt" #227745 total packets 0 impossibles, 4 major errors, 48 skips, 5 doubles  [*, *, 25-31-0]    IMP near 59000??? or maybe upper bytes/CRC is IMP
			#bad filename = "test_0s_20_50_147_symbols.txt" #227698:  10 impossibles, 5 major errors, 12 skips, 41 doubles
		'''
		filename = "test_0s_20_70_147_symbols_2_missing_lots.txt" #3371  0 impossibles, 357 major errors, 696 skips, 0 doubles

			#filename = "test_0s_100_25_11_symbols_3.txt" #27 impossibles, 0 major errors, 3 skips, 44 doubles    imp counts: 51, 40, 38 38 37 37...
			#filename = "test_0s_50_40_11_symbols_3.txt" #1 impossibles, 1 major errors, 221 skips, 6 doubles     impossible had count 51
		filename = "test_0s_100_40_11_symbols_3.txt" # 87157: 1 impossibles, 1 major errors, 229 skips, 6 doubles   more skips?!?!? oh, longer data file   [*,*,12-15]

		filename = "test_0s_50_40_11_symbols_4.txt"  #  154866   5 impossibles, 2 major errors, 255 skips, 17 doubles

		filename = "test_0s_50_40_11_symbols_5.txt" #100658 total packets 4 impossibles, 2 major errors, 236 skips, 35 doubles


		filename = "test_0s_50_40_11_symbols_6.txt" #with 3240 and 3242  19789 total packets 1 impossibles, 1 major errors, 34 skips, 2 doubles
		
		filename = "test_0s_50_40_11_symbols_7.txt" #13607 total packets 2 impossibles, 0 major errors, 29 skips, 9 doubles
		
		#suddenly switched to an odd count!
		filename = "test_0s_50_40_11_symbols_8.txt" #74045 total packets 0 impossibles, 580 major errors, 202 skips, 13 doubles
													#74045 total packets 0 impossibles, 293 major errors, 204 skips, 13 doubles after changing bit 1&5 rule from 6 to 2
													#74045 total packets 0 impossibles, 293 major errors, 204 skips, 13 doubles
													#74045 total packets 0 impossibles, 0 major errors, 209 skips, 13 doubles after changing bit 9 rule from 2 to 6

		'''
		with open("data_captures/"+filename, "r") as infile:	
			print("Using {}".format(filename))

			#print batches at transitions to help figure out math
			if 0:		
				print("print batches at transitions to help figure out math")
				#num = 5+256*2
				p = False
				x = -1
				count = 0
				line = infile.readline()
				while line:
					x+=1

					if line[0:7] == '2 3 3 6' or line[0:7] == '4 2 1 0': count = 1  #[0, *]
					'''
					if line[0:7] == '2 7 5 1':  #[248, *, *] - 6
						count = 8
						p = True
					'''
					'''
					if line[0:15] == '2 7 5 1 2 4 3 5': #[248, 255] - [6,0]
						count = 8
						p = True
					'''
					#count = 1


					#if line[0:31] == '6 1 2 0 5 7 5 6 7 7 1 4 4 3 6 0':
					#	count = 256
					if count:
						symbols = [int(n) for n in line.split(' ')[0:20]]
						solution = solver([0,0,0], symbols, debug=False, ignore=8, print_error=False, print_result=False)
						print
						print("{:6}: {} [{:3}, {:3}, {:3}] [{:08b}, {:08b}, {:08b}]".format(x, symbols[0:16], solution[0], solution[1],solution[2], solution[0], solution[1],solution[2]))
						count -= 1
						if not count and p: print()
					#if (x-64)%(128*256) == 10: print()
					line = infile.readline()
					if not x % 1000 and x: input("Press Enter to continue...")			

			#check every packet in the file
			if 0:
				print("\nCheck every packet, verify they are in sequential order to verify my math is right.")
				solution = [116,  78, 233]
				last_solution = [116,  78, 233]
				last_sol = solution[0] + 256*solution[1] + 256*256*solution[2] -2
				line = infile.readline()
				x = -1
				minors = 0
				majors = 0
				skips = 0
				dbls = 0
				imps = 0
				while line:
					x += 1
					#if x < 227510:  #skip some entries if need be
					#	line = infile.readline()
					#	continue
					symbols = [int(n) for n in line.split(' ')[0:20]]
					solution = solver([0,0,0], symbols, debug=False, ignore=8, print_error=False, print_result=False)
					sol = solution[0] + 256*solution[1] + 256*256*solution[2]
					#try:
					if solution == "Impossible" :
						print(x, symbols, "solution =", solution)
						#solver([0,0,0], symbols, debug=False, ignore=0, print_error=True, print_result=False)
						#if len(line) >= 154-2
						print("Last value, maybe count:", line.split(' ')[-1], end="")
						imps += 1
					else:
						if sol-2 != last_sol:
							if sol-4 == last_sol:
								print("{}: missing packet".format(x))
								skips += 1
							elif sol == last_sol:
								print("{}: doubled packet".format(x))
								dbls += 1
							elif x: #skip x=0
								print("{}: mismatch of {}   {} {} {} {}".format(x, sol-last_sol-2,last_solution, solution,last_sol, sol))
								print("{}: {} [{:3}, {:3}, {:3}] [{:08b}, {:08b}, {:08b}]".format(x, symbols[0:16], solution[0], solution[1],solution[2], solution[0], solution[1],solution[2]))
								majors += 1
						last_sol = sol
						last_solution = solution
					line = infile.readline()
				print("\n#{} total packets {} impossibles, {} major errors, {} skips, {} doubles".format(x+1, imps, majors, skips, dbls))


			#check every packet in the file plus preamble
			if 1:
				print("\nCheck every packet, verify they are in sequential order to verify my math is right.")
				solution = [116,  78, 233]
				last_solution = [116,  78, 233]
				last_sol = solution[0] + 256*solution[1] + 256*256*solution[2] -2
				line = infile.readline()
				x = -1
				minors = 0
				majors = 0
				skips = 0
				dbls = 0
				imps = 0
				while line:
					x += 1
					#if x < 227510:  #skip some entries if need be
					#	line = infile.readline()
					#	continue
					symbols = [int(n) for n in line.split(' ')[0:20]]
					solution = solver([0,0,0,0,0,0],[0,0,4,4,2,7,7,4,6,7,5,6,]+symbols, debug=False, ignore=8-3, print_error=False, print_result=False)
					sol = solution[3] + 256*solution[4] + 256*256*solution[5]
					#try:
					if solution == "Impossible" :
						print(x, symbols, "solution =", solution)
						#solver([0,0,0], symbols, debug=False, ignore=0, print_error=True, print_result=False)
						#if len(line) >= 154-2
						print("Last value, maybe count:", line.split(' ')[-1], end="")
						imps += 1
					else:
						if sol-2 != last_sol:
							if sol-4 == last_sol:
								print("{}: missing packet".format(x))
								skips += 1
							elif sol == last_sol:
								print("{}: doubled packet".format(x))
								dbls += 1
							elif x: #skip x=0
								print("{}: mismatch of {}   {} {} {} {}".format(x, sol-last_sol-2,last_solution, solution,last_sol, sol))
								print("{}: {} [{:3}, {:3}, {:3}] [{:08b}, {:08b}, {:08b}]".format(x, symbols[0:16], solution[0], solution[1],solution[2], solution[0], solution[1],solution[2]))
								majors += 1
						last_sol = sol
						last_solution = solution
					line = infile.readline()
				print("\n#{} total packets {} impossibles, {} major errors, {} skips, {} doubles".format(x+1, imps, majors, skips, dbls))




		solution = solver([0,0,0,0], [6,1,2,2, 4,7,4,7, 3,4,4,2, 3,4,0,7, 0,7,3,2], debug=False, ignore=8)#, print_error=False)  #startup
		print(solution)
		solution = solver([0,0,0,0,0], [6,1,2,2, 4,7,4,7, 3,4,4,2, 3,4,0,7, 0,7,3,2], debug=False, ignore=8)#, print_error=False)  #startup
		print(solution)
		solution = solver([0,0,0,0,0], [2,3,3,6, 7,7,2,6, 2,7,4,3, 3,3,5,5, 2,6,1,4], debug=False, ignore=8, print_error=False)		
		print(solution)

		print(divider)
		sys.exit()	
			
	#try to find the mask value of the zero symbols
	if 0:
		print("Compute the value of zeroes mask, try to find a pattern:")
		symbols = compute_experimental.dzeros_symbols

		zeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,0,0,0,0,0,0,0,0,0,0,] + [0]*(len(symbols)-32)
		solution = solver([0]*(len(symbols)//4), symbols, debug=False, ignore=0, print_error=False, print_result=True, default=False, zeros_symbols=zeros_symbols)#, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)#, print_error=False)
		if solution == "Impossible": 
			print(solution)
		else:
			print("Values:  ", end=" ")
			for x in solution: print("{:02x}".format(x), end=" ")
			print("\nInverted:", end=" ")
			for x in solution: print("{:02x}".format(x^255), end=" ")
			print("\n")

		print("-"*20)
		print("Value of zeroes mask:")
		zeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0, 4,0,0,0,0,0,0,0,0,0,] + [0]*(len(symbols)-32)
		solution = solver([0]*(len(symbols)//4), symbols, debug=False, ignore=0, print_error=False, print_result=True, default=False, zeros_symbols=zeros_symbols)#, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)#, print_error=False)
		if solution == "Impossible": 
			print(solution)
		else:
			print("Values:  ", end=" ")
			for x in solution: print("{:02x}".format(x), end=" ")
			print("\nInverted:", end=" ")
			for x in solution: print("{:02x}".format(x^255), end=" ")
			print("\n")
		'''
		print("\n\nValue of DIFFED zeroes mask:")
		symbols =       [4,0,0,4,4,4,4,4,2,2,2,2,0,0,0,0,6,6,6,6,0,0,4,4,0,0,0,0,0,0,0,0,2,1,0,3,1,0,1,1,2,7,2,6,0,0,5,6,3,3,0,7,3,7,7,2,2,1,3,3,6,4,7,4,5,4,5,3,0,6,5,5,2,4,6,2,6,7,7,0,3,5,6,5,4,5,1,1,0,3,6,4,0,1,3,0,  2,6,1,4, 0,4,1,6, 1,2,0,0,]# 0,0,0,0]
		zeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,0,0,0,0,0,0,0,0,0,0,] + [0]*(len(symbols)-32)
		solution = solver([0]*(len(symbols)//4), symbols, debug=False, ignore=0, print_error=False, print_result=True, default=False, zeros_symbols=zeros_symbols)#, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)#, print_error=False)
		if solution == "Impossible": 
			print(solution)
		else:
			print("Values:")
			for x in solution: print("{:02x}".format(x), end=" ")
			print("\nInverted:")
			for x in solution: print("{:02x}".format(x^255), end=" ")
			print("\n")
		'''

		print("-"*20)
		print("Value of (double) DIFFED zeroes mask:")
		#symbols =  [2,1,0,3,1,0,1,1,2,7,2,6,0,0,5,6,3,3,0,7,3,7,7,2,2,1,3,3,6,4,7,4,5,4,5,3,0,6,5,5,2,4,6,2,6,7,7,0,3,5,6,5,4,5,1,1,0,3,6,4,0,1,3,0,2,6,1,4,0,4,1,6,1,2,0,0,]#0,0,0,0]
		#print(symbols)
		symbols = ([(compute_experimental.dzeros_symbols[x]-compute_experimental.dzeros_symbols[x-1])%8 for x in range(0,len(compute_experimental.dzeros_symbols))])
		#print(symbols)
		symbols = symbols[32:]
		print(symbols)

		zeros_symbols = [0]*(len(symbols))
		solution = solver([0]*(len(symbols)//4), symbols, debug=False, ignore=0, print_error=False, print_result=True, default=False, zeros_symbols=zeros_symbols)#, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)#, print_error=False)
		if solution == "Impossible": 
			print(solution)
		else:
			print("Values:  ", end=" ")
			for x in solution: print("{:02x}".format(x), end=" ")
			print("\nInverted:", end=" ")
			for x in solution: print("{:02x}".format(x^255), end=" ")
			print("\n")


		print("-"*20)
		print("Value of UNDIFFED zeroes mask:")
		#symbols =  [2,1,0,3,1,0,1,1,2,7,2,6,0,0,5,6,3,3,0,7,3,7,7,2,2,1,3,3,6,4,7,4,5,4,5,3,0,6,5,5,2,4,6,2,6,7,7,0,3,5,6,5,4,5,1,1,0,3,6,4,0,1,3,0,2,6,1,4,0,4,1,6,1,2,0,0,]#0,0,0,0]
		#print(symbols)
		symbols = ([(compute_experimental.dzeros_symbols[x]+compute_experimental.dzeros_symbols[x-1])%8 for x in range(0,len(compute_experimental.dzeros_symbols))])
		#print(symbols)
		symbols = symbols[32:]
		print(symbols)

		zeros_symbols = [0]*(len(symbols))
		solution = solver([0]*(len(symbols)//4), symbols, debug=False, ignore=0, print_error=False, print_result=True, default=False, zeros_symbols=zeros_symbols)#, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)#, print_error=False)
		if solution == "Impossible": 
			print(solution)
		else:
			print("Values:  ", end=" ")
			for x in solution: print("{:02x}".format(x), end=" ")
			print("\nInverted:", end=" ")
			for x in solution: print("{:02x}".format(x^255), end=" ")
			print("\n")

		print("-"*20)
		#zeroes 4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,0,0,0,0,0,0,0,0,0, 2,3,3,6,7,7,0,1,3,2,4,2,2,2,7,5,0,3,3,2, 5,4,3,5,7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,5,2,3,4,4,7,5,1,1,2,5,5,7,5,6,2,2,6,7,5,6,0,0,0,0,0,0,0
		print("Value of DIFFED zeroes mask:")
		symbols =  [6,5,4,7, 5,4,5,5] #Impossible at symbol 4      					   #source???
		symbols = [6,7,0,5, 7,0,7,7] #Impossible at symbol 2							#source?

		# opposite 2, 3, 3, 6,  7, 7, 0, 1,  3, 2, 4, 2,  2, 2, 7, 5,  0, 3, 3, 2, 
		symbols = [6,5,5,2] #8- Impossible at symbol 2									
		symbols = [6,7,7,2, 3,3,4,5] #+4							
		symbols = [2,5,0,6, 5,4,4,5] #undiff  IMP at 3				
		symbols = [2,5,6,1, 5,6,7,1] #undiff  IMP at 3				
		zeros_symbols = [0]*(len(symbols))
		solution = solver([0]*(len(symbols)//4), symbols, debug=False, ignore=0, print_error=False, print_result=True, default=False, zeros_symbols=zeros_symbols)#, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)#, print_error=False)
		if solution == "Impossible": 
			print(solution)
		else:
			print("Values:")
			for x in solution: print("{:02x}".format(x), end=" ")
			print("\nInverted:")
			for x in solution: print("{:02x}".format(x^255), end=" ")
			print("\n")
		print(divider)

	#I think this found 4096 possible CRC mask/zero values
	if 0:
		#First try all 1-byte zero states, then 2 bytes, etc.
		#actuals = [[1,2,3,0], [7,1,2,5], [5,2,7,4], [1,6,1,1], [3,7,7,7], [3,1,0,4], [7,7,5,2], [5,0,2,6], [7,7,7,7], [1,0,6,6]]
		actuals = [[7,1,2,5,  2,7,2,4  ]]#,0,0,0,0]]
		goal = len(actuals)

		total_good = 0
		for a in range(1,8,2):
			for b in range(0,8):
				for c in range(0,8):
					for d in range(0,8):
						for e in range(0,8):
							for f in range(0,8):
								for g in range(0,8):
									Z = [a, b, c, d, e, f, g,0]
									#	print(Z)
									zeros_symbols = Z.copy()
									delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in Z]   # 001 010 101 110 
									delta_2 = [(x*2+3)%8 for x in Z]
									delta_6 = [1 + 6 * (x & 1) for x in Z]

									score = 0
									for actual in actuals:
										#solver(in_data_orig, expected_orig, debug=False, ignore=0, print_error=True, print_result=True):
										#solution = solver([0,0], actual, ignore=0)#, debug=True)#, print_error=False)#, print_result=False)
										solution = solver([0,0], actual, ignore=0, print_error=False, print_result=False)
										if solution != "Impossible": 
											score += 1
									if score == goal:
										total_good += 1
										print (Z, solution)
								
		print("Total solutions found:", total_good)
		print(divider)

	#more CRC stuff, code won't work without ignore changed
	if 0:
		actuals = [[7,7,7,7,  0,7,5,6  ]]#,0,0,0,0]]
		goal = len(actuals)
		total_good = 0

		with open("guessed_7125_2724") as f:			#get previous;y found zero candidates
			lines = f.read().splitlines()
			for i in range(0,len(lines)-1):
				line = lines[i].split(']')[0].strip('[')
				Z = [int(x) for x in line.split(',')]
				
				zeros_symbols = Z.copy()
				delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in Z]   # 001 010 101 110 
				delta_2 = [(x*2+3)%8 for x in Z]
				delta_6 = [1 + 6 * (x & 1) for x in Z]

				score = 0
				for actual in actuals:
					#solver(in_data_orig, expected_orig, debug=False, ignore=0, print_error=True, print_result=True):
					#solution = solver([0,0], actual, ignore=0)#, debug=True)#, print_error=False)#, print_result=False)
					solution = solver([0,0], actual, ignore=0, print_error=False, print_result=False)
					if solution != "Impossible": 
						score += 1
				if score == goal:
					total_good += 1
					print (Z, solution)
									
			print("Total solutions found:", total_good)	
			
	#solve for values of last 9 symbils of of preamble... why 9? Because they aren't in section 3. Get a bunch of solutions but none look any better
	if 0:
		print("solve for 2 mystery byte values after the 6 confirmed header/preamble bytes using masks of 0, 0, 4, 0,  0, 0, 0, 0,  0, 0, 0, 0 and 0,0,4,2, 3,1,3,3, 4,2,2,4 ")
		print("should double check delta math")

		print("\n test 1")
		#Found: [0, 0, 0, 0, 0, 128, 135, 0]
		#0x0 0x0 0x0 0x0 0x0 0x80 0x87 0x0       1000 0000  1000 0111
		Z 	   =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0,  0, 0, 4, 0,  0, 0, 0, 0,  0, 0, 0, 0]
		print("Z last 8:", Z[6*4:])
		zeros_symbols = Z.copy()
		actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0,  0, 0, 4, 4,  2, 7, 7, 4,  6, 7, 5, 6]
		delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in Z]  +[0]  # 001 010 101 110 
		delta_2 = [(x*2+3)%8 for x in Z]
		delta_6 = [1 + 6 * (x & 1) for x in Z]
		solution = solver([0,0,0,0,0,0,0,0], actual, debug=False, ignore=0, print_result=True, default=False, zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)#, print_error=False)
		if solution == "Impossible": print(solution)
		#Found:        [0, 0, 0, 0, 0, 128, 135, 0]
		#Hex:          0x0 0x0 0x0 0x0 0x0 0x80 0x87 0x0 


		print("\n test 2")
		Z 	   =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		zeros_symbols = Z.copy()
		actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6]
		delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in Z]  +[0]  # 001 010 101 110 
		delta_2 = [(x*2+3)%8 for x in Z]
		delta_6 = [1 + 6 * (x & 1) for x in Z]
		solution = solver([0,0,0,0,0,0,0,0], actual, debug=False, ignore=0, print_result=True, default=False, zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)#, print_error=False)
		if solution == "Impossible": print(solution)
		#Found:        [0, 0, 0, 0, 0, 160, 135, 0]
		#Hex:          0x0 0x0 0x0 0x0 0x0 0xa0 0x87 0x0 



		print("\n test 3")
		#new preamble sec2	
		Z 	   =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0,  0,0,0,0,  0, 0, 0, 0,  0, 0, 0, 0]
		zeros_symbols = Z.copy()
		actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0,  0,0,4,2, 3,1,3,3, 4,2,2,4 ]
		delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in Z]  +[0]  # 001 010 101 110 
		delta_2 = [(x*2+3)%8 for x in Z]
		delta_6 = [1 + 6 * (x & 1) for x in Z]
		solution = solver([0,0,0,0,0,0,0,0], actual, debug=False, ignore=0, print_result=True, default=False, zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)#, print_error=False)
		if solution == "Impossible": print(solution)
		#Hex:          0x0 0x0 0x0 0x0 0x0 0xe0 0xff 0x55


		print("\n test 4")
		Z 	   =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0,  0,0,4,0,  0, 0, 0, 0,  0, 0, 0, 0]
		zeros_symbols = Z.copy()
		actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0,  0,0,4,2, 3,1,3,3, 4,2,2,4 ]
		delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in Z]  +[0]  # 001 010 101 110 
		delta_2 = [(x*2+3)%8 for x in Z]
		delta_6 = [1 + 6 * (x & 1) for x in Z]
		solution = solver([0,0,0,0,0,0,0,0], actual, debug=False, ignore=0, print_result=True, default=False, zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)#, print_error=False)
		#Hex:          0x0 0x0 0x0 0x0 0x0 0xc0 0xff 0x55
		if solution == "Impossible": print(solution)

		print("\n test 5")
		#Z 	   =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0,0,0,2, 0,0,0,0, 0,0,0,0, 2,3,3,6]
		#Z 	   =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0,0,0,2, 0,0,0,0, 0,0,0,0, 0,0,0,0,]
		#Z      =        [0,0,0,0]*9
		#Z 	   =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0,  6,4,2,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0,]  #xe0 xff x15 solving for 8 but data 9 long and actual 8 or 9
		#Z 	   =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0,  6,4,2,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]  #xe0 xff x55          yeah this must be some error or bug right?
		Z 	   =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0,  6,4,2,0, 0,0,4,0, 0,0,0,0, 0,0,0,0] #xc0 xff x55 
		zeros_symbols = Z.copy()
		#actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0,  0,0,4,2, 3,1,3,3, 4,2,2,4, 2,3,3,6]  #
		actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0,  0,0,4,2, 3,1,3,3, 4,2,2,4]  #
		delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in Z]  +[0]  # 001 010 101 110 
		delta_2 = [(x*2+3)%8 for x in Z]
		delta_6 = [1 + 6 * (x & 1) for x in Z]
		solution = solver([0]*8, actual, debug=False, ignore=0, print_result=True, default=False, zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6, print_error=False)
		if solution == "Impossible": print(solution)
		#impossible

		#sys.exit()

		print("\n test 6")
		Z 	   =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0,  0,0,4,2, 3,1,3,3, 4,2,2,4 ]
		print("Z last 8:", Z[6*4:])
		zeros_symbols = Z.copy()
		actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in Z]  +[0]  # 001 010 101 110 
		delta_2 = [(x*2+3)%8 for x in Z]
		delta_6 = [1 + 6 * (x & 1) for x in Z]
		solution = solver([0,0,0,0,0,0,0,0], actual, debug=False, ignore=0, print_result=True, default=False, zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)#, print_error=False)
		#Hex:          0x0 0x0 0x0 0x0 0x0 0xe0 0xff 0x5f 

		print("\n test 7")
		Z 	   =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0,  0,0,4,2, 3,1,3,3, 4,2,2,4 ]
		zeros_symbols = Z.copy()
		actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6]
		delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in Z]  +[0]  # 001 010 101 110 
		delta_2 = [(x*2+3)%8 for x in Z]
		delta_6 = [1 + 6 * (x & 1) for x in Z]
		solution = solver([0,0,0,0,0,0,0,0], actual, debug=False, ignore=0, print_result=True, default=False, zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)#, print_error=False)
		#Hex:          0x0 0x0 0x0 0x0 0x0 0x40 0x78 0xff 

		print("\n test 8")
		Z 	   =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6]
		print("Z last 8:", Z[6*4:])
		zeros_symbols = Z.copy()
		actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0,  0,0,4,2, 3,1,3,3, 4,2,2,4 ]
		delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in Z]  +[0]  # 001 010 101 110 
		delta_2 = [(x*2+3)%8 for x in Z]
		delta_6 = [1 + 6 * (x & 1) for x in Z]
		solution = solver([0,0,0,0,0,0,0,0], actual, debug=False, ignore=0, print_result=True, default=False, zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)#, print_error=False)
		#Hex:          0x0 0x0 0x0 0x0 0x0 0x40 0x78 0x7d 

		print("\n test 9")
		Z 	   =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6 ,0,0,0,0]
		print("Z last 8:", Z[6*4:])
		zeros_symbols = Z.copy()
		actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0,  0,0,4,2, 3,1,3,3, 4,2,2,4 , 2, 3, 3, 6,]
		delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in Z]  +[0]  # 001 010 101 110 
		delta_2 = [(x*2+3)%8 for x in Z]
		delta_6 = [1 + 6 * (x & 1) for x in Z]
		solution = solver([0]*9, actual, debug=False, ignore=0, print_result=True, default=False, zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)#, print_error=False)
		print(solution)
		#impossible

		print("\n test 10")
		Z 	   =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6 ,2,3,3,6]
		print("Z last 8:", Z[6*4:])
		zeros_symbols = Z.copy()
		actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0,  0,0,4,2, 3,1,3,3, 4,2,2,4 , 2, 3, 3, 6,]
		delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in Z]  +[0]  # 001 010 101 110 
		delta_2 = [(x*2+3)%8 for x in Z]
		delta_6 = [1 + 6 * (x & 1) for x in Z]
		solution = solver([0]*9, actual, debug=False, ignore=0, print_result=True, default=False, zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6, print_error=False)
		print(solution)
		#impossible
		print(divider)

	#solve for last 9 symbols of preamble... why 9? Because they aren't in section 2. get: [0, 0, 0, 0, 0, 64, 120, 191] 
	if 0:
		print("solve for 2 mystery bytes after the confirmed header 6 bytes using section 2 preamble  0,0,4,2, 3,1,3,3, 4,2,2,4")
		#Found: [0, 0, 0, 0, 0, 128, 135, 0]
		#0x0 0x0 0x0 0x0 0x0 0x80 0x87 0x0       1000 0000  1000 0111
		Z 	   =        [4, 4, 4, 0,  4, 0, 4, 0,  2, 4, 6, 0,  0, 0, 0, 0,  6, 4, 2, 0,  0,0,4,2, 3,1,3,3, 4,2,2,4           ]
		zeros_symbols = Z.copy()
		actual        = [4, 4, 4, 0,  4, 0, 4, 0,  2, 4, 6, 0,  0, 0, 0, 0,  6, 4, 2, 0,  0, 0, 4, 4,  2, 7, 7, 4,  6, 7, 5, 6]
		delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in Z]  +[0]  # 001 010 101 110 
		delta_2 = [(x*2+3)%8 for x in Z]
		delta_6 = [1 + 6 * (x & 1) for x in Z]
		solution = solver([0,0,0,0,0,0,0,0], actual, debug=False, ignore=0, print_result=True, default=False, zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)#, print_error=False)
		print(solution,"\n\n\n")
		#Hex:          0x0 0x0 0x0 0x0 0x0 0x40 0x78 0xff
		sys.exit()	

	#solve for all after the confirmed header bytes. Obsolete. Better code above
	if 0:
		print("solve for all after the confirmed header bytes")
		#Found: [0, 0, 0, 0, 0, 128, 135, 0]
		#0x0 0x0 0x0 0x0 0x0 0x80 0x87 0x0       1000 0000  1000 0111
		Z 	   =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, ]+4*11*[0]
		zeros_symbols = Z.copy()
		#actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6,  2, 3, 3, 6, 7,7,0,1, 3,2,4,2, 2,2,7,5, 0,3,3,2,  5,4,3,5, 7,0,3,6, 0,0,7,3, 0,4,1,0, 4,2,7,4, 6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7, 5,4,4,3,]
		#those had errors
		actual = compute_experimental.dzeros_symbols
		delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in Z]  +[0]  # 001 010 101 110 
		delta_2 = [(x*2+3)%8 for x in Z]
		delta_6 = [1 + 6 * (x & 1) for x in Z]
		solution = solver([0]*24, actual, debug=False, ignore=0, print_result=True, default=False, zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)#, print_error=False)
		print(solution,"\n\n\n")
		#Found:        [0, 0, 0, 0, 0, 128, 135, 0]
		#Hex:          0x0 0x0 0x0 0x0 0x0  0x80 0x87 0x0 
		#              0x0 0x0 0x0 0x0 0x0 0xa0 0x87 0x0  0x6f 0xb4 0x1e 0xa 0xed 0x31 0xb5 0x89 0x25 0x8b 0x81 0x40 0xb2 0x3b 0xc4 0x18 
		sys.exit()	


	#solve for last 9 symbols of preamble... why 9? Because they aren't in section 3. FAIL  copied from above?
	if 0:
		print("solve for all after the confirmed header bytes using sec2 preamble")
		#Found: [0, 0, 0, 0, 0, 128, 135, 0]
		#0x0 0x0 0x0 0x0 0x0 0x80 0x87 0x0       1000 0000  1000 0111
		Z 	   =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0,  0,0,4,2, 3,1,3,3, 4,2,2,4         , 0, 0, 0, 0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, ]+4*11*[0]
		zeros_symbols = Z.copy()
		actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6, 2, 3, 3, 6, 7,7,0,1, 3,2,4,2, 2,2,7,5, 0,3,3,2,  5,4,3,5, 7,0,3,6, 0,0,7,3, 0,4,1,0, 4,2,7,4, 6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7, 5,4,4,3,]
		actual = compute_experimental.dzeros_symbols

		delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in Z]  +[0]  # 001 010 101 110 
		delta_2 = [(x*2+3)%8 for x in Z]
		delta_6 = [1 + 6 * (x & 1) for x in Z]
		solution = solver([0]*24, actual, debug=False, ignore=0, print_result=True, default=False, zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6, print_error=True)
		print(solution,"\n\n\n")
		#impossible
		sys.exit()	


	#try to solve for preamble, fail
	if 0:
		Z =        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		#Z =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		zeros_symbols = Z.copy()


		#solve for 2 mystery bytes after the confirmed header 6 bytes
		#nibbles      : [a,    2,    2,    2,    f,   impossible starting at 4,6
		#even_bits    : [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

		actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6]
		delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in Z]  + [0] # 001 010 101 110 
		delta_2 = [(x*2+3)%8 for x in Z]
		delta_6 = [1 + 6 * (x & 1) for x in Z]

		#Z =        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]   #lets try building normal deltas then sending Z of 0s... nope exact same answer
		#zeros_symbols = Z.copy()
		solution = solver([0,0,0,0,0,0,0,0], actual, debug=True, ignore=0, print_result=True, print_error=True, default=False, zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)
		print(solution,"\n\n\n")
		sys.exit()	


	if 0:  #needs to be updated for solver to actually use these zero values... obsolete copies of above code??

		print("solve for 2 mystery bytes + 1 after the confirmed header 6 bytes")
		print("zeros_symbols:", zeros_symbols)
		Z 	   =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ] #I think?
		zeros_symbols = Z.copy() + [4, 2, 1, 0, 7, 0, 6, 1, 3, 2] #must add at least 7 for a byte  		works
		zeros_symbols = Z.copy() + [4, 2, 1, 0, 7, 0, 6, 1, 3, 2, 0,2] #must add at least 7 for a byte  		works
		#zeros_symbols = Z.copy() + 10*[0]  #must add at least 7 for a byte  			works
		#zeros_symbols = Z.copy() + [0, 0, 0, 0, 7, 0, 6, 1, 3, 2] #must add at least 7 for a byte
		#zeros_symbols = Z.copy() + [4, 2, 1, 0, 0, 0, 0, 0, 3, 2] #must add at least 7 for a byte    impossible
		#zeros_symbols = Z.copy() + [0, 0, 0, 0, 7, 0, 6, 1, 3, 2] #must add at least 7 for a byte    impossible

		print("zeros_symbols:", zeros_symbols)
		actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6]+[0,6,7,3] #old zero byte1 Found: [0, 0, 0, 0, 0, 128, 135, 0, 250]
		actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6]+[4,2,1,0] #new zero byte1 Found: [0, 0, 0, 0, 0, 128, 135, 0, 110]
		actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6]+[4,2,1,0, 7,0,6,1] #new zero byte1 Found: [0, 0, 0, 0, 0, 128, 135, 0, 110, 180]

		startup4 =      [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6] + [6, 1, 2, 2, 4, 7, 4, 7, 3, 4, 4, 2, 3, 4, 0, 7, 0, 7, 3, 2]
		actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6]+ [6, 1, 2, 2, 4, 7, 4, 7,]           #Found: [0, 0, 0, 0, 0, 128, 135, 0, 169, 114]
		actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6]+ [6, 1, 2, 2, 4, 7, 4, 7, 3, 4, 4, 2]#Found: [0, 0, 0, 0, 0, 128, 135, 0, 199, 198, 6]

		delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in zeros_symbols]   # 001 010 101 110 
		delta_2 = [(x*2+3)%8 for x in zeros_symbols]
		delta_6 = [1 + 6 * (x & 1) for x in zeros_symbols]


		print("lengths are:", len(zeros_symbols),len(actual),len([0,0,0,0,0,0,0,0]+[0]+[0]+[0])*4)



		solution = solver([0,0,0,0,0,0,0,0]+[0]+[0]+[0], actual, debug=False, ignore=0)#, print_error=False)






		'''
		startup4 =      [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6,   6, 1, 2, 2, 4, 7, 4, 7, 3, 4, 4, 2, 3, 4, 0, 7, 0, 7, 3, 2]
		zeros_data_5  = [4, 2, 1, 0, 7, 0, 6, 1, 3, 2, 1, 4, 3, 3, 6, 7, 0, 7, 3, 2]
		#                                              ?  ?  ?  ?  ?  ?
		zeros_symbols = Z + zeros_data_5
		#print(len(zeros_symbols))
		actual=startup4
		delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in zeros_symbols]   # 001 010 101 110 
		delta_2 = [(x*2+3)%8 for x in zeros_symbols]
		delta_6 = [1 + 6 * (x & 1) for x in zeros_symbols]
		solution = solver([0,0,0,0,0,0,0,0]+[0,0,0,0,0], startup4, debug=False, ignore=0)#, print_error=False)
		print(solution)
		'''


		'''
		#Code to try all 6 byte combos. takes a while.
		startup4 =      [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6] + [6, 1, 2, 2, 4, 7, 4, 7, 3, 4, 4, 2, 3, 4, 0, 7, 0, 7, 3, 2]
		zeros_data_5  = [4, 2, 1, 0, 7, 0, 6, 1, 3, 2, 1, 4, 4, 2, 0, 7, 0, 7, 3, 2]
		#                                              ?  ?  ?  ?  ?  ?                   not sure about these 6 bytes
		print("[")							
		for a in range(0,8):
			for b in range(0,8):
				for c in range(0,8):
					for d in range(0,8):
						for e in range(0,8):
							for f in range(0,8):
								#print("Testing",a,b,c,d,e,f,end="... ")
								zeros_data_5  = [4, 2, 1, 0, 7, 0, 6, 1, 3, 2, a, b, c, d, e, f, 0, 7, 3, 2]

								zeros_symbols = Z + zeros_data_5
								#print(len(zeros_symbols))
								actual=startup4
								delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in zeros_symbols]   # 001 010 101 110 
								delta_2 = [(x*2+3)%8 for x in zeros_symbols]
								delta_6 = [1 + 6 * (x & 1) for x in zeros_symbols]
								solution = solver([0,0,0,0,0,0,0,0]+[0,0,0,0,0], startup4, debug=False, ignore=0, print_error=False, print_result=False)
								if solution != "Impossible": 
									#print("Tested",a,b,c,d,e,f)
									#print("solved")
									#sys.exit(0)
									print([a,b,c,d,e,f],",")
		print("]")
		'''

		'''
		#this found nothing new.
		startup4 =      [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6] + [2, 7, 3, 4, 2, 7, 3, 5, 3, 4, 4, 2, 3, 4, 0, 7, 0, 7, 3, 2]
		with open("byte34_solutions.txt", 'r') as f:
			sols = ast.literal_eval(f.read()) 
		for sol in sols:
			zeros_data_5  = [4, 2, 1, 0, 7, 0, 6, 1, 3, 2] + sol + [0, 7, 3, 2]
			zeros_symbols = Z + zeros_data_5
			#print(len(zeros_symbols))
			actual=startup4
			delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in zeros_symbols]   # 001 010 101 110 
			delta_2 = [(x*2+3)%8 for x in zeros_symbols]
			delta_6 = [1 + 6 * (x & 1) for x in zeros_symbols]
			solution = solver([0,0,0,0,0,0,0,0]+[0,0,0,0,0], startup4, debug=False, ignore=0, print_error=False, print_result=False)
			if solution == "Impossible": 
				print("Tested",sol)
				print("eliminated")			
		'''		
				
		#this also found nothing new.		
		startup4 =      [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6] + [6,5, 6, 0, 1, 3, 7, 1, 4, 3, 1, 2, 3, 3, 6, 7, 0, 3, 3, 2]
		with open("old_parse/byte34_solutions.txt", 'r') as f:
			sols = ast.literal_eval(f.read()) 
		for sol in sols:
			zeros_data_5  = [4, 2, 1, 0, 7, 0, 6, 1, 3, 2] + sol + [0, 7, 3, 2]
			zeros_symbols = Z + zeros_data_5
			#print(len(zeros_symbols))
			actual=startup4
			delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in zeros_symbols]   # 001 010 101 110 
			delta_2 = [(x*2+3)%8 for x in zeros_symbols]
			delta_6 = [1 + 6 * (x & 1) for x in zeros_symbols]
			solution = solver([0,0,0,0,0,0,0,0]+[0,0,0,0,0], startup4, debug=False, ignore=0, print_error=False, print_result=False)
			'''
			if solution != "Impossible": 
				print("Tested",sol)
				print("solved")	
			'''	
			if solution == "Impossible": 
				print("Tested",sol)
				print("eliminated")			
				