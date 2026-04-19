# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 14:24:18 2025

@author: abhyu
"""
import time, json, os
from movements import *

class Body:
    
    def __init__(self, muscle_list, movement_list, workout_list):
        self.muscles = muscle_list
        self.movements = movement_list
        self.workouts = workout_list
        self.muscle_stats = {mus: [] for mus in self.muscles}
        
    def weekly_reset(self):
        weekly_stats = {
            "date": time.strftime("%Y-%m-%d %H:%M"), 
            "volume_per_muscle": {mus.name: mus.volume_done for mus in self.muscles}
            }
        
        filename = "master_stat.json"
        with open(filename, "a") as f:
            json.dump(weekly_stats, f)
            f.write("\n")
            
        for muscle in self.muscles:
            muscle.reset_volume()
        self.save_data()
        
    def weekly_resetDB(self, gen_db):
        master_stat = dict(gen_db["master_stat"].find_one()) 
        master_stat[time.strftime("%Y-%m-%d %H:%M")] = {                                            "volume_per_muscle": {mus.name: mus.volume_done for mus in self.muscles}
            }
        gen_db["master_stat"].replace_one({}, master_stat, upsert=True)
             
        for muscle in self.muscles:
            muscle.reset_volume()
        self.save_data()
        
    def volume_done(self):
        return {mus: mus.volume_done for mus in self.muscles}
    
    def volume_needed(self):
        return {mus: mus.volume_needed for mus in self.muscles}
    
    def rest_accumulated(self):
        dummy = [mus.is_ready() for mus in self.muscles]
        return {mus: mus.rest_accumulated for mus in self.muscles}
    
    def is_ready(self):
        return {mus: mus.is_ready() for mus in self.muscles}
    
    def rest_needed(self):
        return {mus: mus.rest_needed for mus in self.muscles}
    
    def load_data(self):
        muscle_dict = {mus.name: mus for mus in self.muscles}
        with open('current_week.json', 'r') as f:
            lines = f.readlines()
        current_state = json.loads(lines[-1])
        for mus in self.muscles:
            mus.volume_done = current_state[mus.name]["volume done"]
            mus.rest_accumulated = current_state[mus.name]["rest accumulated"]
            date_str = current_state[mus.name]["last done"]
            date = datetime.strptime(str(date_str).split('.')[0], '%Y-%m-%d %H:%M:%S')
            mus.last_done = date
            
    def load_dataDB(self, gen_db):
        muscle_dict = {mus.name: mus for mus in self.muscles}
        current_state = current_week = dict(gen_db["current_week"].find_one())
        for mus in self.muscles:
            mus.volume_done = current_state[mus.name]["volume done"]
            mus.rest_accumulated = current_state[mus.name]["rest accumulated"]
            date_str = current_state[mus.name]["last done"]
            date = datetime.strptime(str(date_str).split('.')[0], '%Y-%m-%d %H:%M:%S')
            mus.last_done = date
        
    def save_data(self):
        print("SAVING")
        current_state = {mus.name: {"volume done": mus.volume_done, 
                                    "rest accumulated": mus.rest_accumulated, 
                                    "last done": str(mus.last_done)}
                         for mus in self.muscles}
        with open('current_week.json', 'w') as f:
            json.dump(current_state, f)
            
    def save_dataDB(self, gen_db):
        print("SAVING")
        current_state = {mus.name: {"volume done": mus.volume_done, 
                                    "rest accumulated": mus.rest_accumulated, 
                                    "last done": str(mus.last_done)}
                         for mus in self.muscles}
        gen_db["current_week"].replace_one({}, current_state, upsert=True)

    def muscles_ready(self):
        ready = []
        for mus in self.muscles:
            if mus.is_ready():
                ready.append(mus)
                
    def calander(self):
        #Function that takes workout plan template and tells what workout should be done on each day for the next two weeks, takes whether the workout was done or not and check it off, and if a workout is missed it moved rest days around to make sure the total workout load for the 2 (maybe 1 week) week period is met
        pass
                
    #def last_weights:
    #    self.last_weights = {}
    #    for move in self.movement_list:
    #        self.last_weights[move] = move.last_weight
            
class Workout:
    def __init__(self, name, blocks):
        """
        blocks: list of dicts {movement: sets}
        """
        self.name = name
        self.name_ = '_'.join(name.split(' '))
        self.blocks = blocks
        self.movement_list = set()
        self.muscles = {}
        self.results = {}
        self.last = {}
        self.start_time = 0
        self.end_time = 0

        # collect all movements and muscles
        for block in self.blocks:
            for movement, _ in block.items():
                self.movement_list.add(movement)
                for mus in movement.muscles:
                    self.muscles[mus] = self.muscles.get(mus, 0) + 1

    # ==================================================
    # SAVE / LOAD RESULTS
    # ==================================================
    def save_data(self, end_time):
        """Append current workout results to file"""
        time_elapsed = str(np.ceil((end_time - self.start_time)/60))
        print(self.start_time, end_time, time_elapsed)
        data = {
            "date": time.strftime("%Y-%m-%d %H:%M"),
            "results": {
                move.name: self.results[move] for move in self.results
                },
            "time": time_elapsed
            }
        
        filename = f"{self.name}.json"
        with open(filename, "a") as f:
            json.dump(data, f)
            f.write("\n")
            
    def save_dataDB(self, end_time, workout_db):
        """Append current workout results to file"""
        time_elapsed = str(np.ceil((end_time - self.start_time)/60))
        print(self.start_time, end_time, time_elapsed)
        
        workout_history = dict(workout_db[self.name_].find_one())

        new_workout = {"results": {move.name: self.results[move] for move in self.results}, "time": time_elapsed}
        workout_history[time.strftime("%Y-%m-%d %H:%M")] = new_workout
        workout_db[self.name_].replace_one({}, workout_history, upsert=True)


    def load_data(self):
        move_dic = {move.name: move for move in self.movement_list}
        """Load most recent workout results"""
        filename = f"{self.name}.json"
        if not os.path.exists(filename):
            print("No previous workout data found.")
            return None
        with open(filename, "r") as f:
            lines = f.readlines()
        if not lines:
            print("Workout log is empty.")
            return None
        last_session = json.loads(lines[-1])
        print(f"Loaded last workout from {last_session['date']}")
        res = last_session["results"]
        self.last = {move_dic[move_name]: res[move_name] for move_name in res}
        return res
    
    def load_dataDB(self, workout_db):
        move_dic = {move.name: move for move in self.movement_list}
        """Load most recent workout results"""
        try:
            workout_history = dict(workout_db[self.name_].find_one())
        except:
            print('This database file might not exist...')
            raise
        
        workout_dated = sorted([key if '20' in key else '0' for key in workout_history.keys()])
        last_session = workout_history[workout_dated[-1]]
        print(f"Loaded last workout from {workout_dated[-1]}")
        res = last_session["results"]
        self.last = {move_dic[move_name]: res[move_name] for move_name in res}
        return res
    # ==================================================
    # CORE
    # ==================================================
            
    def is_ready(self):
        return all([move.is_ready() for move in self.movement_list])
    
    def do(self):
        for move in self.results:
            sets = len(self.results[move])
            move.do(sets)
            


    
Push_I_blocks = [
    {flat_chest_press: 3, lateral_raise: 3},
    {incline_chest_press: 3, upright_row: 3},
    {chest_fly: 3, tricep_extension: 3},
    {seated_press: 3, dips: 3},
]

Push_II_blocks = [
    {incline_chest_press: 3, bench_y_raise: 3},
    {chest_fly: 3, rear_delt_crossover: 3},
    {chest_pullovers: 3, tricep_extension: 3},
    {seated_press: 3, dips: 3},
]

Push_III_blocks = [
    {incline_chest_press: 4, bench_y_raise: 4},
    {chest_fly: 3, tricep_extension: 3},
    {chest_pullovers: 3},
    {seated_press: 4, dips: 3},
]

Pull_I_blocks = [
    {incline_curl: 4, lat_pull_up: 3},
    {hammer_curl: 4},
    {rear_delt_crossover: 3, t_bar_row: 3},
    {shrugs: 3},
]

Pull_Iv2_blocks = [
    {incline_curl: 4, lat_pull_up: 3},
    {hammer_curl: 4, rear_delt_crossover: 3},
    {t_bar_row: 4, shrugs: 3},
]

Pull_II_blocks = [
    {lat_pulldown: 3, bent_over_row: 3},
    {deadlift: 3, reverse_fly: 3},
    {incline_curl: 3},
    {preacher_curl: 3, calf_raise: 3},
]

Legs_I_blocks = [
    {squat: 3},
    {rdl: 3},
    {split_squat: 3},
    {sumo_squat: 3, calf_raise: 3},
    ]

Legs_II_blocks = [
    {squat: 4},
    {calf_raise: 4},
    {split_squat: 2},
    {rdl: 3},
    {one_leg_calf_raise: 3},
    ]

Legs_III_blocks = [
    {squat: 4},
    {rdl: 3},
    {machine_calf_raise: 4},
    {leg_extension: 3},
    {leg_curl: 3},
    {one_leg_machine_calf_raise: 3},
    ]

CB_I_blocks = [
    {flat_chest_press : 3, bent_over_row: 3},
    {incline_chest_press : 3, shrugs: 3},
    {chest_fly : 3, rear_delt_crossover: 3},
    {chest_pullovers : 3, calf_raise: 3},
    ]

Arms_I_blocks = [
    {},
    {},
    ]

Push_I = Workout("Push I", Push_I_blocks)
Push_III = Workout("Push III", Push_III_blocks)
Pull_I = Workout("Pull I", Pull_Iv2_blocks)
Pull_II = Workout("Pull II", Pull_II_blocks)
Legs_III = Workout("Legs III", Legs_III_blocks)

#Removing old unused workouts to reduce clutter
#Push_II = Workout("Push II", Push_II_blocks)
#Legs_I = Workout("Legs I", Legs_I_blocks)
#Legs_II = Workout("Legs II", Legs_II_blocks)
#CB_I = Workout("Chest and Back I", CB_I_blocks)


My_body = Body([chest, front_delt, side_delt, rear_delt, tricep, back, bicep, forearm, quad, hamstring, abductor, aductor, glute, calf], [], [Push_I, Push_III, Pull_I, Pull_II, Legs_III])
