###########################################################################################
#This program guesses data bits to match a known/given zero-state and an known output value


import sys, ast

#this version allows expected, print_error
def compute(in_data_orig, expected, debug=False, ignore=0, print_error=True):
	in_data = in_data_orig.copy() # prevent modification of data
	start = 0
	length = len(in_data)*4
	in_data += [0,0]
	nibbles = [x>>(4*i)&0xf for x in in_data for i in range(0, 2)]
	#if debug: print("nibbles:      ", nibbles)
	nips = [x>>(2*i)&0x3 for x in nibbles for i in range(0, 2)]
	#if debug: print("nips:         ", nips,"\n")
	
	odd_bits = [x&1 for x in nips]
	#if debug: print("odd_bits:     ", odd_bits)
	even_bits = [(x&2)>>1 for x in nips]
	#if debug: print("even_bits:    ", even_bits)
	
	#print("odd_bits:     ", odd_bits)
	#odd_merge = [0,0,0,0]+ [ 4* ((x%8==4)|(x%8==2)) & even_bits[x-3] & even_bits[x+1] for x in range(4,length-2)] + [0,0]
	#odd_merge = [0,0,0,0,0,0]+ [ 4* (x%4 > 0) * odd_bits[x-5] * odd_bits[x-1] for x in range(6,length)]			#added this to compensate for byte 0,1 == 4,4. Might actually need to be 3-4 consecutive 4s
	#odd_merge = [0,0,0,0,0,0]+ [ 4* (x%4 < 3) * odd_bits[x-5] * odd_bits[x-1] for x in range(6,length)]			#added this to compensate for byte 0,1 == 4,4. Might actually need to be 3-4 consecutive 4s
	odd_merge = [0,0,0,0,0,0]+ [ 4* (x%4 in [0,2,3]) * odd_bits[x-5] * odd_bits[x-1] for x in range(6,length)]			#added this to compensate for byte 0,1 == 4,4. Might actually need to be 3-4 consecutive 4s
	#print("odd_merge    :", odd_merge)
	
	#print("even_bits    :", even_bits[:-8])
	#even_merge= [0,0,0,0,0,0]+[ 4*  even_bits[x-5] * even_bits[x-1] for x in range(6,length)]	
	#print("even_merge   :", even_merge)
	
	#if debug: print("\ndelta1347:    ", delta_1347[start:start+length])
	odd_single_d0 = [(delta_1347[x+start]*odd_bits[x-0])  for x in range(0, length)]  
	#if debug: print("odd_single_d0:", odd_single_d0)
		
	odd_single_d2 = [(delta_1347[x+start]*odd_bits[x-2])  for x in range(0, length)]  
	#if debug: print("odd_single_d2:", odd_single_d2)
		
	odd_single_d3 = [(delta_1347[x+start]*odd_bits[x-3])  for x in range(0, length)]  
	#if debug: print("odd_single_d3:", odd_single_d3)
		
	odd_single_d6 = [(delta_1347[x+start]*odd_bits[x-6])  for x in range(0, length)]  
	#if debug: print("odd_single_d6:", odd_single_d6)
		
	
	#if debug: print("\ndelta2:       ", delta_2[start:start+length])
	odd_single_d1 = [(delta_2[x+start]*odd_bits[x-1])  for x in range(0, length)]  
	#if debug: print("odd_single_d1:", odd_single_d1)
		
	
	#if debug: print("\ndelta6:       ", delta_6[start:start+length])
	odd_single_d5 = [(delta_6[x+start]*odd_bits[x-5])  for x in range(0, length)]  
	#if debug: print("odd_single_d5:", odd_single_d5)
	
	even_single = [4*even_bits[x] for x in range(0, length)]
	#if debug: print("even_single  :", even_single)
	
	odd_11 = [4*((odd_bits[x]+odd_bits[x-1]+odd_bits[x-2]+odd_bits[x-3])==2 or (odd_bits[x]+odd_bits[x-1]+odd_bits[x-2]+odd_bits[x-3])==3) for x in range(0, length)]
	
	odd_1001000 = [4 * (odd_bits[x-6]*odd_bits[x-3]) for x in range(0, length)]#1nn1nnn
	
	odd_100010 = []
	for x in range(0, length):
		if x%4==0: odd_100010.append(6 * (odd_bits[x-5]*odd_bits[x-1]))
		elif x%4==3: odd_100010.append(6 * (odd_bits[x-5]*odd_bits[x-1]))
		elif x%4==1: odd_100010.append(6 * (odd_bits[x-5]*odd_bits[x-1]))
		elif x%4==2: odd_100010.append(2 * (odd_bits[x-5]*odd_bits[x-1]))
		#else: odd_100010.append(0)
	#if x%4==0: odd_100010 = [6 * (odd_bits[x-5]*odd_bits[x-1]) for x in range(0, length)]
	#if x%4==3: odd_100010 = [2 * (odd_bits[x-5]*odd_bits[x-1]) for x in range(0, length)]
	#if x%4==1: odd_100010 = [2 * (odd_bits[x-5]*odd_bits[x-1]) for x in range(0, length)]
	#if x%4==2: odd_100010 = [2 * (odd_bits[x-5]*odd_bits[x-1]) for x in range(0, length)]
	odd_1000100 = [4 * (odd_bits[x-6]*odd_bits[x-2]) for x in range(0, length)]
	odd_1000010 = [4 * (odd_bits[x-6]*odd_bits[x-1]) for x in range(0, length)]
	odd_1000001 = [4 * (odd_bits[x-6]*odd_bits[x-0]) for x in range(0, length)]
	
	diff = [((odd_single_d0[x] + odd_single_d1[x] + odd_single_d2[x] + odd_single_d3[x] 
	+ odd_single_d5[x] + odd_single_d6[x] + even_single[x] + odd_11[x] + odd_1001000[x] 
	+ odd_100010[x] + odd_1000100[x] + odd_1000010[x] + odd_1000001[x] + odd_merge[x] #+ even_merge[x]
	)%8) for x in range(0, length)]
	
	
	
	try:
		sum = [(zeros_symbols[x+start] - diff[x] + 8) % 8 for x in range(0, length)]
	except:
		print("ERROR compute() crashed")
		print("x =",x)
		print("length =", length)
		print("zeros_symbols:", zeros_symbols, len(zeros_symbols))
		print("diff         :", diff, len(diff))
		sys.exit(1)
		
		
		
	error =  sum[ignore:] != expected[ignore:]
	#if error:
	#	print("Data mismatch")
	
	if debug or (error and print_error):
		print("compute() debug:")
		print("zeros_symbols:", zeros_symbols)
		print("bytes        :", in_data)
		print("nibbles      : [", end='')
		for x in nibbles[0:-4]:
			print("%x,    "%x,end='')
		print('\b\b]')
		print("nips         :", nips[:-8],"\n")
		print("odd_bits     :", odd_bits[:-8])
		print("even_bits    :", even_bits[:-8])
		print("odd_single_d0:", odd_single_d0)
		print("odd_single_d1:", odd_single_d1)
		print("odd_single_d2:", odd_single_d2)
		print("odd_single_d3:", odd_single_d3)
		print("odd_single_d5:", odd_single_d5)
		print("odd_single_d6:", odd_single_d6)
		print("even_single  :", even_single)
		print("odd_11       :", odd_11)
		print("odd_1001000  :", odd_11)
		print("odd_100010   :",  odd_100010)
		print("odd_1000100  :", odd_1000100)
		print("odd_1000010  :", odd_1000010)
		print("odd_1000001  :", odd_1000001)
		print("odd_merge    :", odd_merge)
		#print("even_merge   :", even_merge)
		#print("odd_11b      :", odd_11b)
		#print("odd_11c      :", odd_11c)
		print("diff         :", diff)
		print("sum          :", sum)
		print("expected     :", expected)		
		
	if error and print_error:
		print("sum          :", sum)
		print("expected     :", expected)
		print("                ", end="")
		print(ignore*"-  ", end="")
		for x in range(ignore,length):
			if sum[x] == expected[x]: print("   ",end="")
			else: print("*  ", end="")
		print()
		

	#print(sum)
	return sum




