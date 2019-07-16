import numpy


class Deck:
    def __init__(self, sets_num):
        self.sets_num  = sets_num
        self.deck_size = self.sets_num*52
        self.create_deck()
        self.shuffle_deck()
        return None

    def create_deck(self):
        self.deck = numpy.zeros([self.deck_size,2])
        self.pos  = 0
        for d in range(self.sets_num):
            for suit in range(4):
                for num in range(13):
                    self.deck[d*52 + suit*13 + num][0] =  int(suit + 1)
                    self.deck[d*52 + suit*13 + num][1] =  int(num + 1)
        return None
        
    def get_deck_size(self):
        return self.deck_size
        
    def shuffle_deck(self):
        numpy.random.shuffle(self.deck)
        self.pos = 0
        return None

    def print_deck(self):
        for i in range(self.deck_size):
            print(self.deck[i])
        return None

    def deal_card(self):
        if(self.pos >= self.deck_size):
            self.shuffle_deck()
        card = self.deck[self.pos]
        self.pos += 1	
        return card

    def deal_hand(self,num):
        hand = numpy.zeros([num,2])
        for i in range(num):
            hand[i] = self.deal_card()
        return hand




