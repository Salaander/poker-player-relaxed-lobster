import urllib2
import json

class Player:
    VERSION = "Lobster eats horses"

    def __init__(self):
        self.config = {}
        try:
            self.config_url = "http://salaander.hu/lean.json"
            response = urllib2.urlopen(self.config_url)
            content = str(response.read())
            self.config = json.loads(content)
        except Exception as e:
            print(e)

    def betRequest(self, g):

        #
        # current_buy_in - players[in_action][bet]

        # current_buy_in - players[in_action][bet] + minimum_raise
        try:
            if self.config["force_all_in"]:
                return 5000

            raise_amount = 500
            in_action = g["players"][g["in_action"]]
            """
            if g["round"] == 0:
                raise_amount = 500
            elif g["round"] == 1:
                raise_amount = 200
            else:
                raise_amount = 0
            """
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
            if result < 0:
                result = 0
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
        card1 = int(self.value_cards(cards[0]))
        card2 = int(self.value_cards(cards[1]))
        card1s = cards[0]["suit"]
        card2s = cards[1]["suit"]

        result = card1 + card2 #/ (2 * 14)) * 10

        # flush
        if card1s == card2s:
            result = int(result*1.15)

        # sorra
        if abs(card1 - card2) <= 2:
            result = int(result*1.1)

        # pair
        if card1 == card2:
            result = int(result*1.45)

        return result

    def value_cards(self, card):
        rank = card["rank"]
        switcher = {
                "J": 11,
                "Q": 12,
                "K": 13,
                "A": 14,
        }
        return int(switcher.get(rank, rank))

    def check_matching_cards(self, card, community_cards):
        match_count = 0
        for comm_card in community_cards:
            if (value_cards(card) == value_cards(community_cards)):
                match_count++
        return match_count

    def showdown(self, game_state):
        pass
