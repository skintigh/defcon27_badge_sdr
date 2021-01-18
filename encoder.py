import sys, ast

HDR_LEN = 32
FTR_LEN = 14

#zeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6, 4,2,1,0,7,0,6,1,3,4,1,4,4,2,0,7,0,7,3,2, 5,4,3,5,7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7,5,4,4,3,6,4,0,0,0,0,3,0,0,1]
#zeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6, 4,2,1,0,7,0,6,1,3,4,1,4,4,2,0,7,0,7,3,2,5,4,3,5,7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7,5,4,4,3, 7,7,7,7,0,1,0,0,0,0]

#guesses based on assuming startup is c6c6c6c6
#zeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6,  2, 3, 3, 6,   7, 7, 0, 1,   3, 2, 2, 7,  4,2,0,7 ,0,7,3,2,  5,4,3,5,7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7,5,4,4,3, 7,7,7,7,0,1,0,0,0,0]
#zeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6,  2, 3, 3, 6,   7, 7, 0, 1,   3, 2, 0, 0,  3,4,0,7 ,0,7,3,2,  5,4,3,5,7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7,5,4,4,3, 7,7,7,7,0,1,0,0,0,0]
#zeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6,  2, 3, 3, 6,   7, 7, 0, 1,   3, 2, 0, 0,  3,2,4,3 ,0,7,3,2,  5,4,3,5,7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7,5,4,4,3, 7,7,7,7,0,1,0,0,0,0]

#this taken from compute.py on 1/14/2021
zeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6, 2,3,3,6, 7,7,0,1, 3,2,4,2, 2,2,7,5, 0,3,3,2,           5,4,3,5, 7,0,3,6, 0,0,7,3, 0,4,1,0, 4,2,7,4, 6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7, 5,4,4,3, 7,7,7,7,0,1]

#zeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6,4,2,1,0,7,0,6,1,3,4,1,4,4,2,0,7,6,3,3,2,5,4,3,5,7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7,5,4,4,3, 7,7,7,7,6,6,7,0,0,0]
#zeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6,4,2,1,0,7,0,6,1,3,4,1,4,4,2,0,7,7,1,3,2,5,4,3,5,7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7,5,4,4,3, 7,7,7,7,6,6,7,0,0,0]
#zeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6,4,2,1,0,7,0,6,1,3,4,1,4,4,2,0,7,1,6,6,5,5,4,3,5,7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7,5,4,4,3, 7,7,7,7,6,6,7,0,0,0]
#                                                                                                                  *
#zeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6,4,2,1,0,7,0,6,1,3,4,1,4,4,2,0,7,0,7,3,2,5,4,3,5,7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7,5,4,4,3, 7,7,7,7,6,6,7,0,0,0]
#0:0 1:2(0 2 x) 2:2(8 10 x) 3:2(8 0732 10 4732) 4:2(2 1132 and 0 x132) 5:0 6:1 7(8 0332):1
#                                                                               |       |       |       |       |       |
#                                                                                                                  *
#zeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6,4,2,1,0,7,0,6,1,3,4,1,4,3,4,0,7,0,7,3,2,5,4,3,5,7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7,5,4,4,3, 7,7,7,7,6,6,7,0,0,0]
#0:0 1:2 2:2 3:2 4:2 5:0 6:1 7:1
#                                                                                                                  *
#zeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6,4,2,1,0,7,0,6,1,3,4,1,4,3,3,6,7,0,7,3,2,5,4,3,5,7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7,5,4,4,3, 7,7,7,7,6,6,7,0,0,0]
#same results
#                                                                                                                *
#zeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6,4,2,1,0,7,0,6,1,3,4,1,4,3,3,6,7,0,7,3,2,5,4,3,5,7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7,5,4,4,3, 7,7,7,7,6,6,7,0,0,0]
#no effect
#                                                                               |       |       |       |       |       |
#print(len(zeros_symbols))
#zeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6,4,2,1,0,7,7,6,0,3,4,1,4,3,3,6,7,0,7,3,2,5,4,3,5,7,0,3,6,4,0,7,3,0,4,1,4,4,2,7,4,6,2,0,2,0,7,6,6,1,6,4,1,3,1,4,4,0,7,7,3,5,2,7,7,5,4,4,3, 7,7,7,7,6,6,7,0,0,0]

#delta_1347 = [2 + 4*((x==5)or(x==6)or(x==1)or(x==2)) for x in zeros]   # 001 010 101 110 
delta_1347 = [2 + 4*( x&1 ^ x>>1&1 ) for x in zeros_symbols]   # 001 010 101 110 
#print("delta_1347")
#print(*delta_1347[32:-14]) #don't print 32 symbol header or last 14 symbols
expected_1347 = [2,6,6,2,2,2,6,6,2,2,6,2,2,6,2,2,2,2,2,6,6,2,2,6,2,2,2,6,2,2,2,2,2,2,6,2,2,6,2,2,6,6,2,6,2,2,6,6,6,6,2,6,2,6,2,2,2,2,2,2,6,6,2,2]
#print(*expected_1347)
#assert(delta_1347[HDR_LEN:-FTR_LEN]==expected_1347)

