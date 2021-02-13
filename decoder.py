import sys, ast
#from compute import compute
from compute_experimental import compute
HDR_LEN = 32
FTR_LEN = 14

#these are wrong now...
zeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6, 4,2,1,0,7,0,6,1,3,4,1,4,4,2,0,7,0,7,3,2, 5,4,3,5,7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7,5,4,4,3,6,4,0,0,0,0,3,0,0,1]

#delta_1347 = [2 + 4*((x==5)or(x==6)or(x==1)or(x==2)) for x in zeros]   # 001 010 101 110 
delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in zeros_symbols]   # 001 010 101 110 
#print("delta_1347")
#print(*delta_1347[32:-14]) #don't print 32 symbol header or last 14 symbols
expected_1347 = [2,6,6,2,2,2,6,6,2,2,6,2,2,6,2,2,2,2,2,6,6,2,2,6,2,2,2,6,2,2,2,2,2,2,6,2,2,6,2,2,6,6,2,6,2,2,6,6,6,6,2,6,2,6,2,2,2,2,2,2,6,6,2,2]
#print(*expected_1347)
print("Same =", delta_1347[HDR_LEN:-FTR_LEN]==expected_1347)

#delta_2 = [((x%4)*2+3)%8 for x in zeros]
delta_2 = [(x*2+3)%8 for x in zeros_symbols]
#print(*delta_2[32:-14]) #don't print 32 symbol header or last 14 symbols
#=mod(mod(AH81,4)*2+3,8)
expected_2 = [3,7,5,3,1,3,7,5,1,3,5,3,3,7,3,1,3,1,1,7,5,3,1,5,1,3,1,7,3,3,1,1,3,3,5,3,3,7,1,3,7,7,3,7,3,1,7,7,5,7,3,5,1,5,3,3,3,1,1,1,5,7,1,1]
#print(*expected_2)
print("Same =", delta_2[HDR_LEN:-FTR_LEN]==expected_2)


#delta_6 = [1 + 6*((x==1)or(x==3)or(x==5)or(x==7)) for x in zeros]
delta_6 = [1 + 6 * (x & 1) for x in zeros_symbols]
#print(*delta_6[32:-14])
expected_6 = [1,1,7,1,7,1,1,7,7,1,7,1,1,1,1,7,1,7,7,1,7,1,7,7,7,1,7,1,1,1,7,7,1,1,7,1,1,1,7,1,1,1,1,1,1,7,1,1,7,1,1,7,7,7,1,1,1,7,7,7,7,1,7,7]
#print(*expected_6)
print("Same =", delta_6[HDR_LEN:-FTR_LEN]==expected_6)
print()



def hammingwt(n):
	c = 0
	while n:
		 c += 1
		 n &= n - 1
	return c
	

'''
def compute(in_data_orig, expected, debug=False, ignore=0):
	in_data = in_data_orig.copy() # prevent modification of data
	start = HDR_LEN+5*4
	length = 20
	length = len(in_data)*4
	in_data += [0,0]
	nibbles = [x>>(4*i)&0xf for x in in_data for i in range(0, 2)]
	if debug: print("nibbles:      ", nibbles)
	nips = [x>>(2*i)&0x3 for x in nibbles for i in range(0, 2)]
	if debug: print("nips:         ", nips,"\n")
	
	odd_bits = [x&1 for x in nips]
	if debug: print("odd_bits:     ", odd_bits)
	even_bits = [(x&2)>>1 for x in nips]
	if debug: print("even_bits:    ", even_bits)
	
	
	
	if debug: print("\ndelta1347:    ", delta_1347[start:start+length])
	odd_single_d0 = [(delta_1347[x+start]*odd_bits[x-0])  for x in range(0, length)]  
	if debug: print("odd_single_d0:", odd_single_d0)
		
	odd_single_d2 = [(delta_1347[x+start]*odd_bits[x-2])  for x in range(0, length)]  
	if debug: print("odd_single_d2:", odd_single_d2)
		
	odd_single_d3 = [(delta_1347[x+start]*odd_bits[x-3])  for x in range(0, length)]  
	if debug: print("odd_single_d3:", odd_single_d3)
		
	odd_single_d6 = [(delta_1347[x+start]*odd_bits[x-6])  for x in range(0, length)]  
	if debug: print("odd_single_d6:", odd_single_d6)
		
	
	if debug: print("\ndelta2:       ", delta_2[start:start+length])
	odd_single_d1 = [(delta_2[x+start]*odd_bits[x-1])  for x in range(0, length)]  
	if debug: print("odd_single_d1:", odd_single_d1)
		
	
	if debug: print("\ndelta6:       ", delta_6[start:start+length])
	odd_single_d5 = [(delta_6[x+start]*odd_bits[x-5])  for x in range(0, length)]  
	if debug: print("odd_single_d5:", odd_single_d5)
	
	even_single = [4*even_bits[x] for x in range(0, length)]
	if debug: print("even_single  :", even_single)
	
	#temp = (odd_bits[x]+odd_bits[x-1]+odd_bits[x-2]+odd_bits[x-3])
	odd_11 = [4*((odd_bits[x]+odd_bits[x-1]+odd_bits[x-2]+odd_bits[x-3])==2 or (odd_bits[x]+odd_bits[x-1]+odd_bits[x-2]+odd_bits[x-3])==3) for x in range(0, length)]
	#odd_11 = [4*odd_bits[x]*odd_bits[x-1] for x in range(0, length)]
	#odd_11b = [4*odd_bits[x-1]*odd_bits[x-2] for x in range(0, length)]
	#odd_11c = [4*odd_bits[x-2]*odd_bits[x-3] for x in range(0, length)]
	
	#odd_1001000 = [4 * (odd_bits[x-6]*(~odd_bits[x-5])*(~odd_bits[x-4])*odd_bits[x-3]) for x in range(0, length)]
	
	odd_1001000 = [4 * (odd_bits[x-6]*odd_bits[x-3]) for x in range(0, length)]#1nn1nnn
	
	#odd_1001000 = [4 * (odd_bits[x-6]*odd_bits[x-3]) * ((odd_bits[x-5]+odd_bits[x-4])<2) for x in range(0, length)]#1nn1nnn
	
	#odd_1001000 = [4*( (odd_bits[x-6]+odd_bits[x-5]+odd_bits[x-4]+odd_bits[x-3])>=2 ) for x in range(0, length)]
	
	#odd_1111 = 
	
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
	
	sum = [(zeros_symbols[x+start] - diff[x] + 8) % 8 for x in range(0, length)]
	
	error =  sum[ignore:] != expected[ignore:]
	if error:
		print("Data mismatch")
	
	if debug or error:
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
		print("\nexpected     :", expected)
		print("                ", end="")
		print(ignore*"-  ", end="")
		for x in range(ignore,length):
			if sum[x] == expected[x]: print("   ",end="")
			else: print("*  ", end="")
		print()
		sys.exit(1)
	return sum
'''
###################################################################################



