###########################################################################################
#This program guesses data bits to match a known/given zero-state and an known output value


import sys, ast


from compute import compute

'''
#this version allows expected, print_error
def compute(in_data_orig, expected, debug=False, ignore=0, print_error=True):
	in_data = in_data_orig.copy() # prevent modification of data
	start = ignore*4
	
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
	for x in range(0, length):
		#if   x%12==11: odd_100010.append(6 * (odd_bits[x-5]*odd_bits[x-1]))   #to fic count in byte 3 of count
		if   x%16==11: odd_100010.append(6 * (odd_bits[x-5]*odd_bits[x-1]))   #to fic count in byte 3 of count
		elif x%4==0: odd_100010.append(2 * (odd_bits[x-5]*odd_bits[x-1]))
		elif x%4==1: odd_100010.append(6 * (odd_bits[x-5]*odd_bits[x-1]))  #32? 
		elif x%4==2: odd_100010.append(6 * (odd_bits[x-5]*odd_bits[x-1]))    
		elif x%4==3: odd_100010.append(2 * (odd_bits[x-5]*odd_bits[x-1]))  #6 6 2 6 used to work   2662 should equal merge rule 0,3
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
'''


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
		#print(ignore, L)
		for x in range(0,L):
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
		'''
		for c in in_data: 
			if c != 0x9e: print(chr(c),end=" ")   #printing 9e or 9e 6e kills python???
		print()
		for c in in_data: 		
			print(hex(c%16*16+c//16),end=" ")
		print()
		for c in in_data: 		
			print(chr(c%16*16+c//16),end=" ")
		'''	
	return in_data

