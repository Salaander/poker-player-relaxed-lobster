
class Player:
    VERSION = "First try"

    def betRequest(self, g):

        #
        # current_buy_in - players[in_action][bet]

        # current_buy_in - players[in_action][bet] + minimum_raise

        return g["current_buy_in"] - g["palyers"][g["in_action"]][bet] + g["raise"] + 300

    """
    def _raise(g):
        return g["current_buy_in"] - g["palyers"][g["in_action"]][bet] + g["raise"]

    def check(self):
        return 0
    """

    def showdown(self, game_state):
        pass

