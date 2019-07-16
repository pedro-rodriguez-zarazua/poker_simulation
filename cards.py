import numpy
import pandas


def sort_hand(hand):
	hand_reshape = numpy.reshape(hand,(len(hand),2))
	hand_df      = pandas.DataFrame(hand_reshape, columns=['fig','num'],dtype=int)
	sorted_hand  = hand_df.sort_values(by =['num','fig'])
	return(sorted_hand)

#Cuenta cuantas cartas hay de un mismo kind
def list_kind(hand):
	kinds  = numpy.zeros(5)
	h      = hand.iloc[0,1]
	if(h == 1):
		h = 14
	c = 1
	for i in range(1, hand.shape[0] + 1):
		if(i == hand.shape[0]):
			num = 100
		else:
			num = hand.iloc[i,1]
			if(num == 1):
				num = 14
		if(num == h):
			c += 1
		else:
			if(c == 1):
				if(h > kinds[0]):
					kinds[0] = h
			elif(c == 2):
				if(h > kinds[2]):
					kinds[1] = kinds[2]
					kinds[2] = h
				else:
					kinds[1] = h
			elif(c < 5):
				if(h > kinds[c]):
					kinds[c] = h
			else:
				if(h > kinds[4]):
					kinds[4] = h
			h = num
			c = 1
	#print(kinds)
	return(kinds)

#Cuenta cuantas cartas hay de un mismo color
def list_flush(hand):
	flush = numpy.zeros([4,2])
	for i in range(hand.shape[0]):
		fig = hand.iloc[i,0] - 1
		num = hand.iloc[i,1]
		if(num == 1):
			num = 14
		flush[fig,0]  += 1
		if(flush[fig, 1] < num):
			flush[fig,1] = num
	#print(flush)
	return(flush)

#Cuenta cuantas cartas hacen escalera
def list_straight(hand):	
	num                 = hand.iloc[0,1]
	fig                 = hand.iloc[0,0]

	color_high  		= numpy.zeros(5)
	color_high[0]       = num
	color_high[fig]     = num

	color_count 		= numpy.zeros(5)
	color_count[0]      = 1
	color_count[fig]    = 1
	
	straight  			= numpy.zeros([5,2])
	straight[0,1]		= num
	straight[0,0]		= 1
	straight[fig,1]		= num
	straight[fig,0]     = 1

	for i in range(1, hand.shape[0]):
		num   = hand.iloc[i,1]
		fig   = hand.iloc[i,0]
		if(num > hand.iloc[i-1,1] + 1):
			for i in range(1,len(color_count)):
				color_count[i]  = 0
			color_count[0]    = 1
			color_count[fig]  = 1
			color_high[0]     = num
			color_high[fig]   = num
		else:
			if(num == hand.iloc[i-1,1] + 1):
				color_high[0]     = num
				color_count[0]    += 1
			if(num == color_high[fig] + 1):
				color_count[fig]  += 1
			else:
				color_count[fig]  = 1
			color_high[fig]   = num

		for i in range(0, len(color_count)):
			if(straight[i,0] <= color_count[i] and straight[i,1] < color_high[i]):
				straight[i,0] = color_count[i]				
				straight[i,1]  = color_high[i]
	if(straight[0,1] == 13 and hand.iloc[0,1] == 1):
		straight[0,1]   = 14
		straight[0,0]  += 1
		for i in range(1, len(color_count)):
			indice = 0
			while(hand.iloc[indice, 1] == 1 and indice < hand.shape[0]):
				if(straight[i,1] == 13 and hand.iloc[indice, 0] == i):
					straight[i,1]   = 14
					straight[i,0] += 1
				indice += 1
	#print(straight)
	return(straight)

def hand_value(hand):
	straight   = list_straight(hand)
	kind       = list_kind(hand)
	flush	   = list_flush(hand)	
	hand_class = int(0)
	
	if(hand_class == 0):
		#Straight flush
		straight_flush_high = 0
		for i in range(1,straight.shape[0]):
			if(straight[i,0] >= 5):
				if(straight[i,1] > straight_flush_high):
					straight_flush_high  = straight[i,1]
					straight_flush_color = i
		if(straight_flush_high > 0):
			hand_class = 9
			hand_list  = numpy.array((straight_flush_high,straight_flush_color))
			#print('Color Straight')
	
	if(hand_class == 0):
		#Poker
		if(kind[4] > 0):
			hand_class = 8
			hand_list  = kind[4]
			#print('Poker')
	
	if(hand_class == 0):
		#Full
		if(kind[3] > 0 and kind[2] > 0):
			hand_class = 7
			hand_list  = numpy.array((kind[3],kind[2]))
			#print('Full')
	
	if(hand_class == 0):
		#Flush
		for i in range(flush.shape[0]):
			flush_high = 0
			if(flush[i, 0] >= 5):
				if(flush[i,1] > flush_high):
					flush_high  = flush[i,1]
					flush_color = i + 1
		if(flush_high > 0):
			hand_class = 6
			hand_list  = numpy.array((flush_high, flush_color))
			#print('Flush')
	
	if(hand_class == 0):
		#Straight
		if(straight[0,0] >= 5):	
			hand_class = 5
			hand_list  = straight[0,1]
			#print('Straight')

	if(hand_class == 0):
		#Three of a kind
		if(kind[3] > 0 and kind[2] == 0):
			hand_class = 4
			hand_list  = kind[3]
			#print('Three of a kind')

	if(hand_class == 0):
		#Two pairs
		if(kind[2] > 0 and kind[1] > 0):
			hand_class = 3
			hand_list  = numpy.array((kind[2],kind[1]))
			#print('Two pairs')
	
	if(hand_class == 0):
		#Two of a kind
		if(kind[2] > 0 and kind[1] == 0):
			hand_class = 2
			hand_list  = kind[2]
			#print('Two of a kind')

	if(hand_class == 0):
		#High card
		if(kind[0] > 0 and kind[3] == 0 and kind[2] == 0):
			hand_class = 1
			hand_list  = kind[0]
			#print('High')
	#print(hand_class, hand_list)
	return(hand_class, hand_list)


