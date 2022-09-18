import json
import os
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
    call_dict[f"{i}_over_random"] = n_over_random(i)
    call_dict[f"{i}_under_random"] = n_under_random(i)
    call_dict[f"{i}_over_split"] = n_over_split(i)
    call_dict[f"{i}_under_split"] = n_under_split(i)


test_remainder = call_dict.copy()

game = Game()
n_samples = 100000
f_name = "100k_trials.json"\

if os.path.exists(f_name):
    with open(f_name, "r") as f:
        results_dict = json.load(f)
        print("results dict loaded as")
        print(results_dict)
else:
    results_dict = {}


for strategy in call_dict.keys():
    if strategy not in results_dict:
        results_dict[strategy] = {}


for strategy, strat_call in call_dict.items():
    for opponent, opp_call in test_remainder.items():
        if opponent in results_dict[strategy]:
            continue
        delta = 0
        for i in range(n_samples):
            game.__init__()
            delta += game.run_sim(strat_call, opp_call)
        print(f"{strategy}-{(delta/2/n_samples + 0.5)*100:0.2f}%-{opponent}")
        results_dict[strategy][opponent] = (delta/2/n_samples +0.5)
        results_dict[opponent][strategy] = 1 - (delta/2/n_samples +0.5)
    _ = test_remainder.pop(strategy)


with open(f_name, "w+") as f:
    json.dump(results_dict, f)