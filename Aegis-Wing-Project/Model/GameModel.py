from Model.Agents.PlayerAgent import PlayerAgent
from Model.EnemyPicker import EnemyPicker
from Model.GameState import GameState


class GameModel:
    def __init__(self, turns_until_game_ends: int = 100,
                 board_len:int = 10, board_height: int = 10,
                 player_len: int = 1, player_height: int = 1,
                 player_spawn_x: int = 0, player_spawn_y: int=0,
                 player_lives: int = 1, max_enemies_at_one_time: int = 3):

        self.max_turns = turns_until_game_ends
        #make initial gamestate
        self.gameState = self.create_initial_gamestate(board_len,board_height,
                                   max_enemies_at_one_time,
                                   turns_until_game_ends,player_lives)
        #make initial player agent
        player_agent = PlayerAgent(player_len, player_height,player_spawn_y, player_spawn_x)

        #add player to gamestate
        self.gameState.addAgent(player_agent)
        #update 2D array representation
        self.gameState.update_board()
        self.enemy_picker = None

    def create_initial_gamestate(self,board_len: int, board_height: int,
                 max_enemies_at_one_time: int,
                 turns_left: int , player_lives: int):
        return GameState(board_len = board_len, board_height = board_height,
                                   max_enemies_at_one_time=max_enemies_at_one_time,
                                   turns_left=turns_left, player_lives=player_lives)

    def set_enemy_picker(self,enemy_picker: EnemyPicker):
        self.enemy_picker = enemy_picker

    def update_gamestate(self):
        pass

    #TODO maybe this needs like a controller and a spawn behavior param?
    def playGame(self):
        pass

    #need like a refresh method
    #on key needs to call player take action.