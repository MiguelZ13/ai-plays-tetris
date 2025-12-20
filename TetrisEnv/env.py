from enum import Enum
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame

class TetrisGame:
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 20}
    def __init__(self):
        self.window_size = 512
        
        self.observation_space = spaces.Dict({
            "board": spaces.Box(
                low=0,
                high=2,
                shape=(20, 10),
                dtype=np.int8
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