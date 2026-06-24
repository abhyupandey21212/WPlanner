# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 14:07:18 2025

@author: abhyu
"""
from mucles import *
class Movement:
    def __init__(self, name, prim_muscles, sec_muscles = [], uni = False):
        self.name = name
        self.muscles = prim_muscles
        self.sec_muscles = sec_muscles
        self.uni = uni
        for muscle in prim_muscles:
            muscle.add_move(self)
        
        #IN FUTURE, add prim and sec muscle groups with 1 and 0.5 volume factor
        
    def do(self, sets):
        for muscle in self.muscles:
            muscle.work(sets)
        for muscle in self.sec_muscles:
            muscle.work(0.5*sets)
            
    def is_ready(self):
        return all([muscle.is_ready() for muscle in self.muscles])
    
    def __repr__(self):
        return f'{self.name} involves the muscles {self.muscles}, as well as secondary muscles {self.sec_muscles}'
    
    
    
    
#PUSH
flat_chest_press = Movement('Bench Press', [chest], [front_delt, tricep])
cable_chest_press = Movement('Chest Cable Press', [chest], [front_delt, tricep])
cable_incline_press = Movement('Incline Cable Press', [chest], [front_delt, tricep])
lateral_raise = Movement('Lateral Raise', [side_delt], uni=True)
rear_lateral_raise = Movement('Behind Lateral Raise', [side_delt], uni=True)
incline_chest_press = Movement('Incline Bench Press', [chest], [front_delt, tricep])
upright_row = Movement('Upright Row', [front_delt, side_delt])
chest_fly = Movement('Chest Fly', [chest])
tricep_extension = Movement('Tricep Extension', [tricep])
seated_press = Movement('Seated Press', [front_delt])
machine_shoulder_press = Movement('Machine Shoulder Press', [front_delt])
dips = Movement('Dips', [tricep], [chest])
rear_delt_crossover = Movement('Rear-delt Crossover', [rear_delt])
chest_pullovers = Movement('Chest Pullovers', [chest], [tricep, back])
bench_y_raise = Movement('Bench Y Raise', [side_delt], [front_delt])
tricep_kickback = Movement('Tricep Kickback', [tricep], uni=True)
pec_deck = Movement('Pec Deck', [chest])
rev_pec_deck = Movement('Reverse Pec Deck', [rear_delt])
#PULL
close_grip_pulldown = Movement('Close-grip Pulldowon', [back])
cable_row = Movement('Cable Row', [back])
machine_row = Movement('Machine Row', [back])
shrugs = Movement('Shrugs', [back])
lat_pull_up = Movement('Lat Pullups', [back], [bicep])
lat_pullaround = Movement('Lat Pull-arounds', [back])
deadlift = Movement('Deadlift', [back, lower_back])
bent_over_row = Movement('Bent-over Rows', [back])
t_bar_row = Movement('T-bar Rows', [back])
reverse_fly = Movement('Reverse Fly', [back])
incline_curl = Movement('Incline Curl', [bicep])
preacher_curl = Movement('Preacher Curl', [bicep], uni=True)
baysean_cable_curl = Movement('Baysean Cable Curl', [bicep], uni=True)
zotmann_preacher_curl = Movement('Zottmann Preacher Curl', [bicep], uni=True)
hammer_curl = Movement('Hammer Curl', [bicep, forearm], uni=True)
forearm_curl = Movement('Forearm Curl', [forearm], uni=True)
forearm_ext = Movement('Forearm Extension', [forearm], uni=True)
#LEGS
squat = Movement('Squat', [quad], [lower_back, glute])
rdl = Movement('Romanian Deadlift', [hamstring], [glute, lower_back])
split_squat = Movement('Split Squat', [quad, glute], [hamstring])
leg_extension = Movement('Leg Extension', [quad])
leg_curl = Movement('Leg Curl', [hamstring], [glute])
sumo_squat = Movement('Sumo Squat', [glute], [aductor, quad])
calf_raise = Movement('Calf Raises', [calf])
one_leg_calf_raise = Movement('One Leg Calf Raises', [calf], uni=True)
machine_calf_raise = Movement('Machine Calf Raises', [calf])
one_leg_machine_calf_raise = Movement('One Leg Machine Calf Raises', [calf], uni=True)
smith_lunge = Movement('Smith Machine Lunge', [quad, glute], uni=True)

#ABS
leg_raise = Movement('Leg Raises', [ab])
ab_rollouts = Movement('Ab Rollouts', [ab, chest])
cable_crunch = Movement('Cable Crunch', [ab])

#DEBUGGING
dummy1 = Movement('Dummy 1', [brain])
dummy2 = Movement('Dummy 1', [brain], uni=True)

movements_list = [flat_chest_press, lateral_raise, incline_chest_press, upright_row, chest_fly, tricep_extension, seated_press, dips]