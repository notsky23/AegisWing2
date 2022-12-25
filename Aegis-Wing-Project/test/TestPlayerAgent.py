import unittest

from Model.Agents.Actions import Actions
from Model.Agents.PlayerAgent import PlayerAgent

UP = Actions.UP
DOWN = Actions.DOWN
LEFT = Actions.LEFT
RIGHT = Actions.RIGHT
STOP = Actions.STOP
FIRE = Actions.FIRE

"""
This class verfies PlayerAgent logic and tests methods specific
to the player agent.
"""
class TestPlayerAgent(unittest.TestCase):
    def setUp(self) -> None:
        self.p1 = PlayerAgent()

    def testGetAllRawActions(self):
        action_count = 0

        list_actions_raw = self.p1.get_all_possible_raw_actions()
        for eachAction in list_actions_raw:
            if eachAction == UP:
                action_count += 1
            elif eachAction == DOWN:
                action_count += 1
            elif eachAction == LEFT:
                action_count += 1
            elif eachAction == RIGHT:
                action_count += 1
            elif eachAction == STOP:
                action_count += 1
            elif eachAction == FIRE:
                action_count += 1

        self.assertEqual(6,action_count)

    def testIsPlayer(self):
        self.assertTrue(self.p1.isPlayer())

    def testCopyAgent(self):
        copyAgent = self.p1.deepcopy()

        # check identity, not a shallow copy
        self.assertFalse(self.p1 is copyAgent)

    def testTakeAction(self):
        #this is deep copy with new agent moves
        agentAfterAction = self.p1.take_action(Actions.RIGHT)

        self.assertEqual((0,0), self.p1.get_col_boundaries())
        self.assertEqual((1,1), agentAfterAction.get_col_boundaries())

    def test_take_action_player_agent(self):
        player = PlayerAgent(1, 1, 5, 5)
        # returns a copy with action taken
        after_action = player.take_action(Actions.UP)

        self.assertFalse(player == after_action)  # checking deepcopy working
        self.assertFalse(player.hasMoved())
        self.assertTrue(after_action.hasMoved())

def main():
    unittest.main(verbosity=3)

if __name__ == '__main__':
    main()



