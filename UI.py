# -*- coding: utf-8 -*-
"""
Workout selection UI
"""

import tkinter as tk
from tkinter import ttk
from workouts import *

class WorkoutSelector:
    def __init__(self, workouts):
        """
        workouts: list of Workout objects
        """
        self.workouts = workouts
        self.root = tk.Tk()
        self.root.title("Workout Selector")

        ttk.Label(
            self.root,
            text="Select your workout",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        self.buttons_frame = ttk.Frame(self.root, padding=10)
        self.buttons_frame.pack()

        for w in self.workouts:
            ttk.Button(
                self.buttons_frame,
                text=w.name,
                command=lambda w=w: self.start_workout(w),
                width=25
            ).pack(pady=5)

        ttk.Button(
            self.root,
            text="Exit",
            command=self.root.destroy,
            width=25
        ).pack(pady=10)

        self.root.mainloop()

    def start_workout(self, workout):
        """Launch the selected workout and close this window."""
        self.root.destroy()
        workout.start()

if __name__ == "__main__":
    workout_list = [Push_I, Push_II, Pull_I, Pull_II]
    WorkoutSelector(workout_list)
