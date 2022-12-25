import uuid

from Model.Agents.Actions import Actions
from Model.Agents.AgentInterface import AgentInterface
from Model.Agents.PlayerAgent import PlayerAgent
from Model.Projectiles.ProjectileSuperClass import ProjectileSuperClass


"""
This class represents a simple bullet. It will be 1 X 1,
but it's speed may vary. It should spawn at the middle 
row of any agent that fires.
"""
class SimpleAgentBullet(ProjectileSuperClass):
    
    def __init__(self, currentAgent: AgentInterface, speed = 1):

        action_to_take = None

        #default motion for simple bullet
        if currentAgent.isPlayer():
            action_to_take = Actions.RIGHT
            #this bullet was fired from player agent
            self.agent_is_player_flag = True
        else:
            action_to_take = Actions.LEFT
            #this bullet was fired by enemy agent
            self.agent_is_player_flag = False

        self.direction = action_to_take

        super().__init__(action_to_take, projectile_length=1, projectile_height=1, hp=1, speed = speed)

        reference_agent_row_bounds = currentAgent.get_row_boundaries()

        #get middle of row
        row_spawn = (reference_agent_row_bounds[0] + reference_agent_row_bounds[1]) // 2

        #should be fired from the middle of the agent

        self.lowest_row = row_spawn

        self.all_possible_raw_actions = None

        #set position of bullet
        if self.agent_is_player_flag:
            #must be placed one col ahead of player agent
            self.least_col = currentAgent.get_max_col_boundary() + self.speed
            self.all_possible_raw_actions = [Actions.RIGHT]
        else:
            self.least_col = currentAgent.get_min_col_boundary() - self.speed
            self.all_possible_raw_actions = [Actions.LEFT]

    def isPlayerBullet(self):
        return self.agent_is_player_flag


    def deepcopy(self):
        #agent placeholder, need it since constructor relies on an AgentInterface
        # will override values to match original SimpleBulletAgent
        placeholder = PlayerAgent()
        copy = SimpleAgentBullet(placeholder,self.speed)
        copy.least_col = self.least_col
        copy.lowest_row = self.lowest_row
        copy.agent_is_player_flag = self.agent_is_player_flag
        copy.all_possible_raw_actions = self.all_possible_raw_actions
        copy.direction = self.direction
        return copy

    def get_all_possible_raw_actions(self) -> list:
        return self.all_possible_raw_actions

    def performAction(self,action: Actions) -> None:
        """
        Helper method to takeAction method that will be defined
        by subclasses
        :param action: {Actions} action taken
        :return: None
        """

        if self.agent_is_player_flag == True:
            if action == Actions.RIGHT:
                self.set_position(self.lowest_row, self.least_col + self.speed)
            else:
                raise RuntimeError(f"Action: {action} is invalid for bullet agent, only Actions.Right is valid")

        else:
            if action == Actions.LEFT:
                self.set_position(self.lowest_row, self.least_col - self.speed)
            else:
                raise RuntimeError(f"Action: {action} is invalid for bullet agent, only Actions.Left is valid")

        self.hasAlreadyMoved = True

    def take_action(self, action: Actions):
        """
        Creates a deepcopy of the bullet that has taken the action
        passed
        :param action:
        :return:
        """

        if action not in self.get_all_possible_raw_actions():
            raise RuntimeError(f"The action is not valid, please use one of the following actions {self.get_all_possible_raw_actions()}")

        copy = self.deepcopy()
        copy.performAction(action)
        return copy

    def autoPickAction(self) -> Actions:
        return self.get_all_possible_raw_actions()[0]

    def didHitAgent(self, agent: AgentInterface):
        #player cannot hit player and enemy cannot hit enemy
        if self.agent_is_player_flag == agent.isPlayer():
            return False

        hit_flag = False

        if self.speed > 1:
            #copy bullets, each taking up one x,y pos on grid representing hitting any agents in that path
            copy_bullets = []
            counter = 0

            for i in range(self.speed):
                copied_bullet : SimpleAgentBullet = self.deepcopy()
                if self.agent_is_player_flag:
                    copied_bullet.least_col = self.least_col - counter
                    counter += 1
                else:
                    copied_bullet.least_col = self.least_col + counter
                    counter += 1
                copy_bullets.append(copied_bullet)


            for bullet in copy_bullets:
                each_bullet: SimpleAgentBullet = bullet
                if each_bullet.is_overlapping_other_agent(agent):
                    hit_flag = True
                    break

        else:
            copy_one_col_back = self.deepcopy()
            if copy_one_col_back.agent_is_player_flag:
                copy_one_col_back.least_col = self.least_col - 1
            else:
                copy_one_col_back.least_col = self.least_col + 1

            if self.is_overlapping_other_agent(agent) or copy_one_col_back.is_overlapping_other_agent(agent):
                hit_flag = True

        return hit_flag

    def __str__(self):
        prepend = ""
        if self.isPlayerBullet():
            prepend += "Player Bullet"
        else:
            prepend += "Enemy Bullet"

        prepend += f" at x/col = {self.get_position()[1]}\ty/row = {self.get_position()[0]}\tspeed = {self.speed}"

        return prepend






