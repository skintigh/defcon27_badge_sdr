import re
import sys


max_list = 100
min_match = 30
crc_len = 11
length = 128 + crc_len*2 #  +32 -6 #16 for missing char
#print(length)
lst = (max_list)*[[0,0]]
#print(lst)
# 150: 100/25/11 lowest I saw was 40 matches, but the highest impossibles I saw we 51, 40, 38 38 37 37 need to test max_list

#  10/110 drops a few with len+147 10/100 dropped 1 10/90  20/90 missed 12 in 200000 then a lot unless that was disc errors  20/50 lots of bad packets!!!
#     20/100 w doubles len+149    50/65 40/65 with len+151 (20/70?)    90/25 with +153  100/21 with +155 lots of dupes
# with old way 10 found false positives, so did 20 with max_list at 30. Changed max list to 64 to catch more crc symbols, had to up min_match to avoid multiple entries. 65/50 works ok  40/30 works ok



with open("symbols.txt", 'r') as infile:
	while True:
		line = infile.read(1000000)
		if not line: break
		
		#for ml in  re.finditer('4 4 4 4 2 2 2 2 0 0 0 0 6 6 6 6.{'+str(length)+'}', line): +32 -6 #16 for missing char
		#for ml in  re.finditer('4 0 0 4 4 4 4 4 2 2 2 2 0 0 0 0 6 6 6 6 0 0 4 0 6 5 0 5 2 1 6 1'
		for ml in  re.finditer('4 4 4 4 2 2 2 2 0 0 0 0 6 6 6 6 0 0 4 0 6 5 0 5 2 1 6 1.{'+str(length)+'}', line): 
		#for ml in re.finditer('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6.{'+str(length)+'}', line): #read by line for huge files, works?   pattern is 32x2 long, I want (110-3)x2, so 78*2=156-6
		#for ml in re.finditer('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6 2 3 3 6.{'+str(length-8)+'}', line): #read by line for huge files, works?   pattern is 32x2 long, I want (110-3)x2, so 78*2=156-6
		#for ml in re.finditer('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6 2 3 3 6 7.{'+str(length-10)+'}', line): #read by line for huge files, works?   pattern is 32x2 long, I want (110-3)x2, so 78*2=156-6
		#for ml in re.finditer('4 4 4 0 4 0 4 0 2 4 6 0 0 0 0 0 6 4 2 0 0 0 4 4 2 7 7 4 6 7 5 6 2 3 3 6 7 7 0.{'+str(length-14)+'}', line): #read by line for huge files, works?   pattern is 32x2 long, I want (110-3)x2, so 78*2=156-6
			found = False
			m = ml.group(0)
			for x in range(0, max_list):
				if lst[x][0] == m:			#found so break after                   might be smarter to pop this out of the list and prepend it?     collections.deque would be faster... should print winner only...
					found = True
					entry = lst.pop(x)
					entry[1] += 1
					#if entry[1]==min_match:
						#print(m[64:104])
					#	print(m[64:])
					lst.insert(0, entry) #move to front
					break
			if not found:
				lst.insert(0, [m,1])
			#if len(lst)>max_list: #don't test, just assume full
				#print ("too long", len(lst))
				#lst=lst[-max_list:-1]  #drop oldest entry from end
				last_entry = lst.pop(max_list)
				if last_entry[1] > min_match:  #I am assuming at most 2 will exceed the minimum match...
					#check for duplicate with last symbol different
					#print("max '{}'".format(last_entry[0][64:]))
					highest = True
					for i in range(0,max_list):
						if (lst[i][1] > min_match)\
						and last_entry[0][:-2] == lst[i][0][:-2]: #this first check should eliminate most, then they match except for last CRC symbol:
							#print("double '{}' {}".format(last_entry[0][64:],last_entry[1]))
							#print("double '{}'{}".format(lst[i][0][64:], lst[i][1]))							
							if last_entry[1] < lst[i][1]:
								highest = False
								break
							else:
								lst[i][1] = 0 #prevent it from triggering a dump later
					if highest:
						print(last_entry[0][64-8:], last_entry[1]) #or 64:104   64-8:


#drain list after file exhausted
#print("drain")
while lst:
	last_entry = lst.pop(-1)
	if last_entry[1] > min_match:  #I am assuming at most 2 will exceed the minimum match...
		#check for duplicate with last symbol different
		highest = True
		for i in range(0,len(lst)):
			if (lst[i][1] > min_match)\
			and last_entry[0][:-2] == lst[i][0][:-2]: #this first check should eliminate most, then they match except for last CRC symbol:
				#print("double '{}' {}".format(last_entry[0][64:],last_entry[1]))
				#print("double '{}'{}".format(lst[i][0][64:], lst[i][1]))							
				if last_entry[1] < lst[i][1]:
					highest = False
					break
				else:
					lst[i][1] = 0 #prevent it from triggering a dump later
		if highest:
			print(last_entry[0][64-8:], last_entry[1]) #or 64:104
			#print(len(last_entry[0]))

	'''
	#code for determining how many datagrams per burst. Need to set max_list to be in the thousands for just a few bursts.
	print("length:",len(lst))
	total = 0
	for l in lst: 
		print(l[1],end=' ')
		total += l[1]
	print("\nTotal:", total)
	'''
#print(len('4 4 4 4 2 2 2 2 0 0 0 0 6 6 6 6 0 0 4 0 6 5 0 5 2 1 6 1')+length,"+8 (or 6?) from front + 6 for dead symbols should == 220")
