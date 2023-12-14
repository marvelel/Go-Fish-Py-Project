import random
from operator import itemgetter

## A class representing a card in a standard deck of 52 cards.
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    ## When a Card class is printed, it returns as this string.
    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    ## Returns the Card in a way that can be compared to other cards for sorting or matching.
    def get_as_list(self):
        return [self.suit, self.rank]

## A class representing a standard deck of 52 cards.
class Deck:
    ## The class is initiated to compile a list of 52 unique Card classes.
    def __init__(self):
        self.cards = []
        suits = ["hearts", "diamonds", "clubs", "spades"]
        ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    ## A funtion to shuffle/mix up the 52 cards at the beginning of a game.
    def shuffle(self):
        random.shuffle(self.cards)

    ## A function to remove and return the last Card in a Deck's list, representing drawing a card from the top of a deck.
    def deal(self):
        card_dealt = self.cards.pop()
        return card_dealt
    
    ## A function that checks if there are Card classes left in the Deck and returns True if yes, False if no.
    def cards_left(self):
        if len(self.cards) > 0:
            return True
        else:
            return False

## A class representing a player's hand and books of cards in a game of Go-Fish.
class Hand:
    def __init__(self, bot = False):
        self.cards = []
        self.score = 0
        self.bot = bot

    ## A function that returns True if the Hand class is controlled by a bot, or False if it is controlled by a player.
    def check_bot(self):
        return self.bot

    ## A function that adds a Card class to the list of a Hand class's Cards. Used in conjunction with drawing a card from the deck, or the Deck class deal() function.
    def add_card(self, card):
        self.cards.append(card)
    
    ## A function that returns the list of Card classes in a Hand.
    def get_cards(self):
        return self.cards
    
    ## A function that adds a point to a Hand class stored score, representing the number of books of cards a Hand has received. Used to determine the winner of the game.
    def add_point(self):
        self.score += 1

    ## A function that returns the stored score in a Hand class.
    def get_points(self):
        return self.score
    
    ## A function that changes a Hand's list of Cards. Used when a player successfully receives a Card from another Hand in the game.
    def adjust_hand(self, adjusted_hand):
        self.cards = adjusted_hand

    ## A function that prints a statement reflecting that a Hand has completed a book of cards and has received a point.
    def display_points(self, matching_rank):
        print(f'''{"Bot has" if self.bot else "You have"} a book of {matching_rank}'s. {"They" if self.bot else "You"} have earned a point!''')
        print(f'''{"The bot's" if self.bot else "Your"} points: {self.score}''')

    ## A function that prints out the player's hand organized by rank and suit.
    def display(self):
        temp = []
        temp2 = []

        for card in self.cards:
            temp.append(card.get_as_list())

        temp = sorted(temp, key = itemgetter(0))
        temp = sorted(temp, key = itemgetter(1))

        for list in temp:
            temp2.append(Card(list[0], list[1]))

        print("Your hand:")
        for card in temp2:
            print(card)
        print()
    
    ## A function which represents the entirety of a Hand class's turn. Function dissects for either a player's or bot's turn.
    def asking_phase(self, other_hand, ranks_left):
        still_turn = True
        bot_choices = self.get_cards()

        ## Bot's turn.
        if self.bot:
            print("It's the bot's turn...")
            print()

            ## Conditons of Go-Fish are if a player asks for a card from the other hand successfully, it is still their turn.
            while still_turn:
                still_turn = False

                ## Bot chooses a random card from its own hand to ask the player for. If its hand is empty, it chooses a random rank that has yet to be completed.
                if len(bot_choices) > 0:                                          ## find a way for bot to not ask you for the same card twice
                    bot_choice = random.choice(bot_choices).get_as_list()[1]
                else:
                    bot_choice = random.choice(ranks_left)

