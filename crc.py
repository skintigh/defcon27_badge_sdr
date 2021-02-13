#scrape a capture for every unique CRC, then sort and print them

filename = "test_0s_100_40_11_symbols_3.txt"
crcs = []
l = 11
cutoff = 8
#9/4 3922  11/4 7264  11/5 6490   11/8 4418  11/9 3800
with open("data_captures/"+filename, "r") as infile:	
	line = infile.readline()
	while line:	
		#print(line)
		#print(line.split(' '))
		#crc = [int(n) for n in line.split(' ')[-13:-2]]
		crc = ''.join(line.split(' ')[-2-l:-2])
		#print(crc)
		crcs.append(crc)
		line = infile.readline()
print(len(crcs), len(crcs)/4096)
unique_crcs = list(set(crcs))
#unique_crcs.sort()
#print(unique_crcs)

'''
counts = [crcs.count(crc) for crc in unique_crcs] 
#print(counts)

final = []
y = 0
for x in range(0, len(unique_crcs)):
	if counts[x] > cutoff: y += 1
	final.append[unique_crcs[x]]

print(y)
print(len(final))
print(final)
print(final.sort())
'''
final = [crc for crc in unique_crcs if crcs.count(crc)>cutoff] 
print(len(final))
#print(final)
final.sort()
print(final)