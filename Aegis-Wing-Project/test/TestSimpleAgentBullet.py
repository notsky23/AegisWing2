import unittest

from Model.Agents.Actions import Actions
from Model.Agents.PlayerAgent import PlayerAgent
from Model.Agents.SimpleGoLeftAgent import SimpleGoLeftAgent
from Model.Projectiles.SimpleAgentBullet import SimpleAgentBullet

"""
The tests in this class verify SimpleAgentBullet implementation.
There are tests to check proper spawn location, proper position 
change (in relation to speed and prior position) as well as 
"hit" logic.
"""
class TestSimpleAgentBullet(unittest.TestCase):

    def test_player_bullet_from_player_size_1(self):
        """
        Testing the following methods for a bullet created by
        a player agent of size 1 X 1
        - isPlayerBullet
        - getPosition
        - get_all_possible_raw_actions
        :return: None
        """
        player = PlayerAgent(1, 1, 5, 5)
        player_bullet = SimpleAgentBullet(player)

        # position should be at 5,6
        self.assertEqual((5, 6), player_bullet.get_position())
        self.assertTrue(player_bullet.isPlayerBullet())
        self.assertEqual([Actions.RIGHT], player_bullet.get_all_possible_raw_actions())


    def test_enemy_bullet_from_enemy_size_1(self) -> None:
        """
        Testing the following methods for a bullet created by
        an enemy agent of size 1 X 1
        - isPlayerBullet
        - getPosition
        - get_all_possible_raw_actions
        :return: None
        """
        enemy_ship = SimpleGoLeftAgent(5, 9)
        enemy_bullet = SimpleAgentBullet(enemy_ship)

        # position should be row=5, col=8
        self.assertEqual((5, 8), enemy_bullet.get_position())
        self.assertFalse(enemy_bullet.isPlayerBullet())
        self.assertEqual([Actions.LEFT], enemy_bullet.get_all_possible_raw_actions())


    def test_deep_copy(self):
        """
        Testing deep copy method
        :return: None
        """
        player = PlayerAgent(1, 1, 5, 5)
        player_bullet = SimpleAgentBullet(player)
        player_bullet_copy = player_bullet.deepcopy()

        # check deep copy not shallow
        self.assertFalse(player_bullet == player_bullet_copy)
        self.assertEqual(player_bullet.least_col, player_bullet_copy.least_col)
        self.assertEqual(player_bullet.lowest_row, player_bullet_copy.lowest_row)
        self.assertEqual(player_bullet.isPlayerBullet(), player_bullet_copy.isPlayerBullet())
        self.assertEqual(player_bullet.direction, player_bullet_copy.direction)

        # check the same for enemy bullet
        enemy_ship = SimpleGoLeftAgent(5, 9)
        enemy_bullet = SimpleAgentBullet(enemy_ship)
        enemy_bullet_copy = enemy_bullet.deepcopy()

        self.assertFalse(enemy_bullet == enemy_bullet_copy)
        self.assertEqual(enemy_bullet.least_col, enemy_bullet_copy.least_col)
        self.assertEqual(enemy_bullet.lowest_row, enemy_bullet_copy.lowest_row)
        self.assertEqual(enemy_bullet.isPlayerBullet(), enemy_bullet_copy.isPlayerBullet())
        self.assertEqual(enemy_bullet.direction, enemy_bullet_copy.direction)


    def test_player_bullet_from_player_size_2(self):
        """
        Testing the following methods for a bullet created by
        a player agent of size 2 X 2
        - isPlayerBullet
        - getPosition (should be spawned at lowest row)
        - get_all_possible_raw_actions
        :return: None
        """
        player = PlayerAgent(2, 2, 5, 5)
        player_bullet = SimpleAgentBullet(player)

        # position should be at row=5, col=7
        self.assertEqual((5, 7), player_bullet.get_position())
        self.assertTrue(player_bullet.isPlayerBullet())
        self.assertEqual([Actions.RIGHT], player_bullet.get_all_possible_raw_actions())


    def test_enemy_bullet_from_enemy_size_2(self):
        """
        Testing the following methods for a bullet created by
        an enemy agent of size 2 X 2
        - isPlayerBullet
        - getPosition (should be spawned at lowest row)
        - get_all_possible_raw_actions
        :return: None
        """
        enemy_ship = SimpleGoLeftAgent(5, 8)
        enemy_ship.agent_length = 2
        enemy_ship.agent_height = 2
        enemy_bullet = SimpleAgentBullet(enemy_ship)

        # position should be row=5, col=8
        self.assertEqual((5, 7), enemy_bullet.get_position())
        self.assertFalse(enemy_bullet.isPlayerBullet())
        self.assertEqual([Actions.LEFT], enemy_bullet.get_all_possible_raw_actions())


    def test_player_bullet_from_player_size_3(self):
        """
        Testing the following methods for a bullet created by
        a player agent of size 3 X 3
        - isPlayerBullet
        - getPosition (should be spawned in the middle row)
        - get_all_possible_raw_actions
        :return: None
        """
        player = PlayerAgent(3, 3, 5, 0)
        player_bullet = SimpleAgentBullet(player)
        #player is taking up rows/y = 5,6,7
        #player is taking up columns/x = 0,1,2

        # position should be at row/y=6, col/x=3
        self.assertEqual((6, 3), player_bullet.get_position())
        self.assertTrue(player_bullet.isPlayerBullet())
        self.assertEqual([Actions.RIGHT], player_bullet.get_all_possible_raw_actions())


    def test_enemy_bullet_from_enemy_size_3(self):
        """
        Testing the following methods for a bullet created by
        an enemy agent of size 3 X 3
        - isPlayerBullet
        - getPosition (should be spawned in the middle row)
        - get_all_possible_raw_actions
        :return: None
        """
        enemy_ship = SimpleGoLeftAgent(5, 8)
        enemy_ship.agent_length = 3
        enemy_ship.agent_height = 3
        enemy_bullet = SimpleAgentBullet(enemy_ship)
        #enemy agent is taking up column/x = 8,9,10
        #enemy agent is taking up row/y = 5,6,7

        # position should be row=5, cols=8
        self.assertEqual((6, 7), enemy_bullet.get_position())
        self.assertFalse(enemy_bullet.isPlayerBullet())
        self.assertEqual([Actions.LEFT], enemy_bullet.get_all_possible_raw_actions())


    def test_didHit_all_size_1_speed_1(self):
        """
        Testing bullet and agent clashes. All sizes of agents
        are length = 1, height = 1.
        All speed of bullets are = 1
        :return: None
        """
        # player bullet should not hit player bullet
        player = PlayerAgent(1, 1, 5, 0)
        # player is taking up rows/y = 5
        # player is taking up columns/x = 0

        # position should be at row=5,col=1
        player_bullet = SimpleAgentBullet(player)
        player_moved_to_bullet = player.take_action(Actions.RIGHT)

        # player agent is not affected by player bullets
        self.assertFalse(player_bullet.didHitAgent(player_moved_to_bullet))

        # enemy agent not affected by enemy bullets
        enemy_ship = SimpleGoLeftAgent(5, 9)
        #should be at position row=5, col=8
        enemy_bullet = SimpleAgentBullet(enemy_ship)
        enemy_ship_moved = enemy_ship.take_action(Actions.LEFT)
        self.assertFalse(enemy_bullet.didHitAgent(enemy_ship_moved))

        # make an enemy ship where player bullet is
        enemy_2 = SimpleGoLeftAgent(5, 1)
        self.assertTrue(player_bullet.didHitAgent(enemy_2))

        # make a player at position where enemy bullet is
        player_2 = PlayerAgent(1,1,5,8)
        self.assertTrue(enemy_bullet.didHitAgent(player_2))

    def test_didHit_all_size_1_speed_2(self):
        """
        Testing bullet and agent clashes. All sizes of agents
        are length = 1, height = 1.
        All speed of bullets are = 2
        :return: None
        """

        player = PlayerAgent(1, 1, 5, 0)
        player_bullet = SimpleAgentBullet(player,speed=2)

        #should be "spawned" at row=5, col=2
        self.assertEqual((5,2), player_bullet.get_position())

        #if enemy existed at row=5, col=1, it should have hit it
        enemy = SimpleGoLeftAgent(5,1)
        self.assertTrue(player_bullet.didHitAgent(enemy))
        # if enemy existed where is spawned it should hit it
        enemy_2 = SimpleGoLeftAgent(5,2)
        self.assertTrue(player_bullet.didHitAgent(enemy_2))

        #-------------Same situation but for enemy agent--------#

        enemy_prime = SimpleGoLeftAgent(5,9)
        enemy_bullet = SimpleAgentBullet(enemy_prime,speed=2)

        #bullet should be at position 5,7
        self.assertEqual((5,7), enemy_bullet.get_position())
        #if player was in range of bullet then it hits
        player_in_range_1 = PlayerAgent(1,1,5,8)
        player_in_range_2 = PlayerAgent(1,1,5,7)

        self.assertTrue(enemy_bullet.didHitAgent(player_in_range_1))
        self.assertTrue(enemy_bullet.didHitAgent(player_in_range_2))

    def test_performAction(self):
        """
        Testing the movement is accurate even with speed > 1
        :return:
        """

        player = PlayerAgent(1, 1, 5, 0)
        #position should be at row=5, col=1
        player_bullet_s1 = SimpleAgentBullet(player, speed=1)
        self.assertEqual((5,1), player_bullet_s1.get_position())
        s1_after_move = player_bullet_s1.take_action(Actions.RIGHT)
        self.assertEqual((5,2),s1_after_move.get_position())

        #now try with bullet w/ speed > 1
        player_bullet_s2 = SimpleAgentBullet(player,speed=2)
        self.assertEqual((5,2), player_bullet_s2.get_position())
        s2_after_move = player_bullet_s2.take_action(Actions.RIGHT)
        self.assertEqual((5,4), s2_after_move.get_position())

        #--------Same situation but using enemy agent----------#
        enemy_prime = SimpleGoLeftAgent(5, 9)
        enemy_bullet = SimpleAgentBullet(enemy_prime, speed=1)
        self.assertEqual((5,8),enemy_bullet.get_position())
        e1_after_move = enemy_bullet.take_action(Actions.LEFT)
        self.assertEqual((5,7), e1_after_move.get_position())

        e_b2 = SimpleAgentBullet(enemy_prime, speed=2)
        self.assertEqual((5,7), e_b2.get_position())
        e_b2_after_move = e_b2.take_action(Actions.LEFT)
        self.assertEqual((5,5), e_b2_after_move.get_position())


def main():
    unittest.main(verbosity=3)

if __name__ == '__main__':
    main()