import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
import cv2
import time
import random

# Game settings
WIDTH = 500
HEIGHT = 300
PLAYER_X = 60
PLAYER_SIZE = 30
GRAVITY = 4
JUMP_FORCE = -12

st.set_page_config(page_title="Mouse Parkour")

# Initialize session state
if "player_y" not in st.session_state:
    st.session_state.player_y = HEIGHT - PLAYER_SIZE
if "vel" not in st.session_state:
    st.session_state.vel = 0
if "obstacles" not in st.session_state:
    st.session_state.obstacles = []
if "running" not in st.session_state:
    st.session_state.running = False
if "score" not in st.session_state:
    st.session_state.score = 0

st.title("🏃 Mouse Parkour")

# Start button
if st.button("Start Game"):
    st.session_state.player_y = HEIGHT - PLAYER_SIZE
    st.session_state.vel = 0
    st.session_state.obstacles = []
    st.session_state.score = 0
    st.session_state.running = True

# Canvas for mouse detection
canvas = st_canvas(
    fill_color="rgba(0,0,0,0)",
    stroke_width=0,
    background_color="white",
    width=WIDTH,
    height=HEIGHT,
    drawing_mode="freedraw",
    key="canvas",
)

# Mouse pressed detection
mouse_pressed = False
if canvas.json_data and "objects" in canvas.json_data:
    mouse_pressed = len(canvas.json_data["objects"]) > 0

# Game loop
if st.session_state.running:

    # Control
    if mouse_pressed:
        st.session_state.vel = JUMP_FORCE
    else:
        st.session_state.vel += GRAVITY

    st.session_state.player_y += st.session_state.vel
    st.session_state.player_y = max(0, min(st.session_state.player_y, HEIGHT - PLAYER_SIZE))

    # Spawn obstacles
    if random.random() < 0.03:
        st.session_state.obstacles.append([WIDTH, HEIGHT - PLAYER_SIZE, 25, PLAYER_SIZE])

    # Move obstacles
    for obs in st.session_state.obstacles:
        obs[0] -= 6

    # Remove off-screen obstacles
    st.session_state.obstacles = [o for o in st.session_state.obstacles if o[0] > -40]

    # Collision detection
    for ox, oy, ow, oh in st.session_state.obstacles:
        if ox < PLAYER_X + PLAYER_SIZE and ox + ow > PLAYER_X:
            if st.session_state.player_y + PLAYER_SIZE > oy:
                st.session_state.running = False

    # Draw frame
    frame = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8) * 255

    # Draw player
    cv2.rectangle(
        frame,
        (PLAYER_X, int(st.session_state.player_y)),
        (PLAYER_X + PLAYER_SIZE, int(st.session_state.player_y + PLAYER_SIZE)),
        (0, 0, 0),
        -1,
    )

    # Draw obstacles
    for ox, oy, ow, oh in st.session_state.obstacles:
        cv2.rectangle(
            frame,
            (int(ox), int(oy)),
            (int(ox + ow), int(oy + oh)),
            (255, 0, 0),
            -1,
        )

    st.session_state.score += 1

    # Show frame
    st.image(frame, clamp=True)
    st.write(f"Score: {st.session_state.score}")

    time.sleep(0.03)
    st.experimental_rerun()

else:
    st.write("Press Start Game to begin.")
