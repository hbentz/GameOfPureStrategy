import random
import numpy as np

def random_pick(curr_stock, ally, opp, game_state):
    return random.choice(ally.hand)


def same_value(curr_stock, ally, opp, game_state):
    return curr_stock


def n_under_pure(n):
    def callback(curr_stock, ally, opp, game_state):
        arr = np.asarray(ally.hand)
        index = (np.abs(arr - (curr_stock -n))).argmin()
        return ally.hand[index]
    return callback


def n_over_pure(n):
    def callback(curr_stock, ally, opp, game_state):
        arr = np.asarray(ally.hand)
        index = (np.abs(arr - (curr_stock + n))).argmin()
        return ally.hand[index]
    return callback


def n_under_random(n):
    def callback(curr_stock, ally, opp, game_state):
        if curr_stock - n in ally.hand:
            return curr_stock - n
        else:
            return random.choice(ally.hand)
    return callback


def n_over_random(n):
    def callback(curr_stock, ally, opp, game_state):
        if curr_stock + n in ally.hand:
            return curr_stock + n
        else:
            return random.choice(ally.hand)
    return callback


def n_under_split(n):
    def callback(curr_stock, ally, opp, game_state):
        if curr_stock - n in ally.hand:
            return curr_stock - n
        elif curr_stock >= 8:
            return max(ally.hand)
        else:
            return min(ally.hand)
    return callback


def n_over_split(n):
    def callback(curr_stock, ally, opp, game_state):
        if curr_stock + n in ally.hand:
            return curr_stock + n
        elif curr_stock >= 8:
            return max(ally.hand)
        else:
            return min(ally.hand)
    return callback


def max_bet(curr_stock, ally, opp, game_state):
    return max(ally.hand)


def min_bet(curr_stock, ally, opp, game_state):
    return min(ally.hand)


def split_bet(curr_stock, ally, opp, game_state):
    if curr_stock >= 8:
        return max(ally.hand)
    else:
        return min(ally.hand)


def win_threshold_percent_bet(curr_stock, ally, opp, game_state):
    desired_bid = int(curr_stock / (46 - ally.points) * sum(ally.hand))
    arr = np.asarray(ally.hand)
    index = (np.abs(arr - desired_bid)).argmin()
    return ally.hand[index]


def win_threshold_percent_bet2(curr_stock, ally, opp, game_state):
    desired_bid = int((curr_stock + game_state.tie_carry) / (46 - ally.points) * sum(ally.hand))
    arr = np.asarray(ally.hand)
    index = (np.abs(arr - desired_bid)).argmin()
    return ally.hand[index]


def max_delta(curr_stock, ally, opp, game_state):
    return ((13 - curr_stock) + 1)


def bide_simple(curr_stock, ally, opp, game_state):
    if opp.points <= 0:
        return min(ally.hand)
    elif curr_stock + 2 in ally.hand:
        return curr_stock + 2
    else:
        return max(ally.hand)


def card_counter(curr_stock, ally, opp, game_state):
    if curr_stock > (sum(game_state.bid_pile) + curr_stock) / (len(game_state.bid_pile) + 1):
        if curr_stock + 2 in ally.hand:
            return curr_stock + 2
        else:
            return max(ally.hand)
    else:
        return min(ally.hand)
