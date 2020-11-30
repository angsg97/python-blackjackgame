from libdw import sm
import random
import time
import os

class Deck():
    '''Object that helps to initialize lists of 52 Cards, and provides the method drawCard that returns a card object 
    from the remaining list of cards randomly, simulating a drawing system from a real deck of cards. Also has method resetDeck to re-initialize cards'''

    dictOfCardValues = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10} # 13 card Values
    dictOfCardSuits = {'Clubs': '♣', 'Diamonds': '♦', 'Hearts': '♥', 'Spades': '♠'} # 4 Suits, Clubs, Diamonds, Hearts and Spades

    def __init__(self, seed = None):
        # Initialize Seed if user provides it
        if seed is not None:
            random.seed(seed)
        self.listofCards = []

        # Initialize deck of cards
        for value in self.dictOfCardValues:
            for suit in self.dictOfCardSuits:
                self.listofCards.append((value, suit))

    def drawCard(self):
        ''' 1. Initializes and returns a card object
            2. Removes selected card from the listOfcards set'''

        selectedCard = random.choice(self.listofCards)
        self.listofCards.remove(selectedCard)

        # Create card object to be returned
        selectedCardObject = Card(self.dictOfCardValues[selectedCard[0]], selectedCard[0], \
            selectedCard[1], self.dictOfCardSuits[selectedCard[1]])
        
        return selectedCardObject

    def resetDeck(self):
        # Function to reset the Deck by recreating all Card Objects
        self.listofCards = []

        # Initialize deck of cards
        for value in self.dictOfCardValues:
            for suit in self.dictOfCardSuits:
                self.listofCards.append((value, suit))

        
class Card():
    '''Card Object to contain attributes of card passed in and also self.printedCard which is the string array to print card
    Contains method getPrintedCard, getCardArrayForPrint and getValue'''

    def __init__(self, value, valueSymbol, suit, suitSymbol):
        self.suit = suit
        self.value = value

        if valueSymbol != '10':
            self.printedCard = [ '┌───────┐', \
                                f'│{valueSymbol}      │', \
                                '│       │', \
                                f'|   {suitSymbol}   |', \
                                '│       │', \
                                f'│      {valueSymbol}│', \
                                '└───────┘'
            ]

        else:
            # Print card with a 10
            self.printedCard = [ '┌───────┐', \
                                f'│{valueSymbol}     │', \
                                '│       │', \
                                f'|   {suitSymbol}   |', \
                                '│       │', \
                                f'│     {valueSymbol}│', \
                                '└───────┘'
            ]

    def getPrintedCard(self):
        # Transforms array of lines into a single string, joined by newline characters
        delimiter = '\n'
        finalString = delimiter.join(self.printedCard)

        return finalString

    def getCardArrayForPrint(self):
        '''To provide the basic arrays of the lines of each card, so that Player class can combine each line before printing it altogether'''
        return self.printedCard

    def getValue(self):
        return self.value


class Player():
    '''Player Class that contains player's cards for the current game, with method getPrintHand to print all cards currently in hand
    Acts as Parent Class to UserPlayer and BotPlayer'''

    def __init__(self):
        self.handCards = []

    def addCard(self, cardObject):
        self.handCards.append(cardObject)

    def handValue(self):
        if self.handCards == []:
            return 0
        else:
            cardValue = 0
            containsAce = False
            for card in self.handCards:
                # If card Value is 1, add counter so we can calculate if the Aces are 1 or 11
                if card.getValue() == 1:
                    containsAce = True

                cardValue += card.getValue()

            # Since the maximum number of Aces in a hand with the value 11 can only be 1, since 2 Aces with 11 automatically busts you at 22,
            # Then we only need to check if one of the Aces needs to be converted into an 11
    
            if containsAce and cardValue <= 11:
                cardValue += 10 # Ace is converted from 1 to 11, add 10 to value

            return cardValue
                
    def getPrintHand(self):
        # Create blank array of 7 empty strings
        finalList = ['' for i in range(7)]

        listOfCardArrays = []
        for card in self.handCards:
            listOfCardArrays.append(card.getCardArrayForPrint())

        for i in range(7):
            for cardNumber in range(len(self.handCards)):
                finalList[i] = finalList[i] + listOfCardArrays[cardNumber][i] + ' '
        
        delimiter = '\n'
        finalString = delimiter.join(finalList)

        return finalString


