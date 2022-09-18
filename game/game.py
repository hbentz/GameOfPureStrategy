import random

class Player:
    def __init__(self):
        self.hand = list(range(1,14))
        self.points = 0


class Game:
    def __init__(self):
        self.bid_pile = list(range(1,14))
        random.shuffle(self.bid_pile)
        self.tie_carry = 0
        self.p1 = Player()
        self.p2 = Player()

    def resolve_bids(self, curr_stock, p1_bid, p2_bid):
        self.p1.hand.remove(p1_bid)
        self.p2.hand.remove(p2_bid)

        if p1_bid == p2_bid:
            self.tie_carry += curr_stock
        elif p1_bid > p2_bid:
            self.p1.points += self.tie_carry + curr_stock
            self.tie_carry = 0
        else:
            self.p2.points += self.tie_carry + curr_stock
            self.tie_carry = 0

    def run_sim(self, p1_strat, p2_strat):
        while len(self.bid_pile):
            curr_stock = random.choice(self.bid_pile)
            self.bid_pile.remove(curr_stock)
            p1_bid = p1_strat(curr_stock, self.p1, self.p2, self)
            p2_bid = p2_strat(curr_stock, self.p2, self.p1, self)
            self.resolve_bids(curr_stock, p1_bid, p2_bid)
            if self.p1.points >= 46:
                return 1
            if self.p2.points >= 46:
                return -1
        return 0  # Tie game
