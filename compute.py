#zeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6, 4,2,1,0, 7,0,6,1 ,3,4,1,4, 4,2,0,7, 0,7,3,2,        5,4,3,5,7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7, 5,4,4,3, 6,4,0,0,0,0,3,0,0,1]
#zeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6,  2,3,3,6,   7,7,0,1,   3,2,4, 6,  3,2,4,3 ,0,7,3,2,  5,4,3,5,7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7, 5,4,4,3, 7,7,7,7,0,1,0,0,0,0]
#3240 starts at 201
#3242 starts at 9
#3244 73
#3246 137
#dzeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6, 2,3,3,6, 7,7,0,1, 3,2,4, 2,  2, 2, 7, 5,  0, 7, 3, 2,  5,4,3,5,7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7, 5,4,4,3, 7,7,7,7,0,1, 0,0,0,0]
#recorded during glitch, asssume 1,0,0,0,0
#dzeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6, 2,3,3,6, 7,7,0,1, 3,2,4,2, 2,2,7,5, 4,3,3,2,            5,4,3,5,7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7, 5,4,4,3, 7,7,7,7,0,1, 0,0,0,0]
#                                                																       ^ ^		
#recorded during glitch 2:
#dzeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6, 2,3,3,6, 7,7,0,1, 3,2,4,2, 2,2,7,5, 0,3,3,2,           5,4,3,5, 7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7, 5,4,4,3, 7,7,7,7,0,1]
#                                                																         ^		
dzeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6, 2,3,3,6, 7,7,0,1, 3,2,4,2, 2,2,7,5, 0,3,3,2,           5,4,3,5, 7,0,3,6, 0,0,7,3, 0,4,1,0, 4,2,7,4, 6,2,0,2, 0,7,6,6, 1,6,4,1, 3,1,4,4, 0,7,7,3, 5,2,7,7,  5,4,4,3, 7,7,7,7,0,1]
#                                                                                           																         ^	   ^ had to change this for start up data, either thise bits wrong or math it wrong again...    	   
#workng 0 packet:                                                                 [2,5,2,2, 6,6,2,7, 4,4,2,4, 4,1,6,7, 0,7,3,2,           5,4,3,5, 7,0,3,6, 4,0,7,3, 0,4,1,4, 4,2,7,4, 6,2,0,2, 0,7,6,6, 1,6,4,1, 3,1,4,4, 0,7,7,3, 5,2,7,7,]#,7,7,3, 0,3,1,6, 4,4])]  7773031644  #1/6 recording
#                                                         0,0,4,2,3,1,3,3,4,2,2,4                                                                           ^              ^
dzeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6, 2,3,3,6, 7,7,0,1, 3,2,4,2, 2,2,7,5, 0,3,3,2,           5,4,3,5, 7,0,3,6, 4,0,7,3, 0,4,1,4, 4,2,7,4, 6,2,0,2, 0,7,6,6, 1,6,4,1, 3,1,4,4, 0,7,7,3, 5,2,7,7,  1,0,0,3,2,0,0,0,0,0] #use valid crc
dzeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6, 2,3,3,6, 7,7,0,1, 3,2,4,2, 2,2,7,5, 0,3,3,2,           5,4,3,5, 7,0,3,6, 4,0,7,3, 0,4,1,4, 4,2,7,4, 6,2,0,2, 0,7,6,6, 1,6,4,1, 3,1,4,4, 0,7,7,3, 5,2,7,7,  1,0,0,3, 2,0,0,0, 0,0,0,0]  #to computer last 2 symbols...
dzeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6, 2,3,3,6, 7,7,0,1, 3,2,4,2, 2,2,7,5, 0,3,3,2,           5,4,3,5, 7,0,3,6, 4,0,7,3, 0,4,1,4, 4,2,7,4, 6,2,0,2, 0,7,6,6, 1,6,4,1, 3,1,4,4, 0,7,7,3, 5,2,7,7,  1,0,0,3, 2,0,0,0, 0,0,0,0, 0,0,0,0] #because out of range error
dzeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6, 2,3,3,6, 7,7,0,1, 3,2,4,2, 2,2,7,5, 0,3,3,2,           5,4,3,5, 7,0,3,6, 4,0,7,3, 0,4,1,4, 4,2,7,4, 6,2,0,2, 0,7,6,6, 1,6,4,1, 3,1,4,4, 0,7,7,3, 5,2,7,7,  7,7,7,3, 0,3,1,6, 4,4,0,0, 0,0,0,0] #because out of range error

