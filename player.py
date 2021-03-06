import urllib2
import json
import traceback

class Player:
    VERSION = "Lobster eats horses"

    def __init__(self):
        self.raise_amount = 0
        self.config = {}
        self.config["force_all_in"] = False
        self.config["basic_raise_amount"] = 0
        try:
            if False:
                self.config_url = "http://salaander.hu/lean.json"
                response = urllib2.urlopen(self.config_url, timeout=1)
                content = str(response.read())
                self.config = json.loads(content)
        except Exception as e:
            print(e)

    def betRequest(self, g):
        try:
            if self.config["force_all_in"]:
                return 5000

            if self.config["basic_raise_amount"]:
                assert isinstance(self.config["basic_raise_amount"], int)
                if self.config["basic_raise_amount"] >= 0:
                    self.raise_amount = int(self.config["basic_raise_amount"])

            in_action = g["players"][g["in_action"]]

            if len(g["community_cards"]) == 0:
                self.pre_flop(g)
            elif len(g["community_cards"]) == 3:
                self.flop(g)
            elif len(g["community_cards"]) == 4:
                self.turn(g)
            elif len(g["community_cards"]) == 5:
                self.river(g)

            result = int(g["current_buy_in"] - in_action["bet"] + self.raise_amount)

            if result < 0:
                result = 0

            return result
        except Exception as ex:
            print(ex)
            traceback.print_exc()
            return 1200

    def action_maching_card(self,g):
        in_action = g["players"][g["in_action"]]
        for card in in_action["hole_cards"]:
            if self.check_matching_cards(card,g["community_cards"]) > 0 and self.value_cards(card) > 8:
                self.raise_amount += 100

    def pre_flop(self, g):
        in_action = g["players"][g["in_action"]]
        strength = self.strength(in_action["hole_cards"])

        if strength < 24 and self.am_i_dealer():
            return 0

        if strength <= 12:
            return 0

        if 12 < strength < 19:
            if g["pot"] > 200:
                self.raise_amount = -100
            else:
                self.raise_amount = 0
            stack_defense = 0.1
            if g["current_buy_in"] > int(in_action["stack"] * stack_defense):
                return 0

        if strength >= 19:
            self.raise_amount += 100
            if g["pot"] > 500:
                self.raise_amount = 0

        if strength >= 24:
            self.raise_amount += 300

    def am_i_dealer(self, g):
        return g["in_action"] == g["dealer"]

    def flop(self,g):
        self.raise_amount = 0
        self.action_maching_card(g)

    def turn(self,g):
        self.raise_amount = 0
        self.action_maching_card(g)

    def river(self,g):
        self.raise_amount = 0
        self.action_maching_card(g)

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
            if (self.value_cards(card) == self.value_cards(comm_card)):
                match_count += 1
        return match_count
        # return len([])

    def check_flush(self, cards, community_cards):
        suits = [i["suit"] for i in cards + community_cards]
        for i in set(suits):
            if suits.count(i) >= 5:
                return True
        return False

    def showdown(self, game_state):
        pass
