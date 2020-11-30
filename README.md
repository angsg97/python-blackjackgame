# Blackjack Simulator Game
## by Ang Song Gee

### 1. The Game

I have created a single-player *Blackjack* game, which uses **command line inputs** and **print statements** to interact with the user. The rules of the game may not follow the exact Blackjack rules that are used officially; Simply, the aim of the game is to draw enough cards, until you are able to get a sufficiently high value that trumps the values of the other players' cards. However, one caveat is that the value of your cards **may not exceed 21** to win the game. Each player takes turns, during the player's turn, he/she must decide whether to draw or to pass. It's ok to keep drawing, but beware, going above a value of 21 instantly ends your turn, as that is considered a BUST, and a losing hand. Here are the card values:

|   Card Value Number    |      Card Numerical Value      |
| :--------------------: | :----------------------------: |
| 2, 3, 4, 5, 6, 7, 8, 9 | Follows the number of the Card |
|      10, J, Q, K       |               10               |
|           A            |         Either 1 or 11         |

The Ace is a special card, it can either be 1 or 11, depending on the value of the other cards in your hand. If your hand value is 10 or less without the Ace, it takes a value of 11. Otherwise, it takes the value of 1, as a value of 11 would cause your hand value to be greater than 21. 

In this game, Bots are present in the game to play along with you; I mean, how could it be a Blackjack game without other players right? By waging Tokens and winning games against the Bots, you would be able to increase your Token count. Feed the inner gambler in you, while having nothing at stake in real life!

### 2. How to Play

There are 2 Game Modes available:

1. **Practice Mode**
2. **AI Mode**

In **Practice Mode**, the Player gets the chance to practice drawing cards from the Dealer, and to Practice getting a hang of the odds required to stay below a hand value of 21. At the start, the dealer deals 2 Cards to the player. The total hand value is shown to you, and you are to decide whether you would like to draw or not to draw. If you decide not to draw, your turn ends immediately, and that is the value of your final hand. You may keep drawing, but if your hand value goes above 21, the game ends there. The great part about this mode is that, no tokens are lost! Practice to your heart's desire!

At the starting screen in the game, Enter '1' to play in Practice Mode. At the end of each round, you may decide to draw again by entering 'Y' or 'y', and to return to the Main Screen by entering 'N' or 'n'.

In **AI Mode**, this is where the stakes are raised! At the beginning of the program, you get 1000 Tokens. Before the game starts, you get to choose how many AI Players you want to play against, together with how many Tokens you would like to Bet. ***BEWARE!*** The more players there are, the harder it will be to win! Basically, each AI Bot will mirror your Bet, and the Tokens go into a prize pool, which goes to the winner, or is split equally in the case of multiple winners. Your turn position in the game is randomized, during your turn, the game plays in the same way as in Practice Mode, just draw cards until you'd like to stop. 

After each player has ended this turn, the hand value are revealed! The player(s) with the highest hand value under or equal to 21 is(are) the winner(s). If you lost, then your Tokens are gone. If you won, then you win the amount in the prize pool, which again, could be shared between more than 1 player. 

At the starting screen in the game, Enter '2' to play in AI Mode. You will then get to choose between 1-6 Bot Players, and how many Tokens you would like to wager (Between 100 to 500). Depending on your position, which is randomly determined, you will most likely see a few bots taking their turns, before you. During your turn, same as Practice, you may decide to draw again by entering 'Y' or 'y', and to return to the Main Screen by entering 'N' or 'n'.

After all players have taken their turns, a table will be displayed, showing the final hand values of each player. The console will display whether you've won or not, and showing you how many tokens you have won or lost! 

That's all there is to playing the Blackjack Simulator Game! Enjoy!



### 3. My Code

These are the imported libraries used in this code

- **sm from libdw**
- **random**
- **time**
- **os**

Object Oriented Programming is used heavily in this code, and these are the classes used

1. **Card**
2. **Deck**
3. **Player** (Parent Class)
   - **UserPlayer** (Child Class)
   - **BotPlayer** (Child Class)
4. **GameSM**

All the code is stored in and ran from the blackjack.py file. 

### 3.1 Card