def main():
	#compute([0,0,0,0], data_symbols[0][1][0:16])

	'''
	print("test by hamming weight")
	for h in range(0,9): 
		print(h)
		for n in range(0,256):
			if hammingwt(n) == h:
				print(data_symbols[n][0])
				result = compute(data_symbols[n][0], data_symbols[n][1][0:length])
				#print(result[0:length])
				#print(data_symbols[n][1][0:length])
				print(result[0:length] == data_symbols[n][1][0:length])			
		print()
	'''

	if 1:
		with open("generated_data_byte_captures/data_0XYY.txt", 'r') as f:
			data_symbols = ast.literal_eval(f.read())
		print(len(data_symbols), "data records loaded")	
		length = 4 * (len(data_symbols[0][0]) +2)
		print("test in order")
		errors = tests = 0
		ignore = 2 #ignore first 2 symbols
		for n in range(0,len(data_symbols)):
			tests += 1
			#print(data_symbols[n][0])
			data_symbols[n][1][0] = (data_symbols[n][1][0]-1)%8 #fix errors in data
			data_symbols[n][1][1] = (data_symbols[n][1][1]+2)%8
			result = compute(data_symbols[n][0]+[0,0], data_symbols[n][1][0:length], ignore = 8+5)
			#print(result[0:length])
			#print(data_symbols[n][1][0:length])
			if not(result[ignore:length] == data_symbols[n][1][ignore:length]):
				print("Error on", data_symbols[n][0])
				errors += 1
		print(errors,"errors in", tests, "tests\n")


	if 1:
		print("loading data...")
		with open("generated_data_byte_captures/data_2bytes.txt", 'r') as f:
			data_symbols = ast.literal_eval(f.read())
		print(len(data_symbols), "data records loaded")
		length = 4 * (len(data_symbols[0][0]) +2)

		print("test in order")
		errors = tests = 0
		ignore = 2 #ignore first 2 symbols
		for n in range(0,len(data_symbols)):
			tests += 1
			#print(data_symbols[n][0])
			data_symbols[n][1][0] = 5 #fix errors in data
			data_symbols[n][1][1] = 4
			result = compute(data_symbols[n][0]+[0,0], data_symbols[n][1][0:length], ignore = 8+5)
			#print(result[0:length])
			#print(data_symbols[n][1][0:length])
			#if not(result[ignore:length] == data_symbols[n][1][ignore:length]):
			if not(result[0:length] == data_symbols[n][1][0:length]):
				print("Error on", n, data_symbols[n][0])
				errors += 1
				sys.exit()
		print(errors,"errors in", tests, "tests\n")



	print("Test", [0x50,0x60,0x70,0x80,0x90,0xa0,0xb0,0xc0])
	compute([0x50,0x60,0x70,0x80,0x90,0xa0,0xb0,0xc0], [5,4,1,6,0,0,5,7,4,0,3,4,0,2,3,7,1,4,5,5,0,4,4,5,6,7,4,3,3,0,4,0],ignore=13)#,4,3,2,4,7,5,7,3,5,2,7,7,5,2,7,0,6,6,7,5,2,4,6,1,7,0])

if __name__ == "__main__":
	main()																																																																																																												