def solver(in_data_orig, expected_orig, debug=False, ignore=0, print_error=True, print_result=True):
	in_data = in_data_orig.copy()# prevent modification of data
	expected = expected_orig.copy()#+8*[0]
	if debug and False:
		print("solver() debug:")
		print("in_data",in_data)
		print("len",len(in_data)*4)
		print("expected",expected)
		print("len",len(expected))

	sum = compute(in_data, expected+8*[0], debug, ignore, print_error)
	
	L = len(in_data*4)
	while sum[0:L] != expected[0:L]:
		if debug:
			print()
			print(sum)
			print(expected)
		for x in range(ignore,L):
			if sum[x] != expected[x]:
				#print(x)
				#print(in_data)
				in_data[x//4] += 1<<2*(x%4)	
				#print(in_data)
				if (in_data[x//4] // (1<<2*(x%4))) > 3: 
					if print_error: 
						print(sum)
						print(expected)					#sys.exit(1)
						print("Impossible", x)
					return "Impossible"
				sum = compute(in_data, expected, debug, ignore, print_error)
				break

		
		
	if print_result:
		print("Sum          :",sum)
		print("Expected     :",expected)
		print("Found:", in_data)
		for c in in_data: 	print(hex(c),end=" ")
		print()
		for c in in_data: 
			if c != 0x9e: print(chr(c),end=" ")   #printing 9e or 9e 6e kills python???
		print()
	return in_data



if 1:
	#                                                                                                          |           |           |           |           |           |
	#startup3 = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6, 2, 7, 3, 4, 2, 7, 3, 5, 3, 4, 4, 2, 3, 4, 0, 7, 0, 7, 3, 2, 5, 4, 5, 0, 5, 0, 0, 6, 2, 6, 2, 3, 2, 3, 5, 4, 2, 4, 6, 1, 7, 3, 1, 1, 5, 5, 1, 6, 1, 7, 6, 1, 1, 4, 1, 1, 6, 7, 7, 3, 5, 2, 7, 7, 7, 1, 2, 5, 2, 7, 2, 4]#, 0, 0]
	#Z =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6, 0, 6, 7, 3, 6, 3, 5, 1, 1, 6, 1, 1, 3, 3, 5, 5, 0, 7, 3, 2, 5, 4, 3, 5, 7, 0, 3, 6, 4, 0, 7, 3, 0, 4, 1, 4, 4, 2, 7, 4, 6, 2, 0, 2, 0, 7, 6, 6, 1, 6, 4, 1, 3, 1, 4, 4, 0, 7, 7, 3, 5, 2, 7, 7, 5, 4, 4, 3, 6, 4, 0, 0]#, 0, 0] #, 3, 0, 0, 1] Found: [0, 0, 0, 0, 0, 0, 0, 0, 51, 51, 13, 0, 0, 48, 52, 176, 51, 69, 48, 52, 149, 0, 0, 0, 129, 170]
	# Found: [0, 0, 0, 0, 0, 0, 0, 0, 51, 51, 13, 0, 0, 48, 52, 176, 51, 69, 48, 52, 149, 0, 0, 0, 129, 170]
	# 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x33 0x33 0xd 0x0 0x0 0x30 0x34 0xb0 0x33 0x45 0x30 0x34 0x95 0x0 0x0 0x0 0x81 0xaa 
   # 3 3 \d   0 4 ° 3 E 0 4      ª  


	#                                                                                  |                        |          |           |            |           |          |
	#Z =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 7, 3, 6, 3, 5, 1, 1, 6, 1, 1, 3, 3, 5, 5, 0, 7, 3, 2, 5, 4, 3, 5, 7, 0, 3, 6, 4, 0, 7, 3, 0, 4, 1, 4, 4, 2, 7, 4, 6, 2, 0, 2, 0, 7, 6, 6, 1, 6, 4, 1, 3, 1, 4, 4, 0, 7, 7, 3, 5, 2, 7, 7, 5, 4, 4, 3, 6, 4, 0, 0]#, 0, 0] #, 3, 0, 0, 1] Found: [0, 0, 0, 0, 0, 128, 135, 0, 51, 51, 13, 0, 0, 48, 52, 176, 51, 69, 48, 52, 149, 0, 0, 0, 129, 170]
	# Found: [0, 0, 0, 0, 0, 128,| 135, 0,| 51, 51, 13, 0, 0, 48, 52, 176, 51, 69, 48, 52, 149, 0, 0, 0, 129, 170]
	# 0x0 0x0 0x0 0x0 0x0 0x80 0x87 0x0 | 0x33 0x33 0xd 0x0 0x0 0x30 0x34 0xb0 0x33 0x45 0x30 0x34 0x95 0x0 0x0 0x0 0x81 0xaa 
   #3 3 \d    0 4 ° 3 E 0 4      ª 
	
	
	#                                                                                                          |           |           |           |           |           |
	#startup3 = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6, 6, 7, 3, 4, 2, 7, 3, 5, 3, 4, 4, 2, 3, 4, 0, 7, 0, 7, 3, 2, 5, 4, 5, 0, 5, 0, 0, 6, 2, 6, 2, 3, 2, 3, 5, 4, 2, 4, 6, 1, 7, 3, 1, 1, 5, 5, 1, 6, 1, 7, 6, 1, 1, 4, 1, 1, 6, 7, 7, 3, 5, 2, 7, 7, 7, 1, 2, 5, 2, 7, 2, 4]#, 0, 0]
	#Z =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6, 0, 6, 7, 3, 6, 3, 5, 1, 1, 6, 1, 1, 3, 3, 5, 5, 0, 7, 3, 2, 5, 4, 3, 5, 7, 0, 3, 6, 4, 0, 7, 3, 0, 4, 1, 4, 4, 2, 7, 4, 6, 2, 0, 2, 0, 7, 6, 6, 1, 6, 4, 1, 3, 1, 4, 4, 0, 7, 7, 3, 5, 2, 7, 7, 5, 4, 4, 3, 6, 4, 0, 0]#, 0, 0] #, 3, 0, 0, 1] Found: [0, 0, 0, 0, 0, 0, 0, 0, 51, 51, 13, 0, 0, 48, 52, 176, 51, 69, 48, 52, 149, 0, 0, 0, 129, 170]
	# Found: [0, 0, 0, 0, 0, 0, 0, 0, 49, 51, 13, 0, 0, 48, 52, 176, 51, 69, 48, 52, 149, 0, 0, 0, 129, 170]
	# 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x31 0x33 0xd 0x0 0x0 0x30 0x34 0xb0 0x33 0x45 0x30 0x34 0x95 0x0 0x0 0x0 0x81 0xaa 
   # 1 3 \d     0 4 ° 3 E 0 4      ª 

	#init pattern + 2
	#          |           |           |           |           |           |
	startup3 = [6, 7, 3, 4, 2, 7, 3, 5, 3, 4, 4, 2, 3, 4, 0, 7, 0, 7, 3, 2]
	Z =        [0, 6, 7, 3, 6, 3, 5, 1, 1, 6, 1, 1, 3, 3, 5, 5, 0, 7, 3, 2]
	# Found: [49, 51, 13, 0, 0]
	# 0x31 0x33 0xd 0x0 0x0 






	#earliest startup counter
	#          |           |           |           |           |           |
	startup3 = [4, 0, 0, 6, 1, 4, 5, 1, 4, 3, 1, 2, 3, 3, 6, 7, 0, 3, 3, 2]
	# Found: [214, 151, 12, 0, 8]
	# 0xd6 0x97 0xc 0x0 0x8 
	
	#          |           |           |           |           |           |
	startup3 = [0, 0, 0, 6, 1, 4, 5, 1, 4, 3, 1, 2, 3, 3, 6, 7, 0, 3, 3, 2]
	# Found: [212, 151, 12, 0, 8]
	# 0xd4 0x97 0xc 0x0 0x8 
	
	#          |           |           |           |           |           |
	startup3 = [4, 2, 7, 5, 1, 2, 6, 4, 2, 3, 1, 2, 3, 3, 6, 7, 0, 3, 3, 2]
	# Found: [202, 23, 12, 0, 8]
	# 0xca 0x17 0xc 0x0 0x8 
		
	#          |           |           |           |           |           |
	startup3 = [0, 2, 7, 5, 1, 2, 6, 4, 2, 3, 1, 2, 3, 3, 6, 7, 0, 3, 3, 2]
	# Found: [200, 23, 12, 0, 8]
	# 0xc8 0x17 0xc 0x0 0x8 	

	#          |           |           |           |           |           |
	startup3 = [4, 4, 6, 7, 3, 2, 5, 2, 2, 3, 1, 2, 3, 3, 6, 7, 0, 3, 3, 2]
	# Found: [206, 23, 12, 0, 8]
	# 0xce 0x17 0xc 0x0 0x8 		
	
	#          |           |           |           |           |           |
	startup3 = [4, 6, 7, 5, 1, 2, 6, 4, 2, 3, 1, 2, 3, 3, 6, 7, 0, 3, 3, 2]
	# Found: [194, 23, 12, 0, 8]
	# 0xc2 0x17 0xc 0x0 0x8 		
	
	#          |           |           |           |           |           |
	startup3 = [0, 6, 7, 5, 1, 2, 6, 4, 2, 3, 1, 2, 3, 3, 6, 7, 0, 3, 3, 2]
	# Found: [192, 23, 12, 0, 8]
	# 0xc0 0x17 0xc 0x0 0x8 		
	
	#          |           |           |           |           |           |
	startup3 = [4, 0, 6, 7, 3, 2, 5, 2, 2, 3, 1, 2, 3, 3, 6, 7, 0, 3, 3, 2]
	# Found: [198, 23, 12, 0, 8]
	# 0xc6 0x17 0xc 0x0 0x8 	
	
	#          |           |           |           |           |           |
	startup3 = [0, 0, 6, 7, 3, 2, 5, 2, 2, 3, 1, 2, 3, 3, 6, 7, 0, 3, 3, 2]
	# Found: [196, 23, 12, 0, 8]
	# 0xc4 0x17 0xc 0x0 0x8 	
	
	#          |           |           |           |           |           |
	startup3 = [4, 2, 1, 6, 2, 2, 0, 3, 3, 1, 1, 2, 3, 3, 6, 7, 0, 3, 3, 2]
	# Found: [186, 151, 12, 0, 8]
	# 0xba 0x97 0xc 0x0 0x8  	
	
	
	
	
	
	#          |           |           |           |           |           |	
	Z=         [6, 5, 0, 3, 6, 7, 5, 4, 2, 2, 1, 4, 4, 2, 0, 7, 0, 7, 3, 2]
	#init pattern
	startup3 = [2, 7, 3, 4, 2, 7, 3, 5, 3, 4, 4, 2, 3, 4, 0, 7, 0, 7, 3, 2]
	#Found: [54, 230, 0, 0, 0]   0x36 0xe6 0x0 0x0 0x0 


	#init pattern + 2
	#startup3 = [6, 7, 3, 4, 2, 7, 3, 5, 3, 4, 4, 2, 3, 4, 0, 7, 0, 7, 3, 2]
	#Found: [52, 230, 0, 0, 0]   0x34 0xe6 0x0 0x0 0x0 

	
	
	#earliest startup counter
	#          |           |           |           |           |           |
	startup3 = [4, 0, 0, 6, 1, 4, 5, 1, 4, 3, 1, 2, 3, 3, 6, 7, 0, 3, 3, 2]
	# Found: [211, 74, 1, 0, 8]	0xd3 0x4a 0x1 0x0 0x8 
	startup3 = [0, 0, 0, 6, 1, 4, 5, 1, 4, 3, 1, 2, 3, 3, 6, 7, 0, 3, 3, 2]
	# Found: [209, 74, 1, 0, 8] 0xd1 0x4a 0x1 0x0 0x8 
	startup3 = [4, 2, 7, 5, 1, 2, 6, 4, 2, 3, 1, 2, 3, 3, 6, 7, 0, 3, 3, 2]
	#Found: [207, 74, 1, 0, 8]
	startup3 = [0, 2, 7, 5, 1, 2, 6, 4, 2, 3, 1, 2, 3, 3, 6, 7, 0, 3, 3, 2]
	#Found: [205, 74, 1, 0, 8]
	startup3 = [4, 4, 6, 7, 3, 2, 5, 2, 2, 3, 1, 2, 3, 3, 6, 7, 0, 3, 3, 2]
	#Found: [203, 74, 1, 0, 8]
	startup3 = [4, 6, 7, 5, 1, 2, 6, 4, 2, 3, 1, 2, 3, 3, 6, 7, 0, 3, 3, 2]
	#Found: [199, 74, 1, 0, 8]
	startup3 = [0, 6, 7, 5, 1, 2, 6, 4, 2, 3, 1, 2, 3, 3, 6, 7, 0, 3, 3, 2]
	#197
	startup3 = [4, 0, 6, 7, 3, 2, 5, 2, 2, 3, 1, 2, 3, 3, 6, 7, 0, 3, 3, 2]
	#195
	startup3 = [0, 0, 6, 7, 3, 2, 5, 2, 2, 3, 1, 2, 3, 3, 6, 7, 0, 3, 3, 2]
	#Found: [193, 74, 1, 0, 8]
	startup3 = [4, 2, 1, 6, 2, 2, 0, 3, 3, 1, 1, 2, 3, 3, 6, 7, 0, 3, 3, 2]
	#Found: [191, 74, 1, 0, 8]
	
	
	#other earliest startup counter
	startup3 = [2, 3, 5, 1, 6, 2, 0, 2, 1, 2, 3, 2, 3, 3, 6, 7, 0, 3, 3, 2]
	# Found: [14, 73, 1, 0, 8]
	# 0xe 0x49 0x1 0x0 0x8 




	startup3 = [0, 0, 6, 1, 4, 3, 2, 7, 1, 4, 4, 3, 1, 3, 6, 7, 0, 3, 3, 2]
	#Found: [1, 247, 1, 0, 8]
	#0x1 0xf7 0x1 0x0 0x8 

	#rollover
	startup3 = [4, 2, 1, 0, 7, 0, 6, 1, 7, 4, 1, 4, 4, 2, 0, 7, 0, 3, 3, 2]
	#Found: [255, 0, 2, 0, 8]
	#0xff 0x0 0x2 0x0 0x8 
	
	
	
	#test 11 rollover
	startup3 = [0, 0, 6, 1, 4, 3, 2, 7, 5, 0, 4, 3, 1, 3, 6, 7, 0, 3, 3, 2]
	#Found: [1, 247, 11, 0, 8]
	startup3 = [4, 2, 1, 0, 7, 0, 6, 1, 3, 2, 2, 3, 4, 4, 7, 6, 6, 3, 3, 2]
	#Found: [255, 0, 20, 0, 8]




	#          |           |           |           |           |           |	
	Z=         [2, 3, 3, 6, 7, 7, 0, 1, 3, 4, 1, 4, 4, 2, 0, 7, 0, 7, 3, 2]       #third block should be 3 2 . .
	#test 11 rollover
	startup3 = [0, 0, 6, 1, 4, 3, 2, 7, 5, 0, 4, 3, 1, 3, 6, 7, 0, 3, 3, 2]
	#Found: [255, 87, 9, 0, 8]
	startup3 = [4, 2, 1, 0, 7, 0, 6, 1, 3, 2, 2, 3, 4, 4, 7, 6, 6, 3, 3, 2]
	#Found: [1, 0, 20, 0, 8]

	#earliest startup counter
	startup3 = [4, 0, 0, 6, 1, 4, 5, 1, 4, 3, 1, 2, 3, 3, 6, 7, 0, 3, 3, 2]
	#Found: [45, 74, 1, 0, 8]

	#init
	startup3 = [2, 7, 3, 4, 2, 7, 3, 5, 3, 4, 4, 2, 3, 4, 0, 7, 0, 7, 3, 2]
	#Found: [200, 230, 2, 0, 0]




	Z = [2, 3, 3, 6,  7, 7, 0, 1,  5, 1, 1, 3, 2, 3, 6, 0, 6, 7, 3, 2]   #1,0,19
	#test 11 rollover
	startup3 = [0, 0, 6, 1, 4, 3, 2, 7, 5, 0, 4, 3, 1, 3, 6, 7, 0, 3, 3, 2]
	#Found: [255, 87, 154, 0, 8]

	startup3 = [4, 2, 1, 0, 7, 0, 6, 1, 3, 2, 2, 3, 4, 4, 7, 6, 6, 3, 3, 2]
	#Found: [1, 0, 7, 0, 8]

	#init
	startup3 = [2, 7, 3, 4, 2, 7, 3, 5, 3, 4, 4, 2, 3, 4, 0, 7, 0, 7, 3, 2]	
	#Found: [200, 230, 17, 0, 0]
	#0xc8 0xe6 0x11 0x0 0x0 



	#Z = [2, 3, 3, 6,   7, 4, 4, 6,   5, 1, 1, 3, 2, 3, 6, 0, 6, 7, 3, 2]   #imp
	Z = [2, 3, 3, 6,   7, 3, 2, 4,   5, 1, 1, 3, 2, 3, 6, 0, 6, 7, 3, 2]   #
	
	startup3 = [0, 0, 6, 1, 4, 3, 2, 7] #Found: [255, 239]
	startup3 = [4, 2, 1, 0, 7, 0, 6, 1] #Found: [1, 56]

	Z = [2, 3, 3, 6,   7, 7, 4, 7,   5, 1, 1, 3, 2, 3, 6, 0, 6, 7, 3, 2]   #
	

	startup3 = [0, 0, 6, 1, 4, 3, 2, 7] #Found: [255, 183]       should be 255 and go to 0...????
	startup3 = [4, 2, 1, 0, 7, 0, 6, 1] #Found: [1, 0]
	
	startup3 = [0, 0, 6, 1, 4, 3, 2, 7, 5, 0, 4, 3, 1, 3, 6, 7, 0, 3, 3, 2]
	
	
	
	Z = [2, 3, 3, 6,   7, 7, 0, 1,   3, 2, 2, 3,  2, 3, 6, 0, 6, 7, 3, 2] 
	startup3 = [0, 0, 6, 1,  4, 3, 2, 7,  5,0,4,3] #Found: [255, 87, 189]	
	#startup3 = [4, 2, 1, 0,  7, 0, 6, 1,  3,2,2,3] #Found: [1, 0, 0]	
	
	startup3 = [6,5,0,3, 4,4,6,2 ,3,0,1,2] #Found: [254, 111, 27]  0xfe 0x6f 0x1b
	#startup3 = [2, 3, 3, 6,   7, 7, 6,2, 2,7,4,3] #Found: [0, 80, 153] 0x0 0x50 0x99

	
	'''	
	#          |           |           |           |           |           |           |           |           |           |           |           |           |           |
	startup3 = [5, 4, 5, 0, 5, 0, 0, 6, 2, 6, 2, 3, 2, 3, 5, 4, 2, 4, 6, 1, 7, 3, 1, 1, 5, 5, 1, 6, 1, 7, 6, 1, 1, 4, 1, 1, 6, 7, 7, 3, 5, 2, 7, 7, 7, 1, 2, 5, 2, 7, 2, 4]#, 0, 0]
	Z =        [5, 4, 3, 5, 7, 0, 3, 6, 4, 0, 7, 3, 0, 4, 1, 4, 4, 2, 7, 4, 6, 2, 0, 2, 0, 7, 6, 6, 1, 6, 4, 1, 3, 1, 4, 4, 0, 7, 7, 3, 5, 2, 7, 7, 5, 4, 4, 3, 6, 4, 0, 0]#, 0, 0] #, 3, 0, 0, 1]
	#Found: [48, 52, 176, 51, 69, 48, 52, 149, 0, 0, 0, 129, 170]
	#0x30 0x34 0xb0 0x33 0x45 0x30 0x34 0x95 0x0 0x0 0x0 0x81 0xaa 
	#0 4 ° 3 E 0 4      ª 
	'''

	'''
	startup3 = [7, 1, 2, 5, 2, 7, 2, 4]
	Z =        [5, 4, 4, 3, 6, 4, 0, 0]  #Found: [129, 170] = 0x81 0xaa 
	'''

	'''
	startup3 = [7, 1, 2, 5, 2, 7, 2, 4]

	Z =        [5, 6, 5, 5, 4, 4, 7, 2]#, 0, 0]  # Found: [45, 40]
	Z=         [1, 0, 2, 2, 4, 6, 0, 3]#, 2, 4]#+2 Found: [155, 32] = 0x9b 0x20 
	'''

	'''
	for x in range(0,2):
		for y in range(0,2):
			#Z = [2, 3, 3, 6,   7, 7, 0, 1,   3, 2, 2, 3,   2, 3, 6, x,  6, 7, 3, 2]   #0xc6 0xc6 0x36 0x*5 
			#Z = [2, 3, 3, 6,   7, 7, 0, 1,   3, 2, 2, 7,   2, 3, 6, x,  6, 7, 3, 2] #0xc6 0xc6 0xb6
			#Z = [2, 3, 3, 6,   7, 7, 0, 1,   3, 2, 4, 0]  #c6c6e6
			Z = [2, 3, 3, 6, 7, 7, 0, 1, 3, 2, 6, 7] #0xc6 0xc6 0x96 
			Z = [2, 3, 3, 6, 7, 7, 0, 1, 3, 2, 6, 5] #0xc6 0xc6 0xd6 	
			Z = [2, 3, 3, 6, 7, 7, 0, 1, 3, 2, 4, 0] #0xc6 0xc6 0xe6		
			Z = [2, 3, 3, 6, 7, 7, 0, 1, 3, 2, 0, 0] #0xc6 0xc6 0xc6	
			Z = [2, 3, 3, 6,   7, 7, 0, 1,   3, 2, 0, 0,   3,2,4,1,  0+4*x, 1+4*y, 3, 2]
			print("\n\n",Z)
			zeros_symbols = Z.copy()
			delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in zeros_symbols]   # 001 010 101 110 
			delta_2 = [(x*2+3)%8 for x in zeros_symbols]
			delta_6 = [1 + 6 * (x & 1) for x in zeros_symbols]
			solution = solver([0,0,0,0,0], [6,1,2,2, 4,7,4,7, 3,4,4,2, 3,4,0,7, 0,7,3,2], debug=False, ignore=0, print_error=False)
			solution = solver([0,0,0,0,0], [2,3,3,6,7,7,2,6,2,7,4,3,3,3,5,5,2,6,1,4], debug=False, ignore=0, print_error=False)		
	sys.exit()
	
	for x in range(0,1):
		for y in range(0,8):		
			Z = [2, 3, 3, 6,   7, 7,x,y]
			print(Z)

			zeros_symbols = Z.copy()


			delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in zeros_symbols]   # 001 010 101 110 
			delta_2 = [(x*2+3)%8 for x in zeros_symbols]
			delta_6 = [1 + 6 * (x & 1) for x in zeros_symbols]


			startup3 = [0, 0, 6, 1,  4, 3, 2, 7,  5,0,4,3] #Found: [255, 87, 189]	
			solution = solver([0,0], startup3, debug=False, print_error=False, ignore=0)
			
			startup3 = [4, 2, 1, 0,  7, 0, 6, 1,  3,2,2,3] #Found: [1, 0, 0]	
			solution = solver([0,0], startup3, debug=False, print_error=False, ignore=0)#, print_error=False)
		
		
			startup3 = [6,5,0,3, 4,4,6,2 ,3,0,1,2] #Found: [254, 111, 27]  0xfe 0x6f 0x1b
			solution = solver([0,0], startup3, debug=False, print_error=False, ignore=0)#, print_error=False)
			
			startup3 = [2, 3, 3, 6,   7, 7, 6,2, 2,7,4,3] #Found: [0, 80, 153] 0x0 0x50 0x99	
			solution = solver([0,0], startup3, debug=False, print_error=False, ignore=0)#, print_error=False)	
	'''
	Z = [2, 3, 3, 6,   7, 7, 0, 1,   3, 2, 0, 0,]
	zeros_symbols = Z.copy()
	delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in zeros_symbols]   # 001 010 101 110 
	delta_2 = [(x*2+3)%8 for x in zeros_symbols]
	delta_6 = [1 + 6 * (x & 1) for x in zeros_symbols]
	
	
	#solution = solver([4,4], [2, 1, 2, 0, 5, 5, 6, 1], debug=False, ignore=0)#, print_error=False, print_result=False)
	#print()
	#solution = solver([0, 1, 235], [2, 3, 3, 6, 5, 6, 6, 3, 5, 0, 4, 4, 2, 1, 5, 5], debug=False, ignore=0)#, print_error=False, print_result=False)
	#sys.exit()	
	
	#with open("test_0s_110_symbols.txt") as infile:
	with open("test_0s_20_90_147_symbols.txt") as infile:	
		'''
		num = 5+256*2
		for x in range(0,55616+(1+num)*128*10000):
			line = infile.readline()
			if x < 55616-4*128: continue
			#if x < 24700: continue
			if (x-64)%(128*256) < 10:
			#if x<25100:
				symbols = [int(n) for n in line.split(' ')[0:20]]
				solution = solver([0,0,0], symbols, debug=False, ignore=0, print_error=False, print_result=False)
				print("{}: {} [{:3}, {:3}, {:3}] [{:08b}, {:08b}, {:08b}]".format(x, symbols[0:16], solution[0], solution[1],solution[2], solution[0], solution[1],solution[2]))
			if (x-64)%(128*256) == 10: print()
		'''
		
		#this code tests a recording of 200000 and the math works!
		solution = [116,  78, 233]
		last_solution = [116,  78, 233]
		last_sol = solution[0] + 256*solution[1] + 256*256*solution[2] -2
		line = infile.readline()
		x = 0
		while line:
			symbols = [int(n) for n in line.split(' ')[0:20]]
			solution = solver([0,0,0], symbols, debug=False, ignore=0, print_error=False, print_result=False)
			sol = solution[0] + 256*solution[1] + 256*256*solution[2]
			if sol-2 != last_sol:
				print(x,last_solution, solution,last_sol, sol)
				print("{}: {} [{:3}, {:3}, {:3}] [{:08b}, {:08b}, {:08b}]".format(x, symbols[0:16], solution[0], solution[1],solution[2], solution[0], solution[1],solution[2]))
			last_sol = sol
			last_solution = solution
			line = infile.readline()
			x += 1
	sys.exit()	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	for x in range(0,8):
		for y in range(0,8):		
			Z = [2, 3, 3, 6,   7, 7, 0, 1,   3, 2, x,y]
			print(Z)

			zeros_symbols = Z.copy()

			init = len(startup3)//4 * [0]

			delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in zeros_symbols]   # 001 010 101 110 
			delta_2 = [(x*2+3)%8 for x in zeros_symbols]
			delta_6 = [1 + 6 * (x & 1) for x in zeros_symbols]


			print(len(zeros_symbols),len(startup3),len(init)*4)

			startup3 = [0, 0, 6, 1,  4, 3, 2, 7,  5,0,4,3] #Found: [255, 87, 189]	
			solution = solver(init, startup3, debug=False, print_error=False, ignore=0)#, print_error=False)
			
			startup3 = [4, 2, 1, 0,  7, 0, 6, 1,  3,2,2,3] #Found: [1, 0, 0]	
			solution = solver(init, startup3, debug=False, print_error=False, ignore=0)#, print_error=False)
		
		
			startup3 = [6,5,0,3, 4,4,6,2 ,3,0,1,2] #Found: [254, 111, 27]  0xfe 0x6f 0x1b
			solution = solver(init, startup3, debug=False, print_error=False, ignore=0)#, print_error=False)
			
			startup3 = [2, 3, 3, 6,   7, 7, 6,2, 2,7,4,3] #Found: [0, 80, 153] 0x0 0x50 0x99	
			solution = solver(init, startup3, debug=False, print_error=False, ignore=0)#, print_error=False)	
		


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
		





if 0:
	print("solve for 2 mystery bytes after the confirmed header 6 bytes")
	#Found: [0, 0, 0, 0, 0, 128, 135, 0]
	#0x0 0x0 0x0 0x0 0x0 0x80 0x87 0x0       1000 0000  1000 0111
	Z =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	zeros_symbols = Z.copy()
	actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6]
	delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in Z]   # 001 010 101 110 
	delta_2 = [(x*2+3)%8 for x in Z]
	delta_6 = [1 + 6 * (x & 1) for x in Z]
	solution = solver([0,0,0,0,0,0,0,0], actual, debug=True, ignore=0)#, print_error=False)
	print("\n\n\n")

if 0:
	Z =        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	zeros_symbols = Z.copy()


	#solve for 2 mystery bytes after the confirmed header 6 bytes
	#nibbles      : [a,    2,    2,    2,    f,   impossible starting at 4,6
	#even_bits    : [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6]
	delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in Z]   # 001 010 101 110 
	delta_2 = [(x*2+3)%8 for x in Z]
	delta_6 = [1 + 6 * (x & 1) for x in Z]
	solution = solver([0,0,0,0,0,0,0,0], actual, debug=True, ignore=0)#, print_error=False)
	print("\n\n\n")
	



print("solve for 2 mystery bytes + 1 after the confirmed header 6 bytes")
print("zeros_symbols:", zeros_symbols)
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


print(len(zeros_symbols),len(actual),len([0,0,0,0,0,0,0,0]+[0]+[0]+[0])*4)



solution = solver([0,0,0,0,0,0,0,0]+[0]+[0]+[0], actual, debug=True, ignore=0)#, print_error=False)






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
	'''
	if solution != "Impossible": 
		print("Tested",sol)
		print("solved")	
	'''	
	if solution == "Impossible": 
		print("Tested",sol)
		print("eliminated")			
		
				
