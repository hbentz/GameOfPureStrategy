import math
import os
import numpy as np
from strategies import random_pick, same_value, min_bet, max_bet, split_bet,\
    win_threshold_percent_bet, win_threshold_percent_bet2, max_delta,\
    n_under_pure, n_over_pure, n_under_random, n_over_random, n_under_split, n_over_split
from ..game import Game

call_dict = {
    "random_pick": random_pick,
    "same_value": same_value,
    "min_bet": min_bet,
    "max_bet": max_bet,
    "split_bet": split_bet,
    "win_threshold_percent_bet": win_threshold_percent_bet,
    "win_threshold_percent_bet2": win_threshold_percent_bet2,
    "max_delta": max_delta,
}

for i in range(1, 9):
    call_dict[f"{i}_over_pure"] = n_over_pure(i)
    call_dict[f"{i}_under_pure"] = n_under_pure(i)
    #call_dict[f"{i}_over_random"] = n_over_random(i)
    #call_dict[f"{i}_under_random"] = n_under_random(i)
    #call_dict[f"{i}_over_split"] = n_over_split(i)
    #call_dict[f"{i}_under_split"] = n_under_split(i)

def elo_prob(rating_1, rating_2):
    return 1.0 / (1 + 1.0 * math.pow(10, (rating_1 - rating_2)/10000))

# The string name of the item vs index in the arry
elo_dict = {}
elo_dict_reversed = {}
for i, key in enumerate(call_dict.keys()):
    elo_dict[key] = i
    elo_dict_reversed[i] = key

elo_prev = [0] * len(call_dict.keys())
elo_prev = np.asarray(elo_prev, dtype=np.float64)
elo_curr = elo_prev.copy()

k_max = 100
k__decay = 1
game = Game()
k = 1
n_trials = 100

for run in range(100000):
    # Reset the list of opponents available
    rr_remainder = call_dict.copy()
    for strategy, strat_call in call_dict.items():
        for opponent, opp_call in rr_remainder.items():
            # Skip mirror matches
            if strategy == opponent:
                continue

            # Run n_trials matches recording the W-L delta for the strategy
            delta = 0
            for _ in range(n_trials):
                game.__init__()
                delta += game.run_sim(strat_call, opp_call)
            # Get the actual win rate and the expected win rate
            p1_win_rate = 0.5 + (delta / 2)
            Pa = elo_prob(elo_prev[elo_dict[strategy]], elo_prev[elo_dict[opponent]])
            Pb = 1 - Pa
            # Award Elo accordingly, rounding to prevent elo blowups
            elo_curr[elo_dict[strategy]] += round(k * (p1_win_rate - Pa))
            elo_curr[elo_dict[opponent]] += round(k * ((1 - p1_win_rate) - Pb))
        # Once a strategy has played all opponents, remove it so it doesn't get any double jeporady matches
        _  = rr_remainder.pop(strategy)
    # Shift the ELO curves up so they're all above zero
    if min(elo_curr) < 0:
        elo_curr -= min(elo_curr)
    # Update the elo rankings, only after all matches are played so the rankings are order agnostic
    elo_prev = elo_curr
    # Print our the results
    os.system('cls')
    sorted_ind = np.argsort(elo_curr)
    for index in reversed(sorted_ind):
        print(f"{elo_curr[index]:0.0f} : {elo_dict_reversed[index]}")
    _ = input()
