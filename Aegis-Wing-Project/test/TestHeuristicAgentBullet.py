import unittest

from Model.Agents.Actions import Actions
from Model.Agents.EnemyMoveFireHeuristicAgent import EnemyMoveFireHeuristicAgent
from Model.Agents.SimpleGoLeftAgent import SimpleGoLeftAgent


class TestHeuristicAgentBullet(unittest.TestCase):

    def test_take_action_SimpleGoLeft(self):
        """
        Testing SimpleGoLeft Agent.
        This agent should not be able to go right
        take_action(Action.RIGHT) should just return the agent itself

        :return:
        """
        enemy_1 = EnemyMoveFireHeuristicAgent(5,5)
        after_action = enemy_1.take_action(Actions.RIGHT)

        #should return copy with updated position
        self.assertFalse(enemy_1 == after_action)

        #has moved is true since action was valid
        self.assertTrue(after_action.hasMoved())

        after_action.setHasMovedStatus(False)
        after_action2 = after_action.take_action(Actions.STOP)

        # should return shallow copy since no change made
        self.assertTrue(after_action2 == after_action)

        # has moved is false since action was invalid
        self.assertFalse(after_action2.hasMoved())


    def test_take_action_SimpleGoLeft2(self):
        """
        Testing SimpleGoLeft Agent.
        This agent should not be able to go up
        take_action(Action.UP) should just return the agent itself

        :return:
        """
        enemy_1 = SimpleGoLeftAgent(5,5)
        after_action = enemy_1.take_action(Actions.UP)

        #should return shallow copy since no change made
        self.assertTrue(enemy_1 == after_action)

        #has moved is false since action was invalid
        self.assertFalse(after_action.hasMoved())

    def test_take_action_SimpleGoLeft3(self):
        """
        Testing SimpleGoLeft Agent.
        This agent should not be able to go DOWN
        take_action(Action.DOWN) should just return the agent itself

        :return:
        """
        enemy_1 = SimpleGoLeftAgent(5,5)
        after_action = enemy_1.take_action(Actions.DOWN)

        #should return shallow copy since no change made
        self.assertTrue(enemy_1 == after_action)

        #has moved is false since action was invalid
        self.assertFalse(after_action.hasMoved())

    def test_take_action_SimpleGoLeft4(self):
        """
        Testing SimpleGoLeft Agent.
        This agent should not be able to STOP
        take_action(Action.STOP) should just return the agent itself

        :return:
        """
        enemy_1 = SimpleGoLeftAgent(5,5)
        after_action = enemy_1.take_action(Actions.STOP)

        #should return shallow copy since no change made
        self.assertTrue(enemy_1 == after_action)

        #has moved is false since action was invalid
        self.assertFalse(after_action.hasMoved())

    def test_take_action_SimpleGoLeft_Valid(self):
        """
        Testing SimpleGoLeft Agent.
        This agent should not be able to go left
        take_action(Action.LEFT) should just return the agent itself

        :return:
        """
        enemy_1 = SimpleGoLeftAgent(5,5)
        after_action = enemy_1.take_action(Actions.LEFT)

        self.assertEquals((5,4), after_action.get_position())

        #should return deepcopy
        self.assertFalse(enemy_1 == after_action)

        #has moved is true since action was valid
        self.assertTrue(after_action.hasMoved())

def main():
    unittest.main(verbosity=3)

if __name__ == '__main__':
    main()