Object that represents a playing card. A **Card** is initialized by passing 4 values, the **value**, **valueSymbol**, **suit** and **suitSymbol**, which will come from the the **Deck** class. **printedCard** is an attribute of **Card**, which is a list of strings that when joined together by newline characters and printed, shows a playing card on the console. The **Card** class contains 3 methods: **getPrintedCard()**, **getCardArrayForPrint()** and **getValue()**.

- **getPrintedCard()** returns a string that is obtained by joining the strings in the list **printedCard**, by '\n' character. This String is used to print out a single card on the console on its own
- **getCardArrayForPrint()** returns the array **printedCard**, which is used in the **Player** class to combine various cards together for printing in the console
- **getValue()** returns the value of the **Card**, stored in the **value** attribute, which was passed in upon initialization from the **Deck** class

### 3.2 Deck

Object that initializes a list of 52 cards, there being 13 different card values and 4 different suits available. A **Deck** is initialized with no arguments; During initialization, each **Card** is initialized using a double for Loop, through the 13 card values and 4 different suits, where each card is represented by a tuple, inside a list named **listOfCards**. The **Deck** class contains 2 methods: **drawCard()** and **resetDeck()**.

- **drawcard()** initializes and returns a randomized **Card** Object from the stored list, while also removing the values of the selected **Card** Object from the **listOfCards** list. This simulates a card being drawn from a deck
- **resetDeck()** resets the **listOfCards** list by emptying the list, and then recreating all 52 **Card** Objects and repopulating the list with those cards

### 3.3 Player

An object that functions as the Parent class for the **UserPlayer** and **BotPlayer** classes. This object contains basic functionality such as storing and adding **Cards**, getting the total value of cards in the hand, and functions to help to print the entire hand in the console. It is initialized without any arguments. One key attribute of this class is the **handCards** list, a list containing all the card objects associated with that **Player**. The **Player** class contains 3 methods: **addCard()**, **handValue()** and **getPrintHand()**.

- **addCard()** takes in a **Card** Object as an argument, and appends that **Card** into the **handCards** list. Simulates adding a card to a Player's hand
- **handValue()** calculates and returns the total value of the **Player**'s' hand, by summing up the total value of all the **Card** Objects in **handCards**. If there is in Ace in the hand, determines whether or not that Ace's value is 1 or 11 based on the total hand value
- **getPrintHand()** returns a string for printing a **Player**'s hand cards in the console. It combines the individual rows of lines of all the **Card** objects, before then joining all the rows using a '\n'. This has to be done in this manner as the console is printed line by line

#### 3.3.1 UserPlayer (Child of Player Class)

An object that inherits the **Player** Class, building upon **Player** methods and attributes. **UserPlayer** is initialized with a *integer* argument containing the number of starting tokens, with a default value of 1000. Contains integer attribute **tokens** to store amount of tokens the **UserPlayer** has throughout the entire game session, and methods to get and edit **tokens**, as well as a method to reset the **Player**'s Hand cards. The **UserPlayer** class contains 4 methods: **getTokens()**, **winTokens()**, **loseTokens()** and **clearHand()**.

- **getTokens()** returns the value of the attribute **tokens**
- **winTokens()** increases the **Userplayer**'s **tokens** based on the value of the argument passed in
- **loseTokens()** subtracts the **Userplayer**'s **tokens** based on the value of the argument passed in
- **clearHand()** reset the **UserPlayer**'s hand when called, by setting the value of the inherited attribute **handCards** to an empty list

#### 3.3.2 BotPlayer (Child of Player Class)

An object that inherits the **Player** Class, building upon **Player** methods and attributes. **BotPlayer** is initialized with a string argument **name**, which is then stored in a class attribute **self.name**. The **BotPlayer** class contains 2 methods: **getBotName()**, **getConcealedHand()**.

- **getBotName()** returns the value of the attribute name
- **getConcealedHand()** is a variation of the **getPrintHand()** in the **Player** class, which instead of printing all cards, only prints the first card revealed, while the rest of the cards are printed lying face down. Similarly, **getConcealedHand()** combines rows of lines and then join them by a '\n' character and returns that string for printing in the console later on

