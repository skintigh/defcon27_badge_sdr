###########################################################################################
#This program guesses data bits to match a known/given zero-state and an known output value

import sys, ast
from compute import compute


def solver(in_data_orig, expected_orig, debug=False, ignore=0, print_error=False, print_result=False, default=True, zeros_symbols=False, delta_1347=False, delta_2=False, delta_6=False):  #in_data_orig and expected are ONLY the values to be computed, ignore sets the pos in zero_symbols
	in_data = in_data_orig.copy()# prevent modification of data
	expected = expected_orig.copy()#+8*[0]
	if debug and False:
		print("solver() debug:")
		print("in_data",in_data)
		print("len",len(in_data)*4)
		print("expected",expected)
		print("len",len(expected))


	if not default or zeros_symbols or delta_1347 or delta_2 or delta_6:
		assert(zeros_symbols and delta_1347 and delta_2 and delta_6)

	if default: sum = compute(in_data, expected+8*[0], debug, ignore, print_error)
	else: sum = compute(in_data, expected+8*[0], debug, ignore, print_error, zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)
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
				else: sum = compute(in_data, expected, debug, ignore, print_error,zeros_symbols=zeros_symbols, delta_1347=delta_1347, delta_2=delta_2, delta_6=delta_6)
				break	
		
	if print_result:
		print("solver results:")
		#print("Sum          :",sum)
		#print("Expected     :",expected[4*ignore:])
		print("Found:       ", in_data, end="")
		print("\nHex:          ", end="")
		for c in in_data: 	print(hex(c),end=" ")
		print("\nASCII:        ", end="")
		for c in in_data: 
			if c >= 0x80: print("?",end=" ")
			else: print(chr(c),end=" ")   #printing 9e or 9e 6e kills python???
		print("\nRev hex:      ", end="")
		for c in in_data: 		
			print(hex(c%16*16+c//16),end=" ")
		print("\nrev hex ASCII ", end="")
		for c in in_data:
			if c >= 0x80: print("?",end=" ")
			else: print(chr(c%16*16+c//16),end=" ")
		print()

	return in_data

solution = solver([4,4], [2, 1, 2, 0, 5, 5, 6, 1], debug=False, ignore=8)#, print_error=False, print_result=False)
if solution == "Impossible": 
	print("Failed sanity check")
	sys.exit(1)

solution = solver([0,0,0], [4,0,0,6, 1,4,5,1, 4,3,1,2, 3,3,6,7, 0,3,3,2], debug=False, ignore=8, print_error=False, print_result=False)		#lowest count seen  [45, 74, 197]   0x2d 0x4a 0xc5  - J ?
if solution == "Impossible": 
	print("Failed sanity check")
	sys.exit(1)

#test with a startup data packet.
#correct value is ?!?!?
if 0:
	#startup3 = [#4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6,  
	            #2, 7, 3, 4,  2, 7, 3, 5,  3, 4, 4, 2,  3, 4, 0, 7,  0, 7, 3, 2, 
	startup3 = [5, 4, 5, 0,  5, 0, 0, 6,  2, 6, 2, 3,  2, 3, 5, 4,  2, 4, 6, 1,  7, 3, 1, 1,  5, 5, 1, 6,  1, 7, 6, 1,  1, 4, 1, 1,  6, 7, 7, 3,  5, 2, 7, 7,  
	            ]

	solution = solver(len(startup3)//4*[0], startup3, ignore=8+5, debug=True)  #ignore preamble and first 5 bytes
	#0x30 0xb4 0xb0 0xb3 0x45 0x30 0x34 0x35 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 
	#0 ´ ° ³ E 0 4 5 


	startup3 = [4, 4, 4, 0, 4, 0, 4, 0, 2, 4, 6, 0, 0, 0, 0, 0, 6, 4, 2, 0, 0, 0, 4, 4, 2, 7, 7, 4, 6, 7, 5, 6,  
	            2, 7, 3, 4,  2, 7, 3, 5,  3, 4, 4, 2,  3, 4, 0, 7,  0, 7, 3, 2, 
	            5, 4, 5, 0,  5, 0, 0, 6,  2, 6, 2, 3,  2, 3, 5, 4,  2, 4, 6, 1,  7, 3, 1, 1,  5, 5, 1, 6,  1, 7, 6, 1,  1, 4, 1, 1,  6, 7, 7, 3,  5, 2, 7, 7,  
	            ]#7, 1, 2, 5]# 2, 7, 2, 4]#, 0, 0]
	#This test fails on symbol 16, probably because symbols 12-19 are guesses
	#solution = solver(len(startup3)//4*[0], startup3, ignore=8, debug=False)  #ignore preamble

	#old results
	# Found: [0, 0, 0, 0, 0, 0, 0, 0, 51, 51, 13, 0, 0, 48, 52, 176, 51, 69, 48, 52, 149, 0, 0, 0, 129, 170]
	# 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x33 0x33 0xd 0x0 0x0 0x30 0x34 0xb0 0x33 0x45 0x30 0x34 0x95 0x0 0x0 0x0 0x81 0xaa 
    # 3 3 \d   0 4 ° 3 E 0 4      ª  

#mini tests with sequential values
if 0:  
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
	#should assert coorect values
	'''
	[254, 255, 223]
	[0, 0, 224]
	[254, 151, 223]
	[0, 152, 223]
	[248, 143, 223]
	[248, 144, 223]
	'''

	solution3 = solver([0,0,0], t3, debug=False, ignore=8, print_error=False, print_result=False) 
	print(solution3)
	solution4 = solver([0,0,0], t4, debug=False, ignore=8, print_error=False, print_result=False)
	print(solution4)

	solution5 = solver([0,0,0], t5, debug=False, ignore=8, print_error=False, print_result=False) 
	print(solution5) #[248, 143, 223] odd_100010   : [0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 2, 0]
	solution6 = solver([0,0,0], t6, debug=False, ignore=8, print_error=False, print_result=False) 
	print(solution6) #[248, 16, 255]  odd_100010   : [0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 6]

#guess at byte 2 zero symbols
if 1:
	if 1:
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

#verify vs recorded counts
if 1:
	#filename = "test_0s_20_70_147_symbols.txt" #Total errors: 61   new zero syms:  [*, *, 25-31-0] #0 impossibles, 5 major errors, 48 skips, 5 doubles
	#bad filename = "test_0s_20_50_147_symbols.txt" #227698:  10 impossibles, 5 major errors, 12 skips, 41 doubles

	#filename = "test_0s_20_70_147_symbols_2_missing_lots.txt" #3371  0 impossibles, 357 major errors, 696 skips, 0 doubles

	#filename = "test_0s_100_25_11_symbols_3.txt" #27 impossibles, 0 major errors, 3 skips, 44 doubles    imp counts: 51, 40, 38 38 37 37...
	#filename = "test_0s_50_40_11_symbols_3.txt" #1 impossibles, 1 major errors, 221 skips, 6 doubles     impossible had count 51
	#filename = "test_0s_100_40_11_symbols_3.txt" # 87157: 1 impossibles, 1 major errors, 229 skips, 6 doubles   more skips?!?!? oh, longer data file   [*,*,12-15]

	#filename = "test_0s_50_40_11_symbols_4.txt"  #  154866   5 impossibles, 2 major errors, 255 skips, 17 doubles

	#filename = "test_0s_50_40_11_symbols_5.txt" #19789 total packets 1 impossibles, 1 major errors, 34 skips, 2 doubles

	filename = "test_0s_50_40_11_symbols_6.txt" #

	with open(filename, "r") as infile:	
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
					solution = solver([0,0,0], symbols, debug=False, ignore=8, print_error=False, print_result=False)
					print
					print("{:6}: {} [{:3}, {:3}, {:3}] [{:08b}, {:08b}, {:08b}]".format(x, symbols[0:16], solution[0], solution[1],solution[2], solution[0], solution[1],solution[2]))
					count -= 1
					if not count and p: print()
				#if (x-64)%(128*256) == 10: print()
				line = infile.readline()
				if not x % 1000: input("Press any key to continue...")			

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


	solution = solver([0,0,0,0], [6,1,2,2, 4,7,4,7, 3,4,4,2, 3,4,0,7, 0,7,3,2], debug=False, ignore=8)#, print_error=False)  #startup
	print(solution)
	solution = solver([0,0,0,0,0], [6,1,2,2, 4,7,4,7, 3,4,4,2, 3,4,0,7, 0,7,3,2], debug=False, ignore=8)#, print_error=False)  #startup
	print(solution)
	solution = solver([0,0,0,0,0], [2,3,3,6, 7,7,2,6, 2,7,4,3, 3,3,5,5, 2,6,1,4], debug=False, ignore=8, print_error=False)		
	print(solution)

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

sys.exit()

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
		
				
