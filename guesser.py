import sys, ast


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
	+ odd_100010[x] + odd_1000100[x] + odd_1000010[x] + odd_1000001[x]
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
	

	while sum != expected:#[:-8]:
		if debug:
			print()
			print(sum)
			print(expected)
		for x in range(ignore,len(in_data*4)):
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
		for c in in_data: 	print(chr(c),end=" ")
		print()
	return in_data



'''
startup3 = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6, 2, 7, 3, 4, 2, 7, 3, 5, 3, 4, 4, 2, 3, 4, 0, 7, 0, 7, 3, 2, 5, 4, 5, 0, 5, 0, 0, 6, 2, 6, 2, 3, 2, 3, 5, 4, 2, 4, 6, 1, 7, 3, 1, 1, 5, 5, 1, 6, 1, 7, 6, 1, 1, 4, 1, 1, 6, 7, 7, 3, 5, 2, 7, 7, 7, 1, 2, 5, 2, 7, 2, 4]#, 0, 0]
Z =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6, 0, 6, 7, 3, 6, 3, 5, 1, 1, 6, 1, 1, 3, 3, 5, 5, 0, 7, 3, 2, 5, 4, 3, 5, 7, 0, 3, 6, 4, 0, 7, 3, 0, 4, 1, 4, 4, 2, 7, 4, 6, 2, 0, 2, 0, 7, 6, 6, 1, 6, 4, 1, 3, 1, 4, 4, 0, 7, 7, 3, 5, 2, 7, 7, 5, 4, 4, 3, 6, 4, 0, 0]#, 0, 0] #, 3, 0, 0, 1] Found: [0, 0, 0, 0, 0, 0, 0, 0, 51, 51, 13, 0, 0, 48, 52, 176, 51, 69, 48, 52, 149, 0, 0, 0, 129, 170]

#                                                                                |                         |          |           |            |           |          |
Z =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 7, 3, 6, 3, 5, 1, 1, 6, 1, 1, 3, 3, 5, 5, 0, 7, 3, 2, 5, 4, 3, 5, 7, 0, 3, 6, 4, 0, 7, 3, 0, 4, 1, 4, 4, 2, 7, 4, 6, 2, 0, 2, 0, 7, 6, 6, 1, 6, 4, 1, 3, 1, 4, 4, 0, 7, 7, 3, 5, 2, 7, 7, 5, 4, 4, 3, 6, 4, 0, 0]#, 0, 0] #, 3, 0, 0, 1] Found: [0, 0, 0, 0, 0, 128, 135, 0, 51, 51, 13, 0, 0, 48, 52, 176, 51, 69, 48, 52, 149, 0, 0, 0, 129, 170]
'''

'''
#          |           |           |           |           |           |           |           |           |           |           |           |           |           |
startup3 = [5, 4, 5, 0, 5, 0, 0, 6, 2, 6, 2, 3, 2, 3, 5, 4, 2, 4, 6, 1, 7, 3, 1, 1, 5, 5, 1, 6, 1, 7, 6, 1, 1, 4, 1, 1, 6, 7, 7, 3, 5, 2, 7, 7, 7, 1, 2, 5, 2, 7, 2, 4]#, 0, 0]
Z =        [5, 4, 3, 5, 7, 0, 3, 6, 4, 0, 7, 3, 0, 4, 1, 4, 4, 2, 7, 4, 6, 2, 0, 2, 0, 7, 6, 6, 1, 6, 4, 1, 3, 1, 4, 4, 0, 7, 7, 3, 5, 2, 7, 7, 5, 4, 4, 3, 6, 4, 0, 0]#, 0, 0] #, 3, 0, 0, 1]
startup3 = [7, 1, 2, 5, 2, 7, 2, 4]
Z =        [5, 4, 4, 3, 6, 4, 0, 0]


startup3 = [7, 1, 2, 5, 2, 7, 2, 4]

Z =        [5, 6, 5, 5, 4, 4, 7, 2]#, 0, 0]  # Found: [45, 40]
Z=         [1, 0, 2, 2, 4, 6, 0, 3]#, 2, 4]#+2 Found: [155, 32]

zeros_symbols = Z.copy()

init = len(startup3)//4 * [0]

delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in zeros_symbols]   # 001 010 101 110 
delta_2 = [(x*2+3)%8 for x in zeros_symbols]
delta_6 = [1 + 6 * (x & 1) for x in zeros_symbols]


print(len(zeros_symbols),len(startup3),len(init)*4)

solution = solver(init, startup3, debug=True, ignore=0)#, print_error=False)

sys.exit()
'''

if 0:
	print("solve for 2 mystery bytes after the confirmed header 6 bytes")
	#Found: [0, 0, 0, 0, 0, 128, 135, 0]
	#0x0 0x0 0x0 0x0 0x0 0x80 0x87 0x0 
	Z =        [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	zeros_symbols = Z.copy()
	actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6]
	delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in Z]   # 001 010 101 110 
	delta_2 = [(x*2+3)%8 for x in Z]
	delta_6 = [1 + 6 * (x & 1) for x in Z]
	solution = solver([0,0,0,0,0,0,0,0], actual, debug=True, ignore=0)#, print_error=False)
	print("\n\n\n")


if 1:
	Z =        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	zeros_symbols = Z.copy()


	#solve for 2 mystery bytes after the confirmed header 6 bytes
	actual        = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6]
	delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in Z]   # 001 010 101 110 
	delta_2 = [(x*2+3)%8 for x in Z]
	delta_6 = [1 + 6 * (x & 1) for x in Z]
	solution = solver([0,0,0,0,0,0,0,0], actual, debug=True, ignore=0)#, print_error=False)
	print("\n\n\n")
	
sys.exit()


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
sys.exit()
solution = solver([0,0,0,0,0,0,0,0]+[0]+[0]+[0], actual, debug=True, ignore=0)#, print_error=False)





sys.exit()
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
		
				
