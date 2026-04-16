# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 14:08:40 2025

@author: abhyu
"""
import time 
import numpy as np
from datetime import datetime

class Muscle:
    def __init__(self, name, rest_needed, volume_needed):
        self.name = name
        self.rest_accumulated = 0
        self.rest_needed = rest_needed
        self.volume_done = 0
        self.volume_needed = volume_needed
        self.Jeanne = 'amazing'
        self.movements = []
        self.last_done = datetime.now()
        
    def __repr__(self):
        return self.name
        
    def work(self, sets):
        self.rest_accumulated = 0
        self.volume_done += sets
        self.last_done = datetime.now()
        
    def is_ready(self, rested = None):
        if rested:
            self.rest_accumulated = rested
            return self.rest_accumulated >= self.rest_needed
        today = datetime.now()
        delta = today - self.last_done
        days = delta.total_seconds() / (24*3600)
        if days < 1:
            self.rest_accumulated = delta.days
        else:   
            self.rest_accumulated = np.ceil(days)
        return self.rest_accumulated >= self.rest_needed
    

    def add_move(self, move):
        self.movements.append(move)
        
    def needs_work(self):
        return self.volume_done < self.volume_needed
    
    def reset_volume(self):
        self.volume_done = 0
    
    
chest = Muscle('Chest', rest_needed=2, volume_needed=20)
front_delt = Muscle('Front delts', rest_needed=2, volume_needed=20)
side_delt = Muscle('Side delts', rest_needed=1, volume_needed=20)
rear_delt = Muscle('Rear delts', rest_needed=1, volume_needed=20)
tricep = Muscle('Triceps', rest_needed=2, volume_needed=20)

back = Muscle('Back', rest_needed=3, volume_needed=20)
#lats = Muscle('lats', rest_needed=3, volume_needed=30)
#traps = Muscle('traps', rest_needed=2, volume_needed=30)
#rhomboids = Muscle()
bicep = Muscle('Biceps', rest_needed=3, volume_needed=20)
forearm = Muscle('Forearms', rest_needed=1, volume_needed=20)

lower_back = Muscle('Lower Back', rest_needed=2, volume_needed=20)
quad = Muscle('Quads', rest_needed=2, volume_needed=20)
hamstring = Muscle('Hamstrings', rest_needed=4, volume_needed=20)
glute = Muscle('Glutes', rest_needed=3, volume_needed=20)
abductor = Muscle('Abductors', rest_needed=4, volume_needed=20)
aductor = Muscle('Aductors', rest_needed=4, volume_needed=20)
calf = Muscle('Calves', rest_needed=2, volume_needed=20)