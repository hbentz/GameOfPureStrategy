from array import array
import math
import os
import time
import numpy as np
import itertools
import game_vectorized

N_CARDS = 5
DISPLAY_STRATEGIES = 10
MAX_ELO = 5000
MIN_ELO = 1
N_ROUNDS = 1000
ELO_K = 32


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


game = game_vectorized.Game(N_CARDS)
game.compute_strategy_outcomes()
game.compute_scores()
game.compute_summary_scores()

strategy_participation = np.ones(game.strategy_space)/game.strategy_space
previous_elos = np.ones(game.strategy_space) * 1600
current_elos = np.ones(game.strategy_space) * 1600

for n in range(N_ROUNDS):
    start_time = time.time()
    for s1, s2 in itertools.combinations(list(range(N_CARDS)), 2):
        Pa = elo_prob(previous_elos[s1], previous_elos[s2])
        Pb = 1 - Pa
        current_elos[s1] += ELO_K * (game.vs_summary[s1, s2] - Pa)# * strategy_participation[s2]
        current_elos[s2] += ELO_K * (game.vs_summary[s2, s1] - Pb)# * strategy_participation[s1]
    current_elos = normalize_elos(current_elos)
    strategy_participation = current_elos / np.sum(current_elos)
    previous_elos = current_elos.copy()
    os.system('cls')
    sorted_ind = np.argsort(current_elos)
    print(f"Round {n}:" + ("( %s seconds )" % (time.time() - start_time)))
    for index in reversed(sorted_ind):
        if index > DISPLAY_STRATEGIES and index < (game.strategy_space - DISPLAY_STRATEGIES):
            continue
        print(f"{game.dealer_space[index]} : {current_elos[index]:0.1f} : {strategy_participation[index]:0.3f}")# : {game.vs_summary[index, list(reversed(sorted_ind))]}")


