from crc_list import crcs_10_ordered_by_symbol as crcs
import compute_experimental
import guesser

#crc 0 is at index 4035
#2955: [1, 0, 0]	00001
#2251: [21, 40, 10]	a2815
#203: [23, 40, 10]	a2817
#2070: [5, 136, 10]	a8805
#51 is crc for all 0s I think
zeros_symbols =   compute_experimental.dzeros_symbols[:4*24] + [int(c) for c in str(crcs[51])] + [0,0]

#data and count all 0s, using 3 preamble bytes
#packet length, crc segment (orig), crc index
known=[
[1,49,1583],   #make count 1,0,0 once made segment 118, using old compute, no preamble
[2, 107, 3432],
[4, 7, 225],
[7, 72, 2314],
[8, 17, 545],
[11, 91, 2920],

[12, 0, None],
[13, 38, None],  #adding 'B' changed segment to 91
[14, 121, None],   #adding a 'B' changed segment to 17
[16, 28, None],
[19, 83, None],
[21, 63, None],
[22, 101, None],
[23, 85, None],
[25, 45, None],
[26, 114, None],
[28, 15, None],
#[, , ],
]

if 1:
	for k in known:
		if k[2] and k[2] != []:
			print(k)
			length = k[0]
			crc_index = k[2]
			crc_str = crcs[crc_index]
			crc_symbols = [int(c) for c in str(crc_str)]

			data_bytes_in = [0x80,0x87,0] + [0,0,0,0,length,0,0,0,0,0,0,0,0,0,0,0]
			symbols = compute_experimental.compute(data_bytes_in, [0,0,0,0]*len(data_bytes_in), debug=False, ignore=8-3, print_error=False) + crc_symbols + [0,0]
			#data_bytes_out = guesser.solver([0]*(3+16+3), symbols, debug=False, ignore=5, print_error=False, print_result=False) #using orig crc table
			###data_bytes_out = guesser.solver([0]*(3+16+3), symbols, debug=False, ignore=5, print_error=False, print_result=False, zeros_symbols=zeros_symbols)
			data_bytes_out = guesser.solver([0]*(3+16+3), symbols, debug=False, ignore=5, print_error=False, print_result=False, default=False, zeros_symbols=zeros_symbols)
			print(data_bytes_out)
			#for c in data_bytes_out: print("{:02x}".format(c),end=" ")
			for c in range(0,22): 
				print("{:02x}".format(data_bytes_out[c]),end=" ")
				if c in [2,18]: print(end=" ")
			crc_value = data_bytes_out[-1]*65536 +data_bytes_out[-2]*256 + data_bytes_out[-3]
			print("\t{:05x}\n".format(crc_value))
			#print(data_bytes_out)




if 0: #print all CRC byte values
	print(compute_experimental.dzeros_symbols[:4*24])
	
	for i in range(0,len(crcs)):
		crc_symbols = [int(c) for c in str(crcs[i])] + [0, 0]
		#print(crc_symbols)
		solution = guesser.solver([0]*4, [5,2,7,7,]+crc_symbols, debug=False, ignore=8+16-1, print_error=False, print_result=False, default=False, zeros_symbols=zeros_symbols)
		#print(solution)
		crc_value = solution[-1]*65536 +solution[-2]*256 + solution[-3]
		print("{:4d}: {}\t{:05x}".format(i,solution[1:],crc_value), end="")
		if not crc_value: print(" ##########")
		else: print()

'''
data_bytes = [1,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0] #segment 118 0x0000000000014F00 once, failed 4 times after
data_bytes = [1,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0] #segment 16! 0x0000000000004F00, failed, reboot and fail, fail
data_bytes = [10,10,10,0,2,0,0,0,0,0,0,0,0,0,0,0] #segemnt 7    0x0000A30000014F00 3x
data_bytes = [10,10,10,0,3,0,0,0,0,0,0,0,0,0,0,0] #fail, seg 54 0x0000000000014F00 2x
data_bytes = [10,10,10,0,4,0,0,0,0,0,0,0,0,0,0,0] #0x0000000000014F00 107   worked twice! 3x!
data_bytes = [12,10,10,0,4,0,0,0,0,0,0,0,0,0,0,0] #seg 68 0x0000000000014F00		
data_bytes = [10,10,10,0,8,0,0,0,0,0,0,0,0,0,0,0] #0x0000000000000000 segment 121
data_bytes = [10,10,10,0,11,0,0,0,0,0,0,0,0,0,0,0] # seg 38 0x0000000000000000
data_bytes = [0,0,8,0,2,0,0,0,0,0,0,0,0,0,0,0] #seg 23 B d0 d0 d0 d0 E -- length = 4   0x0000C30000014F00
data_bytes = [255,255,7,0,2,0,0,0,0,0,0,0,0,0,0,0] #seg 81 0x0000C30000014F00
data_bytes = [11,10,10,0,4,0,0,0,0,0,0,0,0,0,0,0] #2*10-2->18->segemnt 7. dumbass it's + not - ...  fail!?
data_bytes = [9 ,10,10,0,4,0,0,0,0,0,0,0,0,0,0,0] #2*10+2=22->segemnt 7. 2*9+4=22->  fail, wtf!?!
data_bytes = [10,10,10,0,2,0,0,0,0,0,0,0,0,0,0,0] #segment 7 0x0000230000014F00
data_bytes = [8 ,10,10,0,4,0,0,0,0,0,0,0,0,0,0,0] #fail with 3 glitches   maybe becaues compute is wrong I'm not making the expected packet?
data_bytes = [32,128,8,0,4,0,0,0,0,0,0,0,0,0,0,0] #seg 74 0x0000000000014F00


#using new compute
#data_bytes = [8,10,10,0,4,0,0,0,0,0,0,0,0,0,0,0] 
data_bytes = [0x80,0x87,0, 10,10,10,0,2,0,0,0,0,0,0,0,0,0,0,0] #seg 7, B d0 d0 d0 d0 E -- length = 4 0x0000230000014F00
data_bytes = [10,10,10,0,2,0,0,0,0,0,0,0,0,0,0,0] #seg 7, B d0 d0 d0 d0 E              -- length = 4 0x0000230000014F00 work x2, fail, work x2 , fail, work --- at repeat of 10.
data_bytes = [10,10,10,0,4,0,0,0,0,0,0,0,0,0,0,0] #seg 107 B d0 d0 d0 d0 d0 d0 d0 d0 E -- length = 8 0x0000000000014F00
data_bytes = [10,10,10,0,8,0,0,0,0,0,0,0,0,0,0,0] #seg 121 data_bytes = [10,10,10,0,4,0,0,0,0,0,0,0,0,0,0,0]
data_bytes = [10,10,10,0,11,0,0,0,0,0,0,0,0,0,0,0] #seg 38 B d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d0 d7 d0 d7 d0 d7 E -- length = 22  0x0000000000000000  070707?? workx4
data_bytes = [1,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0] #seg 16 fail shortx2
'''