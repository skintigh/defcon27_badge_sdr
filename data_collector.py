#use serial interface to update the packet, then capture the packet and record it

import serial
import re
import sys
from pprint import pprint
from time import sleep as sleep
chunk_size = 1000000
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)	

def read_symbols():
	lst = []
	max_list = 30  #128 and 256 find bad data
	min_match = 30 #10 found false positives, so did 20
	last = None
	with open("symbols.txt", 'r') as infile:
		infile.seek(0,2)
		end = infile.tell()
		infile.seek(end-chunk_size)
		data = infile.read(chunk_size)
		#print(len(data))
			
		if len(data) != chunk_size: 
			print("Error last file chunk size", len(data))
			return
		#print(data)
		for ml in re.finditer('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6 .{147}', data):
			found = False
			m = ml.group(0)
			#print(m)
			
			for x in range(0, len(lst)):
				if lst[x][0] == m:			#found so break after
					found == True
					lst[x][1] += 1
					if lst[x][1]==min_match:
						#print(m)
						last = m
					break
			if not found:
				lst.append([m,1])
			if len(lst)>max_list:
				lst=lst[-max_list:-1]
	return last
	

def get_data_symbols(prev_data, n=0):
	#print(n)
	if n == 50:
		print("get_data_symbols failure n ==", n)
		sys.exit(1)
	#data = None
	data = read_symbols()
	while data == None:
		print(".",end='')
		sys.stdout.flush()
		#sys.stdout.flush()
		sleep(0.1)
		data = read_symbols()
	#data = read_symbols()
	#print(data)
	data = data.split('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6 ')[1] #chop header
	data = [int(s) for s in data.split(' ')] #convert to list
	data = data[4*5:4*16] #return just user data portion
	
	if data == prev_data or data == None:
		sleep(0.1)
		data = get_data_symbols(prev_data,n+1)
	return data

def get_data_symbols_long(prev_data, n=0):
	#print(n)
	if n == 50:
		print("get_data_symbols failure n ==", n)
		sys.exit(1)
	#data = None
	data = read_symbols()
	while data == None:
		print(".",end='')
		sys.stdout.flush()
		#sys.stdout.flush()
		sleep(0.1)
		data = read_symbols()
	#data = read_symbols()
	#print(data)
	data = data.split('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6 ')[1] #chop header
	#data = [int(s) for s in data.split(' ')] #convert to list
	#data = data[] #return just user data portion
	
	if data == prev_data or data == None:
		sleep(0.1)
		data = get_data_symbols_long(prev_data,n+1)
	return data


def update_packet(a=0,b=0,c=0,d=0,e=0,f=0,g=0,h=0,i=0, debug=False):
	str = 'u {0:02x}{1:02x}{2:02x}{3:02x}{4:02x}{5:02x}{6:02x}{7:02x}{8:02x}'.format(a,b,c,d,e,f,g,h,i)
	if debug: print("update_packet set to", str)
	ser.write(str.encode())
	sleep(0.10)
	ser.write(b'y\r\n')
	#sleep(0.15)
	r = ser.read(1000).decode('ascii')
	if debug: print(r)
	if "Loading Data:" not in r:
		print("update_packet: error with command to write data")
		print('"Loading Data" not in', r)
		sys.exit()
	#print(r)
	sleep(0.4)	#0.3 fails
	
def update_packet_ary(data, debug=False):
	str = 'u {0:02x}{1:02x}{2:02x}{3:02x}{4:02x}{5:02x}{6:02x}{7:02x}{8:02x}'.format(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8])
	if debug: print("update_packet set to", str)
	ser.write(str.encode())
	sleep(0.10)
	ser.write(b'y\r\n')
	sleep(0.15)
	r = ser.read(1000).decode('ascii')
	if debug: print(r)
	if "Loading Data:" not in r:
		print("update_packet: error with command to write data")
		print('"Loading Data" not in', r)
		sys.exit()
	#print(r)
	sleep(0.4)	#0.3 fails




def main(debug=False):
	print("#data_collector...", end=' ')
	sys.stdout.flush()
	db = []
	ser.write(b'?\r\n')
	r = ser.read(1000).decode('ascii')
	#print(r)
	if "U <hex bytes>: Update transmit packet" not in r:
		print("Serial port failure")
		sys.exit(1)


	
	update_packet(0,0,255,0xff,0xff,0xff,debug=True)
	symbols = get_data_symbols(0)
	#print(symbols)
	expected = [3, 7, 6, 2, 4, 4, 5, 4, 6, 2, 1, 5, 2, 6, 7, 6, 4, 3, 0, 1, 7, 4, 0, 2, 0, 7, 6, 6, 1, 6, 4, 1, 3, 1, 4, 4, 0, 7, 7, 3, 5, 2, 7, 7]
	if symbols != expected:
		print("Error setting symbols to 0xFFFFFFFF")
		print("Expected:",expected)
		print("Received:",symbols)
		#sys.exit(1)



	'''
	a=b=d=e=f=0
	for c in range(0, 256):
		for d in range(0, 256):
			update_packet(0,0,c,d,0,0)
			symbols = get_data_symbols(symbols)
			if debug: 
				print(c, symbols[0:16])
			else:
				print("%02x%02x"%(c,d), end=' ')
				sys.stdout.flush() #need this when no \r\n, other times too?
			db.append([[a, b, c, d, e, f],symbols])
			
		#write ever 256 just in case
		with open("data_2bytes.txt", 'w') as outfile:
			outfile.write('[\n')
			for l in db: 
				outfile.write(str(l)+",\n")
			outfile.write(']\n')		
	'''

	for x in range(0,1000):
		for pos in range(0,9):
			for bit in range(0,8):
				data = 9*[0]
				print(pos,bit)
				data[pos]=pow(2,bit)
				update_packet_ary(data,debug=True)
				symbols = get_data_symbols_long(symbols)
				#db.append([data,symbols])
				db.append(symbols) #just save it like normal data, I can decode

		with open("data_1_bit_per_byte_raw_4.txt", 'a') as outfile:
			#outfile.write('[\n')
			for l in db: 
				outfile.write(str(l)+"\n")
			#outfile.write(']\n')
			db = []


	#print('\n\n[')
	#for l in db: print(l,end=",\n")
	#print(']')
	

	
		#print(*db, sep=', ', end=']\n')

main()
