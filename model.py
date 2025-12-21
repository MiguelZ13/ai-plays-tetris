import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque

class DQN(nn.Module):
    def __init__(self, obs_space, num_actions):
        super().__init__()
        img_shape = obs_space["board"].shape
        
        self.cnn = nn.Sequential(
            nn.Conv2d(img_shape[0], 32, 4, 2),
            nn.ReLU(),
            nn.Conv2d(32, 32, 3, 1),
            nn.ReLU()
        )
        
        with torch.no_grad():
            temp = torch.zeros(1, *img_shape)
            cnn_out_dim = self.cnn(temp).view(1, -1).size()
        
        self.piece_emb = nn.Embedding(obs_space["current_piece"].n, 8)
        self.rot_emb = nn.Embedding(obs_space["current_rotation"].n, 4)
        self.x_emb = nn.Embedding(obs_space["x_position"].n, 8)
        self.next_emb = nn.Embedding(7, 8)
        
        emb_dim = 8 + 4 + 8 + 3 * 8
        
        self.mlp = nn.Sequential(
            nn.Linear(emb_dim, 256),
            nn.ReLU()
        )
        
        self.fc = nn.Sequential(
            nn.Linear(cnn_out_dim + 256, 512),
            nn.ReLU(),
            nn.Linear(512, num_actions)
        )
    
    def forward(self, obs):
        img = obs["board"].float()
        if img.max() > 1:
            img = img / 255.0
        
        piece = self.piece_emb(obs["current_piece"])
        rot = self.rot_emb(obs["current_rotation"])
        x = self.x_emb(obs["x_position"])
        
        next_pieces = self.next_emb(obs["next_pieces"])
        next_pieces = next_pieces.view(next_pieces.size(0), -1)
        
        disc_fusion = torch.cat([piece, rot, x, next_pieces], dim=1)
        
        img_feat = self.cnn(img).view(img.size(0), -1)
        disc_feat = self.mlp(disc_fusion)
        
        fusion = torch.cat([img_feat, disc_feat], dim=1)
        
        return self.fc(fusion)


        