def best_hand(unsorted_hand, size = 5):
	hand            = sort_hand(unsorted_hand)
	h_class, h_list = hand_value(hand)

	if(hand.shape[0] < size):
		size = hand.shape[0]
	best_hand   = numpy.zeros([size,2])	
				
	#High card	
	if(h_class == 1):
		best_hand = find_best_high(best_hand, hand, size, 0)

	#Two of a kind
	elif(h_class == 2):
		if(h_list == 14):
			pair     = hand.loc[hand['num'] == 1]
			not_pair = hand.loc[hand['num'] != 1]
			for i in range(2):
				pair.iat[i, 1] = 14
		else:
			pair     = hand.loc[hand['num'] == h_list]
			not_pair = hand.loc[hand['num'] != h_list]
		for i in range(2):
			best_hand[i] = pair.iloc[i].values
		best_hand = find_best_high(best_hand, not_pair, size - 2, 2)
	
	#Two pairs
	elif(h_class == 3):
		if(h_list[0] == 14):
			pair1     = hand.loc[hand['num'] == 1]
			not_pair  = hand.loc[hand['num'] != 1]
			for i in range(2):
				pair1.iat[i, 1] = 14
		else:
			pair1     = hand.loc[hand['num'] == h_list[0]]
			not_pair  = hand.loc[hand['num'] != h_list[0]]

		pair2     = hand.loc[hand['num'] == h_list[1]]
		not_pair  = not_pair.loc[not_pair['num'] != h_list[1]]
		for i in range(2):
			best_hand[i] = pair1.iloc[i].values
		for i in range(2,4):
			best_hand[i] = pair2.iloc[i - 2].values
		best_hand = find_best_high(best_hand, not_pair, size - 4, 4)
		
		
	#Three of a kind
	elif(h_class == 4):
		if(h_list == 14):
			trio     = hand.loc[hand['num'] == 1]
			not_trio = hand.loc[hand['num'] != 1]
			for i in range(3):
				trio.iat[i, 1] = 14
		else:
			trio     = hand.loc[hand['num'] == h_list]
			not_trio = hand.loc[hand['num'] != h_list]
		for i in range(3):
			best_hand[i] = trio.iloc[i].values
		best_hand = find_best_high(best_hand, not_trio, size - 3, 3)

	#Straight
	elif(h_class == 5):
		indice = 0
		if(h_list == 14):
			best_hand[indice] = hand.loc[hand['num'] == 1].iloc[0]
			best_hand[0,1] = 14
			indice += 1
		while(indice < size):
			for i in range(hand.shape[0]):
				if(hand.iloc[hand.shape[0] - i - 1, 1] == h_list - indice):
					best_hand[indice] = hand.iloc[hand.shape[0] - i - 1]
			indice += 1
	
	#Flush
	elif(h_class == 6):
		color = hand.loc[hand['fig'] == h_list[1]]	
		if(h_list[0] == 14):
			best_hand[0] = color.iloc[0]
			best_hand[0,1] = 14
			for i in range(1, size):
				best_hand[i] = color.iloc[color.shape[0] - i]		
		else:	
			for i in range(size):
				best_hand[i] = color.iloc[color.shape[0] - i - 1]		
		
		
	#Full
	elif(h_class == 7):
		trio_high = h_list[0]
		if(trio_high == 14):
			trio_high = 1
			trio = hand.loc[hand['num'] == trio_high]
			for i in range(3):
				trio.iat[i,1]=14
		else:
			trio = hand.loc[hand['num'] == trio_high]

		pair_high = h_list[1]
		if(pair_high == 14):
			pair_high = 1
			pair = hand.loc[hand['num'] == pair_high]
			for i in range(2):
				pair.iat[i,1]=14
		else:
			pair = hand.loc[hand['num'] == pair_high]
		best_hand = numpy.concatenate((trio,pair))

	#Poker
	elif(h_class == 8):
		poker_high = h_list
		if(poker_high == 14):
			poker_high = 1
			poker      = hand.loc[hand['num'] == poker_high]
			for i in range(len(poker)):
				poker.iat[i,1] = 14
		else:
			poker = hand.loc[hand['num'] == poker_high]
		not_poker = hand.loc[hand['num'] != poker_high]
		
		if(len(not_poker) == 0):
			for i in range(len(poker)):
				best_hand[i] = poker.iloc[i]
		else:
			for i in range(4):
				best_hand[i] = poker.iloc[i]
			best_hand = find_best_high(best_hand, not_poker, size - 4, 4)

	#Straight flush
	elif(h_class == 9):
		color = hand.loc[hand['fig'] == h_list[1]]	
		if(h_list[0] == 14):
			best_hand[0] = color.iloc[0]
			best_hand[0,1] = 14
			for i in range(1, size):
				best_hand[i] = color.iloc[color.shape[0] - i]		
		else:	
			for i in range(size):
				best_hand[i] = color.iloc[color.shape[0] - i - 1]
	#print(best_hand)
	return(h_class, best_hand)

