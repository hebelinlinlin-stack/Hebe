import streamlit as st
import time
from streamlit_canvas import st_canvas
import random

st.set_page_config(page_title="Parkour Game", layout="wide")

# Game constants
WIDTH = 600
HEIGHT = 400
PLAYER_SIZE = 20
GRAVITY = 1
JUMP_POWER = -15
GROUND_Y = HEIGHT - PLAYER_SIZE
OBSTACLE_WIDTH = 30
OBSTACLE_HEIGHT = 40
SPEED = 4

# Initialize session state
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

st.title("Parkour Game (Streamlit)")

# Controls
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Controls")
    jump = st.button("Jump")

with col2:
    speed = st.slider("Game Speed", 2, 10, SPEED)

# Reset button
if st.button("Restart Game"):
    st.session_state.player_y = GROUND_Y
    st.session_state.velocity = 0
    st.session_state.obstacles = []
    st.session_state.score = 0
    st.session_state.game_over = False

# Game loop container
placeholder = st.empty()

# Main game loop (single frame per rerun)
if not st.session_state.game_over:

    # Player jump
    if jump and st.session_state.player_y == GROUND_Y:
        st.session_state.velocity = JUMP_POWER

    # Apply gravity
    st.session_state.velocity += GRAVITY
    st.session_state.player_y += st.session_state.velocity

    # Prevent falling below ground
    if st.session_state.player_y > GROUND_Y:
        st.session_state.player_y = GROUND_Y
        st.session_state.velocity = 0

    # Spawn obstacles
    if random.random() < 0.02:
        st.session_state.obstacles.append([WIDTH, GROUND_Y])

    # Move obstacles
    new_obstacles = []
    for ox, oy in st.session_state.obstacles:
        ox -= speed
        if ox + OBSTACLE_WIDTH > 0:
            new_obstacles.append([ox, oy])
        # Collision detection
        if ox < PLAYER_SIZE and ox + OBSTACLE_WIDTH > 0:
            if st.session_state.player_y + PLAYER_SIZE > oy:
                st.session_state.game_over = True
    st.session_state.obstacles = new_obstacles

    # Score
    st.session_state.score += 1

# Draw frame
canvas = st_canvas(
    fill_color="white",
    stroke_width=1,
    background_color="black",
    height=HEIGHT,
    width=WIDTH,
    drawing_mode="transform",
    key="canvas",
)

# Draw player
canvas.json_data["objects"].append({
    "type": "rect",
    "left": 50,
    "top": st.session_state.player_y,
    "width": PLAYER_SIZE,
    "height": PLAYER_SIZE,
    "fill": "cyan",
})

# Draw obstacles
for ox, oy in st.session_state.obstacles:
    canvas.json_data["objects"].append({
        "type": "rect",
        "left": ox,
        "top": oy,
        "width": OBSTACLE_WIDTH,
        "height": OBSTACLE_HEIGHT,
        "fill": "red",
    })

# Update canvas
placeholder.write(f"Score: {st.session_state.score}")

# Game over screen
if st.session_state.game_over:
    st.error("Game Over")
