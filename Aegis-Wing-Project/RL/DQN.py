import random
import numpy as np
import pandas as pd
from operator import add
import collections
import torch
import torch.nn as nn
import torch.nn.functional as F
from Model.GameState import GameState
import torch.optim as optim
import copy

DEVICE = 'cpu'  # 'cuda' if torch.cuda.is_available() else 'cpu'
REWARD_BULLET_PATH = -50  # do not want player ending 2 or < spaces away from any bullet since they will lose hp
REWARD_NEAR_BULLET = -10  # Check how many possible future paths collide with bullet and assign -10 for each
REWARD_WIN = 10000  # reward winning the game
REWARD_LOSE = -1000
REWARD_LOSE_LIFE = -100
REWARD_TURN = 5
PLAYER_HP = 3


class DQNAgent(torch.nn.Module):
    def __init__(self, params):
        super().__init__()
        self.reward = 0
        self.gamma = 0.9
        self.dataframe = pd.DataFrame()
        self.short_memory = np.array([])
        self.agent_target = 1
        self.agent_predict = 0
        self.learning_rate = params['learning_rate']
        self.epsilon = 1
        self.actual = []
        self.first_layer = params['first_layer_size']
        self.second_layer = params['second_layer_size']
        self.third_layer = params['third_layer_size']
        self.memory = collections.deque(maxlen=params['memory_size'])
        self.weights = params['weights_path']
        self.load_weights = params['load_weights']
        self.optimizer = None
        self.totalTurns = params['turns']
        self.network()

    def network(self):
        # Layers
        self.f1 = nn.Linear(392, self.first_layer)
        self.f2 = nn.Linear(self.first_layer, self.second_layer)
        self.f3 = nn.Linear(self.second_layer, self.third_layer)
        self.f4 = nn.Linear(self.third_layer, 6)
        # weights
        if self.load_weights:
            self.model = self.load_state_dict(torch.load(self.weights))
            print("weights loaded")

    def forward(self, x):
        x = F.relu(self.f1(x))
        x = F.relu(self.f2(x))
        x = F.relu(self.f3(x))
        x = F.softmax(self.f4(x), dim=-1)
        return x

    def get_state(self, game: GameState):
        """
        Return the state.
        The state is a numpy array of (8*7*7) x 1 , representing:
            - Player Location (in Grid)
            - Heuristic Enemy Locations
            - GoLeft Enemy Locations
            - BasicFireAndMove Locations
            - Counter Enemy Locations
            - Enemy Bullet Locations
            - Player Bullet Location

            Each position in list corresponds to a location and enemy type. The locations go in
            groups of 7 with a 1 representing that this agent is in that location. For example the
            first seven elements represent the bottom row far left state, the next seven one space to
            the right on the bottom row, and so on with wrapping around to the left as we increase the row.
        """

        player_list_arr = game.gameBoard.get_board_with_agents_RL(game, 1, 1)
        left_list_arr = game.gameBoard.get_board_with_agents_RL(game, 2, 2)
        fire_move_list_arr = game.gameBoard.get_board_with_agents_RL(game, 3, 3)
        heur_list_arr = game.gameBoard.get_board_with_agents_RL(game, 4, 4)
        counter_list_arr = game.gameBoard.get_board_with_agents_RL(game, 5, 5)

        player_proj_list_arr =  game.gameBoard.get_board_with_proj_RL(game, True)
        enemy_proj_list_arr = game.gameBoard.get_board_with_proj_RL(game, False)

        state = []
        for eachRowIndex in range(len(player_list_arr)):
            for eachColIndex in range(len(player_list_arr[eachRowIndex])):
                if player_list_arr[eachRowIndex][eachColIndex] == 1:
                    state.append(1)
                else:
                    state.append(0)

                if left_list_arr[eachRowIndex][eachColIndex] == 1:
                    state.append(1)
                else:
                    state.append(0)

                if fire_move_list_arr[eachRowIndex][eachColIndex] == 1:
                    state.append(1)
                else:
                    state.append(0)

                if heur_list_arr[eachRowIndex][eachColIndex] == 1:
                    state.append(1)
                else:
                    state.append(0)

                if counter_list_arr[eachRowIndex][eachColIndex] == 1:
                    state.append(1)
                else:
                    state.append(0)

                if player_proj_list_arr[eachRowIndex][eachColIndex] == 1:
                    state.append(1)
                else:
                    state.append(0)

                if enemy_proj_list_arr[eachRowIndex][eachColIndex] == 1:
                    state.append(1)
                else:
                    state.append(0)

        state = np.array(state)

        return state

    def set_reward(self, game: GameState):
        """
        Return the reward.
        The reward is:
            -10 when Snake crashes.
            +10 when Snake eats food
            0 otherwise
        """

        # reward for killing an agent = points for that agent
        # -10 points for each agent in the surround check up/down & left/right
        # -5 points for each surrounding bullet
        # reward for surviving - .5 point for each turn survived (Every 5 turns is one point)

        # TODO: Check reworking scores
        # check for score
        # difference old_score vs new_score
        self.reward = 0
        if game.isWin():
            self.reward = REWARD_WIN
            return self.reward
        if game.isLose():
            self.reward = REWARD_LOSE
            return self.reward

        # add score reward for surviving
        self.reward += game.lastHit
        if game.lostLife:
            self.reward += REWARD_LOSE_LIFE

        self.reward += (self.totalTurns - game.turns_left) / 2
        self.reward += self.check_enemy_neighbors_up_down(game)
        self.reward += self.check_enemy_neighbors_left_right(game)
        self.reward += self.check_Bullet_Paths(game)

        return self.reward

    def remember(self, state, action, reward, next_state, done):
        """
        Store the <state, action, reward, next_state, is_done> tuple in a
        memory buffer for replay memory.
        """
        self.memory.append((state, action, reward, next_state, done))

    def replay_new(self, memory, batch_size):
        """
        Replay memory.
        """
        if len(memory) > batch_size:
            minibatch = random.sample(memory, batch_size)
        else:
            minibatch = memory
        for state, action, reward, next_state, done in minibatch:
            self.train()
            torch.set_grad_enabled(True)
            target = reward
            next_state_tensor = torch.tensor(np.expand_dims(next_state, 0), dtype=torch.float32).to(DEVICE)
            state_tensor = torch.tensor(np.expand_dims(state, 0), dtype=torch.float32, requires_grad=True).to(DEVICE)
            if not done:
                target = reward + self.gamma * torch.max(self.forward(next_state_tensor)[0])
            output = self.forward(state_tensor)
            target_f = output.clone()
            target_f[0][np.argmax(action)] = target
            target_f.detach()
            self.optimizer.zero_grad()
            loss = F.mse_loss(output, target_f)
            loss.backward()
            self.optimizer.step()

    def train_short_memory(self, state, action, reward, next_state, done):
        """
        Train the DQN agent on the <state, action, reward, next_state, is_done>
        tuple at the current timestep.
        """
        self.train()
        torch.set_grad_enabled(True)
        target = reward
        next_state_tensor = torch.tensor(next_state.reshape((1, 392)), dtype=torch.float32).to(DEVICE)
        state_tensor = torch.tensor(state.reshape((1, 392)), dtype=torch.float32, requires_grad=True).to(DEVICE)
        if not done:
            target = reward + self.gamma * torch.max(self.forward(next_state_tensor[0]))
        output = self.forward(state_tensor)
        target_f = output.clone()
        target_f[0][np.argmax(action)] = target
        target_f.detach()
        self.optimizer.zero_grad()
        loss = F.mse_loss(output, target_f)
        loss.backward()
        self.optimizer.step()

    def check_Bullet_Paths(self, game: GameState):
        """
        Creates a negative reward for each enemy bullet in a radius.
        Gives -5 points for each up to a maximum of -45
        Checks 2 columns to the right of player and -1,0,1 row up/down.
         X |  |  |  |
           |  |  |
        Also checks 3 spaces to the right in the player row.
        Args:
            game: The current gamestate

        Returns: the negative reward

        """
        neg_reward = 0
        # gets the lowest row then the least col
        player_y, player_x = game.getPlayerPos()
        check_y = [player_y - 1, player_y, player_y + 1]
        check_x = [player_x + 1, player_x + 2]
        check_x2 = player_x + 3

        enemy_proj = list(filter(lambda x: x.isPlayerBullet() is False, game.current_projectiles))
        if len(enemy_proj) > 0:
            for proj in enemy_proj:
                proj_y, proj_x = proj.get_position()
                if proj_y in check_y:
                    if proj_x in check_x:
                        neg_reward -= 5
                    if proj_y == player_y and proj_x == check_x2:
                        neg_reward -= 5

        return neg_reward

    def check_enemy_neighbors_left_right(self, game: GameState):
        """
        Creates a negative reward for each enemy agent left or right of player.
        Gives -10 points for each up to a maximum of -50 (max of 5 agents for our current game loop)
        Checks up to columns to the right of player and -1,0,1 row up/down.
        |  |  | X |  |  |  |
        Also check 2 columns left of player and same rows.
        Args:
            game: The current gamestate

        Returns: the negative reward

        """
        neg_reward = 0
        # gets the lowest row then the least col
        player_y, player_x = game.getPlayerPos()
        check_y = [player_y - 1, player_y, player_y + 1]
        # checks the 3 columns to the right of the player and 2 to the left
        check_x = [player_x - 1, player_x - 2, player_x + 1, player_x + 2, player_x + 3]
        check_x2 = player_x + 3

        enemy_agents = list(filter(lambda x: x.isPlayer() is False, game.current_agents))
        if len(enemy_agents) > 0:
            for enemy in enemy_agents:
                proj_y, proj_x = enemy.get_position()
                if proj_y in check_y:
                    if proj_x in check_x:
                        neg_reward -= 10
                    if proj_y == player_y and proj_x == check_x2:
                        neg_reward -= 10

        return neg_reward


    def check_enemy_neighbors_up_down(self, game: GameState):
        """
        Creates a negative reward for each enemy agent above/below/on player
        Gives -10 points for each up to a maximum of -50 (max of 5 agents)
        Checks the player column 2 rows down up to 2 rows above.
        On the max rows also checks the columns 1 left and 1 right of player
        Args:
            game: The current gamestate

        Returns: the negative reward

        """
        neg_reward = 0
        # gets the lowest row then the least col
        player_y, player_x = game.getPlayerPos()
        check_y = [player_y - 2, player_y - 1, player_y, player_y + 1, player_y + 2]
        check_y2 = [player_y - 2, player_y + 2]
        # checks the 3 columns to the right of the player and 2 to the left
        check_x = [player_x - 1, player_x + 1]

        enemy_agents = list(filter(lambda x: x.isPlayer() is False, game.current_agents))
        if len(enemy_agents) > 0:
            for enemy in enemy_agents:
                proj_y, proj_x = enemy.get_position()
                if proj_y in check_y:
                    if proj_x == player_x:
                        neg_reward -= 10
                    elif proj_y in check_y2 and proj_x in check_x:
                        neg_reward -= 10

        return neg_reward
