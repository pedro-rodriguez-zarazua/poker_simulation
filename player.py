import cards
import numpy
import random

class Player:
    def __init__(self, name, ini_stack):
        self.name        = name
        self.stack       = ini_stack
        self.minbet      = 1
        self.in_game     = True
        self.in_round    = False
        self.blind       = 0
        self.play_hand   = False
        self.all_in      = False
        self.reset_all_bets()
        return None 
        
    def set_in_game(self, ingame):
        self.in_game = ingame
        return None
    def set_in_round(self, inround):
        self.in_round = inround
        return None
    def set_hand(self, hand):
        self.hand = hand
        return None 
    def set_flop(self, flop):
        self.flop = flop
        return None 
    def set_turn(self, turn):
        self.turn = turn
        return None 
    def set_river(self, river):
        self.river = river
        return None
    def set_stack(self, stack):
        self.stack = stack
        return None 
    def set_bet(self, amount):
        self.bet = amount
        return None 
    def set_blind(self, blind):
        self.blind = blind
        return None

    def set_best_hand_flop(self):
        flop_cards = numpy.concatenate((self.hand,self.flop))
        self.hand_class, self.best_hand = cards.best_hand(flop_cards)
        return None
    def set_best_hand_turn(self):
        turn_cards = numpy.concatenate((self.hand,self.flop,self.turn))
        self.hand_class, self.best_hand = cards.best_hand(turn_cards)
        return None
    def set_best_hand_river(self):
        all_cards = numpy.concatenate((self.hand,self.flop,self.turn,self.river))
        self.hand_class, self.best_hand = cards.best_hand(all_cards)
        return None
        
    def get_in_game(self):
        return self.in_game
    def get_in_round(self):
        return self.in_round
    def get_bet(self):
        return self.bet
    def get_accumulative_bet(self):
        return self.accumulative_bet
    def get_name(self):
        return self.name
    def get_hand(self):
        return self.hand
    def get_stack(self):
        return self.stack
    def get_best_hand(self):
        return self.hand_class, self.best_hand 
    def get_all_in(self):
        return self.all_in
            
    def reset_all_bets(self):
        self.bet              = 0
        self.accumulative_bet = 0
        return None
    
    def cash_bet(self, amount):
        self.stack += amount
        return None 		
    
    def pay_blind(self, amount):
        if(amount <= self.stack):
            pay         = amount
        elif(amount > self.stack and self.stack > 0):
            pay         = self.stack
            self.all_in = True
        else:
            pay         = 0
            self.in_game     = False
            self.in_round    = False
        self.stack            -= pay
        self.bet              += pay
        self.accumulative_bet += pay
        return(pay)

    def show_player(self):
        player_str = self.name
        
        spc_num = 20 - len(player_str)
        for i in range(spc_num):
            player_str += " "
        player_str += str(self.in_game)
        
        spc_num = 30 - len(player_str)
        for i in range(spc_num):
            player_str += " "
        player_str += str(self.in_round)
        
        spc_num = 40 - len(player_str)
        for i in range(spc_num):
            player_str += " "
        player_str += str(self.stack)
        
        spc_num = 50 - len(player_str)
        for i in range(spc_num):
            player_str += " "
        player_str += str(self.hand[0])
        
        spc_num = 65 - len(player_str)
        for i in range(spc_num):
            player_str += " "
        player_str += str(self.hand[1])
        
        spc_num = 80 - len(player_str)
        for i in range(spc_num):
            player_str += " "
        player_str += str(self.bet)
        
        spc_num = 85 - len(player_str)
        for i in range(spc_num):
            player_str += " "
        player_str += str(self.accumulative_bet)
        
        print(player_str)
        return None
        
    def show_player_as_oponent(self):
        player_str = self.name
        
        spc_num = 20 - len(player_str)
        for i in range(spc_num):
            player_str += " "
        player_str += str(self.in_game)
        
        spc_num = 30 - len(player_str)
        for i in range(spc_num):
            player_str += " "
        player_str += str(self.in_round)
        
        spc_num = 40 - len(player_str)
        for i in range(spc_num):
            player_str += " "
        player_str += str(self.stack)
        
        spc_num = 50 - len(player_str)
        for i in range(spc_num):
            player_str += " "
        player_str += str(self.bet)
        
        spc_num = 60 - len(player_str)
        for i in range(spc_num):
            player_str += " "
        player_str += str(self.accumulative_bet)
        
        print(player_str)
        return None 
        
    def show_name(self):
        print(self.name)
        return None 
        
    def show_stack(self):
        print(self.stack)
        return None 
    def show_table(self, fase):
        table_str = ""
        if(fase == "flop"):
            for i in range(len(self.flop)):
                table_str += str(self.flop[i])
        elif(fase == "turn"):
            for i in range(len(self.flop)):
                table_str += str(self.flop[i])
            table_str += str(self.turn)
        elif(fase == "river"):
            for i in range(len(self.flop)):
                table_str += str(self.flop[i])
            table_str += str(self.turn)
            table_str += str(self.river)
        print(table_str)
        return None
    def show_hand(self):
        hand_string = str(self.hand[0])
        for i in range(1 ,len(self.hand)):
            hand_string = hand_string + ' ' + str(self.hand[i])
        print('Player ' + self.name + ' hand' + hand_string)
        return None
        
    def show_best_hand(self):
        print(self.hand_class)
        print(self.best_hand)
        return None