class UserPlayer(Player):
    '''Child class of Player with attributes and methods to contain and modify UserPlayer's tokens, and clearhand to reset Player's hand cards'''
    def __init__(self, tokens = 1000):
        self.tokens = tokens
        Player.__init__(self)

    def getTokens(self):
        return self.tokens

    def winTokens(self, amt):
        self.tokens += amt

    def loseTokens(self, amt):
        self.tokens -= amt

    def clearHand(self):
        self.handCards = []

class BotPlayer(Player):
    '''Child Class of Player which contains the bot's Name, and also a method to print out a concealed hand'''
    def __init__(self, name):
        self.name = name
        Player.__init__(self)

    def getBotName(self):
        return self.name

    def getConcealedHand(self):
        # Create blank array of 7 empty strings
        finalList = ['' for i in range(7)]

        firstCard = self.handCards[0].getCardArrayForPrint()

        hiddenCard = [ '┌───────┐', \
                      f'│░░░░░░░|', \
                       '│░░░░░░░│', \
                      f'|░░░░░░░|', \
                       '│░░░░░░░│', \
                      f'│░░░░░░░|', \
                       '└───────┘'
        ]

        for i in range(7):
            finalList[i] = finalList[i] + firstCard[i] + ' '
            for cardNumber in range(len(self.handCards) - 1):
                finalList[i] = finalList[i] + hiddenCard[i] + ' '

        delimiter = '\n'
        finalString = delimiter.join(finalList)

        return finalString


