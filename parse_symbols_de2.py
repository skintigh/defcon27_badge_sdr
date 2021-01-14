import re
import sys
from collections import deque

max_list = 10
min_match = 110
length = 147
de = deque(max_list*[[0,0]])
print(de)

#  10/110 works with doubles with len+149    50/65 40/65 with len+151   90/25 with +153  100/21 with +155 lots of dupes

with open("symbols.txt", 'r') as infile:
	while True:
		line = infile.read(100000)
		if not line: break
		#for ml in re.finditer('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6 .{147}', line): #read by line for huge files, works?
		#for ml in re.finditer('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6 .{'+str(length)+'}', line): #read by line for huge files, works?   pattern is 32x2 long, I want (110-3)x2, so 78*2=156-6
		#for ml in re.finditer('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6 2 3 3 6.{'+str(length-8)+'}', line): #read by line for huge files, works?   pattern is 32x2 long, I want (110-3)x2, so 78*2=156-6
		#for ml in re.finditer('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6 2 3 3 6 7.{'+str(length-10)+'}', line): #read by line for huge files, works?   pattern is 32x2 long, I want (110-3)x2, so 78*2=156-6
		for ml in re.finditer('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6 2 3 3 6 7 7 0.{'+str(length-14)+'}', line): #read by line for huge files, works?   pattern is 32x2 long, I want (110-3)x2, so 78*2=156-6
			found = False
			m = ml.group(0)
			for x in range(0, max_list):
				#print(x)
				if de[x][0] == m:			#found so break after                   might be smarter to pop this out of the list and prepend it?     collections.deque would be faster... should print winner only...
					found = True
					entry = de[x]
					de.remove(entry)
					entry[1] += 1
					if entry[1]==min_match:
						print(m[64:104])
					de.appendleft(entry) #move to front
					break
			if not found:
				de.appendleft([m,1])
				de.pop() #drop oldest entry from end


	'''
	#code for determining how many datagrams per burst. Need to set max_list to be in the thousands for just a few bursts.
	print("length:",len(lst))
	total = 0
	for l in lst: 
		print(l[1],end=' ')
		total += l[1]
	print("\nTotal:", total)
	'''