if 0:
	#Z = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6,  2, 3, 3, 6,   7, 7, 0, 1,   3, 2,0, 0,  3,2,4,3 ,0,7,3,2,  	Z= [5,4,3,5,7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7,5,4,4,3, 7,7,7,7,0,1,0,0,0,0]
	#                      
	#Z = [2, 3, 3, 6,   7, 7, 0, 1,   3, 2, 4, 0,  3,2,4,3 ,0,7,3,2, ]

	#startup3 = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6,  2, 7, 3, 4,  2, 7, 3, 5,  3, 4, 4, 2,  3, 4, 0, 7,  0, 7, 3, 2,  	startup3 = [5, 4, 5, 0, 5, 0, 0, 6, 2, 6, 2, 3, 2, 3, 5, 4, 2, 4, 6, 1, 7, 3, 1, 1, 5, 5, 1, 6, 1, 7, 6, 1, 1, 4, 1, 1, 6, 7, 7, 3, 5, 2, 7, 7, 7, 1, 2, 5]#, 2, 7, 2, 4]#, 0, 0]

	# Found: [0, 0, 0, 0, 0, 0, 0, 0, 51, 51, 13, 0, 0, 48, 52, 176, 51, 69, 48, 52, 149, 0, 0, 0, 129, 170]
	# 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x33 0x33 0xd 0x0 0x0 0x30 0x34 0xb0 0x33 0x45 0x30 0x34 0x95 0x0 0x0 0x0 0x81 0xaa 
   # 3 3 \d   0 4 ° 3 E 0 4      ª  

	#                                                                                  |                        |          |           |            |           |          |

	# Found: [0, 0, 0, 0, 0, 128,| 135, 0,| 51, 51, 13, 0, 0, 48, 52, 176, 51, 69, 48, 52, 149, 0, 0, 0, 129, 170]
	# 0x0 0x0 0x0 0x0 0x0 0x80 0x87 0x0 | 0x33 0x33 0xd 0x0 0x0 0x30 0x34 0xb0 0x33 0x45 0x30 0x34 0x95 0x0 0x0 0x0 0x81 0xaa 
   #3 3 \d    0 4 ° 3 E 0 4      ª 
		
	#          |           |           |           |           |           |           |           |           |           |           |           |           |           |
	startup3 = [5, 4, 5, 0, 5, 0, 0, 6, 2, 6, 2, 3, 2, 3, 5, 4, 2, 4, 6, 1, 7, 3, 1, 1, 5, 5, 1, 6, 1, 7, 6, 1, 1, 4, 1, 1, 6, 7, 7, 3, 5, 2, 7, 7, 7, 1, 2, 5, 2, 7, 2, 4]#, 0, 0]
	Z =        [5, 4, 3, 5, 7, 0, 3, 6, 4, 0, 7, 3, 0, 4, 1, 4, 4, 2, 7, 4, 6, 2, 0, 2, 0, 7, 6, 6, 1, 6, 4, 1, 3, 1, 4, 4, 0, 7, 7, 3, 5, 2, 7, 7, 5, 4, 4, 3, 6, 4, 0, 0]#, 0, 0] #, 3, 0, 0, 1]
	#Found: [48, 52, 176, 51, 69, 48, 52, 149, 0, 0, 0, 129, 170]
	#0x30 0x34 0xb0 0x33 0x45 0x30 0x34 0x95 0x0 0x0 0x0 0x81 0xaa 
	#0 4 ° 3 E 0 4      ª 
	zeros_symbols = Z.copy()
	delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in zeros_symbols]   # 001 010 101 110 
	delta_2 = [(x*2+3)%8 for x in zeros_symbols]
	delta_6 = [1 + 6 * (x & 1) for x in zeros_symbols]
	solution = solver(len(startup3)//4*[0], startup3, debug=False, ignore=0)
	sys.exit()




before = [6,5,0,3, 4,4,4,7, 5,0,2,2, 3,1,6,0, 4,6,1,4]# ,3,1,5,7,0,3,6,4,0 7 3 0 4 1 4 4 2 7 4 6 2 0 2 0 7 6 6 1 6 4 1 5 2 3 4 4 7 5 1 1 2 5 5 1 0 4 4 6 5 1 5 6 0 3  146
after =  [2,3,3,6, 7,7,0,1, 3,2,0,2, 2,2,7,5, 2,6,1,4]  #,3,1,5,7,0,3,6,4,0 7 3 0 4 1 4 4 2 7 4 6 2 0 2 0 7 6 6 1 6 4 1 5 2 3 4 4 7 5 1 1 2 5 5 7 1 4 7 0 4 3 2 0 0 4  152	
t3=[6,5,0,3,4,0,0,5,0,6,4,2,4,3,6,0,4,6,1,4]#,5,3,1,5,7,0,3,6,4,0,7,3,0,4 1 4 4 2 7 4 6 2 0 2 0 7 6 6 1 6 4 1 5 2 3 4 4 7 5 1 1 2 5 5 5 2 5 2 4 5 6 7 2 4 1  43
t4=[2,3,3,6,7,3,6,0,7,7,1,4,4,3,6,0,4,6,1,4] #,5,3,1,5,7,0,3,6,4,0,7 3 0 4 1 4 4 2 7 4 6 2 0 2 0 7 6 6 1 6 4 1 5 2 3 4 4 7 5 1 1 2 5 5 1 0 4 4 2 5 1 1 6 0 3  95

t5=[2, 7, 5, 1, 2, 4, 5, 6, 6, 0, 4, 1, 2, 3, 6, 0]
t6=[2, 7, 5, 1, 0, 7, 0, 7, 6, 5, 1, 4, 4, 3, 6, 0]

if 0:  #mini tests
	Z = [2, 3, 3, 6,   7, 7, 0, 1,   3, 2, 0, 0]
	zeros_symbols = Z.copy()
	delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in zeros_symbols]   # 001 010 101 110 
	delta_2 = [(x*2+3)%8 for x in zeros_symbols]
	delta_6 = [1 + 6 * (x & 1) for x in zeros_symbols]

	#1277: [2, 3, 3, 6, 7, 7, 6, 0, 7, 7, 1, 4, 4, 3, 6, 0] [  0, 144, 127] [00000000, 10010000, 01111111]
	#should be 255?
	print(solver([0,0,0], [2, 3, 3, 6, 7, 7, 6, 0, 7, 7, 1, 4, 4, 3, 6, 0] , debug=False, ignore=0))

	sys.exit()
	#print(solver([0,0,0], [2, 3, 3, 6, 7, 7, 6, 6, 6, 5, 3, 4, 3, 1, 6, 0] , debug=False, ignore=0))
	print(solver([0,0,0], [6, 5, 0, 3, 4, 4, 0, 5, 0, 6, 4, 2, 4, 3, 6, 0] , debug=False, ignore=0))

	print(" was 	[254, 159, 255] last should be 127")
	sys.exit()
	print(solver([0,0,0], [2, 3, 1, 7, 5, 5, 6, 7, 5, 7, 1, 4, 4, 3, 6, 0] , debug=False, ignore=0))
	print("was [ 16,  16, 143] should be [ 16,  144, 143]  ")
	sys.exit()


	print(solver([0,0,0], [2, 3, 3, 6, 1, 0, 7, 5, 7, 6, 4, 1, 2, 3, 6, 0], debug=False, ignore=0))
	print("was [  0, 167, 175] should be [  0, 135, 175] ")
	sys.exit()

	print(solver([0,0,0], [2, 1, 2, 0, 3, 0, 0, 3, 1, 1, 5, 4, 2, 2, 7, 5], debug=False, ignore=0))
	print("was [  4,  39, 176] should be 4 7 127")
	sys.exit()

	solution1 = solver([0,0,0], before, debug=False, ignore=0)#, print_error=False, print_result=False)
	print(solution1) #Found: [254, 255, 119]
	solution2 = solver([0,0,0], after, debug=False, ignore=0, print_error=False)#, print_result=False)
	print(solution2)
	#sys.exit()

	solution3 = solver([0,0,0], t3, debug=False, ignore=0, print_error=False, print_result=False) 
	print(solution3)
	solution4 = solver([0,0,0], t4, debug=False, ignore=0, print_error=False, print_result=False)
	print(solution4)
	#sys.exit()

	solution5 = solver([0,0,0], t5, debug=False, ignore=0, print_error=False, print_result=False) 
	print(solution5) #[248, 143, 223] odd_100010   : [0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 2, 0]

	solution6 = solver([0,0,0], t6, debug=False, ignore=0, print_error=False, print_result=False) 
	print(solution6) #[248, 16, 255]  odd_100010   : [0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 6]

	sys.exit()

