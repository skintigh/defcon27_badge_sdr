#reverse engineer crc by using long counts
from crc_list import crcs_10_ordered_by_symbol as crcs
from crc_list import crcs_10_values as crcs_values
#from crc_list import crcs_10_values_51 as crcs_values_51
#from crc_list import crcs_10_values_4035 as crcs_values_4035
#import crc_list
from guesser import solver
import sys
import compute_experimental
import guesser

#make a table for all 16 bits in each of the 16 bytes, initialize with None
bit_values = [8*[None],8*[None],8*[None],]
bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [None, None, None, None, None, None, None, None]]
bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, None, None, None, None]]
bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, None, None, None]]
bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, None, None]] +[8*[None],8*[None],8*[None],]
bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, None, None], [None, None, None, None, None, None, None, None], [None, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, None, None, None, None]]
bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, None, None], [None, None, None, None, None, None, None, None], [None, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, None, None],8*[None]]
bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, None, None], [None, None, None, None, None, None, None, None], [None, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, None], [None, None, None, None, None, None, None, None]]
bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, None, None], [None, None, None, None, None, None, None, None], [688273, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, None], [None, None, None, None, None, None, None, None]]
bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, None, None], [None, None, None, None, None, None, None, None], [None, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, None, None, None, None, None, None, None]]
bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, None, None], [None, None, None, None, None, None, None, None], [688273, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, None, None, None, None, None, None, None]]
bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, None, None], [None, None, None, None, None, None, None, None], [688273, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, None, None, None, None, None, None]]
bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, None, None], [None, None, None, None, None, None, None, None], [688273, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, None, None, None, None, None]]
#found 0,0 by using baseline computed for all 0s    except the packet probably ended with 7,7,7 and my 0,0 was wrong and poisoned a bunch of others...
bit_values = [[688169, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, None, None], [None, None, None, None, None, None, None, None], [688273, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, None, None, None, None, None]]
bit_values = [[688169, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, None, None], [None, None, None, None, None, None, None, None], [688273, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, None, None, None, None],8*[None],8*[None],8*[None],8*[None],8*[None],8*[None],8*[None],8*[None],8*[None]]
bit_values = [[688169, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, None, None], [41506, None, None, None, None, None, None, None], [688273, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [33468, 2075, 663680, 527, None, None, None, None], [696893, 655420, 32798, 33413, None, None, None, 2592], [656, 168, 52, 26, 41607, 688129, 663559, 699022], [8328, 33291, 666285, 688286, 10752, 32943, 666143, 664109], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
bit_values = [[688169, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, None, None], [41506, None, None, None, None, None, None, None], [688273, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, 664093, 663596, 10908, 8715], [690306, 171, 657949, 690342, 10268, 32801, 666168, 41529], [657937, 666154, 35477, 697005, 665777, 698549, 656024, 8742], [33468, 2075, 663680, 527, 658095, 690335, 698375, 656033], [696893, 655420, 32798, 33413, 666250, 138, 10368, 2592], [656, 168, 52, 26, 41607, 688129, 663559, 699022], [8328, 33291, 666285, 688286, 10752, 32943, 666143, 664109], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
bit_values = [[688169, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, 32909, 690308], [41506, None, None, None, None, None, None, None], [688273, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, 664093, 663596, 10908, 8715], [690306, 171, 657949, 690342, 10268, 32801, 666168, 41529], [657937, 666154, 35477, 697005, 665777, 698549, 656024, 8742], [33468, 2075, 663680, 527, 658095, 690335, 698375, 656033], [696893, 655420, 32798, 33413, 666250, 138, 10368, 2592], [656, 168, 52, 26, 41607, 688129, 663559, 699022], [8328, 33291, 666285, 688286, 10752, 32943, 666143, 664109], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
bit_values = [[688169, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, 32909, 690308], [41506, 35355, None, None, None, None, None, None], [688273, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, 664093, 663596, 10908, 8715], [690306, 171, 657949, 690342, 10268, 32801, 666168, 41529], [657937, 666154, 35477, 697005, 665777, 698549, 656024, 8742], [33468, 2075, 663680, 527, 658095, 690335, 698375, 656033], [696893, 655420, 32798, 33413, 666250, 138, 10368, 2592], [656, 168, 52, 26, 41607, 688129, 663559, 699022], [8328, 33291, 666285, 688286, 10752, 32943, 666143, 664109], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
bit_values = [[688169, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, 32909, 690308], [41506, 35355, 690735, 664208, None, None, None, None], [688273, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, 664093, 663596, 10908, 8715], [690306, 171, 657949, 690342, 10268, 32801, 666168, 41529], [657937, 666154, 35477, 697005, 665777, 698549, 656024, 8742], [33468, 2075, 663680, 527, 658095, 690335, 698375, 656033], [696893, 655420, 32798, 33413, 666250, 138, 10368, 2592], [656, 168, 52, 26, 41607, 688129, 663559, 699022], [8328, 33291, 666285, 688286, 10752, 32943, 666143, 664109], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
bit_values = [[688169, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, 32909, 690308], [41506, 35355, 690735, 664208, 10786, None, None, None], [688273, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, 664093, 663596, 10908, 8715], [690306, 171, 657949, 690342, 10268, 32801, 666168, 41529], [657937, 666154, 35477, 697005, 665777, 698549, 656024, 8742], [33468, 2075, 663680, 527, 658095, 690335, 698375, 656033], [696893, 655420, 32798, 33413, 666250, 138, 10368, 2592], [656, 168, 52, 26, 41607, 688129, 663559, 699022], [8328, 33291, 666285, 688286, 10752, 32943, 666143, 664109], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
'''
a8029 a08b6 0823b aa09a 0a82d aaa11 a2a8f a0aa0  #0,0 wrong
082b0 020b8 0083c 0021e 0008f a8020 0a010 02808 
00a04 00282 000a1 a8037 a201c 0880e 0808d a8884  #2,6 
0a222 08a1b a8a2f a2290 02a22  N/A   N/A   N/A   #3,1 3,4
a8091 a202f a0810 08208 02084 00822 00211 a808f 
a2020 08810 02208 00884 00222 00091 a802f a2010 
08808 02204 00882 00221 a221d a202c 02a9c 0220b #6,4 6,6
a8882 000ab a0a1d a88a6 0281c 08021 a2a38 0a239  #7,1 throuh 7,6
a0a11 a2a2a 08a95 aa2ad a28b1 aa8b5 a0298 02226  *8,0 8,5 8,7
082bc 0081b a2080 0020f a0aaf a889f aa807 a02a1  #9,0 9,2 through 9,6
aa23d a003c 0801e 08285 a2a8a 0008a 02880 00a20  10,0 10,3 10,4 10,5
00290 000a8 00034 0001a 0a287 a8001 a2007 aaa8e  11,4 11,7
02088 0820b a2aad a809e 02a00 080af a2a1f a222d  12,0 through 12,6
 N/A   N/A   N/A   N/A   N/A   N/A   N/A   N/A  
 N/A   N/A   N/A   N/A   N/A   N/A   N/A   N/A  
 N/A   N/A   N/A   N/A   N/A   N/A   N/A   N/A  
 '''
bit_values = [[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,]
bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
bit_values = [[664227, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, 8711, 690308], [41506, 10385, None, None, None, None, None, None], [None, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, 688279, 663596, 34838, 8715], [690306, 41505, 698519, 666156, 35478, 8875, 690354, 41529], [698523, 666154, 35477, 697005, 665777, 657983, 656024, 32940], [8246, 2075, 688650, 41093, 698405, 666133, 658061, 656033], [655543, 655420, 32798, 8207, 690176, 41472, 10368, 2592], [656, 168, 52, 26, 13, 688129, 663559, 657412], [33282, 8321, 690215, 664084, 34954, 8741, 690325, 664109], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
bit_values = [[664227, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, 8711, 690308], [41506, 10385, 690735, 664208, None, None, None, None], [None, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, 688279, 663596, 34838, 8715], [690306, 41505, 698519, 666156, 35478, 8875, 690354, 41529], [698523, 666154, 35477, 697005, 665777, 657983, 656024, 32940], [8246, 2075, 688650, 41093, 698405, 666133, 658061, 656033], [655543, 655420, 32798, 8207, 690176, 41472, 10368, 2592], [656, 168, 52, 26, 13, 688129, 663559, 657412], [33282, 8321, 690215, 664084, 34954, 8741, 690325, 664109], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
bit_values = [[664227, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, 8711, 690308], [41506, 10385, 690735, 664208, 34984, None, None, None], [None, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, 688279, 663596, 34838, 8715], [690306, 41505, 698519, 666156, 35478, 8875, 690354, 41529], [698523, 666154, 35477, 697005, 665777, 657983, 656024, 32940], [8246, 2075, 688650, 41093, 698405, 666133, 658061, 656033], [655543, 655420, 32798, 8207, 690176, 41472, 10368, 2592], [656, 168, 52, 26, 13, 688129, 663559, 657412], [33282, 8321, 690215, 664084, 34954, 8741, 690325, 664109], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
bit_values = [[664227, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, 8711, 690308], [41506, 10385, 690735, 664208, 34984, 8756, None, None], [None, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, 688279, 663596, 34838, 8715], [690306, 41505, 698519, 666156, 35478, 8875, 690354, 41529], [698523, 666154, 35477, 697005, 665777, 657983, 656024, 32940], [8246, 2075, 688650, 41093, 698405, 666133, 658061, 656033], [655543, 655420, 32798, 8207, 690176, 41472, 10368, 2592], [656, 168, 52, 26, 13, 688129, 663559, 657412], [33282, 8321, 690215, 664084, 34954, 8741, 690325, 664109], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
bit_values = [[664227, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, 8711, 690308], [41506, 10385, 690735, 664208, 34984, 8756, None, None], [None, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, 688279, 663596, 34838, 8715], [690306, 41505, 698519, 666156, 35478, 8875, 690354, 41529], [698523, 666154, 35477, 697005, 665777, 657983, 656024, 32940], [8246, 2075, 688650, 41093, 698405, 666133, 658061, 656033], [655543, 655420, 32798, 8207, 690176, 41472, 10368, 2592], [656, 168, 52, 26, 13, 688129, 663559, 657412], [33282, 8321, 690215, 664084, 34954, 8741, 690325, 664109], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
#trusting my previous math for 4,0...
bit_values = [[664227, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, 8711, 690308], [41506, 10385, 690735, 664208, 34984, 8756, None, None], [0xa8091, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, 688279, 663596, 34838, 8715], [690306, 41505, 698519, 666156, 35478, 8875, 690354, 41529], [698523, 666154, 35477, 697005, 665777, 657983, 656024, 32940], [8246, 2075, 688650, 41093, 698405, 666133, 658061, 656033], [655543, 655420, 32798, 8207, 690176, 41472, 10368, 2592], [656, 168, 52, 26, 13, 688129, 663559, 657412], [33282, 8321, 690215, 664084, 34954, 8741, 690325, 664109], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
'''
a22a3 a08b6 0823b aa09a 0a82d aaa11 a2a8f a0aa0 
082b0 020b8 0083c 0021e 0008f a8020 0a010 02808 
00a04 00282 000a1 a8037 a201c 0880e 02207 a8884 
0a222 02891 a8a2f a2290 088a8 02234  N/A   N/A  
a8091 a202f a0810 08208 02084 00822 00211 a808f 
a2020 08810 02208 00884 00222 00091 a802f a2010 
08808 02204 00882 00221 a8097 a202c 08816 0220b 
a8882 0a221 aa897 a2a2c 08a96 022ab a88b2 0a239 
aa89b a2a2a 08a95 aa2ad a28b1 a0a3f a0298 080ac 
02036 0081b a820a 0a085 aa825 a2a15 a0a8d a02a1 
a00b7 a003c 0801e 0200f a8800 0a200 02880 00a20 
00290 000a8 00034 0001a 0000d a8001 a2007 a0804 
08202 02081 a8827 a2214 0888a 02225 a8895 a222d 
 N/A   N/A   N/A   N/A   N/A   N/A   N/A   N/A  
 N/A   N/A   N/A   N/A   N/A   N/A   N/A   N/A  
 N/A   N/A   N/A   N/A   N/A   N/A   N/A   N/A  
'''






#started again over due to errors
bit_values = [[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,]
#eleven 0s
bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
#  N/A  a08b6 0823b aa09a 0a82d aaa11 a2a8f a0aa0 
# 082b0 020b8 0083c 0021e 0008f  N/A   N/A   N/A  
#again just trans
bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
#  N/A  a08b6 0823b aa09a 0a82d aaa11 a2a8f a0aa0 
# 082b0 020b8 0083c 0021e 0008f a8020  N/A   N/A 

#short trans of tests, stopped after bit 2,
bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
#  N/A  a08b6 0823b aa09a 0a82d aaa11 a2a8f a0aa0 
# 082b0 020b8 0083c 0021e 0008f a8020 0a010 02808 
# 00a04  N/A   N/A   N/A   N/A   N/A   N/A   N/A 

#long trans of same
bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
#  N/A  a08b6 0823b aa09a 0a82d aaa11 a2a8f a0aa0 
# 082b0 020b8 0083c 0021e 0008f a8020 0a010 02808 
# 00a04 00282 000a1 a8037  N/A   N/A   N/A   N/A  

#again
bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
#  N/A  a08b6 0823b aa09a 0a82d aaa11 a2a8f a0aa0 
# 082b0 020b8 0083c 0021e 0008f a8020 0a010 02808 
# 00a04 00282 000a1 a8037 a201c 0880e  N/A   N/A 

#glitched data iterate, stopped after a minute
bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, None, None], [None, None, None, None, None, None, None, None], [None, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
#  N/A  a08b6 0823b aa09a 0a82d aaa11 a2a8f a0aa0 
# 082b0 020b8 0083c 0021e 0008f a8020 0a010 02808 
# 00a04 00282 000a1 a8037 a201c 0880e  N/A   N/A  
#  N/A   N/A   N/A   N/A   N/A   N/A   N/A   N/A  
#  N/A  a202f a0810 08208 02084 00822 00211 a808f 
# a2020 08810 02208  N/A   N/A   N/A   N/A   N/A  

#glitch short trans, stopped after a few minutes when i got 5,7
bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, None, None], [None, None, None, None, None, None, None, None], [None, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
#  N/A  a08b6 0823b aa09a 0a82d aaa11 a2a8f a0aa0 
# 082b0 020b8 0083c 0021e 0008f a8020 0a010 02808 
# 00a04 00282 000a1 a8037 a201c 0880e  N/A   N/A  
#  N/A   N/A   N/A   N/A   N/A   N/A   N/A   N/A  
#  N/A  a202f a0810 08208 02084 00822 00211 a808f 
# a2020 08810 02208 00884 00222 00091 a802f a2010 

#iter data 1bit
bit_values = [[664227, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, 8711, 690308], [41506, 10385, None, None, None, None, None, None], [None, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, 688279, 663596, 34838, 8715], [690306, 41505, 698519, 666156, 35478, 8875, 690354, 41529], [698523, 666154, 35477, 697005, 665777, 657983, 656024, 32940], [8246, 2075, 688650, 41093, 698405, 666133, 658061, 656033], [655543, 655420, 32798, 8207, 690176, 41472, 10368, 2592], [656, 168, 52, 26, 13, 688129, 663559, 657412], [33282, 8321, 690215, 664084, 34954, 8741, 690325, 664109], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
# a22a3 a08b6 0823b aa09a 0a82d aaa11 a2a8f a0aa0 
# 082b0 020b8 0083c 0021e 0008f a8020 0a010 02808 
# 00a04 00282 000a1 a8037 a201c 0880e 02207 a8884 
# 0a222 02891  N/A   N/A   N/A   N/A   N/A   N/A  
#  N/A  a202f a0810 08208 02084 00822 00211 a808f 
# a2020 08810 02208 00884 00222 00091 a802f a2010 
# 08808 02204 00882 00221 a8097 a202c 08816 0220b 
# a8882 0a221 aa897 a2a2c 08a96 022ab a88b2 0a239 
# aa89b a2a2a 08a95 aa2ad a28b1 a0a3f a0298 080ac 
# 02036 0081b a820a 0a085 aa825 a2a15 a0a8d a02a1 
# a00b7 a003c 0801e 0200f a8800 0a200 02880 00a20 
# 00290 000a8 00034 0001a 0000d a8001 a2007 a0804 
# 08202 02081 a8827 a2214 0888a 02225 a8895 a222d 
#  N/A   N/A   N/A   N/A   N/A   N/A   N/A   N/A  
#  N/A   N/A   N/A   N/A   N/A   N/A   N/A   N/A  
#  N/A   N/A   N/A   N/A   N/A   N/A   N/A   N/A  


#found baseline then ran test data
BASELINE = 0xa2a11
bit_values = [[664227, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, 8711, 690308], [41506, 10385, None, None, None, None, None, None], [688273, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, 688279, 663596, 34838, 8715], [690306, 41505, 698519, 666156, 35478, 8875, 690354, 41529], [698523, 666154, 35477, 697005, 665777, 657983, 656024, 32940], [8246, 2075, 688650, 41093, 698405, 666133, 658061, 656033], [655543, 655420, 32798, 8207, 690176, 41472, 10368, 2592], [656, 168, 52, 26, 13, 688129, 663559, 657412], [33282, 8321, 690215, 664084, 34954, 8741, 690325, 664109], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
# a22a3 a08b6 0823b aa09a 0a82d aaa11 a2a8f a0aa0 
# 082b0 020b8 0083c 0021e 0008f a8020 0a010 02808 
# 00a04 00282 000a1 a8037 a201c 0880e 02207 a8884 
# 0a222 02891  N/A   N/A   N/A   N/A   N/A   N/A  
# a8091 a202f a0810 08208 02084 00822 00211 a808f 
# a2020 08810 02208 00884 00222 00091 a802f a2010 
# 08808 02204 00882 00221 a8097 a202c 08816 0220b 
# a8882 0a221 aa897 a2a2c 08a96 022ab a88b2 0a239 
# aa89b a2a2a 08a95 aa2ad a28b1 a0a3f a0298 080ac 
# 02036 0081b a820a 0a085 aa825 a2a15 a0a8d a02a1 
# a00b7 a003c 0801e 0200f a8800 0a200 02880 00a20 
# 00290 000a8 00034 0001a 0000d a8001 a2007 a0804 
# 08202 02081 a8827 a2214 0888a 02225 a8895 a222d 
#  N/A   N/A   N/A   N/A   N/A   N/A   N/A   N/A  
#  N/A   N/A   N/A   N/A   N/A   N/A   N/A   N/A  
#  N/A   N/A   N/A   N/A   N/A   N/A   N/A   N/A  

#1bit files
bit_values = [[664227, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, 8711, 690308], [41506, 10385, 690735, 664208, 34984, 8756, None, None], [688273, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, 688279, 663596, 34838, 8715], [690306, 41505, 698519, 666156, 35478, 8875, 690354, 41529], [698523, 666154, 35477, 697005, 665777, 657983, 656024, 32940], [8246, 2075, 688650, 41093, 698405, 666133, 658061, 656033], [655543, 655420, 32798, 8207, 690176, 41472, 10368, 2592], [656, 168, 52, 26, 13, 688129, 663559, 657412], [33282, 8321, 690215, 664084, 34954, 8741, 690325, 664109], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
# a22a3 a08b6 0823b aa09a 0a82d aaa11 a2a8f a0aa0 
# 082b0 020b8 0083c 0021e 0008f a8020 0a010 02808 
# 00a04 00282 000a1 a8037 a201c 0880e 02207 a8884 
# 0a222 02891 a8a2f a2290 088a8 02234  N/A   N/A  
# a8091 a202f a0810 08208 02084 00822 00211 a808f 
# a2020 08810 02208 00884 00222 00091 a802f a2010 
# 08808 02204 00882 00221 a8097 a202c 08816 0220b 
# a8882 0a221 aa897 a2a2c 08a96 022ab a88b2 0a239 
# aa89b a2a2a 08a95 aa2ad a28b1 a0a3f a0298 080ac 
# 02036 0081b a820a 0a085 aa825 a2a15 a0a8d a02a1 
# a00b7 a003c 0801e 0200f a8800 0a200 02880 00a20 
# 00290 000a8 00034 0001a 0000d a8001 a2007 a0804 
# 08202 02081 a8827 a2214 0888a 02225 a8895 a222d 
#  N/A   N/A   N/A   N/A   N/A   N/A   N/A   N/A  
#  N/A   N/A   N/A   N/A   N/A   N/A   N/A   N/A  
#  N/A   N/A   N/A   N/A   N/A   N/A   N/A   N/A  

#byte_15
bit_values = [[664227, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, 8711, 690308], [41506, 10385, 690735, 664208, 34984, 8756, None, None], [688273, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, 688279, 663596, 34838, 8715], [690306, 41505, 698519, 666156, 35478, 8875, 690354, 41529], [698523, 666154, 35477, 697005, 665777, 657983, 656024, 32940], [8246, 2075, 688650, 41093, 698405, 666133, 658061, 656033], [655543, 655420, 32798, 8207, 690176, 41472, 10368, 2592], [656, 168, 52, 26, 13, 688129, 663559, 657412], [33282, 8321, 690215, 664084, 34954, 8741, 690325, 664109], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [690181, 664069, 657541, 655909, 655509, 655405, 655377, 655375]]
# a22a3 a08b6 0823b aa09a 0a82d aaa11 a2a8f a0aa0 
# 082b0 020b8 0083c 0021e 0008f a8020 0a010 02808 
# 00a04 00282 000a1 a8037 a201c 0880e 02207 a8884 
# 0a222 02891 a8a2f a2290 088a8 02234  N/A   N/A  
# a8091 a202f a0810 08208 02084 00822 00211 a808f 
# a2020 08810 02208 00884 00222 00091 a802f a2010 
# 08808 02204 00882 00221 a8097 a202c 08816 0220b 
# a8882 0a221 aa897 a2a2c 08a96 022ab a88b2 0a239 
# aa89b a2a2a 08a95 aa2ad a28b1 a0a3f a0298 080ac 
# 02036 0081b a820a 0a085 aa825 a2a15 a0a8d a02a1 
# a00b7 a003c 0801e 0200f a8800 0a200 02880 00a20 
# 00290 000a8 00034 0001a 0000d a8001 a2007 a0804 
# 08202 02081 a8827 a2214 0888a 02225 a8895 a222d 
#  N/A   N/A   N/A   N/A   N/A   N/A   N/A   N/A  
#  N/A   N/A   N/A   N/A   N/A   N/A   N/A   N/A  
# a8805 a2205 a0885 a0225 a0095 a002d a0011 a000f 

#byte_14.txt
bit_values = [[664227, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, 8711, 690308], [41506, 10385, 690735, 664208, 34984, 8756, None, None], [688273, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, 688279, 663596, 34838, 8715], [690306, 41505, 698519, 666156, 35478, 8875, 690354, 41529], [698523, 666154, 35477, 697005, 665777, 657983, 656024, 32940], [8246, 2075, 688650, 41093, 698405, 666133, 658061, 656033], [655543, 655420, 32798, 8207, 690176, 41472, 10368, 2592], [656, 168, 52, 26, 13, 688129, 663559, 657412], [33282, 8321, 690215, 664084, 34954, 8741, 690325, 664109], [None, None, None, None, None, None, None, None], [663589, 657429, 655885, 655489, 655399, 655380, 32778, 8197], [690181, 664069, 657541, 655909, 655509, 655405, 655377, 655375]]
# a22a3 a08b6 0823b aa09a 0a82d aaa11 a2a8f a0aa0 
# 082b0 020b8 0083c 0021e 0008f a8020 0a010 02808 
# 00a04 00282 000a1 a8037 a201c 0880e 02207 a8884 
# 0a222 02891 a8a2f a2290 088a8 02234  N/A   N/A  
# a8091 a202f a0810 08208 02084 00822 00211 a808f 
# a2020 08810 02208 00884 00222 00091 a802f a2010 
# 08808 02204 00882 00221 a8097 a202c 08816 0220b 
# a8882 0a221 aa897 a2a2c 08a96 022ab a88b2 0a239 
# aa89b a2a2a 08a95 aa2ad a28b1 a0a3f a0298 080ac 
# 02036 0081b a820a 0a085 aa825 a2a15 a0a8d a02a1 
# a00b7 a003c 0801e 0200f a8800 0a200 02880 00a20 
# 00290 000a8 00034 0001a 0000d a8001 a2007 a0804 
# 08202 02081 a8827 a2214 0888a 02225 a8895 a222d 
#  N/A   N/A   N/A   N/A   N/A   N/A   N/A   N/A  
# a2025 a0815 a020d a0081 a0027 a0014 0800a 02005 
# a8805 a2205 a0885 a0225 a0095 a002d a0011 a000f 

#byte_13.txt
bit_values = [[664227, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, 8711, 690308], [41506, 10385, 690735, 664208, 34984, 8756, None, None], [688273, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, 688279, 663596, 34838, 8715], [690306, 41505, 698519, 666156, 35478, 8875, 690354, 41529], [698523, 666154, 35477, 697005, 665777, 657983, 656024, 32940], [8246, 2075, 688650, 41093, 698405, 666133, 658061, 656033], [655543, 655420, 32798, 8207, 690176, 41472, 10368, 2592], [656, 168, 52, 26, 13, 688129, 663559, 657412], [33282, 8321, 690215, 664084, 34954, 8741, 690325, 664109], [657553, 655919, 655504, 32808, 8212, 2058, 517, 688261], [663589, 657429, 655885, 655489, 655399, 655380, 32778, 8197], [690181, 664069, 657541, 655909, 655509, 655405, 655377, 655375]]
# a22a3 a08b6 0823b aa09a 0a82d aaa11 a2a8f a0aa0 
# 082b0 020b8 0083c 0021e 0008f a8020 0a010 02808 
# 00a04 00282 000a1 a8037 a201c 0880e 02207 a8884 
# 0a222 02891 a8a2f a2290 088a8 02234  N/A   N/A  
# a8091 a202f a0810 08208 02084 00822 00211 a808f 
# a2020 08810 02208 00884 00222 00091 a802f a2010 
# 08808 02204 00882 00221 a8097 a202c 08816 0220b 
# a8882 0a221 aa897 a2a2c 08a96 022ab a88b2 0a239 
# aa89b a2a2a 08a95 aa2ad a28b1 a0a3f a0298 080ac 
# 02036 0081b a820a 0a085 aa825 a2a15 a0a8d a02a1 
# a00b7 a003c 0801e 0200f a8800 0a200 02880 00a20 
# 00290 000a8 00034 0001a 0000d a8001 a2007 a0804 
# 08202 02081 a8827 a2214 0888a 02225 a8895 a222d 
# a0891 a022f a0090 08028 02014 0080a 00205 a8085 
# a2025 a0815 a020d a0081 a0027 a0014 0800a 02005 
# a8805 a2205 a0885 a0225 a0095 a002d a0011 a000f 
#xor a2a11
# 008b2 022a7 aa82a 08a8b a823c 08000 0009e 020b1 
# aa8a1 a0aa9 a222d a280f a2a9e 0aa31 a8a01 a0219 
# a2015 a2893 a2ab0 0aa26 00a0d aa21f a0816 0a295 
# a8833 a0280 0a03e 00881 aa2b9 a0825  N/A   N/A  
# 0aa80 00a3e 02201 aa819 a0a95 a2233 a2800 0aa9e 
# 00a31 aa201 a0819 a2295 a2833 a2a80 0aa3e 00a01 
# aa219 a0815 a2293 a2830 0aa86 00a3d aa207 a081a 
# 0a293 a8830 08286 0003d aa087 a08ba 0a2a3 a8828 
# 0828a 0003b aa084 088bc 002a0 0202e 02889 aaabd 
# a0a27 a220a 0a81b a8a94 08234 00004 0209c 028b0 
# 02aa6 02a2d aaa0f a0a1e 0a211 a8811 a0291 a2031 
# a2881 a2ab9 a2a25 a2a0b a2a1c 0aa10 00a16 02215 
# aa813 a0a90 0a236 00805 aa29b a0834 0a284 0083c 
# 02280 0283e 02a81 aaa39 a0a05 a221b a2814 0aa94 
# 00a34 02204 0281c 02a90 02a36 02a05 aaa1b a0a14 
# 0a214 00814 02294 02834 02a84 02a3c 02a00 02a1e 

#global variable, apparently


depth = len(bit_values)
#print("depth =", depth)

def find_baseline(solution):
	xor_sol = solution[3:]
		#last_solution = 0

	unknowns = 0 #must know all bits to compute baseline
	for i in range(0,depth):
		
		for x in range(0,8):
			if (xor_sol[i]&pow(2,x)) and bit_values[i][x] == None:
				unknowns += 1
				last_none_bit = x
				last_none_byte = i

	if unknowns == 0	:
		crc_value = solution[-1]*65536 +solution[-2]*256 + solution[-3]
		new_value=crc_value
		for i in range(0,depth):
			for x in range(0,8):
				if (xor_sol[i]&pow(2,x)):# and bit_values[i][x] != None:
					new_value^=bit_values[i][x]
		print("Baseline found:", hex(new_value))
		#sys.exit()
		return new_value
	else:
		print("*** find_baseline(): All bits must be known, but unknown bits =", unknowns)

def find_bits(solution,last_solution=None,baseline=None, print_too_many=True):
	#xor_sol = [solution[x] for x in range(3,depth+3)]
	if last_solution:
		#try:
		xor_sol = [solution[x]^last_solution[x] for x in range(3,depth+3)]
		#except:
		#	print(solution,last_solution)
	else:
		xor_sol = solution[3:]
		#last_solution = 0

	#fill in any nones we can
	#first count Nones, if there are >1 skip
	Nones = 0 #need one bit to change in the ENTIRE PACKET to learn the new bit
	for i in range(0,depth):
		
		for x in range(0,8):
			if (xor_sol[i]&pow(2,x)) and bit_values[i][x] == None:
				Nones += 1
				last_none_bit = x
				last_none_byte = i
		#print(Nones)

	if Nones == 1:
		crc_value = solution[-1]*65536 +solution[-2]*256 + solution[-3]
		if last_solution:	
			last_crc_value = last_solution[-1]*65536 +last_solution[-2]*256 + last_solution[-3]
			new_value = crc_value^last_crc_value
		elif baseline:
			new_value = crc_value^baseline
		else:
			print("Error, find_bits either needs a baseline or the last_solution")
			sys.exit(1)
		for i in range(0,depth):
			for x in range(0,8):
				if (xor_sol[i]&pow(2,x)) and bit_values[i][x] != None:
					new_value^=bit_values[i][x]




		#bit_values[i][last_none_bit] = crc_value^last_crc_value
		bit_values[last_none_byte][last_none_bit] = new_value
		print("\n####################")
		print("# New value at {},{} #".format(last_none_byte,last_none_bit))
		print("####################")
		#print("bit_values =", bit_values)  #print the raw variable
		print_bit_values(bit_values)
	elif Nones>1 and print_too_many:
		print("find_bits(): too many unknown bits:", Nones)

def print_bit_values(bit_values,xor=0):
	if xor: print("xor {:05x}".format(xor))
	#print(bit_values)
	for x in range(0,len(bit_values)):
		print("# ",end="")
		for y in range(0,8):
			if bit_values[x][y]: 
				print("{:05x}".format(bit_values[x][y] ^ xor), end = " ")
			else:
				print(" N/A ", end=" ")
		print()

def compute_crc(solution, baseline=BASELINE, silent=False):#crc_list.baseline_crc_value):
	computed_crc_value = baseline
	#print("baseline_crc_value starts as {:05x}".format(computed_crc_value))
	for i in range(0,depth):
		#print(i,hex(computed_crc_value))
		for x in range(0,8):
			if (solution[i+3]&pow(2,x)):
				if bit_values[i][x]:				
					computed_crc_value ^= bit_values[i][x]
					#print("byte {} bit {} ^= {:05x}".format(i,x,bit_values[i][x]))
				else:
					if not silent: print("*** Error: can't compute CRC, values missing[{}][{}]".format(i,x))
					return None
	return(computed_crc_value)

def iterate_file(filename, limit = 2000000000, increment = 1000, print_lines = True):
	with open(filename, "r") as infile:	
		print("\n\n\nUsing:", filename)
		count = 0		

		#check every packet in the file plus preamble
		line = infile.readline()
		try:
			symbols = [0,0,4,4,2,7,7,4,6,7,5,6,] + [int(n) for n in line.split()[0:74]] + [0,0]
		except:
			print(line)
			print(line.split(' '))
			print(len(line.split(' ')))
			print("error")
			e = sys.exc_info()[0]
			print("error", e)
			sys.exit()


		last_solution = solver([0]*(len(symbols)//4),symbols, debug=False, ignore=8-3, print_error=False, print_result=False)
		if last_solution == "Impossible": 
			print("last_solution is",last_solution)
			sys.exit(1)
		print("initial last_solution[3:] =")
		print("".join("{:2x} ".format(num) for num in last_solution[3:]))

		baseline = find_baseline(last_solution)
		if baseline != BASELINE: 
			print("*** Error finding baseline ***")   #need to start with all 0s or known bits?
			baseline = BASELINE
		else:
			last_crc_value = last_solution[-1]*65536 +last_solution[-2]*256 + last_solution[-3]
			computed_crc_value = compute_crc(last_solution,baseline)			
			if not (computed_crc_value==last_crc_value): 
				if computed_crc_value: print("crc error {:05x} {:05x}".format(computed_crc_value,last_crc_value))
				print("xor difference =", hex(computed_crc_value^last_crc_value))
				sys.exit(1)
		

		line = infile.readline()

		while line and count < limit:
			count += 1
			symbols = [0,0,4,4,2,7,7,4,6,7,5,6,] + [int(n) for n in line.split(' ')[0:74]] + [0,0]
			solution = solver([0]*(len(symbols)//4),symbols, debug=False, ignore=8-3, print_error=False, print_result=False)
			
			if solution == "Impossible":
				print(count, solution)
				line = infile.readline()
				continue
			if print_lines: print("".join("{:3d} ".format(num) for num in solution[3:]))

			#find a pattern for another test
			#if solution[7] == 248: 
			#	print("".join("{:3d} ".format(num) for num in solution))
			#	print(line)

			#find unknown bits
			find_bits(solution,last_solution, print_too_many=print_lines) #xor packets when too many unknowns
			#find_bits(solution,baseline=0xa2a11) #to solve 1 unknown

			#find_baseline(solution)  #why would i do this every time?
			

			#verify CRC
			'''
			computed_crc_value = compute_crc(solution,baseline)
			crc_value = solution[-1]*65536 +solution[-2]*256 + solution[-3]
			if computed_crc_value != crc_value: #ignore None?
				
				if computed_crc_value: 
					print("CRC error {:05x} {:05x}".format(computed_crc_value,crc_value))
					print("xor difference =", hex(computed_crc_value^crc_value))
				else: 
					print("CRC error {} {}".format(computed_crc_value,crc_value))					
				#sys.exit(1)
			'''


			#skip through faster
			#for _ in range(0,100):
			#	line = infile.readline()


			line = infile.readline()
			last_solution=solution
			if count%increment == 0: print (count)

def test_transitions(filename, pattern, limit = 2000000000, display_count=2, increment = 1000, print_lines = True):  #display_count must be 2 to test 1 for new bits...
	with open(filename, "r") as infile:	
		print("\n\nUsing:", filename)
		#print batches at transitions to help figure out math

		comp_count = 0 #number to compute
		long_count = 0 #count of packets
		compute_last_sol = True
		line = infile.readline()
		while line and long_count < limit:
			if long_count % increment  == 0: print(long_count)

			
			if comp_count <=0 and line[0:len(pattern)] == pattern:
				comp_count = display_count
				compute_last_sol = True
			
			#for use with glitch data
			#if comp_count <= 0 and line[0:40] == '4 2 1 0 7 0 6 1 3 2 4 2 2 2 7 5 0 7 5 5 ':
			#if comp_count <- 0 and line[0:48] == '4 2 1 0 7 0 6 1 3 2 4 2 2 2 7 5 4 3 3 2 5 0 5 2 ':  
			#	comp_count = 8

			#get the first line of a batch
			if compute_last_sol:
				compute_last_sol = False
				symbols = [0,0,4,4,2,7,7,4,6,7,5,6,] + [int(n) for n in line.split(' ')[0:74]] + [0,0]
				last_solution = solver([0]*(len(symbols)//4),symbols, debug=False, ignore=8-3, print_error=False, print_result=False)
				if last_solution == "Impossible":
					print(long_count, "comp_count =", comp_count, "last_solution =", last_solution,"skipping lines")
					comp_count = 0;
				else:
					if print_lines:
						print("-----")
						print("".join("{:3d} ".format(num) for num in last_solution[3:]))
					last_crc_value = last_solution[-1]*65536 +last_solution[-2]*256 + last_solution[-3]

					'''
					#test for a symbol to make a pattern
					if last_solution[4] == 255:
						print("".join("{:3d} ".format(num) for num in solution))
						print(line)
						sys.exit()
					'''

			elif comp_count>0:  #compute a number of lines when comp_count is positive
				symbols = [0,0,4,4,2,7,7,4,6,7,5,6,] + [int(n) for n in line.split(' ')[0:74]] + [0,0]
				solution = solver([0]*(len(symbols)//4),symbols, debug=False, ignore=8-3, print_error=False, print_result=False)

				if solution == "Impossible":
					print(long_count, comp_count, solution)
					line = infile.readline()
					continue

				if print_lines: 
					print("".join("{:3d} ".format(num) for num in solution[3:]))
					#print(symbols[12:12+16])

				crc_value = solution[-1]*65536 +solution[-2]*256 + solution[-3]
				#xor_sol = [solution[x]^last_solution[x] for x in [3,4,5]]
				find_bits(solution,last_solution,print_too_many=False) #xor packets when too many unknowns
				#find_bits(solution)

				'''
				if solution[3] == 255:
					print("".join("{:3d} ".format(num) for num in solution))
					print(line)
					sys.exit()
				'''


				'''
				symbols = [int(n) for n in line.split(' ')[0:20]]
				solution = solver([0,0,0], symbols, debug=False, ignore=8, print_error=False, print_result=False)
				print
				print("{:6}: {} [{:3}, {:3}, {:3}] [{:08b}, {:08b}, {:08b}]".format(x, symbols[0:20], solution[0], solution[1],solution[2], solution[0], solution[1],solution[2]))
				comp_count -= 1
				if not comp_count and p: print()
				'''
			#if (x-64)%(128*256) == 10: print()
			comp_count -= 1
			long_count += 1
			line = infile.readline()
			#if not x % 1000: input("Press any key to continue...")		




if __name__ == "__main__": 
	bit_values = [8*[None],8*[None],8*[None],8*[None],8*[None],8*[None],8*[None],8*[None],8*[None],8*[None],8*[None],8*[None],8*[None],8*[None],8*[None],8*[None],]					#for demo
	BASELINE = 0 #???

	print("Bit values:")
	print_bit_values(bit_values)
	if BASELINE:
		print("\nBit values", end=" ")
		print_bit_values(bit_values, xor=BASELINE)

	#get row 0 bits up to [1,1]   success!
	if 0:
		#dirname = "data_captures/"
		#for filename in ["test_0s_20_70_147_symbols.txt", "test_0s_100_40_11_symbols_3.txt", "test_0s_50_40_11_symbols_4.txt", "test_0s_50_40_11_symbols_5.txt", 		"test_0s_50_40_11_symbols_6.txt", "test_0s_50_40_11_symbols_7.txt", "test_0s_50_40_11_symbols_8.txt"]: #these lines end with 7 7 7
		#for filename in ["test_0s_20_70_147_symbols.txt" ]:  #long... all 0, at lesat 1,3 around 1200
		#for filename in ["test_0s_100_40_11_symbols_3.txt"]:# hrough 1,1 by 500
		#, "test_0s_50_40_11_symbols_4.txt", "test_0s_50_40_11_symbols_5.txt", 		"test_0s_50_40_11_symbols_6.txt", "test_0s_50_40_11_symbols_7.txt", "test_0s_50_40_11_symbols_8.txt"]: #these lines end with 7 7 7

			
		#for filename in ["test_glitched_100_40_11_symbols.txt","test_glitched_100_40_11_symbols_2.txt","test_glitched_100_40_11_symbols_3.txt","test_glitched_100_40_11_symbols_4.txt","test_glitched_100_40_11_symbols_b.txt"]:
		#for filename in ["test_glitched_100_40_11_symbols_b.txt","test_glitched_100_40_11_symbols_2.txt","test_glitched_100_40_11_symbols_3.txt","test_glitched_100_40_11_symbols_4.txt"]: # _b is cleaner than orig
		
		dirname = "generated_data_byte_captures/"	

		for filename in ["eleven_0s.txt"]: #1,0 by 300   1,3 by 2200  [1,4] 3300
		#  N/A  a08b6 0823b aa09a 0a82d aaa11 a2a8f a0aa0 
		# 082b0 020b8 0083c 0021e 0008f  N/A   N/A   N/A  


		#for filename in ["byte_15.txt"]:	#1,1 in under 200	!	
		#  N/A  a08b6 0823b aa09a 0a82d aaa11 a2a8f a0aa0 
		#  N/A  020b8  N/A   N/A   N/A   N/A   N/A   N/A 			

		#these need some counter bits...
		#for filename in ["data_1_bit_per_byte_raw.txt","data_1_bit_per_byte_raw_2.txt","data_1_bit_per_byte_raw_3.txt","data_1_bit_per_byte_raw_4.txt"]:#,"../data_1_bit_per_byte_raw.txt"]: 1 does byte 4 up to 9, 2 does 16, 3 to 29, 4 up to 46   all end with 777 with new zeros			
		#for filename in ["byte_15.txt", "data_1_bit_per_byte_raw.txt",]:

			iterate_file(dirname+filename, print_lines = False)
		print("bit_values =", bit_values)
		print_bit_values(bit_values)
		sys.exit()


	#after byte_15:
	bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]


	#get row 1  success!
	if 0:
		dirname = "data_captures/"
		#1,6 by 14500, 2 byte ; 1,7 39200 ; 2,0 56000
		#for filename in ["test_0s_20_70_147_symbols.txt"]: #end with 777

		#1,7 by 24000 ; 2,0 73,000; 2,1 81000, 2,2 147,000
		#for filename in ["test_0s_100_40_11_symbols_3.txt"]: #end with 777

		# 1,7 32k  2,1 82k
		#for filename in ["test_0s_50_40_11_symbols_4.txt"]:

		#1,7 40k   
		#for filename in ["test_0s_50_40_11_symbols_5.txt", "test_0s_50_40_11_symbols_6.txt", "test_0s_50_40_11_symbols_7.txt", "test_0s_50_40_11_symbols_8.txt"]: #end with 777
		#1.6 15k end
		#for filename in ["test_0s_50_40_11_symbols_6.txt", "test_0s_50_40_11_symbols_7.txt", "test_0s_50_40_11_symbols_8.txt"]: #end with 777
		#1.6 11k,
		#for filename in ["test_0s_50_40_11_symbols_7.txt", "test_0s_50_40_11_symbols_8.txt"]: #end with 777

		#odd!  1,7 20300 2,0 70k   fastest to 1,7
		for filename in ["test_0s_50_40_11_symbols_8.txt"]: #odd!!!  end with 777
			#pattern = '6 5 0 3' # 			transitions of 2nd byte,  	count=2   counter started even
			#if comp_count <=0  and  line[0:7] == '2 7 5 1': comp_count = 8 #[248] - [6]                             transitions of 2nd byte  even
			pattern = '0 0 6 1'#			transitions of 2nd byte, display 2 lines not 8		started odd 		-- test_0s_50_40_11_symbols_8.txt
		#very different counter lcations
		#for filename in ["test_glitched_100_40_11_symbols.txt","test_glitched_100_40_11_symbols_2.txt","test_glitched_100_40_11_symbols_3.txt","test_glitched_100_40_11_symbols_4.txt","test_glitched_100_40_11_symbols_b.txt"]:#also 777. where did I get those zeros???

		#1,7 40k, 2,0 56k, 2,1 154k... more?
		#for filename in ["test_0s_20_70_147_symbols.txt"]:

		#1,4 4k "generated_data_byte_captures/eleven_0s.txt"
			test_transitions(dirname+filename, pattern, increment = 100000, limit = 20300, print_lines = False)

		print("bit_values =", bit_values)
		print_bit_values(bit_values)
		sys.exit()


	bit_values = [[None, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]

	#get row 2 by trans    FAIL
	if 0:
		dirname = "data_captures/"

		'''
		doing these by trans does nothing for the first 4 bytes!!!!!
		# row 0 1 2 5 6 7 8 9 10 11 12 2300, [3,0] 2500, [3,1] 3200, [3,2] 4500, [3,3] 7100   11500
		#for filename in ["test_glitched_100_40_11_symbols_b.txt"]: # _b is cleaner than orig        1M

		#hardly anything until 700,  012 5-12 2300, 3,0 2500, 3,1 3200 3,2 4500...
		#for filename in ["test_glitched_100_40_11_symbols_2.txt"]:  #4M   hardly anything until 700, 

		#hardly anything until 700,  012 5-12 2300, 3,0 2500, 3,1 3200 3,2 4500...
		#for filename in ["test_glitched_100_40_11_symbols_3.txt"]: #7M

		#hardly anything until 700,  012 5-12 2300, 3,0 2500, 3,1 3200 3,2 4500...
		for filename in ["test_glitched_100_40_11_symbols_4.txt"]: 
		'''



		#1,6 by 14500, 2 byte ; 1,7 39200 ; 2,0 56000
		#220k none
		for filename in ["test_0s_20_70_147_symbols.txt"]: #end with 777

		#1,7 by 24000 ; 2,0 73,000; 2,1 81000, 2,2 147,000
		#80k none
		#for filename in ["test_0s_100_40_11_symbols_3.txt"]: #end with 777

		# 1,7 32k  2,1 82k
		#150k none
		#for filename in ["test_0s_50_40_11_symbols_4.txt"]:

		#1,7 40k    none???
		#for filename in ["test_0s_50_40_11_symbols_5.txt", "test_0s_50_40_11_symbols_6.txt", "test_0s_50_40_11_symbols_7.txt", "test_0s_50_40_11_symbols_8.txt"]: #end with 777
		#1.6 15k end
		#for filename in ["test_0s_50_40_11_symbols_6.txt", "test_0s_50_40_11_symbols_7.txt", "test_0s_50_40_11_symbols_8.txt"]: #end with 777
		#1.6 11k,
		#for filename in ["test_0s_50_40_11_symbols_7.txt", "test_0s_50_40_11_symbols_8.txt"]: #end with 777

		#odd!  1,7 20300 2,0 70k   fastest to 1,7
		#for filename in ["test_0s_50_40_11_symbols_8.txt"]: #odd!!!  end with 777


			#pattern = '6 5 0 3' # 			transitions of 2nd byte,  	counter started even
			#pattern = '2 7 5 1 2 4 3 5': comp_count = 8 #[248, 255] - [6,0]             transitions of 3rd byte

			pattern = '6 5 0 3 4 4 4 7' #[254, 255]   even
			#pattern = '6 5 0 3 4 4 4 7 5 0 6 0'# 254,255,255 even

			print(compute_experimental.compute([0x80, 0x87, 0x00, 254, 255, 255], 4*6*[0], ignore = 5, print_error=False,)[12:] )
			#print(compute_experimental.compute([0x80, 0x87, 0x00, 255, 255], 4*5*[0], ignore = 5, print_error=False,)[12:] )   #odd
			#sys.exit()

			#pattern = '0 0 6 1 4 3 2 7'# [255, 255]				transitions of 3rd		started odd 	
		#very different counter lcations
		#for filename in ["test_glitched_100_40_11_symbols.txt","test_glitched_100_40_11_symbols_2.txt","test_glitched_100_40_11_symbols_3.txt","test_glitched_100_40_11_symbols_4.txt","test_glitched_100_40_11_symbols_b.txt"]:#also 777. where did I get those zeros???

		#1,7 40k, 2,0 56k, 2,1 154k... more?
		#for filename in ["test_0s_20_70_147_symbols.txt"]:

		#1,4 4k "generated_data_byte_captures/eleven_0s.txt"
			test_transitions(dirname+filename, pattern, increment = 10000, limit = 999999999, print_lines = False)


	#get row 2 iterate
	if 0:
		dirname = "generated_data_byte_captures/"	
		#these don't increment
		# 1 does [byte 4] up to 9, 2 does 16, 3 to 29, 4 up to 46    all end with 777 with new zeros		
		#for filename in ["data_1_bit_per_byte_raw.txt"]: #012 5-12 and 3,0 1800   			  3,1 3400  end 5400
		for filename in ["data_1_bit_per_byte_raw_2.txt"]: #012 5-12 and 3,0 1630  			  3,1 3200...
		#for filename in ["data_1_bit_per_byte_raw_3.txt"]: #012 5-12 2000,         		  3,0 2700, 3,1 3400...
		#for filename in ["data_1_bit_per_byte_raw_4.txt"]: #hardly til 700,  012 5-12 2300,   3,0 2500, 3,1 3200 3,2 4500...

			iterate_file(dirname+filename, limit = 1630, increment = 2000, print_lines = False)
		print("bit_values =", bit_values)
		print_bit_values(bit_values)

	bit_values = [[664227, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, 8711, 690308], [41506, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, 688279, 663596, 34838, 8715], [690306, 41505, 698519, 666156, 35478, 8875, 690354, 41529], [698523, 666154, 35477, 697005, 665777, 657983, 656024, 32940], [8246, 2075, 688650, 41093, 698405, 666133, 658061, 656033], [655543, 655420, 32798, 8207, 690176, 41472, 10368, 2592], [656, 168, 52, 26, 13, 688129, 663559, 657412], [33282, 8321, 690215, 664084, 34954, 8741, 690325, 664109], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]

	if 0:
		dirname = "data_captures/"


		#these increment so I could use transistions!
		#45 slow   cant get 4,0 without 0,0?
		# all but 4,0 (after 1-bit data) in 70
		#for filename in ["test_glitched_100_40_11_symbols_b.txt","test_glitched_100_40_11_symbols_2.txt","test_glitched_100_40_11_symbols_3.txt","test_glitched_100_40_11_symbols_4.txt"]: # _b is cleaner than orig
		#45 slow
		#for filename in ["test_glitched_100_40_11_symbols_2.txt"]: 
		#45 slow
		#for filename in ["test_glitched_100_40_11_symbols_3.txt"]: 
		#45 slow
		for filename in ["test_glitched_100_40_11_symbols_4.txt"]:  #70, [4,0] 3700
		


		#dirname = "generated_data_byte_captures/"	
		#0,0 2,0
		#for filename in ["byte_15.txt"]:		


		#these don't increment
		# 1 does [byte 3] up to 9, 2 does 16, 3 to 29, 4 up to 46    all end with 777 with new zeros	

		#012 5-12 and 3,0 1800    3,1 3400  end 5400
		#for filename in ["data_1_bit_per_byte_raw.txt"]:

		#012 5-12 and 3,0 1700    3,1 3200...
		#for filename in ["data_1_bit_per_byte_raw_2.txt"]:

		#012 5-12 2000, 3,0 2700, 3,1 3400...
		#for filename in ["data_1_bit_per_byte_raw_3.txt"]:

		#hardly anything until 700,  012 5-12 2300, 3,0 2500, 3,1 3200 3,2 4500...
		#for filename in ["data_1_bit_per_byte_raw_4.txt"]:
			iterate_file(dirname+filename, limit = 9999999999999, increment = 100, print_lines = False)
		print("bit_values =", bit_values)
		print_bit_values(bit_values)

	bit_values = [[664227, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, 8711, 690308], [41506, None, None, None, None, None, None, None], [688273, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, 688279, 663596, 34838, 8715], [690306, 41505, 698519, 666156, 35478, 8875, 690354, 41529], [698523, 666154, 35477, 697005, 665777, 657983, 656024, 32940], [8246, 2075, 688650, 41093, 698405, 666133, 658061, 656033], [655543, 655420, 32798, 8207, 690176, 41472, 10368, 2592], [656, 168, 52, 26, 13, 688129, 663559, 657412], [33282, 8321, 690215, 664084, 34954, 8741, 690325, 664109], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
	

	if 0:
		dirname = "generated_data_byte_captures/"	
		#dirname = "data_captures/"
		for filename in ["byte_15.txt","byte_14.txt","byte_13.txt",]:
			iterate_file(dirname+filename, limit = 9999999999999, increment = 100, print_lines = False)
		print("bit_values =", bit_values)
		print_bit_values(bit_values)


	bit_values = [[664227, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, 8711, 690308], [41506, None, None, None, None, None, None, None], [688273, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, 688279, 663596, 34838, 8715], [690306, 41505, 698519, 666156, 35478, 8875, 690354, 41529], [698523, 666154, 35477, 697005, 665777, 657983, 656024, 32940], [8246, 2075, 688650, 41093, 698405, 666133, 658061, 656033], [655543, 655420, 32798, 8207, 690176, 41472, 10368, 2592], [656, 168, 52, 26, 13, 688129, 663559, 657412], [33282, 8321, 690215, 664084, 34954, 8741, 690325, 664109], [None, None, None, None, None, None, None, None], [663589, 657429, 655885, 655489, 655399, 655380, 32778, None], [690181, 664069, 657541, 655909, 655509, 655405, 655377, 655375]]
	

	if 0:
		dirname = "generated_data_byte_captures/"	
		#dirname = "data_captures/"
		#for filename in ["byte_15.txt","byte_14.txt","byte_13.txt",]:

		#              3,1 700   3,2 2100  3,3 4700 (5400)  ,   3,4 4500        (5000),     (7500)                    , 3,5 1900
		for filename in ["data_1_bit_per_byte_raw.txt","data_1_bit_per_byte_raw_2.txt","data_1_bit_per_byte_raw_3.txt","data_1_bit_per_byte_raw_4.txt"]:#,"../data_1_bit_per_byte_raw.txt"]: 1 does byte 4 up to 9, 2 does 16, 3 to 29, 4 up to 46   all end with 777 with new zeros			

			iterate_file(dirname+filename, limit = 9999999999999, increment = 100, print_lines = False)
		print("bit_values =", bit_values)
		print_bit_values(bit_values)

	bit_values = [[664227, 657590, 33339, 696474, 43053, 698897, 666255, 658080], [33456, 8376, 2108, 542, 143, 688160, 40976, 10248], [2564, 642, 161, 688183, 663580, 34830, 8711, 690308], [41506, 10385, 690735, 664208, 34984, 8756, None, None], [688273, 663599, 657424, 33288, 8324, 2082, 529, 688271], [663584, 34832, 8712, 2180, 546, 145, 688175, 663568], [34824, 8708, 2178, 545, 688279, 663596, 34838, 8715], [690306, 41505, 698519, 666156, 35478, 8875, 690354, 41529], [698523, 666154, 35477, 697005, 665777, 657983, 656024, 32940], [8246, 2075, 688650, 41093, 698405, 666133, 658061, 656033], [655543, 655420, 32798, 8207, 690176, 41472, 10368, 2592], [656, 168, 52, 26, 13, 688129, 663559, 657412], [33282, 8321, 690215, 664084, 34954, 8741, 690325, 664109], [None, None, None, None, None, None, None, None], [663589, 657429, 655885, 655489, 655399, 655380, 32778, None], [690181, 664069, 657541, 655909, 655509, 655405, 655377, 655375]]

	if 1:
		dirname = "generated_data_byte_captures/"	
		#dirname = "data_captures/"
		#for filename in ["byte_15.txt","byte_14.txt","byte_13.txt",]:

		#              3,1 700   3,2 2100  3,3 4700 (5400)  ,   3,4 4500        (5000),     (7500)                    , 3,5 1900 (end 11500)
		for filename in ["data_1_bit_per_byte_raw.txt","data_1_bit_per_byte_raw_2.txt","data_1_bit_per_byte_raw_3.txt","data_1_bit_per_byte_raw_4.txt"]:#,"../data_1_bit_per_byte_raw.txt"]: 1 does byte 4 up to 9, 2 does 16, 3 to 29, 4 up to 46   all end with 777 with new zeros			

			iterate_file(dirname+filename, limit = 9999999999999, increment = 100, print_lines = False)
		print("bit_values =", bit_values)
		print_bit_values(bit_values)

	if 0:
		dirname = "generated_data_byte_captures/"
		#for filename in ["data_1_bit_per_byte_raw_4.txt"]:
		#dirname = "data_captures/"
		#nada for filename in ["test_0s_50_40_11_symbols_5.txt", "test_0s_50_40_11_symbols_6.txt", "test_0s_50_40_11_symbols_7.txt", "test_0s_50_40_11_symbols_8.txt"]: #end with 777
		#nada for filename in ["test_0s_20_70_147_symbols.txt", "test_0s_100_40_11_symbols_3.txt", "test_0s_50_40_11_symbols_4.txt", "test_0s_50_40_11_symbols_5.txt", 		"test_0s_50_40_11_symbols_6.txt", "test_0s_50_40_11_symbols_7.txt", "test_0s_50_40_11_symbols_8.txt"]: #these lines end with 7 7 7
		for filename in ["data_1_bit_per_byte_raw.txt","data_1_bit_per_byte_raw_2.txt","data_1_bit_per_byte_raw_3.txt","data_1_bit_per_byte_raw_4.txt"]:#,"../data_1_bit_per_byte_raw.txt"]: 1 does byte 4 up to 9, 2 does 16, 3 to 29, 4 up to 46   all end with 777 with new zeros			
		#for filename in ["test_glitched_100_40_11_symbols.txt","test_glitched_100_40_11_symbols_2.txt","test_glitched_100_40_11_symbols_3.txt","test_glitched_100_40_11_symbols_4.txt","test_glitched_100_40_11_symbols_b.txt"]:#also 777. where did I get those zeros???
		#for filename in ["byte_15.txt","byte_14.txt","byte_13.txt",]:
			pattern = '6 5 0 3 4 4 4 7' #[254, 255]   even
			#pattern = '6 5 0 3 4 4 4 7 5 0 6 0'# 254,255,255 even
			#pattern = '0 0 6 1 4 3 2 7 5 0 6 0'#odd


			#print(compute_experimental.compute([0x80, 0x87, 0x00, 254, 255, 255,0,0], 4*8*[0], ignore = 5, print_error=False,)[12:] )
			test_transitions(dirname+filename, pattern, increment = 10000, limit = 999999999, print_lines = True)
		print("bit_values =", bit_values)
		print_bit_values(bit_values)


	#obsolete    just do transistions only, for speed after finding the low bits
	if 0:
		OUTPUT_LINES = False
		dirname = "data_captures/"
		#1,6 by 14500, 2 byte ; 1,7 39200 ; 2,0 56000
		#for filename in ["test_0s_20_70_147_symbols.txt"]: #end with 777

		#1,7 by 24000 ; 2,0 73,000; 2,1 81000, 2,2 147,000
		#for filename in ["test_0s_100_40_11_symbols_3.txt"]: #end with 777

		# 1,7 32k  2,1 82k
		#for filename in ["test_0s_50_40_11_symbols_4.txt"]:

		#1,7 40k   
		#for filename in ["test_0s_50_40_11_symbols_5.txt", "test_0s_50_40_11_symbols_6.txt", "test_0s_50_40_11_symbols_7.txt", "test_0s_50_40_11_symbols_8.txt"]: #end with 777
		#1.6 15k end
		#for filename in ["test_0s_50_40_11_symbols_6.txt", "test_0s_50_40_11_symbols_7.txt", "test_0s_50_40_11_symbols_8.txt"]: #end with 777
		#1.6 11k,
		#for filename in ["test_0s_50_40_11_symbols_7.txt", "test_0s_50_40_11_symbols_8.txt"]: #end with 777

		#odd!  1,7 21k 2,0 70k
		#for filename in ["test_0s_50_40_11_symbols_8.txt"]: #end with 777

		#very different counter lcations
		#for filename in ["test_glitched_100_40_11_symbols.txt","test_glitched_100_40_11_symbols_2.txt","test_glitched_100_40_11_symbols_3.txt","test_glitched_100_40_11_symbols_4.txt","test_glitched_100_40_11_symbols_b.txt"]:#also 777. where did I get those zeros???

		#1,7 40k, 2,0 56k, 2,1 154k... more?
		#for filename in ["test_0s_20_70_147_symbols.txt"]:

		#dirname = "generated_data_byte_captures/"
		#1,4 4k
		for filename in ["eleven_0s.txt"]: 
			
			with open(dirname+filename, "r") as infile:	
				print("\n\nUsing:", filename)
				#print batches at transitions to help figure out math
				#num = 5+256*2
				#p = False
				#x = -1
				comp_count = 0
				increment = 10000
				long_count = 0
				compute_last_sol = True
				line = infile.readline()
				while line:
					if long_count % increment  == 0: print(long_count)   #100 okay for 2 byte transm 1000 for 3


					#if comp_count <=0  and  line[0:15] == '2 7 5 1 2 4 3 5': comp_count = 8 #[248, 255] - [6,0]             transitions of 3rd byte
					#if comp_count <=0  and  line[0:7] == '2 7 5 1': comp_count = 8 #[248] - [6]                             transitions of 2nd byte
					
					if comp_count <=0 and line[0:7] == '6 5 0 3': # 0, 6, 3, 4, 1, 0, 2, 4, 1, 3, 5, 5			transitions of 2nd byte, display 2 lines not 8   	counting evens
					#if comp_count <=0 and line[0:7] == '0 0 6 1': #0 5 1 0 3 5 0 2 1 4 7 5 2 6 1 4				transitions of 2nd byte, display 2 lines not 8		started odd 		)test_0s_50_40_11_symbols_8)
						comp_count = 2
						compute_last_sol = True
						increment = 1000
					

					#for use with glitch data
					#if comp_count <= 0 and line[0:40] == '4 2 1 0 7 0 6 1 3 2 4 2 2 2 7 5 0 7 5 5 ':
					#if comp_count <- 0 and line[0:48] == '4 2 1 0 7 0 6 1 3 2 4 2 2 2 7 5 4 3 3 2 5 0 5 2 ':  # what is this for?
					#	comp_count = 8

					#get the first line of a batch
					if compute_last_sol:
						compute_last_sol = False
						symbols = [0,0,4,4,2,7,7,4,6,7,5,6,] + [int(n) for n in line.split(' ')[0:74]] + [0,0]
						last_solution = solver([0]*(len(symbols)//4),symbols, debug=False, ignore=8-3, print_error=False, print_result=False)
						if last_solution == "Impossible":
							print(long_count, "comp_count =", comp_count, "last_solution =", last_solution,"skipping lines")
							comp_count = 0;
						else:
							if OUTPUT_LINES:
								print("-----")
								print("".join("{:3d} ".format(num) for num in last_solution[3:]))
							last_crc_value = last_solution[-1]*65536 +last_solution[-2]*256 + last_solution[-3]


					elif comp_count>0:  #compute a number of lines when comp_count is positive
						symbols = [0,0,4,4,2,7,7,4,6,7,5,6,] + [int(n) for n in line.split(' ')[0:74]] + [0,0]
						solution = solver([0]*(len(symbols)//4),symbols, debug=False, ignore=8-3, print_error=False, print_result=False)

						if solution == "Impossible":
							print(long_count, comp_count, solution)
							line = infile.readline()
							continue

						if OUTPUT_LINES: 
							print("".join("{:3d} ".format(num) for num in solution[3:]))
							#print(symbols[12:12+16])

						crc_value = solution[-1]*65536 +solution[-2]*256 + solution[-3]
						#xor_sol = [solution[x]^last_solution[x] for x in [3,4,5]]
						find_bits(solution,last_solution,print_too_many=False) #xor packets when too many unknowns
						#find_bits(solution)

						#if solution[3] == 255:
						#	print("".join("{:3d} ".format(num) for num in solution))
						#	print(line)
						#	sys.exit()


						'''
						symbols = [int(n) for n in line.split(' ')[0:20]]
						solution = solver([0,0,0], symbols, debug=False, ignore=8, print_error=False, print_result=False)
						print
						print("{:6}: {} [{:3}, {:3}, {:3}] [{:08b}, {:08b}, {:08b}]".format(x, symbols[0:20], solution[0], solution[1],solution[2], solution[0], solution[1],solution[2]))
						comp_count -= 1
						if not comp_count and p: print()
						'''
					#if (x-64)%(128*256) == 10: print()
					comp_count -= 1
					long_count += 1
					line = infile.readline()
					#if not x % 1000: input("Press any key to continue...")			
		print("\nbit_values =", bit_values)
		print_bit_values(bit_values)	



	#iterate through files
	if 0 :
		OUTPUT = False
		dirname = "data_captures/"
		#for filename in ["test_0s_20_70_147_symbols.txt", "test_0s_100_40_11_symbols_3.txt", "test_0s_50_40_11_symbols_4.txt", "test_0s_50_40_11_symbols_5.txt", 		"test_0s_50_40_11_symbols_6.txt", "test_0s_50_40_11_symbols_7.txt", "test_0s_50_40_11_symbols_8.txt"]: #these lines end with 7 7 7
		#for filename in ["test_0s_20_70_147_symbols.txt" ]:  #long... all 0, at lesat 1,3 around 1200
		#for filename in ["test_0s_100_40_11_symbols_3.txt"]:# hrough 1,1 by 500
		#, "test_0s_50_40_11_symbols_4.txt", "test_0s_50_40_11_symbols_5.txt", 		"test_0s_50_40_11_symbols_6.txt", "test_0s_50_40_11_symbols_7.txt", "test_0s_50_40_11_symbols_8.txt"]: #these lines end with 7 7 7

			
		#for filename in ["test_glitched_100_40_11_symbols.txt","test_glitched_100_40_11_symbols_2.txt","test_glitched_100_40_11_symbols_3.txt","test_glitched_100_40_11_symbols_4.txt","test_glitched_100_40_11_symbols_b.txt"]:
		#for filename in ["test_glitched_100_40_11_symbols_b.txt","test_glitched_100_40_11_symbols_2.txt","test_glitched_100_40_11_symbols_3.txt","test_glitched_100_40_11_symbols_4.txt"]: # _b is cleaner than orig
		
		dirname = "generated_data_byte_captures/"	
		#for filename in ["eleven_0s.txt"]: #1,0 by 300   1,3 by 2200
		for filename in ["byte_15.txt"]:	#1,1 in under 200	!	

		#these need some counter bits...
		#for filename in ["data_1_bit_per_byte_raw.txt","data_1_bit_per_byte_raw_2.txt","data_1_bit_per_byte_raw_3.txt","data_1_bit_per_byte_raw_4.txt"]:#,"../data_1_bit_per_byte_raw.txt"]: 1 does byte 4 up to 9, 2 does 16, 3 to 29, 4 up to 46   all end with 777 with new zeros			
		#for filename in ["byte_15.txt", "data_1_bit_per_byte_raw.txt",]:

			iterate_file(dirname+filename, print_lines = True)

		print("bit_values =", bit_values)
		print_bit_values(bit_values)


	#test crafted/collected data. I think this is obsolete now that I have the 1bit data
	if 0:
		for record in collected_data:
			line = record[1]

			#baseline_crc_value = crc_list.baseline_crc_value #crc for all 0s
			#computed_crc_value = compute_crc(last_solution)			
			#if not (computed_crc_value==last_crc_value): sys.exit(1)
			
		

			print(line)
			print(len(line.split(' ')))

			symbols = [0,0,4,4,2,7,7,4,6,7,5,6,] + [int(n) for n in line.split(' ')[0:74]] + [0,0]
			solution = solver([0]*(len(symbols)//4),symbols, debug=False, ignore=8-3, print_error=False, print_result=False)
			print("".join("{:3d} ".format(num) for num in solution))
			if solution == "Impossible":
				print(count, solution)
				line = infile.readline()
				continue

			#find a pattern for another test
			#if solution[7] == 248: 
			#	print("".join("{:3d} ".format(num) for num in solution))
			#	print(line)

			crc_value = solution[-1]*65536 +solution[-2]*256 + solution[-3]
			#xor_sol = [solution[x]^last_solution[x] for x in range(3,depth+3)]   #xor vs previous value if I don't have a baseline value for 0,0,0...
			#xor_sol = [solution[x] for x in range(3,depth+3)]
			find_bits(solution)



		print_bit_values(bit_values)
			#print("\n#{} total packets {} impossibles, {} major errors, {} skips, {} doubles".format(x+1, imps, majors, skips, dbls))	

	#verify crc calc using some known values
	if 0:
		zeros_symbols =   compute_experimental.dzeros_symbols[:4*24] + [int(c) for c in str(crcs[51])] + [0,0]
		known=[
		[0,0,51],
		[1,49,1583],  
		[2, 107, 3432],
		[4, 7, 225],
		[7, 72, 2314],
		[8, 17, 545],
		[11, 91, 2920],]
		


		last_solution = [128, 135, 0] +  [0, 0, 0, 0, 2] + 11*[0]
		last_crc_value = crcs_values[3432]

		sorted_crcs_values = crcs_values.copy()
		sorted_crcs_values.sort()


		baseline_crc_value = last_crc_value 
		#print("baseline_crc_value starts as {:05x}".format(baseline_crc_value))
		for i in range(0,depth):
			for x in range(0,8):
				if (last_solution[i+3]&pow(2,x)):
					baseline_crc_value ^= bit_values[i][x]
					print("byte {} bit {} ^= {:05x}".format(i,x,bit_values[i][x]))

		computed_crc_value = baseline_crc_value
		print("baseline_crc_value starts as {:05x}".format(computed_crc_value))
		print("baseline index is:", crcs_values.index(baseline_crc_value))
		for i in range(0,depth):
			#print(hex(computed_crc_value))
			for x in range(0,8):
				if bit_values[i][x]:
					if (last_solution[i+3]&pow(2,x)):
						computed_crc_value ^= bit_values[i][x]
						#print("byte {} bit {} ^= {:05x}".format(i,x,bit_values[i][x]))
		print(computed_crc_value==last_crc_value)


		print("bit 0 value:", baseline_crc_value ^ crcs_values[1583])
		#sys.exit()


		for q in known:
			solution = [128, 135, 0] +  [0, 0, 0, 0, q[0]] + 11*[0]
			print(solution)
			computed_crc_value = baseline_crc_value
			#print("baseline_crc_value starts as {:05x}".format(computed_crc_value))
			for i in range(0,depth):
				#print(hex(computed_crc_value))
				for x in range(0,8):
					if bit_values[i][x]:
						if (solution[i+3]&pow(2,x)):
							computed_crc_value ^= bit_values[i][x]
							#print("byte {} bit {} ^= {:05x}".format(i,x,bit_values[i][x]))

			print("crc", computed_crc_value)
			print("index by arbitrary symbol pick", crcs_values.index(computed_crc_value))
			print("index by sorted values",sorted_crcs_values.index(computed_crc_value))
			print("crcs_values_51 index", crcs_values_51.index(computed_crc_value))
			print("crcs_values_4035 index",crcs_values_4035.index(computed_crc_value))

			ncrc_symbols = [int(c) for c in str(crcs[crcs_values.index(computed_crc_value)])] + [0, 0]
			nsolution = guesser.solver([0]*4, [5,2,7,7,]+ncrc_symbols, debug=False, ignore=8+16-1, print_error=False, print_result=False, default=False, zeros_symbols=zeros_symbols)
			print("crc solution using base of 51", nsolution)
			nvalue = nsolution[-1]*65536 +nsolution[-2]*256 + nsolution[-3]
			print("index of that by sorted value", hex(sorted_crcs_values.index(nvalue)))
			
			if crcs_values.index(computed_crc_value) != q[2]:
				print("compute failed")
				#print(solution)
				#print("crc_value", hex(crc_value), "computed_crc_value", hex(computed_crc_value), "difference", hex(crc_value^computed_crc_value))
				#print(count)
				#sys.exit()
			else: print("SUCCESS\n")
			

	#calc crc for packets of 0s
	if 0:
		for x in range(0,256):
			solution = [218,135,0, 0,0,0,0,x, 0,0,0,0,0,0,0,0, 0,0,0]
			crc_value = compute_crc(solution)
			if crc_value:
				print("{:3d}: {:3d} {:4d}".format(x, crcs_values.index(crc_value)//32, crcs_values.index(crc_value)))

	#calc crc for packets of 10,10,10,0,length,0s...
	if 0:
		for x in range(0,256):
			solution = [218,135,0, 10,10,10,0,x, 0,0,0,0,0,0,0,0, 0,0,0]
			crc_value = compute_crc(solution)
			if crc_value:
				print("{:3d}: {:3d} {:4d}".format(x, crcs_values.index(crc_value)//32, crcs_values.index(crc_value)))				