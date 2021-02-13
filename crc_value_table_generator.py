#generate a table of CRC values, used to populate crc_list.py

from crc_list import crcs_10_ordered_by_symbol as crcs
import compute_experimental
import guesser

zeros_symbols =   compute_experimental.dzeros_symbols[:4*24] + [int(c) for c in str(crcs[51])] + [0,0]
zeros_symbols =   compute_experimental.dzeros_symbols[:4*24] + [int(c) for c in str(crcs[4096-51])] + [0,0]
crc_values = []
for i in range(0,4096):

	#dzeros_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,0,0,0,0,0,0,0,0,0, 2,3,3,6, 7,7,0,1, 3,2,4,2, 2,2,7,5, 0,3,3,2,      
	#     5,4,3,5, 7,0,3,6, 4,0,7,3, 0,4,1,4, 4,2,7,4, 6,2,0,2, 0,7,6,6, 1,6,4,1, 3,1,4,4, 0,7,7,3, 5,2,7,7,     7,7,7,3, 0,3,1,6, 4,4,0,0, 0,0,0,0] #because out of range error

	crc_symbols = [int(c) for c in str(crcs[i])] + [0, 0]
	#solution = guesser.solver([0]*4, [5,2,7,7,]+crc_symbols, debug=False, ignore=8+16-1, print_error=False, print_result=False)
	solution = guesser.solver([0]*4, [5,2,7,7,]+crc_symbols, debug=False, ignore=8+16-1, print_error=False, print_result=False, default=False, zeros_symbols=zeros_symbols)

	#print(solution)
	#sys.exit()
	'''
	#test I only need one previous byte
	solution2 = guesser.solver([0]*6, crc_symbols, debug=False, ignore=8+16, print_error=False, print_result=False)

	for x in range(1,4):
		if solution[-x] != solution2[-x]:
			print("error",x,i)
	'''
	crc_values.append(solution[-1]*65536 +solution[-2]*256 + solution[-3])

print(crc_values)