import numpy as np
import math
import itertools

class Game:
    def __init__(self, n_cards):
        self.n_cards = n_cards
        # How many possible deals/pure strategies there are
        self.strategy_space = math.factorial(n_cards)

        # All possible shuffles of an n_card deck are stored in self.dealer_space
        # So that the card dealt on turn n is self.dealer_space[deal_id, n] + 1
        # This doubles as all the possible pure strategies
        # Where a strategy with id n will bid self.dealer_space[n, card - 1]
        self.dealer_space = np.ones((self.strategy_space, n_cards), dtype=np.int8)
        
        # Fill the dealerspace with all possible permutations
        for row, permutation in enumerate(itertools.permutations(list(range(n_cards)), n_cards)):
            self.dealer_space[row, :] = permutation
        
        # self.strategy_outcomes[strategy_1, strategy_2, card] = 1: strategy_1 wins the trick, 0: draw, -1: strategy_2 wins the trick
        self.strategy_outcomes = np.zeros((self.strategy_space, self.strategy_space, n_cards), dtype=np.int8)
        
        # self.scores[strategy_1, strategy_2, deal_id, turn] = the score advantage strategy1 gained from turn on deal_id
        self.scores = np.zeros((self.strategy_space, self.strategy_space, self.strategy_space, self.n_cards), dtype=np.int8)

    def compute_strategy_outcomes(self):
        deals, cards = self.dealer_space.shape
        for n in range(1, deals):
            # Roll each strategy by n and compare it to the original to see which would win for what card
            # For a roll of 1 with 4 strategies [s1, s2, s3, s4] vs [s2, s3, s4, s1]
            # As s1 vs s4 will be covered when the roll is 3 ([s1, s2, s3, s4] vs [s4, s3, s2, s1])
            # The last n matchups can be discarded
            p1_beats_p2 = self.dealer_space > np.roll(self.dealer_space, n, axis=0)[:-n]
            p2_beats_p1 = self.dealer_space < np.roll(self.dealer_space, n, axis=0)[:-n]
            # Record the outcomes such that outcome[deal_id, card] = 1: 1: s1 wins, 0: draw, -1: s2 wins
            outcomes = 1 * p1_beats_p2 - 1 * p2_beats_p1
            # For each card value convert the outcomes into the correct space, eg np.diag for n=1 and 4 strategies at an arbitraty card is
            # [[0, s1 vs s2, 0, 0],
            #  [0, 0, s2 vs s3, 0],
            #  [0, 0, 0, s3 vs s4],
            #  [0, 0, 0, 0]]
            for card in range(cards):
                self.strategy_outcomes[:,:,card] += np.diag(1 * p1_beats_p2[:,card] - 1 * p2_beats_p1[:,card], n)

    def compute_scores(self):
        # Find the winner for each turn, note that the indicies for the strategies and deal_ids line up
        for turn in range(self.n_cards):
            self.scores[:, :, :, turn] = self.strategy_outcomes[:, :, self.dealer_space[:, turn]] 
                
        # Back propigate ties
        for turn in range(self.n_cards-1, 0, -1):
            self.scores[:, :, :, turn-1] += (self.scores[:, :, :, turn-1] == 0) * self.scores[:, :, :, turn]
        
        # Compute the scores
        self.scores *= (self.dealer_space + 1)[np.newaxis, np.newaxis, :, :]
                