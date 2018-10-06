
class Player:
    VERSION = "First try"

    def betRequest(self, g):

        #
        # current_buy_in - players[in_action][bet]

        # current_buy_in - players[in_action][bet] + minimum_raise
        """
        in_action = g["players"][g["in_action"]]
        raise_amount = 500
        strength = self.strength(in_action["hole_cards"])
        if strength > 17:
            raise_amount += 100
        if strength > 21:
            raise_amount += 100
        """
        return g["current_buy_in"] - g["players"][g["in_action"]]["bet"] + raise_amount
        #return 0


    def strength(self, cards):
        return (self.value_cards(cards[0]["rank"]) + self.value_cards(cards[1]["rank"])) #/ (2 * 14)) * 10

    def value_cards(self, rank):
        switcher = {
                "J": 11,
                "Q": 12,
                "K": 13,
                "A": 14,
        }
        return switcher.get(rank, rank)


    def showdown(self, game_state):
        pass
