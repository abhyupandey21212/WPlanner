# -*- coding: utf-8 -*-
"""
Created on Sat Oct 18 16:51:54 2025

@author: abhyu
"""


# app.py
import streamlit as st
import numpy as np
from datetime import datetime
import time
from workouts import My_body as my_body # import your existing workout objects
import atexit
import altair as alt
import os, json

# List of all workouts
#my_body.save_data()

my_body.load_data()



WORKOUTS = my_body.workouts

#atexit.register(my_body.save_data)

page = st.sidebar.selectbox("Select page:", ["Workout", "Stats"])

if page == "Workout":
    AUTOSAVE_FILE = "autosave.json"
    # Restore autosaved progress if it exists
    if os.path.exists(AUTOSAVE_FILE):
        autosaved = True
        with open(AUTOSAVE_FILE, "r") as f:
            try:
                autosave_dic = json.load(f)
                st.session_state.workout_progress = autosave_dic["workout_progress"]
                st.session_state.start_time = autosave_dic["start_time"]
                st.info("💾 Autosaved workout progress restored.")
            except json.JSONDecodeError:
                st.session_state.workout_progress = {}
                st.session_state.start_time = time.time()
                autosaved = False
    else:
        st.session_state.workout_progress = {}
        st.session_state.start_time = time.time()
        autosaved = False
        
    st.set_page_config(page_title="Workout Tracker", layout="centered")

    st.title("Workout Tracker")
    st.write("Select a workout to start tracking your session.")

    # Select workout
    selected = st.selectbox("Choose workout:", [w.name for w in WORKOUTS])
    workout = next(w for w in WORKOUTS if w.name == selected)

    if "session_data" not in st.session_state:
        st.session_state.session_data = {}
    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False
    if "start_time" not in st.session_state:
        st.session_state.start_time = None


    # Load last workout results
    last_data = workout.load_data()

    st.subheader(f"Workout: {workout.name}")
            
    if "workout_progress" not in st.session_state:
        st.session_state.workout_progress = {}
        elapsed_time = int((time.time() - workout.start_time)//60)
        #st.session_state.workout_progress["time"] = str(elapsed_time)

    
    #Header buttons
    cols_head = st.columns(3)
    start_button = cols_head[0].button("Start Workout")
    reset_timer = cols_head[1].button("Restart timer")
    #tell_timer = cols_head[2].button("Tell timer")

    if start_button:
        st.session_state.session_data = {"start_time": time.time(), "results": {}}
        if st.session_state.start_time is None:
            st.session_state.start_time = time.time()
        st.session_state.timer_running = True
        if workout.start_time == 0:
            workout.start_time = time.time()    
        
    if reset_timer:
        st.session_state.session_data['start_time'] = time.time()
        st.session_state.start_time = time.time()
        st.success("Timer reset! ✅")
    # Timer display
    with cols_head[2]:
        timer_placeholder = st.empty()
    
        if st.session_state.timer_running and st.session_state.start_time:
            elapsed = time.time() - st.session_state.start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            timer_placeholder.markdown(f"### ⏱️ {minutes:02d}:{seconds:02d}")
        else:
            timer_placeholder.markdown("### ⏸️ 00:00")

    

    if st.session_state.session_data:
        st.write("---")
        
        #st.write("### Fill in your sets:")
        results = {}
        for block_idx, block in enumerate(workout.blocks):
            st.markdown(f"#### Block {block_idx+1}")
            
            #Creating the correct block order
            all_sets = []
            set_lengths = [n_sets for n_sets in block.values()]
            for move, n_sets in block.items():
                all_sets.append([move]*n_sets)
            smaller = min(set_lengths)
            ordered_set = {i: [move for move in block] for i in range(smaller)}
            while max(ordered_set) < max(set_lengths)-1:
                ordered_set[max(ordered_set) + 1] = [all_sets[0][0]]            

            #Filling from autosave
            for move, n_sets in block.items():
                if not autosaved:
                    st.session_state.workout_progress[move.name] = [{"weight": 0.0, "reps": 0} for i in range(n_sets)]


                #st.markdown(f"Set {s+1}")
            #Writting workout
            last_thing = max(ordered_set)
            for s, subset in ordered_set.items():
                    #st.markdown(f"Set {s+1}")
                sets = []   

                for move in subset:
                    if last_data is None:
                        last = None
                    else:
                        last = last_data.get(move.name, [])
                    cols = st.columns(5)
                    cols[0].write(f"Set {s+1}")
                    cols[1].write(f"**{move.name}**")
                    if last is None:
                        last_w = '-'
                        last_r = '-'
                    else:
                        #print('found prev values')
                        #print(last)
                        last_w = last[s]["weight"] if s < len(last) else "-"
                        last_r = last[s]["reps"] if s < len(last) else "-"
                                            
                    # Prefill from autosave if available
                    prev = st.session_state.workout_progress.get(move.name, [])
                    #print(prev)
                    prev_w = prev[s]["weight"] if s < len(prev) else 0.0
                    prev_r = prev[s]["reps"] if s < len(prev) else 0
                    
                    w = cols[2].number_input(
                        f"Weight {move.name} set{s}",
                        value=float(prev_w),
                        label_visibility="collapsed"
                    )
                    r = cols[3].number_input(
                        f"Reps {move.name} set{s}",
                        value=int(prev_r),
                        label_visibility="collapsed"
                    )
                    cols[4].write(f"Last: {last_w}kg × {last_r}")
                    #st.write("---")

                    
                    sets.append({"weight": w, "reps": r})
                    try:
                        results[move].append({"weight": w, "reps": r})
                    except:
                        results[move] = [{"weight": w, "reps": r}]
                    
                    #Autosave
                    st.session_state.workout_progress[move.name][s] = {"weight": w, "reps": r}
                    autosave_dic = {"workout_progress": st.session_state.workout_progress, "start_time": st.session_state.start_time}
                    with open(AUTOSAVE_FILE, "w") as f:
                        json.dump(autosave_dic, f)
                        
                if s == last_thing:
                    st.write("---")


                    
    #Footer buttons
    cols_footer = st.columns(3)   
    finish_button = cols_footer[0].button("Finish Workout")
    cancel_button = cols_footer[2].button("Cancel Workout") 
        
    if finish_button:
        end_time = time.time()
        # Check if any entry was made
        #any_entered = any(s["weight"] or s["reps"] for sets in results.values() for s in sets)
        #if any_entered:
        workout.results = results
        workout.save_data(end_time)
        st.success("Workout saved successfully! 💪")
        st.session_state.session_data = {}
        workout.do()
        my_body.save_data()
        #else:
         #   st.warning("Workout cancelled — no data entered.")
        if os.path.exists(AUTOSAVE_FILE):
            os.remove(AUTOSAVE_FILE)
            
    if cancel_button:
        if os.path.exists(AUTOSAVE_FILE):
            os.remove(AUTOSAVE_FILE)
            st.success("Workout cancelled, nothing saved")
            
    st.write("---")
    st.subheader("🖥 Debug Console")
    
    # Input field for an expression
    console_input = st.text_input("Enter a Python expression to evaluate:")
    
    if console_input:
        try:
            # Evaluate the expression in the context of the app
            result = eval(console_input, {"my_body": my_body, "workout": workout, "results": results})
            st.write("Result:", result)
        except Exception as e:
            st.error(f"Error: {e}")

    
elif page == "Stats":
    st.title("Muscle Stats")


    # Get the muscle data
    volume_done = my_body.volume_done()
    volume_needed = my_body.volume_needed()
    rest_done = my_body.rest_accumulated()
    rest_needed = my_body.rest_needed()
    
    for workout in my_body.workouts:
        cols = st.columns(3)
        cols[0].write(workout.name)
        readiness = "READY" if workout.is_ready() else "NOT READY"
        cols[2].write(readiness) 
        
    st.write("Overview of volume done vs needed and rest.")

    # Build a DataFrame for plotting
    import pandas as pd
    df = pd.DataFrame({
        "Muscle": [mus.name for mus in my_body.muscles],
        "Volume Done": [volume_done[mus] for mus in my_body.muscles],
        "Volume Needed": [volume_needed[mus] for mus in my_body.muscles],
        "Rest Done": [min(7, rest_done[mus]) for mus in my_body.muscles],
        "Rest Needed": [rest_needed[mus] for mus in my_body.muscles]
    })

    # Volume chart overlayed
    volume_df = df.melt(id_vars="Muscle", value_vars=["Volume Done", "Volume Needed"],
                        var_name="Type", value_name="Volume")
    volume_chart = alt.Chart(volume_df).mark_bar(opacity=0.7).encode(
        x=alt.X("Muscle:N", sort=None),
        y=alt.Y("Volume:Q", stack=None),
        #xOffset="Type:N",  # 👈 shifts the bars slightly left/right
        color="Type:N"
    ).properties(width=600, height=400)
    st.altair_chart(volume_chart)
    
    # Rest chart overlayed
    rest_df = df.melt(id_vars="Muscle", value_vars=["Rest Done", "Rest Needed"],
                        var_name="Type", value_name="Rest")
    rest_chart = alt.Chart(rest_df).mark_bar(opacity=0.7).encode(
        x=alt.X("Muscle:N", sort=None),
        y=alt.Y("Rest:Q", stack=None),
        color="Type:N"
    ).properties(width=600, height=400)
    st.altair_chart(rest_chart)
    
    # Weekly reset button
    st.write("---")
    if st.button("Start New Week"):
        my_body.weekly_reset()
        st.success("Weekly stats reset! ✅")
        
    st.write("---")
    st.subheader("🖥 Debug Console")
    
    # Input field for an expression
    console_input = st.text_input("Enter a Python expression to evaluate:")
    
    if console_input:
        try:
            # Evaluate the expression in the context of the app
            result = eval(console_input, {"my_body": my_body, "df": df})
            st.write("Result:", result)
        except Exception as e:
            st.error(f"Error: {e}")