#####################################################################################################
class Player_fish(Player):
    def __init__(self, name, ini_stack):
        Player.__init__(self, name, ini_stack)
        self.minbet = 2
        return(None)
        
    def set_preflop_bet(self, min_bet):
        pay = 0
        if(self.bet < min_bet and min_bet - self.bet <= self.stack):
            pay         = min_bet - self.bet
        elif(self.bet < min_bet and min_bet - self.bet > self.stack):
            pay         = self.stack
            self.all_in = True
        self.bet              += pay
        self.accumulative_bet += pay
        self.stack            -= pay
        return(pay)

    def set_flop_bet(self, min_bet):
        pay = 0
        if(self.bet < min_bet and min_bet - self.bet <= self.stack):
            pay         = min_bet - self.bet
        elif(self.bet < min_bet and min_bet - self.bet > self.stack):
            pay         = self.stack
            self.all_in = True
        self.bet              += pay
        self.accumulative_bet += pay
        self.stack            -= pay
        return(pay)

    def set_turn_bet(self, min_bet):
        pay = 0
        if(self.bet < min_bet and min_bet - self.bet <= self.stack):
            pay         = min_bet - self.bet
        elif(self.bet < min_bet and min_bet - self.bet > self.stack):
            pay         = self.stack
            self.all_in = True
        self.bet              += pay
        self.accumulative_bet += pay
        self.stack            -= pay
        return(pay)

    def set_river_bet(self, min_bet):
        pay = 0
        if(self.bet < min_bet and min_bet - self.bet <= self.stack):
            pay         = min_bet - self.bet
        elif(self.bet < min_bet and min_bet - self.bet > self.stack):
            pay         = self.stack
            self.all_in = True
        self.bet              += pay
        self.accumulative_bet += pay
        self.stack            -= pay
        return(pay)
#####################################################################################################
class Player_console(Player):
    def __init__(self, name, ini_stack):
        Player.__init__(self, name, ini_stack)
        return(None)
        
    def set_preflop_bet(self, min_bet):
        print("Preflop")
        self.show_table("preflop")
        self.show_player()
        pay = int(input("Preflop bet at least = " + str(min_bet - self.bet) + "\n"))
        self.bet              += pay
        self.accumulative_bet += pay
        self.stack            -= pay
        return(pay)

    def set_flop_bet(self, min_bet):
        print("Flop")
        self.show_table("flop")
        self.show_player()
        pay = int(input("Flop bet at least = " + str(min_bet - self.bet) + "\n"))
        self.bet              += pay
        self.accumulative_bet += pay
        self.stack            -= pay
        return(pay)

    def set_turn_bet(self, min_bet):
        print("Turn")
        self.show_table("turn")
        self.show_player()
        pay = int(input("Turn bet at least = " + str(min_bet - self.bet) + "\n"))
        self.bet              += pay
        self.accumulative_bet += pay
        self.stack            -= pay
        return(pay)

    def set_river_bet(self, min_bet):
        print("River")
        self.show_table("river")
        self.show_player()
        pay = int(input("River bet at least = " + str(min_bet - self.bet) + "\n"))
        self.bet              += pay
        self.accumulative_bet += pay
        self.stack            -= pay
        return(pay)