ddelta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in dzeros_symbols]   # 001 010 101 110 
ddelta_2 = [(x*2+3)%8 for x in dzeros_symbols]
ddelta_6 = [1 + 6 * (x & 1) for x in dzeros_symbols]


#this version allows expected, print_error
def compute(in_data_orig, expected, debug=False, ignore=0, print_error=True, zeros_symbols=dzeros_symbols, delta_1347=ddelta_1347, delta_2=ddelta_2, delta_6=ddelta_6):    #in_data_orig and expected are ONLY the values to be computed, ignore sets the pos in zero_symbols
	in_data = in_data_orig.copy() # prevent modification of data
	start = ignore*4
	
	length = len(in_data)*4 #- ignore*4
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
	#odd_merge = [0,0,0,0]+ [ 4* ((x%8==4)|(x%8==2)) & even_bits[x-3] & even_bits[x+1] for x in range(4,length-2)] + [0,0] #passes sanity
	#odd_merge = [0,0,0,0,0,0]+ [ 4* (x%4 > 0) * odd_bits[x-5] * odd_bits[x-1] for x in range(6,length)]			#added this to compensate for byte 0,1 == 4,4. Might actually need to be 3-4 consecutive 4s  fails sanity
	#odd_merge = [0,0,0,0,0,0]+ [ 4* (x%4 < 3) * odd_bits[x-5] * odd_bits[x-1] for x in range(6,length)]			
	
	#odd_merge = [0,0,0,0,0,0]+ [ 4* (x%4 in [0,2,3]) * odd_bits[x-5] * odd_bits[x-1] for x in range(6,length)]	#works most of the time data 0 and 1		fail mini test  test1 127->192
	#odd_merge = [0,0,0,0,0,0]+ [ 4 * odd_bits[x-5] * odd_bits[x-1] for x in range(6,length)]  #fail   test1 119-192
	#odd_merge = [0,0,0,0,0,0]+ [ 4* (x%4 in [0,2]) * odd_bits[x-5] * odd_bits[x-1] for x in range(6,length)] #nope  passes mini test tho   test1 127,255 - 0,192
	#odd_merge = [0,0,0,0,0,0]+ [ 4* (x%4 in [3,2]) * odd_bits[x-5] * odd_bits[x-1] for x in range(6,length)] #maybe... fail
	#odd_merge = [0,0,0,0,0,0]+ [ 4* (x%4 in [3,0]) * odd_bits[x-5] * odd_bits[x-1] for x in range(6,length)] #maybe...  winner for data 2    test1 255,233,95-0,0,192
	#really just 100010?
	#odd_merge = [0,0,0,0,0]+ [ 4* (x%4 in [3,0]) * odd_bits[x-5] * odd_bits[x-1] for x in range(5,length)] # 254,223,95 - 0,0,192
	#odd_merge = [0,0,0,0,0,0]+ [ 4* (x%12 in [0,2,3,4,6,7,8,11]) * odd_bits[x-5] * odd_bits[x-1] for x in range(6,length)] #better...?  95-192
	#odd_merge = [0,0,0,0,0,0]+ [ 4* (x%4 in [3]) * odd_bits[x-5] * odd_bits[x-1] for x in range(6,length)] #maybe... fail

	#odd_merge = [0,0,0,0,0,0]+ [ 4* (x%4 in [0,2]) * odd_bits[x-5] * odd_bits[x-1] for x in range(6,length)]			
	#odd_merge = [0,0,0,0,0,0]+ [ 4* (x%4 in [2,3]) * odd_bits[x-5] * odd_bits[x-1] for x in range(6,length)]			#added this to compensate for byte 0,1 == 4,4. Might actually need to be 3-4 consecutive 4s
	#odd_merge = [0,0,0,0,0,0]+ [ 4* (x%4 in [0,3]) * odd_bits[x-5] * odd_bits[x-1] for x in range(6,length)]			#added this to compensate for byte 0,1 == 4,4. Might actually need to be 3-4 consecutive 4s
	#odd_merge = [0,0,0,0,0,0]+ [ 4 * odd_bits[x-5] * odd_bits[x-1] for x in range(6,length)]			#added this to compensate for byte 0,1 == 4,4. Might actually need to be 3-4 consecutive 4s
	#odd_merge = [0,0,0,0,0,0]+ [ 4* (x%4 in [1,2,3]) * odd_bits[x-5] * odd_bits[x-1] for x in range(6,length)]			#added this to compensate for byte 0,1 == 4,4. Might actually need to be 3-4 consecutive 4s
	#odd_merge = [0,0,0,0,0,0]+ [ 4* (x%4 in [0,1,2,3]) * odd_bits[x-5] * odd_bits[x-1] for x in range(6,length)]	
	#odd_merge = [0,0,0,0,0,0]+ [ 4* (x%4 in [4]) * odd_bits[x-5] * odd_bits[x-1] for x in range(6,length)]	
	#odd_merge = [0,0,0,0,0,0]+ [ 4* (x%12 in [0,2,3,4,6,7,11]) * odd_bits[x-5] * odd_bits[x-1] for x in range(6,length)] #better...?
	#odd_merge = [0,0,0,0,0,0]+ [ 4* (x%12 in [0,2,3,4,6,7,8,9,10,11]) * odd_bits[x-5] * odd_bits[x-1] for x in range(6,length)] #better...?
	pos_odd_merge = [0,0,0,0,0]+ [ 4  * odd_bits[x-5] * odd_bits[x-1] for x in range(5,length)] #better...?

	#print("odd_merge    :", odd_merge)
	
	#print("even_bits    :", even_bits[:-8])
	#even_merge= [0,0,0,0,0,0]+[ 4*  even_bits[x-5] * even_bits[x-1] for x in range(6,length)]	
	#print("even_merge   :", even_merge)
	
	#if debug: print("\ndelta1347:    ", delta_1347[start:start+length])
	#print(length, start, len(zeros_symbols))
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
	#odd_11 = [4*((((odd_bits[x]+odd_bits[x-1]+odd_bits[x-2]+odd_bits[x-3])==2) and (odd_bits[x-3:x+1] != [0,1,1,0])) or (odd_bits[x]+odd_bits[x-1]+odd_bits[x-2]+odd_bits[x-3])==3) for x in range(0, length)]
	
	odd_1001000 = [4 * (odd_bits[x-6]*odd_bits[x-3]) for x in range(0, length)]#1nn1nnn   was working but made no sense
	#odd_1001000 = [0,0,0,0,0,0] + [4 * (odd_bits[x-6]*odd_bits[x-3]) for x in range(6, length)]#1nn1nnn

	odd_100010 = []
	'''
	#shit, this rule depends on how many ignores there are..........
	for x in range(0, length):
		#if   x%12==11: odd_100010.append(6 * (odd_bits[x-5]*odd_bits[x-1]))   #to fic count in byte 3 of count
		if x%12==9: odd_100010.append(6 * (odd_bits[x-5]*odd_bits[x-1]))  #adds 8    #fix byte 2 in capture #8, maybe others
		elif x%12==11: odd_100010.append(6 * (odd_bits[x-5]*odd_bits[x-1]))   #to fic count in byte 3 of count
		elif x%4==0: odd_100010.append(2 * (odd_bits[x-5]*odd_bits[x-1]))  #adds 2
		elif x%4==1: odd_100010.append(2 * (odd_bits[x-5]*odd_bits[x-1]))  #adds 8    #was 6 must be 2 for byte 1 in the odd count in capture #8
		elif x%4==2: odd_100010.append(6 * (odd_bits[x-5]*odd_bits[x-1]))  #adds 32
		elif x%4==3: odd_100010.append(2 * (odd_bits[x-5]*odd_bits[x-1]))  #adds 128 6 6 2 6 used to work   2662 should equal merge rule 0,3
	'''
	for x in range(0, length):
		if x%12 in [8,9]: odd_100010.append( ((4 + delta_1347[x+1+start])%8) * (odd_bits[x-5]*odd_bits[x-1]) ) #8 is a guess
		else: odd_100010.append( (delta_1347[x+1+start]) * (odd_bits[x-5]*odd_bits[x-1]) )

		#else: odd_100010.append(0)
	#if x%4==0: odd_100010 = [6 * (odd_bits[x-5]*odd_bits[x-1]) for x in range(0, length)]
	#if x%4==3: odd_100010 = [2 * (odd_bits[x-5]*odd_bits[x-1]) for x in range(0, length)]
	#if x%4==1: odd_100010 = [2 * (odd_bits[x-5]*odd_bits[x-1]) for x in range(0, length)]
	#if x%4==2: odd_100010 = [2 * (odd_bits[x-5]*odd_bits[x-1]) for x in range(0, length)]

	odd_1000100 = [4 * (odd_bits[x-6]*odd_bits[x-2]) for x in range(0, length)] #was working but makes no sense
	#odd_1000100 = [0,0,0,0,0,0] + [4 * (odd_bits[x-6]*odd_bits[x-2]) for x in range(6, length)] #was working but makes no sense

	odd_1000010 = [4 * (odd_bits[x-6]*odd_bits[x-1]) for x in range(0, length)]
	odd_1000001 = [4 * (odd_bits[x-6]*odd_bits[x-0]) for x in range(0, length)]
	
	diff = [((odd_single_d0[x] + odd_single_d1[x] + odd_single_d2[x] + odd_single_d3[x] 
	+ odd_single_d5[x] + odd_single_d6[x] + even_single[x] + odd_11[x] + odd_1001000[x] 
	+ odd_100010[x] + odd_1000100[x] + odd_1000010[x] + odd_1000001[x] #+ odd_merge[x] 
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
		
	

	error =  sum != expected
	#if error:
	#	print("Data mismatch")
	#print(error)

	if debug or (error and print_error):
		print("compute() debug:")
		print("zeros_symbols:", zeros_symbols[start:])
		print("delta_1347:   ", delta_1347[start:])
		print("delta_2:      ", delta_2[start:])
		print("delta_6:      ", delta_6[start:])
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
		print("odd_1001000  :", odd_1001000)
		print("odd_100010   :",  odd_100010)
		print("odd_1000100  :", odd_1000100)
		print("odd_1000010  :", odd_1000010)
		print("odd_1000001  :", odd_1000001)
		#print("odd_merge    :", odd_merge)
		print("pos_odd_merge:", pos_odd_merge)
		#print("even_merge   :", even_merge)
		#print("odd_11b      :", odd_11b)
		#print("odd_11c      :", odd_11c)
		print("diff         :", diff)
		print("sum          :", sum)
		print("expected     :", expected)
		print()
		
	if error and print_error:
		print("sum          :", sum)
		print("expected     :", expected)
		print("                ", end="")
		#print(4*ignore*"-  ", end="")
		for x in range(0, length):
			if sum[x] == expected[x]: print("   ",end="")
			else: print("*  ", end="")
		print()
		

	#print(sum)
	return sum
