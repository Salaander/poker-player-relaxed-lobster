
class Player:
    VERSION = "Horse meat is tasty"

    def betRequest(self, g):

        #
        # current_buy_in - players[in_action][bet]

        # current_buy_in - players[in_action][bet] + minimum_raise
        try:
            raise_amount = 500
            in_action = g["players"][g["in_action"]]
            if g["round"] == 0:
                raise_amount = 500
            elif g["round"] == 1:
                raise_amount = 200
            else:
                raise_amount = 0
            strength = self.strength(in_action["hole_cards"])
            if strength <= 12:
                return 0
            if 12 < strength < 19:
                if g["pot"] > 200:
                    raise_amount = -100
                else:
                    raise_amount = 0
            if strength >= 19:
                raise_amount += 100
                if g["pot"] > 500:
                    raise_amount = 0
            if strength >= 24:
                raise_amount += 300
            result = int(g["current_buy_in"] - in_action["bet"] + raise_amount)
            #print(result)
            return result
        except Exception as ex:
            return 1200

    def _call(self, g):
        in_action = g["players"][g["in_action"]]
        return int(g["current_buy_in"] - in_action["bet"])

    def _raise(self, g, amount):
        assert isinstance(amount, int)
        in_action = g["players"][g["in_action"]]
        return int(g["current_buy_in"] - in_action["bet"] + amount)


    def strength(self, cards):
        card1 = int(self.value_cards(cards[0]["rank"]))
        card2 = int(self.value_cards(cards[1]["rank"]))
        card1s = cards[0]["suit"]
        card2s = cards[1]["suit"]

        result = card1 + card2 #/ (2 * 14)) * 10

        # flush
        if card1s == card2s:
            result = int(result*1.2)

        # sorra
        if abs(card1 - card2) <= 2:
            result = int(result*1.2)
        return result

    def value_cards(self, rank):
        switcher = {
                "J": 11,
                "Q": 12,
                "K": 13,
                "A": 14,
        }
        return int(switcher.get(rank, rank))


    def showdown(self, game_state):
        pass
