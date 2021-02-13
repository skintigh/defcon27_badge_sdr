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
#alternate starts, trying to fix count vascilation
dzeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,0,0,0,0,0,0,0,0,0, 2,3,3,6, 7,7,0,1, 3,2,4,2, 2,2,7,5, 0,3,3,2,           5,4,3,5, 7,0,3,6, 4,0,7,3, 0,4,1,4, 4,2,7,4, 6,2,0,2, 0,7,6,6, 1,6,4,1, 3,1,4,4, 0,7,7,3, 5,2,7,7,  7,7,7,3, 0,3,1,6, 4,4,0,0, 0,0,0,0] #because out of range error
#dzeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,0,0,0,0,0,0,0,0,0,0, 2,3,3,6, 7,7,0,1, 3,2,4,2, 2,2,7,5, 0,3,3,2,           5,4,3,5, 7,0,3,6, 4,0,7,3, 0,4,1,4, 4,2,7,4, 6,2,0,2, 0,7,6,6, 1,6,4,1, 3,1,4,4, 0,7,7,3, 5,2,7,7,  7,7,7,3, 0,3,1,6, 4,4,0,0, 0,0,0,0] #because out of range error
#dzeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,4,0,4,0,0,0,0,0,0,0,0,0, 2,3,3,6, 7,7,0,1, 3,2,4,2, 2,2,7,5, 0,3,3,2,           5,4,3,5, 7,0,3,6, 4,0,7,3, 0,4,1,4, 4,2,7,4, 6,2,0,2, 0,7,6,6, 1,6,4,1, 3,1,4,4, 0,7,7,3, 5,2,7,7,  7,7,7,3, 0,3,1,6, 4,4,0,0, 0,0,0,0] #because out of range error
#dzeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,4,0,4,0,4,4,4,0,0,0,0,0, 2,3,3,6, 7,7,0,1, 3,2,4,2, 2,2,7,5, 0,3,3,2,           5,4,3,5, 7,0,3,6, 4,0,7,3, 0,4,1,4, 4,2,7,4, 6,2,0,2, 0,7,6,6, 1,6,4,1, 3,1,4,4, 0,7,7,3, 5,2,7,7,  7,7,7,3, 0,3,1,6, 4,4,0,0, 0,0,0,0] #because out of range error
#dzeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,4,0,4,0,4,4,4,4,0,0,0,0, 2,3,3,6, 7,7,0,1, 3,2,4,2, 2,2,7,5, 0,3,3,2,           5,4,3,5, 7,0,3,6, 4,0,7,3, 0,4,1,4, 4,2,7,4, 6,2,0,2, 0,7,6,6, 1,6,4,1, 3,1,4,4, 0,7,7,3, 5,2,7,7,  7,7,7,3, 0,3,1,6, 4,4,0,0, 0,0,0,0] #because out of range error
#dzeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,0,0,0,0,0,0,0,0,0,4, 2,3,3,6, 7,7,0,1, 3,2,4,2, 2,2,7,5, 0,3,3,2,           5,4,3,5, 7,0,3,6, 4,0,7,3, 0,4,1,4, 4,2,7,4, 6,2,0,2, 0,7,6,6, 1,6,4,1, 3,1,4,4, 0,7,7,3, 5,2,7,7,  7,7,7,3, 0,3,1,6, 4,4,0,0, 0,0,0,0] #because out of range error

ddelta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in dzeros_symbols]   # 001 010 101 110 
ddelta_2 = [(x*2+3)%8 for x in dzeros_symbols]
ddelta_6 = [1 + 6 * (x & 1) for x in dzeros_symbols]

def deltaf_0236(x): #x is prev value or zero value
	return 2 + 4*( x&1 ^ x>>1&1 )   #this mean 2->6 not 2???
def deltaf_1(x):
	return (x*2+3)%8
def deltaf_5(x):
	return 1 + 6 * (x & 1)