#####################################################################################################
class Player_random(Player):
    def __init__(self, name, ini_stack, probabilidad):
        Player.__init__(self, name, ini_stack)
        self.probabilidad = probabilidad
        self.minbet       = 5
        self.maxbet       = 10
        return(None)
    
    def set_preflop_bet(self, min_bet):
        pay = 0
        random_num = random.random()
        if(random_num > self.probabilidad):
            self.play_hand = True
        else:
            self.play_hand = False
        if(self.play_hand == True):
            mybet = random.randint(self.minbet,self.maxbet)
            max_bet = max(mybet, min_bet - self.bet)
            if(self.bet < max_bet and self.stack >= max_bet - self.bet):
                pay         = max_bet - self.bet
            elif(self.bet < max_bet and max_bet - self.bet > self.stack):
                pay         = self.stack
                self.all_in = True
            self.bet              += pay
            self.accumulative_bet += pay
            self.stack            -= pay 
        return(pay)

    def set_flop_bet(self, min_bet):
        pay = 0
        if(self.play_hand == True):
            mybet = random.randint(self.minbet,self.maxbet)
            max_bet = max(mybet, min_bet)
            if(self.bet < max_bet and self.stack >= max_bet - self.bet):
                pay                    = max_bet - self.bet
            elif(self.bet < max_bet and max_bet - self.bet > self.stack):
                pay         = self.stack
                self.all_in = True
            self.bet              += pay
            self.accumulative_bet += pay
            self.stack            -= pay 
        return(pay)

    def set_turn_bet(self, min_bet):
        pay = 0
        if(self.play_hand == True):
            mybet = random.randint(self.minbet,self.maxbet)
            max_bet = max(mybet, min_bet)
            if(self.bet < max_bet and self.stack >= max_bet - self.bet):
                pay                    = max_bet - self.bet
            elif(self.bet < max_bet and max_bet - self.bet > self.stack):
                pay         = self.stack
                self.all_in = True
            self.bet              += pay
            self.accumulative_bet += pay
            self.stack            -= pay 
        return(pay)

    def set_river_bet(self, min_bet):
        pay = 0
        if(self.play_hand == True):
            mybet = random.randint(self.minbet,self.maxbet)
            max_bet = max(mybet, min_bet)
            if(self.bet < max_bet and self.stack >= max_bet - self.bet):
                pay                    = max_bet - self.bet
            elif(self.bet < max_bet and max_bet - self.bet > self.stack):
                pay         = self.stack
                self.all_in = True
            self.bet              += pay
            self.accumulative_bet += pay
            self.stack            -= pay 
        return(pay)
#####################################################################################################
class Player_simple(Player):
    def __init__(self, name, ini_stack):
        Player.__init__(self, name, ini_stack)
        self.minbet = 5
        self.probabilidad = 0.5
        return(None)
    
    def set_preflop_bet(self, min_bet):
        rank = cards.rank_hand(self.hand)
        pay = 0
        if(self.bet + min_bet < self.stack*0.1):
            pay         = min_bet - self.bet
        elif(min_bet > self.stack):
            pay         = self.stack
            self.all_in = True
        self.bet              += pay
        self.accumulative_bet += pay
        self.stack            -= pay
        return(pay)

    def set_flop_bet(self, min_bet):
        random_num = random.random()
        pay = 0
        if(random_num > self.probabilidad and self.stack >= min_bet):
            pay         = min_bet - self.bet
        elif(min_bet > self.stack):
            pay         = self.stack
            self.all_in = True
        self.bet              += pay
        self.accumulative_bet += pay
        self.stack            -= pay
        return(pay)

    def set_turn_bet(self, min_bet):
        random_num = random.random()
        pay = 0
        if(random_num > self.probabilidad and self.stack >= min_bet):
            pay         = min_bet - self.bet
        elif(min_bet > self.stack):
            pay         = self.stack
            self.all_in = True
        self.bet              += pay
        self.accumulative_bet += pay
        self.stack            -= pay
        return(pay)

    def set_river_bet(self, min_bet):
        random_num = random.random()
        pay = 0
        if(random_num > self.probabilidad and self.stack >= min_bet):
            pay         = min_bet - self.bet
        elif(min_bet > self.stack):
            pay         = self.stack
            self.all_in = True
        self.bet              += pay
        self.accumulative_bet += pay
        self.stack            -= pay
        return(pay)
#####################################################################################################
class Player_aggresive(Player):
    def __init__(self, name, ini_stack):
        Player.__init__(self, name, ini_stack)
        return(None)
        
    def set_preflop_bet(self, min_bet):
        rank = cards.rank_hand(self.hand)
        if(rank > 3 and (0.15*self.stack) >= self.bet + min_bet):
            self.play_hand = True
        pay = 0
        if(self.play_hand == True):
            if(self.bet + min_bet < 4*self.blind):
                pay  = 4*self.blind - self.bet
            else:
                pay  = min_bet - self.bet
            self.bet              += pay
            self.accumulative_bet += pay
            self.stack            -= pay
        return(pay)

    def set_flop_bet(self, min_bet):
        pay = 0
        if(self.play_hand == True and self.stack >= min_bet):
            if(self.bet + min_bet < 4*self.blind):
                pay  = 4*self.blind - self.bet
            else:
                pay  = min_bet - self.bet
            self.bet              += pay
            self.accumulative_bet += pay
            self.stack            -= pay
        return(pay)

    def set_turn_bet(self, min_bet):
        pay = 0
        if(self.play_hand == True and self.stack >= min_bet):
            if(self.bet + min_bet < 4*self.blind):
                pay  = 4*self.blind - self.bet
            else:
                pay  = min_bet - self.bet
            self.bet              += pay
            self.accumulative_bet += pay
            self.stack            -= pay
        return(pay)

    def set_river_bet(self, min_bet):
        pay = 0
        if(self.play_hand == True and self.stack >= min_bet):
            if(self.bet + min_bet < 4*self.blind):
                pay  = 4*self.blind - self.bet
            else:
                pay  = min_bet - self.bet
            self.bet              += pay
            self.accumulative_bet += pay
            self.stack            -= pay
        return(pay)
