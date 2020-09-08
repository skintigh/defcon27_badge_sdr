import re
import sys

lst = []
max_list = 30  #128 and 256 find bad data
min_match = 30 #10 found false positives, so did 20

with open("symbols.txt", 'r') as infile:
	while True:
		line = infile.read(1000000)
		if not line: break
		for ml in re.finditer('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6 .{147}', line): #read by line for huge files, works?
			found = False
			m = ml.group(0)
			#print(m)
			for x in range(0, len(lst)):
				if lst[x][0] == m:			#found so break after
					found == True
					lst[x][1] += 1
					if lst[x][1]==min_match:
						print(m)
						#sys.stdout.flush()
					break
			if not found:
				#print(m,"not found")
				lst.append([m,1])
			#if len(lst) == 15:
			#	break
			if len(lst)>max_list:
				#print ("too long", len(lst))
				lst=lst[-max_list:-1]
			#print(len(lst))

	'''
	#code for determining how many datagrams per burst. Need to set max_list to be in the thousands for just a few bursts.
	print("length:",len(lst))
	total = 0
	for l in lst: 
		print(l[1],end=' ')
		total += l[1]
	print("\nTotal:", total)
	'''