##                for chosen_card in bot_choices:                                   ## whenever bot asks for a card, it is deleted from their hand
##                    if chosen_card.get_as_list()[1] == bot_choice:
##                        del bot_choices[bot_choices.index(chosen_card)]

                print (f"Bot is asking if you have any {bot_choice}'s...")

                ## If the player has any cards that the bot has asked for, they are removed and added to the bot's hand. Print statement reflects what's happened.
                ## Bot is successfull, so it is still its turn.
                for i in range(3):                                                              ## inefficient solution to missing matching cards
                    for card in other_hand.get_cards():
                        if card.get_as_list()[1] == bot_choice:
                            other_hand_list = other_hand.get_cards()
                            self.cards.append(other_hand_list.pop(other_hand_list.index(card)))
                            other_hand.adjust_hand(other_hand_list)
                            print(f"Bot took your {card}.")
                            still_turn = True

                ## A check if all of the books have been completed at this point, and if so ends the loop/turn.
                if len(ranks_left) == 1 and still_turn:
                    still_turn = False
                    continue

                ## Print statement reflects if it is still bot's turn before reiterating.
                if still_turn:
                    print()
                    print("Bot gets to go again!")
                    print()
                ## Print statement reflects bot was unsuccessful and its turn ends.
                else:
                    print(f"You don't have any {bot_choice}'s!")
                    print()

        ## Player's turn.
        else:
            print("It's your turn.")
            print()
            self.display()
            
            ## Conditons of Go-Fish are if a player asks for a card from the other hand successfully, it is still their turn.
            ## Turn initializes by asking player for input which card they would like to ask for.
            while still_turn:
                still_turn = False
                choice = ""
                choice = input("Please select a rank to ask the other player for. (A, 2, 3, etc.)").upper()
                
                ## If input is not a valid card, request for input is reiterated until it is valid.
                while choice not in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
                    choice = input(f"Your answer ({choice}) was not valid. Please select a rank (A, 2, 3, etc.)").upper()

                print(f"You have asked the bot for {choice}'s.")

                ## If bot has a card that the player has asked for, it is removed and added to the player's hand. Print statement reflects what has happened.
                ## Player is successful so it is still their turn.
                for i in range(3):                                                              ## inefficient solution to missing matching cards
                    for card in other_hand.get_cards():
                        if card.get_as_list()[1] == choice:
                            other_hand_list = other_hand.get_cards()
                            self.cards.append(other_hand_list.pop(other_hand_list.index(card)))
                            other_hand.adjust_hand(other_hand_list)
                            print(f"You took the bot's {card}.")
                            still_turn = True

                ## A check if all of the books have been completed, and if so ends the loop/turn.
                if len(ranks_left) == 1 and still_turn:
                    still_turn = False
                    continue

                ## Print statement reflects if it is still the player's turn before reiterating.
                if still_turn:
                    print()
                    print("You get to go again!")
                    print()
                ## Print statement reflects if player was unsuccessful and that their turn is over.
                else:
                    print(f"Bot doesn't have any {choice}'s...")
                    print()

