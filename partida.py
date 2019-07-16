import deck
import cards
import player
import numpy
import pandas
import random

class Partida:
    def __init__(self, players_num, ini_stack):
        self.deck            = deck.Deck(1)
        self.blind           = 2
        
        self.players         = []
        if(players_num > 9):
            players_num  = 9
        rand_players = 6
        for p in range(0, rand_players):
            proba = random.random() 
            self.players.append(player.Player_random('RandPlayer' + str(p), ini_stack, proba))
        fish_players = 0
        for p in range(0, fish_players):
            self.players.append(player.Player_fish('FishPlayer' + str(p), ini_stack))
        
        self.players.append(player.Player_console('ConsolePlayer' + str(0), ini_stack))
        #self.players.append(player.Player_simple('SimplePlayer' + str(0), ini_stack))
        #self.players.append(player.Player_aggresive('AggresivePlayer' + str(0), ini_stack))
        
        self.position  = len(self.players) - 1
        self.reset_game()
        self.set_blinds()
        return None
  
    def show_players(self):
        print("************************************** P L A Y E R S *****************************************")
        for i in range(len(self.players)):
            self.players[i].show_player()
        return None
        
    def show_table_players(self):
        print("********************************* T A B L E   P L A Y E R S **********************************")
        for i in range(len(self.table_players)):
            self.table_players[i].show_player()
        return None
    
    def show_table(self):
        print("**************************************** T A B L E  ******************************************")
        for i in range(len(self.players)):
            self.players[i].show_player_as_oponent()
        self.print_pot()
        return None
    
    def reset_game(self):
        self.deck.shuffle_deck()
        self.pot         = 0
        self.actual_bet  = 0
        self.accum_bet   = 0
    
        self.clean_hands()
        self.reset_all_bets()
        
        self.remove_players()
        self.position = (self.position + 1) % len(self.players)
        while(self.players[self.position].get_in_game() == False):
            self.position = (self.position + 1) % len(self.players)
        self.set_table_players()
        return None 
    
    def clean_hands(self):
        for i in range(len(self.players)):
            self.players[i].set_hand([[],[]])
            self.players[i].set_flop([[],[],[]])
            self.players[i].set_turn([[]])
            self.players[i].set_river([[]])
        return None
    
    def reset_all_bets(self):
        for i in range(len(self.players)):
            self.players[i].reset_all_bets()
        return None
        
    def remove_players(self, min_amount = 0):
        for indice in range(len(self.players)):        
            if(self.players[indice].get_stack() <= min_amount):  
                self.players[indice].set_in_game(False)
                self.players[indice].set_in_round(False)
        return None
        
    def set_table_players(self):
        self.table_players = []
        for i in range(self.position, self.position + len(self.players)):
            if(self.players[i%len(self.players)].get_in_game() == True):
                self.players[i%len(self.players)].set_in_round(True)
                self.table_players.append(self.players[i%len(self.players)])
        return None
        
    def set_blinds(self):
        for i in range(len(self.players)):
            self.players[i].set_blind(self.blind)
        return None
        
    def get_blinds(self):
        self.pot += self.table_players[0].pay_blind(self.blind)
        self.pot += self.table_players[1].pay_blind(2*self.blind)
        return None
    
    def deal_hands(self, num=2):
        for i in range(len(self.table_players)):
            self.table_players[i].set_hand(self.deck.deal_hand(num))
        return None
    
    def set_flop(self, flop):
        for i in range(len(self.table_players)):
            self.table_players[i].set_flop(flop)
            self.table_players[i].set_best_hand_flop()
        return None
        
    def set_turn(self, turn):
        for i in range(len(self.table_players)):
            self.table_players[i].set_turn(turn)
            self.table_players[i].set_best_hand_turn()
        return None 
        
    def set_river(self, river):
        for i in range(len(self.table_players)):
            self.table_players[i].set_river(river)
            self.table_players[i].set_best_hand_river()
        return None
    
    def set_bets(self, fase):
        self.actual_bet = 2*self.blind
        indice          = 2%len(self.table_players)
        while(len(self.table_players) >= 2 and self.table_players[indice].get_bet() != self.actual_bet):
            if(fase == "preflop"):
                bet = self.table_players[indice].set_preflop_bet(self.actual_bet)
            elif(fase == "flop"):
                bet = self.table_players[indice].set_flop_bet(self.actual_bet)
            elif(fase == "turn"):
                bet = self.table_players[indice].set_turn_bet(self.actual_bet)
            elif(fase == "river"):
                bet = self.table_players[indice].set_river_bet(self.actual_bet)   
                 
            if(self.table_players[indice].get_bet() >= self.actual_bet):    
                self.actual_bet = self.table_players[indice].get_bet()
                self.pot       += bet
                indice          = (indice + 1)%len(self.table_players)
            elif(self.table_players[indice].get_all_in() == True and self.table_players[indice].get_bet() < self.actual_bet):    
                self.pot       += bet
                indice          = (indice + 1)%len(self.table_players)
            else:
                self.table_players[indice].set_in_round(False)
                self.table_players.pop(indice)
                indice %= len(self.table_players)
        self.accum_bet += self.actual_bet
        return None
       
    def reset_bet(self):
        for i in range(len(self.players)):
            self.players[i].set_bet(0)
        return None
        
    def rank_hand(self, fase):
        hand_list = numpy.zeros([len(self.table_players),7])
        reg       = numpy.zeros(7)
        for i in range(len(self.table_players)):
            h_class, hand = self.table_players[i].get_best_hand()
            reg[0] = h_class
            for j in range(5):
                reg[j + 1] = hand[j,1]
            reg[6] = i
            hand_list[i] = reg
            
        self.hand_list = pandas.DataFrame(hand_list, columns=['class','h1','h2','h3','h4','h5','player'], dtype=numpy.int8)
        self.hand_list = self.hand_list.sort_values(by =['class','h1','h2','h3','h4','h5'], ascending=False)
        return None
        
    def check_tie(self, index = 0):
        count = 0
        i     = index + 1
        while(i < len(self.hand_list) and self.hand_list.iloc[index,0] == self.hand_list.iloc[i,0]):
            j = 1
            while(j < 6 and self.hand_list.iloc[index,j] == self.hand_list.iloc[i,j]):
                j += 1
            if(j == 6):
                count += 1
            i += 1
        return count
        
    def pay(self):
        index = 0
        if(len(self.table_players) == 1):
            self.table_players[0].cash_bet(self.pot)
            self.pot = 0
        else:
            while(index < len(self.hand_list) and self.pot > 1):
                tie = self.check_tie(index)
                restar_pot = 0
                if(tie == 0):
                    if(self.table_players[self.hand_list.iloc[index].loc['player']].get_all_in() == False):
                        self.table_players[self.hand_list.iloc[index].loc['player']].cash_bet(self.pot)
                        restar_pot = self.pot
                    else:
                        pot_part = int(self.pot*self.table_players[self.hand_list.iloc[index].loc['player']].get_accumulative_bet()/self.accum_bet)
                        self.table_players[self.hand_list.iloc[index].loc['player']].cash_bet(pot_part)
                        restar_pot += pot_part
                    index += 1
                else:
                    accum_part = 0
                    count = 0
                    fin   = False
                    for i in range(index, index + tie + 1):
                        accum_part += self.table_players[self.hand_list.iloc[i].loc['player']].get_accumulative_bet()
                        if(self.table_players[self.hand_list.iloc[i].loc['player']].get_all_in() == False):
                            fin = True
                        count += 1
                    if(fin == True):
                        split_pot  = self.pot
                    else:
                        split_pot  = int(self.pot*accum_part/(count*self.accum_bet))
                    for i in range(index, index + tie + 1):
                        pot_part = int(split_pot*self.table_players[self.hand_list.iloc[i].loc['player']].get_accumulative_bet()/accum_part)
                        self.table_players[self.hand_list.iloc[i].loc['player']].cash_bet(pot_part)
                        restar_pot += pot_part
                        index += 1
                self.pot -= restar_pot
            if(self.pot == 1):
                self.table_players[self.hand_list.iloc[0].loc['player']].cash_bet(self.pot)
                self.pot = 0
        return None
    
    def players_count(self):
        count = 0
        for i in range(len(self.players)):
            if(self.players[i].get_in_game() == True):
                count += 1
        return count
    
    def print_hand_list(self):
        for i in range(len(self.hand_list)):
            print(self.hand_list.iloc[i])
        return None
    def print_accum_bet(self):
        print("Accumulated bet = " + str(self.accum_bet))
        return None
    def print_pot(self):
        print("Pot = " + str(self.pot))
        return None
        
    def run_partida(self, games_num, show = True):
        indice = 0
        players_num = self.players_count()
        while(1 < players_num and indice < games_num):	
            if(show == True):
                print(' ')
                print('*************************************  Ronda numero ' + str(indice)  + '  ***************************************')
                self.show_players()
                self.get_blinds()
            
                print(' ')
                print('Blinds')
                self.show_players()
                self.show_table_players()
                print('Blinds Pot = ' + str(self.pot))
            
            
                etapa_de_partida = "preflop"
                self.deal_hands()
                self.set_bets(etapa_de_partida)
            
                print(' ')
                print('PreFlop')
                self.show_players()
                self.show_table_players()
                print('Preflop Pot = ' + str(self.pot))
            
            
                if(len(self.table_players) >= 2):
                    etapa_de_partida = "flop"
                    self.reset_bet()
                    self.flop = self.deck.deal_hand(3)
                    self.set_flop(self.flop)
                    self.set_bets(etapa_de_partida)
                
                    hand_str = str(self.flop[0]) + "    " + str(self.flop[1]) + "    " + str(self.flop[2])
                    print(' ')
                    print('Flop')
                    print(hand_str)
                    self.show_players()
                    self.show_table_players()
                    print('Flop Pot = ' + str(self.pot))
                

                if(len(self.table_players) >= 2):
                    etapa_de_partida = "turn"
                    self.reset_bet()
                    self.turn = self.deck.deal_hand(1)
                    self.set_turn(self.turn)
                    self.set_bets(etapa_de_partida)
                
                    hand_str += "    " + str(self.turn[0])
                    print(' ')
                    print('Turn')
                    print(hand_str)
                    self.show_players()
                    self.show_table_players()
                    print('Turn Pot = ' + str(self.pot))
                
            
                if(len(self.table_players) >= 2):
                    etapa_de_partida = "river"
                    self.reset_bet()
                    self.river = self.deck.deal_hand(1)
                    self.set_river(self.river)
                    self.set_bets(etapa_de_partida)
                
                    hand_str += "    " + str(self.river[0])
                    print(' ')
                    print('River')
                    print(hand_str)
                    self.show_players()
                    self.show_table_players()
                    print('River Pot = ' + str(self.pot))
                    
            else:
                print(' ')
                print('*************************************  Ronda numero ' + str(indice)  + '  ***************************************')
                self.get_blinds()
                
                etapa_de_partida = "preflop"
                self.deal_hands()
                
                print(' ')
                print('Preflop')
                self.show_table()
                self.set_bets(etapa_de_partida)
                
                if(len(self.table_players) >= 2):
                    etapa_de_partida = "flop"
                    self.reset_bet()
                    self.flop = self.deck.deal_hand(3)
                    self.set_flop(self.flop)
                    
                    print(' ')
                    print('Flop')
                    self.show_table()
                    self.set_bets(etapa_de_partida)
                    
                    
                if(len(self.table_players) >= 2):
                    etapa_de_partida = "turn"
                    self.reset_bet()
                    self.turn = self.deck.deal_hand(1)
                    self.set_turn(self.turn)
                    
                    print(' ')
                    print('Turn')
                    self.show_table()
                    self.set_bets(etapa_de_partida)
                    
                if(len(self.table_players) >= 2):
                    etapa_de_partida = "river"
                    self.reset_bet()
                    self.river = self.deck.deal_hand(1)
                    self.set_river(self.river)
                    
                    print(' ')
                    print('River')
                    self.show_table()
                    self.set_bets(etapa_de_partida)
                    
            if(len(self.table_players) >= 2):
                self.rank_hand(etapa_de_partida)
            self.pay()
            
            print(' ')
            print('Fin de Ronda')
            if(len(self.table_players) == 1):
                hand = self.table_players[0].get_hand()
                win_hand_str = str(hand[0]) + "    " + str(hand[1])
                print('Mano ganadora del jugador ' + self.table_players[0].get_name())
            else:
                h_class, hand = self.table_players[self.hand_list.iloc[0,6]].get_best_hand()
                win_hand_str = str(hand[0]) + "    " + str(hand[1]) + "    " + str(hand[2]) + "    " + str(hand[3]) + "    " + str(hand[4])
                print('Mano ganadora del jugador ' + self.table_players[self.hand_list.iloc[0,6]].get_name())
                
            print(win_hand_str)
            self.show_players()
            self.show_table_players()
            print('Clean Pot = ' + str(self.pot))
            
            self.reset_game()
            
            players_num = self.players_count()
            indice += 1
           
        print(' ')
        print('Fin de la Partida ')
        self.show_players()
        self.show_table_players()
        print('**********************************************************************************************')
        print(' ')

        return None

    def get_players(self):
        return self.players
    def get_table_players(self):
        return self.table_players
        	
    def del_player(self, name):
        indice = 0
        while(1 < len(self.players) and indice < len(self.players)):
            if(name == self.players[indice].get_name()):
                self.players.pop(indice)
            indice += 1
        return None
        
    def show_hands(self):
        for i in range(len(self.players)):
            self.players[i].show_name()
            self.players[i].show_best_hand()
        return None 
        
    def show_hand_list(self):
        print(self.hand_list)
        return None

    def create_txt_file(self, file_name):
        header = 'name,hand,hand_rank,result,bet,stack,mode\n'
        f = open(file_name,"w+")
        f.write(header)
        f.close()
        return None 

    def add_register_txt_all_file(self, txt_file):
        register = ","+","+","+","+","+","+","+"\n"
        f = open(txt_file,"a")
        f.write(register)
        f.close()
        return None 
	
	

