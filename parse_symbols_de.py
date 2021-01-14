import re
import sys
from collections import deque

lst = []
de = deque([])
max_list = 200
min_match = 20
length = 147
#  10/110 works with doubles with len+149    50/65 40/65 with len+151   90/25 with +153  100/21 with +155 lots of dupes
# with old way 10 found false positives, so did 20 with max_list at 30. Changed max list to 64 to catch more crc symbols, had to up min_match to avoid multiple entries. 65/50 works ok  40/30 works ok

with open("symbols.txt", 'r') as infile:
	while True:
		line = infile.read(1000000)
		if not line: break
		#for ml in re.finditer('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6 .{147}', line): #read by line for huge files, works?
		count = 0
		#for ml in re.finditer('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6 .{'+str(length)+'}', line): #read by line for huge files, works?   pattern is 32x2 long, I want (110-3)x2, so 78*2=156-6
		#for ml in re.finditer('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 .{'+str(length)+'}', line):
		#for ml in re.finditer('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6 2 3 3 6.{'+str(length-8)+'}', line): 
		#for ml in re.finditer('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6 2 3 3 6 7.{'+str(length-10)+'}', line): 
		for ml in re.finditer('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6 2 3 3 6 7 7 0.{'+str(length-14)+'}', line): 
			found = False
			count += 1
			m = ml.group(0)
			#print(m)
			#print("count: ", count)
			#for x in range(0, len(lst)):
			for x in range(0, len(de)):
				#print(x)
				#if lst[x][0] == m:			#found so break after                   might be smarter to pop this out of the list and prepend it?     collections.deque would be faster... should print winner only...
				if de[x][0] == m:			#found so break after                   might be smarter to pop this out of the list and prepend it?     collections.deque would be faster... should print winner only...
					found = True
					#print("match: '{0}'".format(m))
					#print("list pre pop:\n", lst)
					#print(len(lst))
					#entry = lst.pop(x)
					entry = de[x]
					de.remove(entry)
					#print("pop", entry)
					#print("list post pop:\n", lst, "\n\n")
					#print(len(lst))
					#lst[x][1] += 1
					entry[1] += 1
					#if lst[x][1]==min_match:
					if entry[1]==min_match:
						print(m[64:104])
						#sys.stdout.flush()
					#lst.insert(0, entry) #move to front
					de.appendleft(entry) #move to front
					#print("count: {} found {}".format(count, found))
					break
			#print("count: {} found {}".format(count, found))
			if not found:
				#print ("not found:\n",m,"\n in:\n", lst)
				#for x in range(0, len(lst)):
				#	if lst[x][0] == m:				#print(m,"not found")
				#		raise()
				#lst.append([m,1])
				#lst.insert(0, [m,1])
				de.appendleft([m,1])
			#if len(lst) == 15:
			#	break
			#if len(lst)>max_list:
			if len(de)>max_list:
				#print ("too long", len(lst))
				#lst=lst[-max_list:-1]  #drop oldest entry from end
				de.pop() #drop oldest entry from end
			#print(len(lst))
			#print(lst)

	'''
	#code for determining how many datagrams per burst. Need to set max_list to be in the thousands for just a few bursts.
	print("length:",len(lst))
	total = 0
	for l in lst: 
		print(l[1],end=' ')
		total += l[1]
	print("\nTotal:", total)
	'''
