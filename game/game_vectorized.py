import numpy as np
import math
import itertools

class Game:
    def __init__(self, n_cards, hamming_filter=0):
        self.n_cards = n_cards
        # How many possible deals/pure strategies there are
        self.n_deals = math.factorial(n_cards)

        # All possible shuffles of an n_card deck are stored in self.dealer_space
        # So that the card dealt on turn n is self.dealer_space[deal_id, n] + 1
        # This doubles as all the possible pure strategies
        # Where a strategy with id n will bid self.dealer_space[n, card - 1]
        self.dealer_space = np.ones((self.n_deals, n_cards), dtype=np.int8)
        
        # Fill the dealerspace with all possible permutations
        for row, permutation in enumerate(itertools.permutations(list(range(n_cards)), n_cards)):
            self.dealer_space[row, :] = permutation
        
        if hamming_filter > 0:
            self.strategies = np.where(self.compute_hamming_distances() <= hamming_filter)[0]
        else:
            self.strategies = np.arange(self.n_deals)

        self.n_strategies = self.strategies.shape[0]

        # self.strategy_outcomes[strategy_1, strategy_2, card] = 1: strategy_1 wins the trick, 0: draw, -1: strategy_2 wins the trick
        self.strategy_outcomes = np.zeros((self.n_strategies, self.n_strategies, n_cards), dtype=np.int8)
        
        # self.scores[strategy_1, strategy_2, deal_id, turn] = the score advantage strategy1 gained from turn on deal_id
        self.scores = np.zeros((self.n_strategies, self.n_strategies, self.n_deals, self.n_cards), dtype=np.int8)
        self.vs_summary = np.zeros((self.n_strategies, self.n_strategies), dtype=np.float)
        self.summary = np.zeros(self.n_strategies, dtype=np.float)

    def compute_strategy_outcomes(self):
        deals, cards = self.dealer_space.shape
        for n in range(1, self.n_strategies):
            # Roll each strategy by n and compare it to the original to see which would win for what card
            # For a roll of 1 with 4 strategies [s1, s2, s3, s4] vs [s2, s3, s4, s1]
            p1_beats_p2 = (self.dealer_space[self.strategies, :] > np.roll(self.dealer_space[self.strategies, :], n, axis=0))
            p2_beats_p1 = (self.dealer_space[self.strategies, :] < np.roll(self.dealer_space[self.strategies, :], n, axis=0))
            # Record the outcomes such that outcome[deal_id, card] = 1: 1: s1 wins, 0: draw, -1: s2 wins
            outcomes = 1 * p1_beats_p2 - 1 * p2_beats_p1
            # For each card value convert the outcomes into the correct space, eg np.diag for n=1 and 4 strategies at an arbitraty card is
            # [[0, s1 vs s2, 0, 0],
            #  [0, 0, s2 vs s3, 0],
            #  [0, 0, 0, s3 vs s4],
            #  [0, 0, 0, 0]]
            for card in range(cards):
                self.strategy_outcomes[:,:,card] += np.diag(outcomes[:-n, card], n)
                self.strategy_outcomes[:,:,card] -= np.diag(outcomes[:-n, card], -n)

    def compute_scores(self):
        # Find the winner for each turn, note that the indicies for the strategies and deal_ids line up
        for turn in range(self.n_cards):
            self.scores[:, :, :, turn] = self.strategy_outcomes[:, :, self.dealer_space[:, turn]] 
                
        # Back propigate ties
        for turn in range(self.n_cards-1, 0, -1):
            self.scores[:, :, :, turn-1] += (self.scores[:, :, :, turn-1] == 0) * self.scores[:, :, :, turn]
        
        # Compute the scores
        self.scores *= (self.dealer_space + 1)[np.newaxis, np.newaxis, :, :]

    def compute_summary_scores(self):
        self.vs_summary += np.sum(np.sum(self.scores, axis=3) > 0, axis=2) * 1.0
        self.vs_summary += np.sum(np.sum(self.scores, axis=3) == 0, axis=2) * 0.5
        self.vs_summary /= self.n_deals
        self.summary = np.sum(self.vs_summary, axis=1)
        self.summary *= 1 / self.n_strategies

    def compute_hamming_distances(self):
        return np.sum(np.abs(self.dealer_space - self.dealer_space[0, :][np.newaxis, :]), axis=1)

