import math
import os
import time
import numpy as np
import itertools
import game_vectorized

MAX_CARDS = 13
DISPLAY_STRATEGIES = 10
MAX_ELO = 5000
MIN_ELO = 1
N_ROUNDS = 1000
ELO_K = 32
HAMMING_FILTER = 6


def elo_prob(rating_1, rating_2):
    # Probability player 1 beats player 2
    return 1.0 / (1 + 1.0 * math.pow(10, (rating_1 - rating_2)/400))


def normalize_elos(elos):
    return_elos = elos.copy()
    if np.min(return_elos) < MIN_ELO:
        return_elos += MIN_ELO - np.min(return_elos)
    if np.max(return_elos) > MAX_ELO:
        return_elos /= np.max(return_elos) / MAX_ELO
    return return_elos

np.set_printoptions(formatter={'float': '{: 0.0f}'.format})

for i in range(3, MAX_CARDS+1):
    game = game_vectorized.Game(i, hamming_filter=HAMMING_FILTER)
    game.compute_strategy_outcomes()
    game.compute_scores()
    game.compute_summary_scores()

    strategy_participation = np.ones(game.n_strategies)/game.n_strategies
    previous_elos = np.ones(game.n_strategies) * 1600
    current_elos = np.ones(game.n_strategies) * 1600

    for n in range(N_ROUNDS):
        start_time = time.time()
        for s1, s2 in itertools.combinations(list(range(i)), 2):
            Pa = elo_prob(previous_elos[s1], previous_elos[s2])
            Pb = 1 - Pa
            current_elos[s1] += ELO_K * (game.vs_summary[s1, s2] - Pa)# * strategy_participation[s2]
            current_elos[s2] += ELO_K * (game.vs_summary[s2, s1] - Pb)# * strategy_participation[s1]
        current_elos = normalize_elos(current_elos)
        strategy_participation = current_elos / np.sum(current_elos)
        previous_elos = current_elos.copy()

    sorted_ind = np.argsort(current_elos)
    print(f"ELO summary for {i} cards and {N_ROUNDS} iterations.")
    for index in reversed(sorted_ind):
        if index > game.n_strategies and index < (game.n_strategies - DISPLAY_STRATEGIES):
            continue
        print(f"{game.dealer_space[game.strategies[index]]} : {current_elos[index]:0.1f}")# : {game.vs_summary[index, list(reversed(sorted_ind))]}")

