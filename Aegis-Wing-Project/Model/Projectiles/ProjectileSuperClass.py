"""
The agent superclass.
This class defines shared methods between all agents.
"""
from Model.Agents.Actions import Actions
from Model.Agents.AgentInterface import AgentInterface
from Model.Agents.AgentSuperClass import AgentSuperClass
from Model.Projectiles.ProjectileInterface import ProjectileInterface


class ProjectileSuperClass(ProjectileInterface,AgentSuperClass):
    """
    This is the abstract class for all projectiles. It is extending the Agent
    super class and implementing the ProjectileInterface.
    """

    def __init__(self, direction: Actions, projectile_length=1, projectile_height=1, lowest_row=0, least_col=0, hp=1,
                speed = 1):

        super().__init__(projectile_length, projectile_height, lowest_row, least_col, hp)

        if speed <= 0:
            raise ValueError("Speed of the prohectile cannot be less than 1")

        #bullet should not be able to fire or stop, it must keep moving
        if direction == Actions.FIRE or direction == Actions.STOP:
            raise ValueError

        self.speed = speed
        self.direction = direction


    def changeSpeed(self, speed: int):
        """
        Changes the number of spaces that the projectile moves each turn.
        Will be used if we want to create complex projectiles
        :return: 
        """
        self.speed = speed
        
    def changeDirection(self, direction: Actions) -> None:
        """
        Changes the direction that the projectile moves each turn.
        Will be used if we want to create complex projectiles
        :return: 
        """
        self.direction = direction

    def isPlayer(self) -> bool:
        raise RuntimeError("A Projectile type class cannot call method isPlayer, did you mean to call isPlayerBullet?")

    def getSpeed(self) -> int:
        return self.speed

    def getCurrentDirection(self) -> Actions:
        return self.direction