#delta_2 = [((x%4)*2+3)%8 for x in zeros]
delta_2 = [(x*2+3)%8 for x in zeros_symbols]
#print(*delta_2[32:-14]) #don't print 32 symbol header or last 14 symbols
#=mod(mod(AH81,4)*2+3,8)
expected_2 = [3,7,5,3,1,3,7,5,1,3,5,3,3,7,3,1,3,1,1,7,5,3,1,5,1,3,1,7,3,3,1,1,3,3,5,3,3,7,1,3,7,7,3,7,3,1,7,7,5,7,3,5,1,5,3,3,3,1,1,1,5,7,1,1]
#print(*expected_2)
#assert(delta_2[HDR_LEN:-FTR_LEN]==expected_2)


#delta_6 = [1 + 6*((x==1)or(x==3)or(x==5)or(x==7)) for x in zeros]
delta_6 = [1 + 6 * (x & 1) for x in zeros_symbols]
#print(*delta_6[32:-14])
expected_6 = [1,1,7,1,7,1,1,7,7,1,7,1,1,1,1,7,1,7,7,1,7,1,7,7,7,1,7,1,1,1,7,7,1,1,7,1,1,1,7,1,1,1,1,1,1,7,1,1,7,1,1,7,7,7,1,1,1,7,7,7,7,1,7,7]
#print(*expected_6)
#assert(delta_6[HDR_LEN:-FTR_LEN]==expected_6)




def hammingwt(n):
	c = 0
	while n:
		 c += 1
		 n &= n - 1
	return c
	

def compute(in_data_orig, skip=5, debug=False, ignore=0):
	in_data = in_data_orig.copy() # prevent modification of data
	start = HDR_LEN + skip*4 #skip header and first 5 bytes by default
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
	
	'''
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
	'''	
	return sum

###################################################################################



def main():
	print(compute([4,4],skip=0))
	print(compute([0,0,16],skip=0))
	print(compute([0,0,-16],skip=0))
	print(compute([0,0,-16-224],skip=0))
	print(compute([0,0,-48],skip=0))
	print(compute([0,0,-48-64-128],skip=0))
	print(compute([0,0,-33],skip=0))
	print(compute([0,0,-1],skip=0))	
	print(compute([0,0,1],skip=0))		
	'''
	for x in range(-150,-140):
		sum = compute([0,x], skip=0)
		print(x, sum)

	for x in range(0,256):
		sum = compute([ord('0'),ord('4'),0xb0,ord('3'),ord('E'),ord('0'),ord('4'),x], skip=5)
		print(x, hex(x), sum)		
		if sum[4*7:] == [1,7,6,1]: print ("^^^^^^^^^^^^^^^")
	'''
		
	#print("Test", [0x50,0x60,0x70,0x80,0x90,0xa0,0xb0,0xc0])
	#for x in range(0, 256):
		#sum = compute([0,0,0,0, 0,0,0,0,  0,0,0,0, 0,x])
		#print (sum)
	'''	
	print(compute([0,0,0,0, 0]))
	print(compute([1,0,0,0, 0]))
	print(compute([255,0,0,0, 0]))
	print(compute([255,0,256-20,0, 0]))
	print(compute([1,0,19,0, 0]))
	print(compute([0,0,0,0, 8]))   #8 -> 0332
	'''
	
	'''
	#find byte len patterns
	print("8 x732")
	for x in range(0,256):
		sum = compute([0,0,0, x,8])
		#print(x, sum, end=" ")  
		if sum[-3:] == [7,3,2]: 
			#print("*****")
			print(x, sum) 
		#else: print(sum[-4:])
		
	print()		
	
	print("10 x732")
	for x in range(0,256):
		sum = compute([0,0,0, x, 10])
		if sum[-3:] == [7,3,2]: 
			print(x, sum) 
		
	print()		

	print("8 x332")		
	for x in range(0,256):
		sum = compute([0,0,0, x,8])
		if sum[-3:] == [3,3,2]: 
			print(x, sum) 
		
	print()		

	print("2 x132")	
	for x in range(0,256):
		sum = compute([0,0,0, x,2])
		if sum[-3:] == [1,3,2]: 
			print(x, sum) 
			
	print()		
	
	print("0 x132")
	for x in range(0,256):
		sum = compute([0,0,0, x,0])
		if sum[-3:] == [1,3,2]: 
			print(x, sum) 
			
	print()
	
	for x in range(0,12):
		sum = compute([0,0,0, 0, x])
		print(x, sum)
	'''	

if __name__ == "__main__":
	main()
