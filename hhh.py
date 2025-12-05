import streamlit as st
import random

st.set_page_config(page_title="Parkour Game", layout="centered")

WIDTH = 600
HEIGHT = 300
PLAYER_SIZE = 25
GRAVITY = 3
JUMP_POWER = -25
GROUND_Y = HEIGHT - PLAYER_SIZE
OBSTACLE_WIDTH = 40
OBSTACLE_HEIGHT = 50

# Session State
if "player_y" not in st.session_state:
    st.session_state.player_y = GROUND_Y
if "velocity" not in st.session_state:
    st.session_state.velocity = 0
if "obstacles" not in st.session_state:
    st.session_state.obstacles = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False

st.title("Parkour Game (Guaranteed Working Version)")

col1, col2, col3 = st.columns(3)

with col1:
    jump = st.button("Jump")

with col2:
    step = st.button("Next Frame")

with col3:
    restart = st.button("Restart")

speed = st.slider("Speed", 5, 20, 10)


# Restart
if restart:
    st.session_state.player_y = GROUND_Y
    st.session_state.velocity = 0
    st.session_state.obstacles = []
    st.session_state.score = 0
    st.session_state.game_over = False


# Game Logic (runs only when button pressed)
if not st.session_state.game_over and (jump or step):

    # Jump button
    if jump and st.session_state.player_y == GROUND_Y:
        st.session_state.velocity = JUMP_POWER

    # Gravity
    st.session_state.velocity += GRAVITY
    st.sessio
