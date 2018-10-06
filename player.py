
class Player:
    VERSION = "First try"

    def betRequest(self, g):

        #
        # current_buy_in - players[in_action][bet]

        # current_buy_in - players[in_action][bet] + minimum_raise
        return g["current_buy_in"] - g["players"][g["in_action"]]["bet"] + 500
        #return 0


    def strength(cards):
        return ((value_cards(cards[0]["rank"]) + value_cards(cards[1]["rank"]))/ (2 * 13)) * 10

    def value_cards(rank):
        switcher = {
                "J": 11,
                "Q": 12,
                "K": 13,
                "A": 14,
        }
        return switcher.get(rank, rank)


    def showdown(self, game_state):
        pass
