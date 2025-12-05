import streamlit as st
import time
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


# Session state
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

st.title("Parkour Game")

col1, col2 = st.columns([1, 2])

with col1:
    jump = st.button("Jump")

with col2:
    speed = st.slider("Game speed", 3, 12, 6)


# Restart
if st.button("Restart"):
    st.session_state.player_y = GROUND_Y
    st.session_state.velocity = 0
    st.session_state.obstacles = []
    st.session_state.score = 0
    st.session_state.game_over = False


# Game update (one frame)
if not st.session_state.game_over:

    # Jump
    if jump and st.session_state.player_y == GROUND_Y:
        st.session_state.velocity = JUMP_POWER

    # Gravity
    st.session_state.velocity += GRAVITY
    st.session_state.player_y += st.session_state.velocity

    # Ground collision
    if st.session_state.player_y > GROUND_Y:
        st.session_state.player_y = GROUND_Y
        st.session_state.velocity = 0

    # Obstacle spawn
    if random.random() < 0.025:
        st.session_state.obstacles.append([WIDTH, GROUND_Y])

    # Move obstacles
    alive = []
    for ox, oy in st.session_state.obstacles:
        ox -= speed
        if ox + OBSTACLE_WIDTH > 0:
            alive.append([ox, oy])

        # Collision
        if 50 < ox + OBSTACLE_WIDTH and 50 + PLAYER_SIZE > ox:
            if st.session_state.player_y + PLAYER_SIZE > oy:
                st.session_state.game_over = True

    st.session_state.obstacles = alive

    st.session_state.score += 1


# Render as SVG
def draw_svg():
    player_y = st.session_state.player_y

    svg = f"""
    <svg width="{WIDTH}" height="{HEIGHT}">
        <rect width="100%" height="100%" fill="black" />

        <!-- Player -->
        <rect x="50" y="{player_y}" width="{PLAYER_SIZE}" height="{PLAYER_SIZE}" fill="cyan" />

        <!-- Obstacles -->
    """

    for ox, oy in st.session_state.obstacles:
        svg += f"""
            <rect x="{ox}" y="{oy}" width="{OBSTACLE_WIDTH}" height="{OBSTACLE_HEIGHT}" fill="red" />
        """

    svg += "</svg>"
    return svg


st.markdown(draw_svg(), unsafe_allow_html=True)
st.write(f"Score: {st.session_state.score}")

if st.session_state.game_over:
    st.error("Game Over")