## A class representing the game of Go-Fish itself, including the complexity of Card and Hand classes.            
class Game:
    ## A function that starts a game.
    def play(self):
        ## List keeps track of what books are left. If the list is empty the game is over as defined later.
        self.ranks_left = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

        ## Initializes and shuffles the deck.
        deck = Deck()
        deck.shuffle()

        ## Initializes the player and the bot's hands.
        player_hand = Hand()
        bot_hand = Hand(bot = True)

        for x in range(5):
            player_hand.add_card(deck.deal())
            bot_hand.add_card(deck.deal())

        print("*" * 30)
        print("Welcome to Go-Fish!")
        print("*" * 30)

        ## Loop ends when the list of books left in self.ranks_left is empty.
        while len(self.ranks_left) > 0:
            print()
            print("*" * 30)
            print("Checking for matches...")
            print("*" * 30)
            print()

            ## Checks if the player has any sets of 4 matching cards.
            self.check_for_matches(player_hand)

            ## Checks if the player's hand is empty and adds a card if the deck is not empty. Print statement reflects what is happening.
            if len(player_hand.get_cards()) == 0 and deck.cards_left():
                print("You're out of cards, so you draw one.")
                print()
                player_hand.add_card(deck.deal())
            elif len(player_hand.get_cards()) == 0:
                print("You're out of cards, but the deck is empty...")
                print()

            ## Start of the player's turn.
            player_hand.asking_phase(bot_hand, self.ranks_left)

            ## Players turn ends, and they draw a card from the deck if it is not empty. Print statement reflects the card drawn from the deck or if nothing is drawn.
            if deck.cards_left():
                print("Go fish!")
                player_hand.add_card(deck.deal())
                print(f"You have drawn {player_hand.get_cards()[-1]}.")
            else:
                print("Go fish! ... But the deck is empty.")

            ## Checks player's hand for matches once more.
            self.check_for_matches(player_hand)
            
            ## Checks if game is over by checking if the list of books completed is empty.
            if len(self.ranks_left) == 0:
                continue

            print()
            print("*" * 30)
            print("Checking for matches...")
            print("*" * 30)
            print()

            ## Checks if the bot has any set of 4 matching cards.
            self.check_for_matches(bot_hand)

            ## Checks if the bot's hand is empty and adds a card if the deck is not empty. Print statement reflects what is happening.            
            if len(bot_hand.get_cards()) == 0 and deck.cards_left():
                print("The bot is out of cards, so they draw one.")
                print()
                bot_hand.add_card(deck.deal())
            elif len(bot_hand.get_cards()) == 0:
                print("The bot is out of cards, but the deck is empty.")
                print()

            ## Start of the bot's turn.
            bot_hand.asking_phase(player_hand, self.ranks_left)

            ## Bot's turn ends, and they draw a card from the deck if it is not empty. Print statement reflects whether a card was drawn.
            if deck.cards_left():
                print("Go fish!")
                bot_hand.add_card(deck.deal())
                print("Bot has drawn a card.")
            else:
                print("Go fish! ... But the deck is empty.")

            ## Checks if bot has any matches once more.
            self.check_for_matches(bot_hand)
        
        ## Print statement reflects that game is over.
        print()
        print("Game over!")

        ## Compares each hand's points and determines a winner. Print statement reflects points and the winner.
        if player_hand.get_points() > bot_hand.get_points():
            print(f"You win by a score of {player_hand.get_points()} to {bot_hand.get_points()}!")
            print("Congratulations!")
        else:
            print(f"You lose by a score of {player_hand.get_points()} to {bot_hand.get_points()}...")
            print("Better luck next time.")

    ## A function that determines if a matching set of 4 cards exists in a hand.
    def check_for_matches(self, hand):
        matching_rank = ""
        has_match = False
        tally_of_cards = [
            {"rank" : "A", "tally" : 0},
            {"rank" : "2", "tally" : 0},
            {"rank" : "3", "tally" : 0},
            {"rank" : "4", "tally" : 0},
            {"rank" : "5", "tally" : 0},
            {"rank" : "6", "tally" : 0},
            {"rank" : "7", "tally" : 0},
            {"rank" : "8", "tally" : 0},
            {"rank" : "9", "tally" : 0},
            {"rank" : "10", "tally" : 0},
            {"rank" : "J", "tally" : 0},
            {"rank" : "Q", "tally" : 0},
            {"rank" : "K", "tally" : 0}
        ]

        ## Creates a tally for the number of cards organized by rank in the hand.
        for card in hand.get_cards(): 
            for tally in tally_of_cards:
                if card.get_as_list()[1] == tally["rank"]:
                    tally["tally"] += 1
        
        ## If the tally is equal to 4 for any number of ranks, they are removed from and a point is added to the hand.
        for tally in tally_of_cards:
            if tally["tally"] == 4:
                matching_rank = tally["rank"]
                has_match = True
            if has_match:
                for i in range(4):
                    for card in hand.get_cards():
                        if matching_rank == card.get_as_list()[1]:
                            new_hand = hand.get_cards()
                            del new_hand[new_hand.index(card)] 
                            hand.adjust_hand(new_hand)
                for rank in self.ranks_left:
                    if matching_rank == rank:
                        del self.ranks_left[self.ranks_left.index(rank)]

                has_match = False
                hand.add_point()
                hand.display_points(matching_rank)

## Initializes and starts the game.
game = Game()
game.play()