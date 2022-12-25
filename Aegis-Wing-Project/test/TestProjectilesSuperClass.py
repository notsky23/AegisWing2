import unittest

from Model.Agents.Actions import Actions
from Model.Agents.PlayerAgent import PlayerAgent
from Model.Agents.SimpleGoLeftAgent import SimpleGoLeftAgent
from Model.GameState import GameState
from Model.Projectiles.ProjectileSuperClass import ProjectileSuperClass
from Model.Projectiles.SimpleAgentBullet import SimpleAgentBullet
#
"""
The tests in this class verify ProjectileSuperClass implementation.
There are tests to check proper spawn location, and proper position 
change (in relation to speed and prior position).
"""
class TestProjectilesSuperClass(unittest.TestCase):

    def setUp(self) -> None:
        self.gamestate = GameState()
        self.projectile_default = ProjectileSuperClass(Actions.RIGHT)

    def test_defualt_values(self):
        """
        Testing default constructor values for ProjectileSuperClass
        :return: None
        """
        proj = self.projectile_default
        self.assertEqual(1, proj.getSpeed())
        self.assertEqual((0,0), proj.get_position())
        self.assertEqual(Actions.RIGHT, proj.getCurrentDirection())

    def test_isPlayer_raises_error(self):
        """
        Testing that the method isPlayer raises an error.
        This method should only be called by player or enemy
        agents. But since Projectile SuperClass inherits this method
        from AgentSuperClass it will raise an error instead of
        returning a bool
        :return:
        """
        error_thrown = False
        proj = self.projectile_default
        try:
            proj.isPlayer()
        except RuntimeError:
            error_thrown = True

        self.assertTrue(error_thrown)

    def test_raise_error_for_invalid_direction(self):
        """
        Cannot pass in Action.Fire or Actions.STOP into projectile
        superclass constructor.
        :return:
        """
        errors_thrown = 0

        try:
            ProjectileSuperClass(Actions.FIRE)
        except ValueError:
            errors_thrown += 1

        try:
            ProjectileSuperClass(Actions.STOP)
        except ValueError:
            errors_thrown += 1

        self.assertEqual(2, errors_thrown)


    def testPlayerProjectile1(self):
        #player, shoots prohectiles no enemies

        gamestate = self.gamestate
        player_agent = PlayerAgent(1,1,5,5)
        enemy_1 = SimpleGoLeftAgent(5,9)
        addedSuccessfully = gamestate.addAgent(player_agent)
        gamestate.addAgent(enemy_1)

        if addedSuccessfully == False:
            raise ValueError

        gamestate.update_board()

        gamestate.moveAllProjectiles()
        newState = gamestate.generateSuccessorState(0,Actions.FIRE)
        newState = newState.generateSuccessorState(1, Actions.LEFT)
        newState.update_board()

        print(newState.gameBoard)

        newState.reset_agents_move_status()
        newState.moveAllProjectiles()
        newState = newState.generateSuccessorState(0, Actions.STOP)
        newState = newState.generateSuccessorState(1, Actions.LEFT)
        newState.update_board()
        print(newState.gameBoard)

        self.assertEqual(1, len(newState.current_agents))
        self.assertEqual(0, len(newState.current_projectiles))


def main():
    unittest.main(verbosity=3)

if __name__ == '__main__':
    main()