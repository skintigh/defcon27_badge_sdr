import re
import sys

lst = []
max_list = 100
min_match = 25
crc_len = 8
length = 147 - 18 + crc_len*2
#print(length)
#  10/110 drops a few with len+147 10/100 dropped 1 10/90  20/90 missed 12 in 200000 then a lot unless that was disc errors  20/50 lots of bad packets!!!
#     20/100 w doubles len+149    50/65 40/65 with len+151 (20/70?)    90/25 with +153  100/21 with +155 lots of dupes
# with old way 10 found false positives, so did 20 with max_list at 30. Changed max list to 64 to catch more crc symbols, had to up min_match to avoid multiple entries. 65/50 works ok  40/30 works ok
count = 0
with open("symbols.txt", 'r') as infile:
	while True:
		line = infile.read(1000000)
		if not line: break
		for ml in re.finditer('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6 .{'+str(length)+'}', line): #read by line for huge files, works?   pattern is 32x2 long, I want (110-3)x2, so 78*2=156-6
		#for ml in re.finditer('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6 2 3 3 6.{'+str(length-8)+'}', line): #read by line for huge files, works?   pattern is 32x2 long, I want (110-3)x2, so 78*2=156-6
		#for ml in re.finditer('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6 2 3 3 6 7.{'+str(length-10)+'}', line): #read by line for huge files, works?   pattern is 32x2 long, I want (110-3)x2, so 78*2=156-6
		#for ml in re.finditer('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6 2 3 3 6 7 7 0.{'+str(length-14)+'}', line): #read by line for huge files, works?   pattern is 32x2 long, I want (110-3)x2, so 78*2=156-6
			found = False
			m = ml.group(0)
			for x in range(0, len(lst)):
				if lst[x][0] == m:			#found so break after                   might be smarter to pop this out of the list and prepend it?     collections.deque would be faster... should print winner only...
					found = True
					entry = lst.pop(x)
					entry[1] += 1
					if entry[1]==min_match:
						#print(m[64:104])
						#print(m[64:])
						count += 1
					lst.insert(0, entry) #move to front
					break
			if not found:
				#print ("not found:\n",m,"\n in:\n", lst)
				#for x in range(0, len(lst)):
				#	if lst[x][0] == m:				#print(m,"not found")
				#		raise()
				#lst.append([m,1])
				lst.insert(0, [m,1])
			#if len(lst) == 15:
			#	break
			if len(lst)>max_list:
				#print ("too long", len(lst))
				lst=lst[-max_list:-1]  #drop oldest entry from end
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
print (count)
