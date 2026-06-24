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

class MuscleGroup:
    def __init__(self, name, muscles, volume_needed, rest_needed):
        pass
    
# volume_needed = MAV starting point (sets/week)
# rest_needed = days (based on RP recovery guidelines)

# inner_chest = Muscle('Inner chest')
# upper_chest = Muscle('Upper chest')
# lower_chest = Muscle('Lower chest')
chest = Muscle('Chest', rest_needed=2, volume_needed=12)#, subgroups=[inner_chest, upper_chest, lower_chest])

front_delt = Muscle('Front delts', rest_needed=1, volume_needed=6)
# Front delts recover fast and get heavy indirect volume from pressing
# MEV is low (~6) because pressing already covers most of it

side_delt = Muscle('Side delts', rest_needed=1, volume_needed=8)
# Fast recovering, can handle high frequency

rear_delt = Muscle('Rear delts', rest_needed=1, volume_needed=6)
# shoulder = MuscleGroup('Shoulder', muscles=[front_delt, side_delt, rear_delt])
# Similar to side delts, very fast recovery

tricep = Muscle('Triceps', rest_needed=1, volume_needed=8)
# Gets heavy indirect volume from all pressing, so direct MEV is lower


back = Muscle('Back', rest_needed=2, volume_needed=12)#, subgroups=['lats', 'traps', 'rhomboids'])

bicep = Muscle('Biceps', rest_needed=1, volume_needed=8)
# Fast recovering, gets indirect volume from all pulling

forearm = Muscle('Forearms', rest_needed=1, volume_needed=6)

lower_back = Muscle('Lower back', rest_needed=3, volume_needed=6)
# Slow to recover, especially if doing heavy compounds

quad = Muscle('Quads', rest_needed=2, volume_needed=12)

hamstring = Muscle('Hamstrings', rest_needed=2, volume_needed=10)

glute = Muscle('Glutes', rest_needed=2, volume_needed=8)
# Gets indirect volume from squats/RDL

abductor = Muscle('Abductors', rest_needed=2, volume_needed=8)
aductor = Muscle('Aductors', rest_needed=2, volume_needed=8)

calf = Muscle('Calves', rest_needed=1, volume_needed=12)
# Notoriously fast recovering, needs high frequency and volume

ab = Muscle('Abs', rest_needed=1, volume_needed=8)
# Recover very quickly, get indirect work from compounds

brain = Muscle('DummyMuscle', rest_needed=0, volume_needed=0)

""" 
# MUSCLES
chest = Muscle('Chest', rest_needed=2, volume_needed=20, subgroups=['upper', 'lower', 'inner'])
inner_chest = Muscle('Inner chest', )
shoulder = Muscle('Shoulder', rest_needed=1, volume_needed=20, subgroups=['Front Delts', 'Front Delts',])
front_delt = Muscle('Front Delts', rest_needed=2, volume_needed=20)
side_delt = Muscle('Side Delts', rest_needed=1, volume_needed=20)
rear_delt = Muscle('Rear Delts', rest_needed=1, volume_needed=20)
tricep = Muscle('Triceps', rest_needed=2, volume_needed=20)
back = Muscle('Back', rest_needed=3, volume_needed=20, subgroups=['lats', 'traps', 'rhomboids'])
bicep = Muscle('Biceps', rest_needed=3, volume_needed=20)
forearm = Muscle('Forearms', rest_needed=1, volume_needed=20)
lower_back = Muscle('Lower Back', rest_needed=2, volume_needed=20)
quad = Muscle('Quads', rest_needed=2, volume_needed=20)
hamstring = Muscle('Hamstrings', rest_needed=4, volume_needed=20)
glute = Muscle('Glutes', rest_needed=3, volume_needed=20)
abductor = Muscle('Abductors', rest_needed=4, volume_needed=20)
aductor = Muscle('Aductors', rest_needed=4, volume_needed=20)
calf = Muscle('Calves', rest_needed=2, volume_needed=20)


# PUSH
flat_chest_press = Movement('Bench Press', {chest: 'inner', front_delt: None, tricep: None})
lateral_raise = Movement('Lateral Raise', {side_delt: None})
rear_lateral_raise = Movement('Behind Lateral Raise', {side_delt: None})
incline_chest_press = Movement('Incline Bench Press', {chest: 'upper', front_delt: None, tricep: None})
upright_row = Movement('Upright Row', {front_delt: None, side_delt: None})
chest_fly = Movement('Chest Fly', {chest: 'inner'})
tricep_extension = Movement('Tricep Extension', {tricep: None})
seated_press = Movement('Seated Press', {front_delt: None})
dips = Movement('Dips', {tricep: None, chest: 'lower'})
rear_delt_crossover = Movement('Rear-delt Crossover', {rear_delt: None})
chest_pullovers = Movement('Chest Pullovers', {chest: 'inner', tricep: None})
bench_y_raise = Movement('Bench Y Raise', {side_delt: None, front_delt: None})

# PULL
shrugs = Movement('Shrugs', {back: 'traps'})
lat_pull_up = Movement('Lat Pullups', {back: 'lats', bicep: None})
lat_pulldown = Movement('Lat Pulldowns', {back: 'lats', bicep: None})
deadlift = Movement('Deadlift', {back: 'lats'})
bent_over_row = Movement('Bent-over Rows', {back: 'rhomboids'})
t_bar_row = Movement('T-bar Rows', {back: 'rhomboids'})
reverse_fly = Movement('Reverse Fly', {back: 'rhomboids'})
incline_curl = Movement('Incline Curl', {bicep: None})
preacher_curl = Movement('Preacher Curl', {bicep: None})
hammer_curl = Movement('Hammer Curl', {bicep: None, forearm: None})

# LEGS
squat = Movement('Squat', {quad: None, lower_back: None})
rdl = Movement('Romanian Deadlift', {hamstring: None, glute: None, lower_back: None})
split_squat = Movement('Split Squat', {quad: None, glute: None, hamstring: None})
leg_extension = Movement('Leg Extension', {quad: None})
leg_curl = Movement('Leg Curl', {hamstring: None, glute: None})
sumo_squat = Movement('Sumo Squat', {aductor: None, quad: None})
calf_raise = Movement('Calf Raises', {calf: None})
one_leg_calf_raise = Movement('One Leg Calf Raises', {calf: None})
machine_calf_raise = Movement('Machine Calf Raises', {calf: None})
one_leg_machine_calf_raise = Movement('One Leg Machine Calf Raises', {calf: None})

# ABS
leg_raise = Movement('Leg Raises', {abs: None})
"""