if 0:
	if 1:
		for x in range(0,8):
			for y in range(0,8):
				#Z = [2, 3, 3, 6,   7, 7, 0, 1,   3, 2, 2, 3,   2, 3, 6, x,  6, 7, 3, 2]   #0xc6 0xc6 0x36 0x*5 
				#Z = [2, 3, 3, 6,   7, 7, 0, 1,   3, 2, 2, 7,   2, 3, 6, x,  6, 7, 3, 2] #0xc6 0xc6 0xb6
				#Z = [2, 3, 3, 6,   7, 7, 0, 1,   3, 2, 4, 0]  #c6c6e6
				#Z = [2, 3, 3, 6,  7, 7, 0, 1,  3, 2, 6, 7] #0xc6 0xc6 0x96 
				#Z = [2, 3, 3, 6,  7, 7, 0, 1,  3, 2, 6, 5] #0xc6 0xc6 0xd6 	
				#Z = [2, 3, 3, 6,  7, 7, 0, 1,  3, 2, 4, 0] #0xc6 0xc6 0xe6		
				#Z = [2, 3, 3, 6,  7, 7, 0, 1,  3, 2, 0, 0] #0xc6 0xc6 0xc6	
				#Z = [2, 3, 3, 6,   7, 7, 0, 1,   3, 2, 0, 0,   3,2,4,1,  0+4*x, 1+4*y, 3, 2]
				Z = [2,3,3,6, 7,7,0,1, 3,2,x,y]# ,2,2,7,5]  #known 0
				#print("\n\n",Z)
				zeros_symbols = Z.copy()
				delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in zeros_symbols]   # 001 010 101 110 
				delta_2 = [(x*2+3)%8 for x in zeros_symbols]
				delta_6 = [1 + 6 * (x & 1) for x in zeros_symbols]
				solution1 = solver([0,0,0], before, debug=False, ignore=0, print_error=False, print_result=False)   #startup
				solution2 = solver([0,0,0], after, debug=False, ignore=0, print_error=False, print_result=False)   #startup
				solution3 = solver([0,0,0], t3, debug=False, ignore=0, print_error=False, print_result=False) 	  #startup
				solution4 = solver([0,0,0], t4, debug=False, ignore=0, print_error=False, print_result=False)   #startup
				if solution1 != "Impossible" and solution2 != "Impossible" and (solution1[2]+1 == solution2[2]):# and (solution3[2]+1 == solution4[2]):  
					print(Z)
					print(solution1)
					print(solution2)
					print(solution3)
					print(solution4)
					#if solution1[2]+1 == solution2[2]: print("!!!!!!!!!!!")
					print()
				#	for c in solution: 		
				#		print(chr(c%16*16+c//16),end=" ")
				#	print()
				#solution = solver([0,0,0], [2,3,3,6, 7,7,6,2, 2,7,4,3,3,3,5,5,2,6,1,4], debug=False, ignore=0, print_error=False)		#0,0x50,?
				#solution = solver([0,0,0], [4,0,0,6, 1,4,5,1, 4,3,1,2, 3,3,6,7, 0,3,3,2], debug=False, ignore=0, print_error=False)		#lowest count seen
		sys.exit()
	
	'''
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
	
if 1:
	Z = [2, 3, 3, 6,   7, 7, 0, 1,   3,2,4,0]

	Z = [4,4,4,0, 4,0,4,0, 2,4,6,0, 0,0,0,0, 6,4,2,0, 0,0,4,4, 2,7,7,4, 6,7,5,6,    2,3,3,6,   7,7,0,1,   3,2,4, 0,  3,2,4,3 ,0,7,3,2,  5,4,3,5,7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7,5,4,4,3, 7,7,7,7,0,1,0,0,0,0]


	zeros_symbols = Z.copy()
	delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in zeros_symbols]   # 001 010 101 110 
	delta_2 = [(x*2+3)%8 for x in zeros_symbols]
	delta_6 = [1 + 6 * (x & 1) for x in zeros_symbols]
	
	if 1:
		print("2 sanity checks")
		solution = solver([4,4], [2, 1, 2, 0, 5, 5, 6, 1], debug=False, ignore=8)#, print_error=False, print_result=False)
		print("Should be 4,4", solution)
		if solution == "Impossible": sys.exit(1)
		#solution = solver([0, 1, 235], [2, 3, 3, 6, 5, 6, 6, 3, 5, 0, 4, 4, 2, 1, 5, 5], debug=False, ignore=0, print_error=False)#, print_result=False)
		#print(solution)
		#sys.exit()	

	if 1:	
		#filename = "test_0s_20_70_147_symbols.txt" #Total errors: 61   new zero syms:  [*, *, 25-31-0] #0 impossibles, 5 major errors, 48 skips, 5 doubles
		#filename = "test_0s_20_50_147_symbols.txt" #10 impossibles, 5 major errors, 12 skips, 41 doubles


		#filename = "test_0s_20_70_147_symbols_2_missing_lots.txt"


		#filename = "test_0s_100_25_11_symbols_3.txt" #27 impossibles, 0 major errors, 3 skips, 44 doubles    imp counts: 51, 40, 38 38 37 37...
		#filename = "test_0s_50_40_11_symbols_3.txt" #1 impossibles, 1 major errors, 221 skips, 6 doubles     impossible had count 51
		#filename = "test_0s_100_40_11_symbols_3.txt" # 87157: 1 impossibles, 1 major errors, 229 skips, 6 doubles   more skips?!?!? oh, longer data file   [*,*,12-15]

		#filename = "test_0s_50_40_11_symbols_4.txt"  #  154866   5 impossibles, 2 major errors, 255 skips, 17 doubles

		filename = "test_0s_50_40_11_symbols_5.txt" #98184:  4 impossibles, 2 major errors, 236 skips, 35 doubles

		with open(filename, "r") as infile:	
			'''
			if 0:
				#print batches at transitions to help figure out math, print based on assumed count    obsolete
				num = 5+256*2
				x = -1
				#for x in range(0,55616+(1+num)*128*10000):
				while True:
					x+=1
					if line == '': print (x)
					line = infile.readline()
					if x < 55616-4*128: continue
					#if x < 24700: continue
					if (x-64)%(128*256) < 10:
					#if x<25100:
						try:
							symbols = [int(n) for n in line.split(' ')[0:20]]
						catch:
							print(line)
							sys.exit(1)
						solution = solver([0,0,0], symbols, debug=False, ignore=0, print_error=False, print_result=False)
						print("{:6}: {} [{:3}, {:3}, {:3}] [{:08b}, {:08b}, {:08b}]".format(x, symbols[0:16], solution[0], solution[1],solution[2], solution[0], solution[1],solution[2]))
					if (x-64)%(128*256) == 10: print()
				sys.exit()
			'''
			if 0:
				#print batches at transitions to help figure out math
				#num = 5+256*2
				p = False
				x = -1
				count = 0
				line = infile.readline()
				while line:
					x+=1
					if line[0:7] == '2 7 5 1':  #[248] - 6
						count = 8
						p = True
					#if line[0:15] == '2 7 5 1 2 4 3 5': #[248, 255] - [6,0]
					#	count = 8
					#	p = True
					#if line[0:7] == '2 3 3 6': count = 1  #[0, *]

					#if line[0:31] == '6 1 2 0 5 7 5 6 7 7 1 4 4 3 6 0':
					#	count = 256
					if count:
						symbols = [int(n) for n in line.split(' ')[0:20]]
						solution = solver([0,0,0], symbols, debug=False, ignore=0, print_error=False, print_result=False)
						print("{:6}: {} [{:3}, {:3}, {:3}] [{:08b}, {:08b}, {:08b}]".format(x, symbols[0:16], solution[0], solution[1],solution[2], solution[0], solution[1],solution[2]))
						count -= 1
						if not count and p: print()
					#if (x-64)%(128*256) == 10: print()
					line = infile.readline()
					if not x % 1000: input("Press any key to continue...")			

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
				print("\n#{} impossibles, {} major errors, {} skips, {} doubles".format(imps, majors, skips, dbls))


	#solution = solver([0,0,0,0], [6,1,2,2, 4,7,4,7, 3,4,4,2, 3,4,0,7, 0,7,3,2], debug=False, ignore=0)#, print_error=False)  #startup
	#solution = solver([0,0,0,0,0], [2,3,3,6,7,7,2,6,2,7,4,3,3,3,5,5,2,6,1,4], debug=False, ignore=0, print_error=False)		

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
		
				