def find_best_high(hand, subset, num, pos):
	indice=0
	while(indice < num and subset.iloc[indice, 1] == 1 and indice + pos < hand.shape[0]):
		hand[pos + indice] = subset.iloc[indice]
		hand[pos + indice, 1] = 14
		indice += 1
	for i in range(hand.shape[0] - pos - indice):
		hand[pos + indice + i] = subset.iloc[subset.shape[0] - i - 1]
	return(hand)

def match_hands(h1_class, hand1, h2_class, hand2):
	if(h1_class > h2_class):
		print('Ganador hand 1')
		print(hand1)
	elif(h2_class > h1_class):
		print('Ganador hand 2')
		print(hand2)
	else:
		indice = 0
		while(hand1[indice, 1] == hand2[indice,1] and indice < 5):
			indice += 1
		if(hand1[indice,1] > hand2[indice,1]):			
			print('Ganador hand 1')
			print(hand1)
		elif(hand2[indice,1] > hand1[indice,1]):			
			print('Ganador hand 2')
			print(hand2)
		else:
			print('empate')
			print(hand1)
			print(hand2)

"""
0.- Unchecked
1.- carta alta
2.- par 
3.- doble par
4.- trio
5.- escalera
6.- color
7.- full
8.- poker
9.- escalera de color
"""

def flop_hand_class(pairhand, flop):
	unsorted_hand = numpy.concatenate((pairhand,flop))
	hand = sort_hand(unsorted_hand)
	hc, hl   = hand_value(hand)
	print(hand)
	return(hc,hl)

def hand_class(unsorted_hand):
	for i in range(2):
		if(unsorted_hand[i,1] == 1):
			unsorted_hand[i,1] = 14

	hand       = sort_hand(unsorted_hand)
	hand_class = numpy.zeros(5)
	if(hand.iloc[0].loc['fig'] == hand.iloc[1].loc['fig']):
		hand_class[3] = hand.iloc[1].loc['fig']
	dif = hand.iloc[1].loc['num'] - hand.iloc[0].loc['num']
	if(dif == 0):
		hand_class[4] =  hand.iloc[1].loc['num']
	elif(dif == 1):
		hand_class[2] =  hand.iloc[1].loc['num']
	elif(dif == 2):
		hand_class[1] =  hand.iloc[1].loc['num']
	elif(dif == 3):
		hand_class[1] =  hand.iloc[1].loc['num']
	elif(dif == 4):
		hand_class[1] =  hand.iloc[1].loc['num']
	else:
		hand_class[0] = hand.iloc[1].loc['num']
	return(hand_class)
	
def rank_hand(hand):
	hclass = hand_class(hand)
		
	if(hclass[4] > 0):
		if(hclass[4] >= 10 ):
			rank = 3
		else:
			rank = 2
	
	elif(hclass[3] > 0):
		if(hclass[3] >= 10):
			rank = 3
		elif(hclass[2] >= 8):
			rank = 3
		elif(hclass[3] >= 8):
			rank = 2
		elif(hclass[2] >= 6):
			rank = 2
		elif(hclass[1] >= 8):
			rank = 2
		else:
			rank = 2
	
	elif(hclass[2] > 0 and hclass[3] == 0):
		if(hclass[2] >= 10):
			rank = 3
		elif(hclass[2] >= 8):
			rank = 2
		else:
			rank = 1

	elif(hclass[1] > 0 and hclass[3] == 0):
		if(hclass[1] >= 10):
			rank = 2
		elif(hclass[1] >= 7):
			rank = 1
		else:
			rank = 0
	elif(hclass[0] > 0 and hclass[3] == 0):
		if(hclass[0] >= 10):
			rank = 1
		else:
			rank = 0
	return(rank)

"""
4.- par
3.- color
2.- straight 0 espacios
1.- straight 1,2 o 3 espacios
0.- high
"""

