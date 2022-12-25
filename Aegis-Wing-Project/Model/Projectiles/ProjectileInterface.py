from Model.Agents.Actions import Actions
from Model.Agents.AgentInterface import AgentInterface
from Model.Agents.AgentSuperClass import AgentSuperClass



class ProjectileInterface(AgentInterface):

    '''
    This interface mandates all methods that must be
    implemented by any subtype. This interface also contains methods of the AgentInreface.
    The methods must be defined by the subtype. Most of these methods will be defined
    in the ProjectileSuperClass.
    '''
    
    def isPlayerBullet(self) -> bool:
        """
        Returns True if projectile was fired from Player Agent, otherwise false
        :return: {bool} True if projectile was fired from Player Agent, otherwise false
        """
        raise NotImplementedError

    def didHitAgent(self,agent: AgentInterface) -> bool:
        """
        This method returns true is the bullet overlaps the agent
        passed in as param.
        :param agent:
        :return:
        """
        raise NotImplementedError

    def getSpeed(self) -> int:
        """
        Returns the speed of the bullet
        :return:
        """
        raise NotImplementedError

    def getCurrentDirection(self) -> Actions:
        """
        Returns the currentDirection of the bullet
        :return:
        """
        raise NotImplementedError

    def getType(self) -> float:
        """
        Returns the variable type (-0.1) for player bullet
        (-0.2) for enemy bullet
        """
