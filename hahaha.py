import streamlit as st
import random

st.set_page_config(page_title="Parkour Game", layout="centered")

WIDTH = 600
HEIGHT = 300
PLAYER_SIZE = 25
GRAVITY = 1
JUMP_POWER = -13
GROUND_Y = HEIGHT - PLAYER_SIZE
OBSTACLE_WIDTH = 35
OBSTACLE_HEIGHT = 50

# Auto-refresh (game loop)
refresh_rate = 40  # ms per frame (~25 FPS)
frame = st.experimental_rerun  # older Streamlit fallback

st_autorefresh = st.experimental_rerun if False else st.autorefresh
st_autorefresh(interval=refresh_rate, key="frame_refresh")

# Session state init
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
if "jump_flag" not in st.session_state:
    st.session_state.jump_flag = False

st.title("Parkour Game")

col1, col2 = st.columns([1, 2])

with col1:
    if st.button("Jump"):
        st.session_state.jump_flag = True

with col2:
    speed = st.slider("Game speed", 3, 12, 6)


if st.button("Restart"):
    st.session_state.player_y = GROUND_Y
    st.session_state.velocity = 0
    st.session_state.obstacles = []
    st.session_state.score = 0
    st.session_state.game_over = False


# Game update only if not game over
if not st.session_state.game_over:

    # Jump
    if st.session_state.jump_flag and st.session_state.player_y == GROUND_Y:
        st.session_state.velocity = JUMP_POWER
    st.session_state.jump_flag = False

    # Gravity
    st.session_state.velocity += GRAVITY
    st.session_state.player_y += st.session_state.velocity

    # Ground collision
    if st.session_state.player_y > GROUND_Y:
        st.session_state.player_y = GROUND_Y