### 3.4 GameSM

Object that inherits the **SM** class from the **sm** package in **lidbw**. It is initialized with no attributes, and *start_state* begins from the state 'Start Screen'. Other attributes include *positionDict*, a dictionary to convert integer positions to strings, Eg. 1 to '1st', and also *botNamesList*, a list of strings containing Bot Names. The **GameSM** class contains 5 methods:  **displayStartMessage()**,  **getUserInputAsInteger()**,  **getUserInputAsChar()**,  **resetGame()** and  **get_next_values()**.

- **displayStartMessage()** is a helper function that helps to print out a multi-line string for the Start message of the program

- **getUserInputAsInteger(start, end)** takes in 2 integer arguments, and gets an input from the User in the console. If valid, an integer input that is between start to end inclusively is returned. If an invalid value is entered, prompts the User to enter a new value until valid

- **getUserInputAsChar(yesList, noList)** takes in 2 lists of strings, and returns True or False based on User input. It gets an input from the User in the console. If the User input is not a string in either of the 2 lists, prompts User to enter a new value until Valid. If User enters a value found in yesList, return True. If User enters a value found in noList, return False

- **resetGame()** helper function to keep code tidy. Runs the **resetDeck()** and **clearHand()** functions on the current instance of the **Deck** and Player Objects respectively, at the end of each game instance in both Practice and AI Mode

- **get_next_values(state, inp)** is a key method of the State Machine, which takes in a state and an input, and runs the steps of the game for that state. Lastly, it returns a tuple containing the next state, as well as the output (True or False). For Output, False is only returned after the User has decided to quit the game, which causes the main loop of the game to end. The Table below summarizes the different States used:

- | State No. | State Name                        | Possible Next State No. |
  | --------- | --------------------------------- | ----------------------- |
  | 1         | Start Screen                      | 2, 5, 7                 |
  | 2         | Practice                          | 3, 4                    |
  | 3         | Practice Loop                     | 3, 4                    |
  | 4         | Start-Over User Dialog (Practice) | 1, 2                    |
  | 5         | AI                                | 6                       |
  | 6         | AI Loop                           | 1, 6                    |
  | 7         | End                               | -                       |

  1. For State No. 1, **Start Screen**, there are 3 possible outputs, based on the User's Input, you can enter either **Practice Mode**, **AI Mode**, or **End**
  2. For State No. 2, **Practice**, it runs the starting sequence of Practice Mode, if the User decide not to draw, the game enters the **Start-Over User Dialog (Practice)**. If the Player draws, enter the **Practice Loop**
  3. For State No. 3, **Practice Loop**, it draws the User a card. If the User's hand value is above 21, or decides not to draw anymore, display Final Value of User's hand, and enter the **Start-Over User Dialog (Practice)**. If User chooses to draw again, enter **Practice Loop** again
  4. For State No. 4, **Start-Over User Dialog (Practice)**, asks the User to decide whether to restart **Practice**, or to go back to the **Start Screen**. Based on User Input, enters the 2 aforementioned states
  5. For State No. 5, **AI**, runs through the Setup for the AI Mode, and deals Cards for the **UserPlayer** and all **BotPlayer** Objects in the game, and determines position of **UserPlayer**. After Setup, enters the **AI Loop**
  6. For State No. 6, **AI Loop**, it determines whether it is a **UserPlayer**'s turn or a **BotPlayer** turn. If it is a **UserPlayer**'s turn, displays the same options as in Practice Loop to also the User to draw cards. This Loop is continued until either the User's Hand Value goes above 21, or the User chooses to stop drawing cards. If it is a **BotPlayer**'s turn, it draws cards and ends it's turn based on a predetermined algorithm. When all Player's turns have come to an end, it tubulates and displays the results, and either adds or substract the **UserPlayer**'s Tokens based on whether the User won or lost. At the end, bring User back to the **Start Screen** State
  7. For State No. 7, **End**, it can only be reached by the User inputting a value of 3 in the Start Screen input dialog. This is the final state in the game, afterwards, the While Loop of the game is terminated and the game process ends

Link to URL of game demo: https://youtu.be/FmMq1bE7KEU