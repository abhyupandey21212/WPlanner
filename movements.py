# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 14:07:18 2025

@author: abhyu
"""
from mucles import *
class Movement:
    def __init__(self, name, muscles):
        self.name = name
        self.muscles = muscles
        for muscle in muscles:
            muscle.add_move(self)
        #IN FUTURE, add prim and sec muscle groups with 1 and 0.5 volume factor
        
    def do(self, sets):
        for muscle in self.muscles:
            muscle.work(sets)
            
    def is_ready(self):
        return all([muscle.is_ready() for muscle in self.muscles])
    
    def __repr__(self):
        return self.name
    
    
    
    
#PUSH
flat_chest_press = Movement('Bench Press', [chest, front_delt, tricep])
lateral_raise = Movement('Lateral Raise', [side_delt])
rear_lateral_raise = Movement('Behind Lateral Raise', [side_delt])
incline_chest_press = Movement('Incline Bench Press', [chest, front_delt, tricep])
upright_row = Movement('Upright Row', [front_delt, side_delt])
chest_fly = Movement('Chest Fly', [chest])
tricep_extension = Movement('Tricep Extension', [tricep])
seated_press = Movement('Seated Press', [front_delt])
dips = Movement('Dips', [tricep, chest])
rear_delt_crossover = Movement('Rear-delt Crossover', [rear_delt])
chest_pullovers = Movement('Chest Pullovers', [chest, tricep])
bench_y_raise = Movement('Bench Y Raise', [side_delt, front_delt])
#PULL
shrugs = Movement('Shrugs', [back])
lat_pull_up = Movement('Lat Pullups', [back, bicep])
lat_pulldown = Movement('Lat Pulldowns', [back, bicep])
deadlift = Movement('Deadlift', [back])
bent_over_row = Movement('Bent-over Rows', [back])
t_bar_row = Movement('T-bar Rows', [back])
reverse_fly = Movement('Reverse Fly', [back])
incline_curl = Movement('Incline Curl', [bicep])
preacher_curl = Movement('Preacher Curl', [bicep])
hammer_curl = Movement('Hammer Curl', [bicep, forearm])
#LEGS
squat = Movement('Squat', [quad, lower_back])
rdl = Movement('Romanian Deadlift', [hamstring, glute, lower_back])
split_squat = Movement('Split Squat', [quad, glute, hamstring])
leg_extension = Movement('Leg Extension', [quad])
leg_curl = Movement('Leg Curl', [hamstring, glute])
sumo_squat = Movement('Sumo Squat', [aductor, quad])
calf_raise = Movement('Calf Raises', [calf])
one_leg_calf_raise = Movement('One Leg Calf Raises', [calf])
machine_calf_raise = Movement('Machine Calf Raises', [calf])
one_leg_machine_calf_raise = Movement('One Leg Machine Calf Raises', [calf])

#ABS
leg_raise = Movement('Leg Raises', [abs])
ab_rollouts = Movement('Ab Rollouts', [abs, chest])

movements_list = [flat_chest_press, lateral_raise, incline_chest_press, upright_row, chest_fly, tricep_extension, seated_press, dips]