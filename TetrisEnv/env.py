from enum import Enum
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random
import pygame
from main import generate_shape
from shapes import Tetromino

class Actions(Enum):
    LEFT = 0
    RIGHT = 1
    ROTATE_LEFT = 2
    ROTATE_RIGHT = 3
    DOWN = 4
    ROTATE_LEFT_LEFT = 5
    ROTATE_LEFT_RIGHT = 6
    ROTATE_RIGHT_LEFT = 7
    ROTATE_RIGHT_RIGHT = 8

class TetrisGame:
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 20}
    def __init__(self, render_mode=None):
        self.window_size = 512
        
        self.observation_space = spaces.Dict({
            "board": spaces.Box(
                low=0,
                high=255,
                shape=(20, 10),
                dtype=np.uint8
            ),
            
            # 0 = 'I'
            # 1 = 'T'
            # 2 = 'O'
            # 3 = 'S'
            # 4 = 'Z'
            # 5 = 'L'
            # 6 = 'J'
            "current_piece": spaces.Discrete(7),
            "current_rotation": spaces.Discrete(4),
            "x_position": spaces.Discrete(10),
            
            "next_pieces": spaces.Discrete([7,7,7])
        })
        
        self._current_piece = random.randint(7)
        self._current_block = Tetromino(self._current_piece)
        self._board = [[0 for _ in range(10)] for _ in range(20)]
        self._current_rot = 0
        self._curr_x = 5
        self._next = [generate_shape() for _ in range(3)]
        
        # 0 = left
        # 1 = right
        # 2 = rotate_left
        # 3 = rotate_right
        # 4 = down
        # 5 = rotate_left + left
        # 6 = rotate_left + right
        # 7 = rotate_right + left
        # 8 = rotate_right + right
        self.action_space = spaces.Discrete(9)
        
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        
        self.window = None
        self.clock = None
        
    def _get_obs(self):
        return {
            "board": self._board, 
            "current_piece": self._current_piece,
            "current_rotation": self._current_rot,
            "x_position": self._curr_x,
            "next_pieces": self._next
        }
    
    