class GameSM(sm.SM):
    '''Main game engine class with all the logic and a child class of SM, a more detailed explanation is found in README.md'''

    start_state = 'Start Screen'
    positionDict = {1: '1st', 2: '2nd', 3: '3rd', 4: '4th', 5: '5th', 6: '6th', 7: '7th'}
    botNamesList = ["WALL-E", "DEEP LEARNING", "MACHINE LEARNING", "DAVE", "INTEL I-7", \
        "APE", "ISTD", "HASS", "ESD", "EPD", "INTRO TO DESIGN 3.007", "VOCAREUM", "E-DIMENSION", "MYPORTAL", "#BIG-D", "DESIGN THINKING"]
    
    def __init__(self):
        # Create Player object for this instance of the game
        self.player = UserPlayer()
        self.deck = Deck()
    
    def get_next_values(self, state, inp):
        if state == 'Start Screen':
            os.system('cls') # On Non-Windows systems, use os.system('clear')
            self.displayStartMessage()
            # Before start screen, check if user has less than 100 tokens, if so, give the user 100 more tokens
            if self.player.getTokens() < 100:
                print(f'''-----------------------------------------------------------------------------------------------------------------------------------------------------

Welcome to the Blackjack Simulator Game! You currently have {self.player.getTokens()} Tokens! That's sad :(
Luckily, the God of Gambling has decided to Bless you with 100 more Tokens. Now you have {self.player.getTokens() + 100} Tokens!

To begin, Enter 1 for Practice Mode, 2 for AI Mode, and 3 to Quit Game: ''')
                self.player.winTokens(100)
            else:
                print(f'''-----------------------------------------------------------------------------------------------------------------------------------------------------

Welcome to the Blackjack Simulator Game! You currently have {self.player.getTokens()} Tokens!
To begin, Enter 1 for Practice Mode, 2 for AI Mode, and 3 to Quit Game: ''')

            nextState = self.getUserInputAsInteger(1, 3)

            if nextState == 1:
                # If 1, g to Practice Mode
                return ('Practice', True)

            elif nextState == 2:
                # If 1, g to AI Mode
                return ('AI', True)

            elif nextState == 3:
                return ('End', False)

        elif state == 'Practice':
            # Begin Practice Mode
            os.system('cls') # On Non-Windows systems, use os.system('clear')
            print('''\n-----------------------------------------------------------------------------------------------------------------------------------------------------
Welcome to Practice Mode! Your tokens will not be affected here\n\n''')
            time.sleep(1)
            print('* The Dealer deals you a hand, here are your Cards: *\n')
            time.sleep(1)

            # Draws 2 cards and add them to players hand
            self.player.addCard(self.deck.drawCard())
            self.player.addCard(self.deck.drawCard())
            print(self.player.getPrintHand())
            time.sleep(1)

            # Get Player Input either YES or NO, then transition to State 'Practice Loop' if YES and 'Start Screen' if NO
            print(f'\nThe value of your hand is {self.player.handValue()}. Would you like to draw another card? (Y/N)')

            if self.getUserInputAsChar(yesList = ['Y', 'y'], noList = ['N', 'n']):
                return ('Practice Loop', True)
            else:
                print(f"\nGood job! You finished the round with a hand value of {self.player.handValue()}")
                return ('Start-Over User Dialog (Practice)', True)

        elif state == 'Practice Loop':
            # Enter Code to Remain in Loop
            print('\n* The Dealer deals you a card, here are your Cards: *\n')
            time.sleep(1)

            # Deal user a card, show current hand
            self.player.addCard(self.deck.drawCard())
            print(self.player.getPrintHand())
            time.sleep(1)

            currentcardValue = self.player.handValue()
            # After drawing a card, if hand value larger than 21, user has lost and game is ended
            if currentcardValue > 21:
                print(f"\nThe value of your hand is {self.player.handValue()}. Oops! That's a bust! GAME OVER\n")
                return ('Start-Over User Dialog (Practice)', True)

            else:
                # Get Player Input either YES or NO, then transition to State 'Practice Loop' if YES and 'Start Screen' if NO
                print(f'\nThe value of your hand is {self.player.handValue()}. Would you like to draw another card? (Y/N)')

                if self.getUserInputAsChar(yesList = ['Y', 'y'], noList = ['N', 'n']):
                    return ('Practice Loop', True)
                else:
                    print(f"\nGood job! You finished the round with a hand value of {self.player.handValue()}")
                    return ('Start-Over User Dialog (Practice)', True)

        elif state == 'Start-Over User Dialog (Practice)':
            # Reset Deck and user hand cards, and get input from user to decide whether to restart game or to go back to start screen
            self.resetGame()
            print(f"Would you like to restart your Game? (Y/N)")

            if self.getUserInputAsChar(yesList = ['Y', 'y'], noList = ['N', 'n']):
                return ('Practice', True)
            else:
                print(f"\nGood job! You finished the round with a hand value of {self.player.handValue()}")
                self.resetGame()
                return ('Start Screen', True)


        elif state == 'AI':
            os.system('cls') # On Non-Windows systems, use os.system('clear')
            # AI Mode Begins, get input from User, how many bots to play with and how many tokens to bet
            maxNoOfBots = 6
            print(f'''\n-----------------------------------------------------------------------------------------------------------------------------------------------------
Welcome to AI Mode! You may choose up to {maxNoOfBots} AI to play against. In this game, each AI will mirror your bet, forming a shared pool of tokens.
The winner wins all tokens in the pool, while multiple winners share their winnings! Good luck!\n''')
            time.sleep(1)
            print(f'How many AI do you want to play against? (1-{maxNoOfBots}) ')
            self.no_OfAI = self.getUserInputAsInteger(1, maxNoOfBots)

            #Limit User to 500 tokens, if less than 500 available, limit it to the maximum
            # User will never have below 100 tokens as before every game we check and if they are below than 100, give them 100
            if self.player.getTokens() < 500:
                print(f'How many tokens would you like to wager? (100-{self.player.getTokens()}) ')
                self.tokenBet = self.getUserInputAsInteger(100, self.player.getTokens())
            else:
                print('How many tokens would you like to wager? (100-500) ')
                self.tokenBet = self.getUserInputAsInteger(100, 500)

            # Determine random starting position for User
            time.sleep(1)
            self.playerPosition = random.randint(1, self.no_OfAI + 1)

            print(f"\nThe game will begin now, you will go {self.positionDict[self.playerPosition]}")
            time.sleep(1)

            # Draws 2 cards and add them to players hand
            self.player.addCard(self.deck.drawCard())
            self.player.addCard(self.deck.drawCard())

            # Initialize AI objects, each bot draws 2 cards
            self.botPlayerList = []
            tempBotNameList = self.botNamesList.copy()

            # Draw 2 cards for each bot object
            for num in range(self.no_OfAI):
                randomBotName = tempBotNameList.pop(random.randint(0, len(tempBotNameList) - 1))
                botPlayer = BotPlayer(randomBotName)
                botPlayer.addCard(self.deck.drawCard())
                botPlayer.addCard(self.deck.drawCard())
                self.botPlayerList.append(botPlayer)

            # Console dialog to show bot dealing cards to User and all Bots
            print("\nDealer is dealing Cards now...")
            time.sleep(1)
            print("\nYour Hand:\n" + self.player.getPrintHand())
            time.sleep(1)
            #Print out each Bot's hand
            for i in range(0, self.no_OfAI):
                print(f"\n{self.botPlayerList[i].getBotName()} Bot's Hand:\n" + self.botPlayerList[i].getConcealedHand())
                time.sleep(1)

            print("\nRound Begin!")
            time.sleep(1)
            #Initialize Player Number counter and Bot Number Counter, to track whose turn it is
            self.playerCounter = 1
            self.botNumberCounter = 0
            self.turnStart = True # Boolean variable to track whether a player or a bot is just starting his turn or continuing it
            return ('AI Loop', True)

        elif state == 'AI Loop':
            #First, check if playerCounter equals to playerPosition, if so, it is the Player's turn to play
            if self.playerCounter == self.playerPosition:
                if self.turnStart:
                    # Player has just started turn
                    print("\nIt's your turn to play now! Here are your cards: \n")
                    print(self.player.getPrintHand())
                    time.sleep(1)

                    # Get Player Input either YES or NO, then transition to State 'Practice Loop' if YES and 'Start Screen' if NO
                    print(f'\nThe value of your hand is {self.player.handValue()}. Would you like to draw another card? (Y/N)')

                    if self.getUserInputAsChar(yesList = ['Y', 'y'], noList = ['N', 'n']):
                        self.turnStart = False
                        return ('AI Loop', True)
                    else:
                        self.turnStart = True
                        print(f"\nYour turn has ended")
                        self.playerCounter += 1
                        return ('AI Loop', True)

                else:
                    # Player's Turn, has drawn more than once already
                    print('\n* The Dealer deals you a card, here are your Cards: *\n')
                    time.sleep(1)
                    self.player.addCard(self.deck.drawCard())
                    print(self.player.getPrintHand())
                    time.sleep(1)

                    currentcardValue = self.player.handValue()
                    if currentcardValue > 21:
                        print(f"\nThe value of your hand is {self.player.handValue()}. Oops! That's a bust! Your turn is Over\n")
                        self.turnStart = True
                        self.playerCounter += 1
                        return ('AI Loop', True)
                    else:
                        print(f'\nThe value of your hand is {self.player.handValue()}. Would you like to draw another card? (Y/N)')

                        if self.getUserInputAsChar(yesList = ['Y', 'y'], noList = ['N', 'n']):
                            return ('AI Loop', True)
                        else:
                            self.turnStart = True
                            print(f"\nYour turn has ended")
                            self.playerCounter += 1
                            return ('AI Loop', True)

            # Else, check if number of turns elapsed is smaller than the number of players, if so, then now is still a Bot's turn
            elif self.playerCounter <= self.no_OfAI + 1:
                if self.turnStart:
                    # Start a new Turn for AI Bot
                    print(f"\n{self.botPlayerList[self.botNumberCounter].getBotName()} Bot's turn. {self.botPlayerList[self.botNumberCounter].getBotName()} Bot's cards:\n")
                    time.sleep(1)
                    print(self.botPlayerList[self.botNumberCounter].getConcealedHand())
                    botHandValue = self.botPlayerList[self.botNumberCounter].handValue()
                    time.sleep(1)

                    # If AI Bot has a hand value of 17 and above, Bot shall not draw anymore cards
                    if botHandValue >= 17:
                        print(f"\n{self.botPlayerList[self.botNumberCounter].getBotName()} Bot chooses to pass")
                        time.sleep(1.5)
                        self.playerCounter += 1
                        self.botNumberCounter += 1
                        return ('AI Loop', True)

                    else:
                        print(f"\n{self.botPlayerList[self.botNumberCounter].getBotName()} Bot chooses to draw again")
                        time.sleep(1.5)
                        self.turnStart = False
                        return ('AI Loop', True)

                else:
                    # AI Bot continues turn, this is Bot's 2nd or greater turn
                    self.botPlayerList[self.botNumberCounter].addCard(self.deck.drawCard())
                    print(f'\n* The Dealer deals {self.botPlayerList[self.botNumberCounter].getBotName()} Bot a card *\n')
                    time.sleep(1)
                    print(self.botPlayerList[self.botNumberCounter].getConcealedHand())
                    botHandValue = self.botPlayerList[self.botNumberCounter].handValue()
                    time.sleep(1)

                    # If AI Bot has a hand value of 17 and above, Bot shall not draw anymore cards
                    if botHandValue >= 17:
                        print(f"\n{self.botPlayerList[self.botNumberCounter].getBotName()} Bot chooses to pass")
                        time.sleep(1.5)
                        self.turnStart = True
                        self.playerCounter += 1
                        self.botNumberCounter += 1
                        return ('AI Loop', True)

                    else:
                        print(f"\n{self.botPlayerList[self.botNumberCounter].getBotName()} Bot chooses to draw again")
                        time.sleep(1.5)
                        return ('AI Loop', True)

            else:
                # Number of Players has exceeded total number, time to end the game and show the results

                # Create list of all player's hand values
                handValueList = [self.player.handValue()]
                for i in range(self.no_OfAI):
                    handValueList.append(self.botPlayerList[i].handValue())

                # calculate the higher winning value, which is 21 or below
                maxWinningValue = 0
                winnersList = []
                for player, number in enumerate(handValueList):
                    if number > maxWinningValue and number <= 21:
                        maxWinningValue = number
                        winnersList = [(player, number)]
                    elif number == maxWinningValue:
                        nextWinner = (player, number)
                        winnersList.append(nextWinner)

                # Get Bot Names to Format table according to the longest Bot Name (Adjust table to Fit Largest Bot Name)
                botNameList = []
                maxBotNameLength = 0
                for i in range(self.no_OfAI):
                    botName = self.botPlayerList[i].getBotName()
                    if len(botName) > maxBotNameLength:
                        maxBotNameLength = len(botName)
                    botNameList.append(botName)

                maxBotNameLength += 6 # 4 Extra characters to account for ' Bot' + 2 more for side spacing

                # Table showcasing results printed
                print("\nGame Over! Here are the results:\n")
                time.sleep(1)
                print(f"{'Player':^{maxBotNameLength}}|{'Hand Value':^14}")
                print('-'*(15 + maxBotNameLength))
                print(f"{'You':^{maxBotNameLength}}|{handValueList[0]:^14}")
                for i in range(self.no_OfAI):
                    botNameString = f"{self.botPlayerList[i].getBotName()} Bot"
                    print(f"{botNameString:^{maxBotNameLength}}|{handValueList[i+1]:^14}")

    
                if len(winnersList) == 1:
                    # If there is only 1 winner
                    if winnersList[0][0] == 0:
                        # Player has Won!
                        tokensWon = self.tokenBet * (self.no_OfAI + 1)
                        print(f"\nYou have Won! Congratulations! Your winnings are {tokensWon} Tokens!\n")
                        self.player.winTokens(tokensWon - self.tokenBet)

                    else:
                        # Player has lost
                        print(f"\nYou have lost! Unfortunately, you have lost {self.tokenBet} Tokens.\n")
                        self.player.loseTokens(self.tokenBet)

                elif len(winnersList) == 0:
                    # List is empty, no player got 21 and below
                    print(f"\nWOW! It seems like all Players have Busted! You all get your Tokens back :)\n")
                else:
                    # More than one winner
                    if winnersList[0][0] == 0:
                        # If player is in the list of winning players
                        winnerNames = 'You and '
                        for i in range(1, len(winnersList)):
                            winnerNames = winnerNames + f"{self.botPlayerList[winnersList[i][0] - 1].getBotName()} Bot and "
                        winnerNames = winnerNames[:-5]

                        tokensWon = (self.tokenBet * (self.no_OfAI + 1)) // len(winnersList)
                        print(f"\n{winnerNames} have shared the Win! You receive {tokensWon}.\n")
                        self.player.winTokens(tokensWon - self.tokenBet)

                    else:
                        # Player has lost
                        print(f"\nYou have lost! Unfortunately, you have lost {self.tokenBet} Tokens.\n")
                        self.player.loseTokens(self.tokenBet)

                self.resetGame()
                os.system('pause') 
                return ('Start Screen', True)


    def resetGame(self):
        self.deck.resetDeck()
        self.player.clearHand()

    def displayStartMessage(self):
        print(f'''
-----------------------------------------------------------------------------------------------------------------------------------------------------

██████╗ ██╗      █████╗  ██████╗██╗  ██╗     ██╗ █████╗  ██████╗██╗  ██╗    ███████╗██╗███╗   ███╗██╗   ██╗██╗      █████╗ ████████╗ ██████╗ ██████╗ 
██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝     ██║██╔══██╗██╔════╝██║ ██╔╝    ██╔════╝██║████╗ ████║██║   ██║██║     ██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
██████╔╝██║     ███████║██║     █████╔╝      ██║███████║██║     █████╔╝     ███████╗██║██╔████╔██║██║   ██║██║     ███████║   ██║   ██║   ██║██████╔╝
██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██   ██║██╔══██║██║     ██╔═██╗     ╚════██║██║██║╚██╔╝██║██║   ██║██║     ██╔══██║   ██║   ██║   ██║██╔══██╗
██████╔╝███████╗██║  ██║╚██████╗██║  ██╗╚█████╔╝██║  ██║╚██████╗██║  ██╗    ███████║██║██║ ╚═╝ ██║╚██████╔╝███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚══════╝╚═╝╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝

Written by: Ang Song Gee

(For a better experience, resize your terminal to Full-Screen!)

''', end = '')

    def getUserInputAsInteger(self, start, end):
        # Gets User input, from an integer range containing start and end
        while True:
            userInput = input("")
            try:
                integerInput = int(userInput)
                if integerInput >= start and integerInput <= end:
                    break
                else:
                    print("Value entered is not Valid! Try again:")
            except ValueError:
                print("Value entered is not Valid! Try again: ")

        return integerInput

    def getUserInputAsChar(self, yesList, noList):
        # Gets User input, from an list of Characters, if User inputs char in yesList, return True, vice versa for noList
        while True:
            userInput = input("")
            if userInput in yesList:
                return True
            
            elif userInput in noList:
                return False

            else:
                print("Character entered is not Valid! Try again")


myGame = GameSM()
myGame.start()
gameStillOn = True

'''After each state, myGame.step will always return True, to keep loop going, until the player inputs 3 in the Start Screen to close the program, 
   at that time the output will be False, which is when this while loop will terminate and the program will end '''
while (gameStillOn):
    gameStillOn = myGame.step(True)