#this version allows expected, print_error
def compute(in_data_orig, expected, debug=False, ignore=0, print_error=True, zeros_symbols=dzeros_symbols, delta_1347=ddelta_1347, delta_2=ddelta_2, delta_6=ddelta_6,
odd_bits_fudge=[]):    #in_data_orig and expected are ONLY the values to be computed, ignore sets the pos in zero_symbols
	in_data = in_data_orig.copy() # prevent modification of data
	start = int(ignore*4)
	
	length = len(in_data)*4 #- ign ore*4
	in_data += [0,0]
	nibbles = [x>>(4*i)&0xf for x in in_data for i in range(0, 2)]
	#if debug: print("nibbles:      ", nibbles)
	nips = [x>>(2*i)&0x3 for x in nibbles for i in range(0, 2)]
	#if debug: print("nips:         ", nips,"\n")
	
	odd_bits = [x&1 for x in nips]
	#if debug: print("odd_bits:     ", odd_bits)
	even_bits = [(x&2)>>1 for x in nips]
	#if debug: print("even_bits:    ", even_bits)
	
	
	#print("even_bits    :", even_bits[:-8])
	#even_merge= [0,0,0,0,0,0]+[ 4*  even_bits[x-5] * even_bits[x-1] for x in range(6,length)]	
	#print("even_merge   :", even_merge)
	
	#if debug: print("\ndelta1347:    ", delta_1347[start:start+length])
	#print(length, start, len(zeros_symbols))
	#dd_single_d0 = [(delta_1347[x+start]*odd_bits[x-0])  for x in range(0, length)]  
	#if debug: print("odd_single_d0:", odd_single_d0)
		
	#dd_single_d2 = [(delta_1347[x+start]*odd_bits[x-2])  for x in range(0, length)]  
	#if debug: print("odd_single_d2:", odd_single_d2)
		
	#dd_single_d3 = [(delta_1347[x+start]*odd_bits[x-3])  for x in range(0, length)]  
	#if debug: print("odd_single_d3:", odd_single_d3)
		
	#dd_single_d6 = [(delta_1347[x+start]*odd_bits[x-6])  for x in range(0, length)]  
	#if debug: print("odd_single_d6:", odd_single_d6)
		
	
	#if debug: print("\ndelta2:       ", delta_2[start:start+length])
	#dd_single_d1 = [(delta_2[x+start]*odd_bits[x-1])  for x in range(0, length)]  
	#if debug: print("odd_single_d1:", odd_single_d1)
		
	
	#if debug: print("\ndelta6:       ", delta_6[start:start+length])
	#dd_single_d5 = [(delta_6[x+start]*odd_bits[x-5])  for x in range(0, length)]  
	#if debug: print("odd_single_d5:", odd_single_d5)
	
	even_single = [4*even_bits[x] for x in range(0, length)]
	#if debug: print("even_single  :", even_single)
	
	'''
	odd_11 = [4*((odd_bits[x]+odd_bits[x-1]+odd_bits[x-2]+odd_bits[x-3])==2 or (odd_bits[x]+odd_bits[x-1]+odd_bits[x-2]+odd_bits[x-3])==3) for x in range(0, length)]
	#odd_11 = [4*((((odd_bits[x]+odd_bits[x-1]+odd_bits[x-2]+odd_bits[x-3])==2) and (odd_bits[x-3:x+1] != [0,1,1,0])) or (odd_bits[x]+odd_bits[x-1]+odd_bits[x-2]+odd_bits[x-3])==3) for x in range(0, length)]
	
	odd_1001000 = [4 * (odd_bits[x-6]*odd_bits[x-3]) for x in range(0, length)]#1nn1nnn   was working but made no sense
	#odd_1001000 = [0,0,0,0,0,0] + [4 * (odd_bits[x-6]*odd_bits[x-3]) for x in range(6, length)]#1nn1nnn
	'''

	#odd_100010 = []
	'''
	#shit, this rule depends on how many igno res there are..........
	for x in range(0, length):
		#if   x%12==11: odd_100010.append(6 * (odd_bits[x-5]*odd_bits[x-1]))   #to fic count in byte 3 of count
		if x%12==9: odd_100010.append(6 * (odd_bits[x-5]*odd_bits[x-1]))  #adds 8    #fix byte 2 in capture #8, maybe others
		elif x%12==11: odd_100010.append(6 * (odd_bits[x-5]*odd_bits[x-1]))   #to fic count in byte 3 of count
		elif x%4==0: odd_100010.append(2 * (odd_bits[x-5]*odd_bits[x-1]))  #adds 2
		elif x%4==1: odd_100010.append(2 * (odd_bits[x-5]*odd_bits[x-1]))  #adds 8    #was 6 must be 2 for byte 1 in the odd count in capture #8
		elif x%4==2: odd_100010.append(6 * (odd_bits[x-5]*odd_bits[x-1]))  #adds 32
		elif x%4==3: odd_100010.append(2 * (odd_bits[x-5]*odd_bits[x-1]))  #adds 128 6 6 2 6 used to work   2662 should equal merge rule 0,3
	'''

	'''
	for x in range(0, length):
		if x%1 in [8,9]: odd_100010.append( ((4 + delta_1347[x+1+start])%8) * (odd_bits[x-5]*odd_bits[x-1]) ) #8 is a guess   wish i wrote down the reason for this rule, like a specific test...
		#if x in [8,9,25,26,27,28,29,32]:odd_100010.append( ((4 + delta_1347[x+1+start])%8) * (odd_bits[x-5]*odd_bits[x-1]) ) 
		#if x in [9,25,26,27,28,29,32, 35,36,38,39,40,42,46,47,50,51,52]:odd_100010.append( ((4 + delta_1347[x+1+start])%8) * (odd_bits[x-5]*odd_bits[x-1]) )  #nope, nust be related to lots of odd 1s
		else: odd_100010.append( (delta_1347[x+1+start]) * (odd_bits[x-5]*odd_bits[x-1]) )

		#else: odd_100010.append(0)
	'''

	#if x%4==0: odd_100010 = [6 * (odd_bits[x-5]*odd_bits[x-1]) for x in range(0, length)]
	#if x%4==3: odd_100010 = [2 * (odd_bits[x-5]*odd_bits[x-1]) for x in range(0, length)]
	#if x%4==1: odd_100010 = [2 * (odd_bits[x-5]*odd_bits[x-1]) for x in range(0, length)]
	#if x%4==2: odd_100010 = [2 * (odd_bits[x-5]*odd_bits[x-1]) for x in range(0, length)]
	'''
	odd_1000100 = [4 * (odd_bits[x-6]*odd_bits[x-2]) for x in range(0, length)] #was working but makes no sense
	#odd_1000100 = [0,0,0,0,0,0] + [4 * (odd_bits[x-6]*odd_bits[x-2]) for x in range(6, length)] #was working but makes no sense

	odd_1000010 = [4 * (odd_bits[x-6]*odd_bits[x-1]) for x in range(0, length)]
	odd_1000001 = [4 * (odd_bits[x-6]*odd_bits[x-0]) for x in range(0, length)]
	'''
	#new rule to explain disparity with 0xd*

	
	'''
	odd_111110 = [4 * (odd_bits[x-5]*odd_bits[x-4]*odd_bits[x-3]*odd_bits[x-2]*odd_bits[x-1]) for x in range(0, length)]
	'''
	'''
	diff = [((odd_single_d0[x] + odd_single_d1[x] + odd_single_d2[x] + odd_single_d3[x] 
	+ odd_single_d5[x] + odd_single_d6[x] + even_single[x] #+ odd_11[x] + odd_1001000[x] 
	+ odd_100010[x] #+ odd_1000100[x] + odd_1000010[x] + odd_1000001[x] + odd_111110[x]#+ even_10001000[x]#+ odd_merge[x] 
	)%8) for x in range(0, length)]
	'''
	

	'''
	even_1xxx1= [4 * (even_bits[x-4]*even_bits[x]) for x in range(0, length)]
	even_10001x= [4 * (even_bits[x-5]*even_bits[x-1]) for x in range(0, length)]
	even_10001000x = [4 * (even_bits[x-8]*even_bits[x-4]) for x in range(0, length)]
	even_01xxxxx = [4 * (even_bits[x-6:x-4] == [0,1]) for x in range(0,length)]
	even_1xxxx = [4 * (even_bits[x-4]) for x in range(0, length)]
	'''


	'''
	try:
		sum = [(zeros_symbols[x+start] - diff[x] + 8) % 8 for x in range(0, length)]
	except:
		print("ERROR compute() crashed")
		print("x =",x)
		print("length =", length)
		print("zeros_symbols:", zeros_symbols, len(zeros_symbols))
		print("diff         :", diff, len(diff))
		sys.exit(1)
	'''	

	'''
	odd_11 = [4*((odd_bits[x]+odd_bits[x-1]+odd_bits[x-2]+odd_bits[x-3])==2 or (odd_bits[x]+odd_bits[x-1]+odd_bits[x-2]+odd_bits[x-3])==3) for x in range(0, length)]
	odd_1001000 = [4 * (odd_bits[x-6]*odd_bits[x-3]) for x in range(0, length)]#1nn1nnn   was working but made no sense
	odd_1000100 = [4 * (odd_bits[x-6]*odd_bits[x-2]) for x in range(0, length)] #was working but makes no sense
	#odd_1000100 = [0,0,0,0,0,0] + [4 * (odd_bits[x-6]*odd_bits[x-2]) for x in range(6, length)] #was working but makes no sense
	odd_1000010 = [4 * (odd_bits[x-6]*odd_bits[x-1]) for x in range(0, length)]
	odd_1000001 = [4 * (odd_bits[x-6]*odd_bits[x-0]) for x in range(0, length)]
	odd_111110 = [4 * (odd_bits[x-5]*odd_bits[x-4]*odd_bits[x-3]*odd_bits[x-2]*odd_bits[x-1]) for x in range(0, length)]
	'''

	odd_011x = [4 * (odd_bits[x-3:x] == [0,1,1]) for x in range(0, length)]
	#odd_011xxxxx = [4 * (odd_bits[x-7:x-4] == [0,1,1]) for x in range(0, length)]


	odd_bits+=odd_bits_fudge

	odd_11xxxxx = [4 * (odd_bits[x-6:x-4] == [1,1]) for x in range(0, length)]

	odd_1xxxx1x = [4 * (odd_bits[x-6] * odd_bits[x-1]) for x in range(0, length)]
	#odd_1011 =  [4 * (odd_bits[x-3:x+1] == [1,0,1,1]) for x in range(0, length)]
	odd_101x =  [4 * (odd_bits[x-3:x] == [1,0,1]) for x in range(0, length)]

	newtotal = []	
	for x in range(0,length):
		d = 7*[0]
		prevz = [zeros_symbols[start+x]] + [0]*7
		for y in range(0,7):#min(x,6)+1):
			if y in [0,2,3,6]:
				if y <= x:
					d[y] = deltaf_0236(prevz[y]) * odd_bits[x-y]
				prevz[y+1] = (prevz[y] + d[y]) % 8   #could skip this for 7=6
			if y == 1:
				if y <= x:
					d[y] = deltaf_1(prevz[y]) * odd_bits[x-y]
				prevz[y+1] = (prevz[y] + d[y]) % 8   #could skip this for 7=6
			if y == 5:
				if y <= x:
					d[y] = deltaf_5(prevz[y]) * odd_bits[x-y]
				prevz[y+1] = (prevz[y] + d[y]) % 8   #could skip this for 7=6
			if y == 4:
				prevz[y+1] = prevz[y]

		#if x>=6 and even_bits[x-6:x-4] == [0,1]: temp = 4
		#else: temp=0
		newtotal.append( ( prevz[0]-d[0]-d[1]-d[2]-d[3]-d[4]-d[5]-d[6] + 4*even_bits[x] 
		+ odd_011x[x] + odd_11xxxxx[x] + odd_1xxxx1x[x] + odd_101x[x]
		)%8 )  #could remove d[4]
		'''
		print("prevz", prevz)
		print("delta", d)
		print()
		if x > 6:
			import sys
			sys.exit()
		'''

	error =  newtotal != expected

	if debug or (error and print_error):
		print("compute() debug:")
		print("zeros_symbols:", zeros_symbols[start:start+length])
		#print("delta_1347:   ", delta_1347[start:])
		#print("delta_2:      ", delta_2[start:])
		#print("delta_6:      ", delta_6[start:])
		print("bytes        :", in_data)
		print("nibbles      : [", end='')
		for x in nibbles[0:-4]:
			print("%x,    "%x,end='')
		print('\b\b]')
		print("nips         :", nips[:-8],'\n')
		print("odd_bits     :", odd_bits[:-8])
		#print("               "+ "|           "*17)
		print("even_bits    :", even_bits[:-8])
		print("even_single  :", even_single)
		print("               "+ "|           "*(length//4+1))
		print("odd_011x     :", odd_011x)		
		print("odd_11xxxxx  :", odd_11xxxxx)
		print("odd_1xxxx1x  :", odd_1xxxx1x)
		print("odd_101x     :", odd_101x)		

		if not print_error:
			print("newtotal     :", newtotal)		
			print("expected     :", expected)
			print()
		
	if error and print_error:
		print("newtotal     :", newtotal)		
		print("expected     :", expected)
		print("                ", end="")
		for x in range(0, length - 8):#len(expected)): #length):   #expected can be shorter, sometimes...? and newtotal can be shorter???
			if newtotal[x] == expected[x]: print("   ",end="")
			else: print("*  ", end="")
		print()
	return newtotal







if __name__ == "__main__":   #only run if this file is run as main script
	if 1:
		filename = "temp3.txt"
		print("Using {}\n".format(filename))	

		#odd_bits_fudge = [1,0,0,0]
		odd_bits_fudge = []

		with open(filename, "r") as infile:					
			line = infile.readline()
			count = 0
			while line:
				symbols =  [int(n) for n in line.split(' ')[0:-2]] #drop the count at end, 
				'''
				expected = [0,0,0,0,8] +  [0xaa]*4 + [0xff]*4 + [0,0,0]
				expected = [0,0,0,0,8] +  [0x55]*4 + [0xff]*4 + [0,0,0]
				expected = [0,0,0,0,8] +  [0x00, 0x55]*2 + [0xff]*4 + [0,0,0]
				expected = [0,0,0,0,8] +  [0,0x55,0,0,0,0,0,0] + [0,0,0,0] + [0,0,0]
				expected = [0,0,0,0,8] +  [0x21,0x43,0x65,0x87,0xff,0xff,0xff,0xff] + [0,0,0,0] + [0,0,0]
				expected = [0,0,0,0,8] +  [0x12,0x34,0x56,0x78,0xff,0xff,0xff,0xff] + [0,0,0,0] + [0,0,0]
				expected = [0,0,0,0,8] +  [0x78,0x9a,0xbc,0xde,0xff,0xff,0xff,0xff] + [0,0,0,0] + [0,0,0]
				#expected = [0,0,0,0,8] +  [3,5,0,0,0,0,0,0] + [0,0,0,0] + [0,0,0]
				'''
				#temp3.txt
				expected = [(243+2*count)%256, 105+(243+2*count)//256, 25, 0, 8 ]+  [0x78,0x9a,0xbc,0xde,0xff,0xff,0xff,0xff] + [0,0,0,0] + [0,0,0]   #digit 2 might be 99 not 105?, 153 is prob 11
				#temp7.txt
				#expected = [(62+2*count)%256, 31+(63+2*count)//256, 30, 0, 8 ]+  [0x00,0x11,0xa6,0x99,0xff,0xff,0xff,0xff] + [0,0,0,0] + [0,0,0]   #digit 2 might be 99 not 105?, 153 is prob 11
				
				#solution = compute(expected, symbols, debug=False, ignore=8, print_error=False, odd_bits_fudge=odd_bits_fudge)
				solution = compute([128,135,0]+expected, [0,0,4,4, 2,7,7,4, 6,7,5,6]+symbols, debug=False, ignore=8-3, print_error=False, odd_bits_fudge=odd_bits_fudge)
				
				#print(expected)
				line = infile.readline()		
				#if solution[0:48] != symbols[0:48]: 
				if solution[12:48+12] != symbols[0:48]: 					
					#print(solution[0:48])
					#print(symbols[0:48])
					solution = compute(expected, symbols, debug=False, ignore=8, print_error=True, odd_bits_fudge=odd_bits_fudge)
					#if count: print(odd_bits_fudge, count)
					from guesser import solver
					#solution = solver(expected, symbols, debug=False, ignore=8, print_error=True)
					solution = solver([0]*16, symbols, debug=False, ignore=8, print_error=False, print_result=False)
					print(solution)
					break
				count += 1
				if count == 3881: count+=1 #skipped packet in temp3.txt
			print("Count was", count,"successes")

	#test bits_fudge
	if 0:
		filename = "temp3.txt"
		print("Using {}\n".format(filename))	

		for i in range(0,256):
			bit_str="{0:08b}".format(i)
			odd_bits_fudge = [int(b) for b in bit_str]
			#print(odd_bits_fudge, end=" ")

			with open(filename, "r") as infile:					
				line = infile.readline()
				count = 0
				while line:
					symbols =  [int(n) for n in line.split(' ')[0:-2]] #drop the count at end, 
					'''
					expected = [0,0,0,0,8] +  [0xaa]*4 + [0xff]*4 + [0,0,0]
					expected = [0,0,0,0,8] +  [0x55]*4 + [0xff]*4 + [0,0,0]
					expected = [0,0,0,0,8] +  [0x00, 0x55]*2 + [0xff]*4 + [0,0,0]
					expected = [0,0,0,0,8] +  [0,0x55,0,0,0,0,0,0] + [0,0,0,0] + [0,0,0]
					expected = [0,0,0,0,8] +  [0x21,0x43,0x65,0x87,0xff,0xff,0xff,0xff] + [0,0,0,0] + [0,0,0]
					expected = [0,0,0,0,8] +  [0x12,0x34,0x56,0x78,0xff,0xff,0xff,0xff] + [0,0,0,0] + [0,0,0]
					expected = [0,0,0,0,8] +  [0x78,0x9a,0xbc,0xde,0xff,0xff,0xff,0xff] + [0,0,0,0] + [0,0,0]
					#expected = [0,0,0,0,8] +  [3,5,0,0,0,0,0,0] + [0,0,0,0] + [0,0,0]
					'''
					expected = [(243+2*count)%256, 105+(243+2*count)//256, 25, 0, 8 ]+  [0x78,0x9a,0xbc,0xde,0xff,0xff,0xff,0xff] + [0,0,0,0] + [0,0,0]   #digit 2 might be 99 not 105?, 153 is prob 11
					solution = compute(expected, symbols, debug=False, ignore=8, print_error=False, odd_bits_fudge=odd_bits_fudge)
					#print(expected)
					line = infile.readline()		
					if solution[0:48] != symbols[0:48]: 
						#solution = compute(expected, symbols, debug=False, ignore=8, print_error=True)
						#print("Count was", count,"successes")
						#print(count)
						if count: print(odd_bits_fudge, count)
						break
					count += 1
					#if count == 17: break

	if 0:
		filename = "temp5.txt"
		with open(filename, "r") as infile:	
			print("Using {}".format(filename))	
			line = infile.readline()
			count = 0
			while line:
				symbols =  [int(n) for n in line.split(' ')[0:-2]] #drop the count at end, 
				expected = [(165+2*count)%256, 34+(165+2*count)//256, 29, 0, 8 ]+  [0,0xf3,0x69,0x09,0,0,0,0] + [0,0,0,0] + [0,0,0]
				solution = compute(expected, symbols, debug=False, ignore=8, print_error=True)
				#print (solution)
				line = infile.readline()
				count += 1
				#if count == 2: break
	if 0:
		line = "114 219   4   0   8 255 255  95 215  93 221  95  95   0   0   0 "
		in_data_orig = [int(n) for n in line.split()]
		in_data_orig=[0x80,0xa7,0xa2,   114, 219 ,  4 ,  0,   8, 255, 255, 255, 255, 255, 255, 255, 255,]
		print (in_data_orig)
		#      |       |       |       |       |       |       |       |       |       |       |       |       |       |       |       |       |       
		line = "6 3 5 5 2 2 6 7 5 1 1 3 1 4 0 7 0 7 3 2 3 7 6 2 4 4 5 4 6 2 1 5 2 6 7 6 6 0 1 6 4 0 2 0 2 1 4 4 7 4 6 7 3 4 3 1 5 5 7 3 5 2 7 7 3 5 4 0 0 1 2 7 6 0  266"
		expected = [0,0,4,4, 2,7,7,4, 6,7,5,6]+[int(n) for n in line.split(' ')[0:-2]]
		print(expected)
		compute(in_data_orig, expected[0:4*len(in_data_orig)], debug=False, ignore=8-3, print_error=True)

		line = "114 219   4   0   8 255 255  95 215  93 221  95  95   0   0   0 "
		in_data_orig = [int(n) for n in line.split()]
		in_data_orig=[114, 219 ,  4 ,  0,   8, 255, 255, 255, 255, 255, 255, 255, 255,]     
		#print (in_data_orig)
		line = "6 3 5 5 2 2 6 7 5 1 1 3 1 4 0 7 0 7 3 2 3 7 6 2 4 4 5 4 6 2 1 5 2 6 7 6 6 0 1 6 4 0 2 0 2 1 4 4 7 4 6 7 3 4 3 1 5 5 7 3 5 2 7 7 3 5 4 0 0 1 2 7 6 0  266"
		expected = [int(n) for n in line.split()[0:-2]]
		#print(expected)
		compute(in_data_orig, expected[0:4*len(in_data_orig)], debug=False, ignore=8, print_error=True)



		line = "   116 219   4   0   8 255 255  255 255  255 255  255  255 "
		in_data_orig = [0x80,0xa7,0xa2, ]+[int(n) for n in line.split()]
		line = "2 1 0 7 4 2 5 5 5 1 1 3 1 4 0 7 0 7 3 2 3 7 6 2 4 4 5 4 6 2 1 5 2 6 7 6 6 0 1 6 4 0 2 0 2 1 4 4 7 4 6 7 3 4 3 1 5 5 7 3 5 2 7 7 1 2 3 4 2 6 3 1 2 4  269"
		expected = [0,0,4,4, 2,7,7,4, 6,7,5,6]+[int(n) for n in line.split()[0:-2]]
		compute(in_data_orig, expected[0:4*len(in_data_orig)+12], debug=False, ignore=8-3, print_error=True)

		line = "116 219   4   0   8 255 255  95 215  93 221  95  95   0   0   0 "
		line = "116 219   4   0   8 255 255  255 255  255 255  255  255 "
		in_data_orig = [int(n) for n in line.split()]
		line = "2 1 0 7 4 2 5 5 5 1 1 3 1 4 0 7 0 7 3 2 3 7 6 2 4 4 5 4 6 2 1 5 2 6 7 6 6 0 1 6 4 0 2 0 2 1 4 4 7 4 6 7 3 4 3 1 5 5 7 3 5 2 7 7 1 2 3 4 2 6 3 1 2 4  269"
		expected = [int(n) for n in line.split()[0:-2]]
		compute(in_data_orig, expected[0:4*len(in_data_orig)], debug=False, ignore=8, print_error=True)



		line = "118 219   4   0   8 255 255  255 255  255 255  255  255 "
		in_data_orig = [0x80,0xa7,0xa2, ]+[int(n) for n in line.split()]
		line = "6 1 0 7 4 2 5 5 5 1 1 3 1 4 0 7 0 7 3 2 3 7 6 2 4 4 5 4 6 2 1 5 2 6 7 6 6 0 1 6 4 0 2 0 2 1 4 4 7 4 6 7 3 4 3 1 5 5 7 3 5 2 7 7 5 4 0 7 2 4 4 4 0 0  270"
		expected = [0,0,4,4, 2,7,7,4, 6,7,5,6]+[int(n) for n in line.split()[0:-2]]
		compute(in_data_orig, expected[0:4*len(in_data_orig)], debug=False, ignore=8-3, print_error=True)

		line = "118 219   4   0   8 255 255  255 255  255 255  255  255 "
		in_data_orig = [int(n) for n in line.split()]
		line = "6 1 0 7 4 2 5 5 5 1 1 3 1 4 0 7 0 7 3 2 3 7 6 2 4 4 5 4 6 2 1 5 2 6 7 6 6 0 1 6 4 0 2 0 2 1 4 4 7 4 6 7 3 4 3 1 5 5 7 3 5 2 7 7 5 4 0 7 2 4 4 4 0 0  270"
		expected = [int(n) for n in line.split()[0:-2]]
		compute(in_data_orig, expected[0:4*len(in_data_orig)], debug=False, ignore=8, print_error=True)



		line = "120 219   4   0   8 255 255  255 255  255 255  255  255 "
		in_data_orig = [0x80,0xa7,0xa2, ]+[int(n) for n in line.split()]
		line = "2 7 5 5 2 2 6 7 5 1 1 3 1 4 0 7 0 7 3 2 3 7 6 2 4 4 5 4 6 2 1 5 2 6 7 6 6 0 1 6 4 0 2 0 2 1 4 4 7 4 6 7 3 4 3 1 5 5 7 3 5 2 7 7 3 3 5 6 6 5 5 1 6 0  269"
		expected = [0,0,4,4, 2,7,7,4, 6,7,5,6]+[int(n) for n in line.split()[0:-2]]
		compute(in_data_orig, expected[0:4*len(in_data_orig)], debug=False, ignore=8-3, print_error=True)

		line = "120 219   4   0   8 255 255  255 255  255 255  255  255 "
		in_data_orig = [int(n) for n in line.split()]
		line = "2 7 5 5 2 2 6 7 5 1 1 3 1 4 0 7 0 7 3 2 3 7 6 2 4 4 5 4 6 2 1 5 2 6 7 6 6 0 1 6 4 0 2 0 2 1 4 4 7 4 6 7 3 4 3 1 5 5 7 3 5 2 7 7 3 3 5 6 6 5 5 1 6 0  269"
		expected = [int(n) for n in line.split()[0:-2]]
		compute(in_data_orig, expected[0:4*len(in_data_orig)], debug=False, ignore=8, print_error=True)

		'''
		6 3 5 5 2 2 6 7 5 1 1 3 1 4 0 7 0 7 3 2 3 7 6 2 4 4 5 4 6 2 1 5 2 6 7 6 6 0 1 6 4 0 2 0 2 1 4 4 7 4 6 7 3 4 3 1 5 5 7 3 5 2 7 7 3 5 4 0 0 1 2 7 6 0  266
		2 1 0 7 4 2 5 5 5 1 1 3 1 4 0 7 0 7 3 2 3 7 6 2 4 4 5 4 6 2 1 5 2 6 7 6 6 0 1 6 4 0 2 0 2 1 4 4 7 4 6 7 3 4 3 1 5 5 7 3 5 2 7 7 1 2 3 4 2 6 3 1 2 4  269
		6 1 0 7 4 2 5 5 5 1 1 3 1 4 0 7 0 7 3 2 3 7 6 2 4 4 5 4 6 2 1 5 2 6 7 6 6 0 1 6 4 0 2 0 2 1 4 4 7 4 6 7 3 4 3 1 5 5 7 3 5 2 7 7 5 4 0 7 2 4 4 4 0 0  270
		2 7 5 5 2 2 6 7 5 1 1 3 1 4 0 7 0 7 3 2 3 7 6 2 4 4 5 4 6 2 1 5 2 6 7 6 6 0 1 6 4 0 2 0 2 1 4 4 7 4 6 7 3 4 3 1 5 5 7 3 5 2 7 7 3 3 5 6 6 5 5 1 6 0  269


		Found:        114 219   4   0   8 255 255  95 215  93 221  95  95   0   0   0 
		Hex:          x72 xdb x04 x00 x08 xff xff x5f xd7 x5d xdd x5f x5f x00 x00 x00 
		ASCII:         r   ?   ?   ?   ?   ?   ?   _   ?   ]   ?   _   _   ?   ?   ?   
		solver results:
		Found:        116 219   4   0   8 255 255  95 215  93 221  95  95   0   0   0 
		Hex:          x74 xdb x04 x00 x08 xff xff x5f xd7 x5d xdd x5f x5f x00 x00 x00 
		ASCII:         t   ?   ?   ?   ?   ?   ?   _   ?   ]   ?   _   _   ?   ?   ?   
		solver results:
		Found:        118 219   4   0   8 255 255  95 215  93 221  95  95   0   0   0 
		Hex:          x76 xdb x04 x00 x08 xff xff x5f xd7 x5d xdd x5f x5f x00 x00 x00 
		ASCII:         v   ?   ?   ?   ?   ?   ?   _   ?   ]   ?   _   _   ?   ?   ?   
		solver results:
		Found:        120 219   4   0   8 255 255  95 215  93 221  95  95   0   0   0 
		Hex:          x78 xdb x04 x00 x08 xff xff x5f xd7 x5d xdd x5f x5f x00 x00 x00 
		ASCII:         x   ?   ?   ?   ?   ?   ?   _   ?   ]   ?   _   _   ?   ?   ?   


		'''
