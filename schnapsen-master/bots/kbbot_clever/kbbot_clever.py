#!/usr/bin/env python
"""
This is a bot that applies propositional logic reasoning to determine its strategy.
The strategy it uses is determined by what is defined in load.py. Here it is to always
pick a Jack to play whenever this is a legal move.

It loads general information about the game, as well as the definition of a strategy,
from load.py.
"""

from api import State, util, Deck
import random, load_clever

from kb import KB, Boolean, Integer

class Bot:

    def __init__(self):
        pass

    def get_move(self, state):

        moves = state.moves()

        random.shuffle(moves)

        for move in moves:

            if not self.kb_consistent_trumpace(state, move):
                # Plays the first move that makes the kb inconsistent. We do not take
                # into account that there might be other valid moves according to the strategy.
                # Uncomment the next line if you want to see that something happens.
                # print "Strategy Applied"

                print "Card played:"
                print util.get_card_name(move[0])
                return move

            if not self.kb_consistent_jack(state, move):
                print "Card played:"
                print util.get_card_name(move[0])
                return move

        # If no move that is entailed by the kb is found, play random move
        return random.choice(moves)

    # Note: In this example, the state object is not used,
    # but you might want to do it for your own strategy.
    def kb_consistent_trumpwedding(self, state, move):
    # type: (State, move) -> bool

        # each time we check for consistency we initialise a new knowledge-base
        kb = KB()

        # Add general information about the game

        suit = State.get_trump_suit(state)
        if suit == "c":
            kb.add_clause(Boolean("tq3"))
            kb.add_clause(Boolean("tk2"))
        elif suit == "d":
            kb.add_clause(Boolean("tq8"))
            kb.add_clause(Boolean("tk7"))
        elif suit == "h":
            kb.add_clause(Boolean("tq13"))
            kb.add_clause(Boolean("tk12"))
        elif suit == "s":
            kb.add_clause(Boolean("tq18"))
            kb.add_clause(Boolean("tk17"))

        load_clever.general_information(kb)

        # Add the necessary knowledge about the strategy
        load_clever.strategy_knowledge(kb)

        # This line stores the index of the card in the deck.
        # If this doesn't make sense, refer to _deck.py for the card index mapping
        index = move[0]
        index2 = move[1]

        # This creates the string which is used to make the strategy_variable.
        # Note that as far as kb.py is concerned, two objects created with the same
        # string in the constructor are equivalent, and are seen as the same symbol.
        # Here we use "pj" to indicate that the card with index "index" should be played with the
        # PlayJack heuristics that was defined in class. Initialise a different variable if 
        # you want to apply a different strategy (that you will have to define in load.py)
        variable_string = "ptw" + str(index)
        strategy_variable = Boolean(variable_string)

        # Add the relevant clause to the loaded knowledge base
        kb.add_clause(~strategy_variable)

        # If the knowledge base is not satisfiable, the strategy variable is
        # entailed (proof by refutation)

        if move[1] != None:
            suit = State.get_trump_suit(state)
            print suit
            print "Move to check out:"
            print move
            print kb.satisfiable()

        return kb.satisfiable()


    def kb_consistent_trumpace(self, state, move):
    # type: (State, move) -> bool

        # each time we check for consistency we initialise a new knowledge-base
        kb = KB()

        # Add general information about the game

        suit = State.get_trump_suit(state)
        if suit == "c":
            kb.add_clause(Boolean("ta0"))
        elif suit == "d":
            kb.add_clause(Boolean("ta5"))
        elif suit == "h":
            kb.add_clause(Boolean("ta10"))
        elif suit == "s":
            kb.add_clause(Boolean("ta15"))

        load_clever.general_information(kb)

        # Add the necessary knowledge about the strategy
        load_clever.strategy_knowledge(kb)

        # This line stores the index of the card in the deck.
        # If this doesn't make sense, refer to _deck.py for the card index mapping
        index = move[0]

        variable_string = "pta" + str(index)
        strategy_variable = Boolean(variable_string)

        # Add the relevant clause to the loaded knowledge base
        kb.add_clause(~strategy_variable)

        # If the knowledge base is not satisfiable, the strategy variable is
        # entailed (proof by refutation)

        return kb.satisfiable()

    def kb_consistent_jack(self, state, move):
    # type: (State, move) -> bool

        # each time we check for consistency we initialise a new knowledge-base
        kb = KB()

        # Add general information about the game
        load_clever.general_information(kb)

        # Add the necessary knowledge about the strategy
        load_clever.strategy_knowledge(kb)

        # This line stores the index of the card in the deck.
        # If this doesn't make sense, refer to _deck.py for the card index mapping
        index = move[0]

        # This creates the string which is used to make the strategy_variable.
        # Note that as far as kb.py is concerned, two objects created with the same
        # string in the constructor are equivalent, and are seen as the same symbol.
        # Here we use "pj" to indicate that the card with index "index" should be played with the
        # PlayJack heuristics that was defined in class. Initialise a different variable if
        # you want to apply a different strategy (that you will have to define in load.py)
        variable_string = "pj" + str(index)
        strategy_variable = Boolean(variable_string)

        # Add the relevant clause to the loaded knowledge base
        kb.add_clause(~strategy_variable)

        # If the knowledge base is not satisfiable, the strategy variable is
        # entailed (proof by refutation)
        return kb.satisfiable()