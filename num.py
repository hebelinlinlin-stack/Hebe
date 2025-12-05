import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import time

st.set_page_config(page_title="Mouse Parkour", layout="centered")

# Game parameters
WIDTH, HEIGHT = 400, 300
block_x, block_y = 50, 250
block_size = 20
obstacle_width = 20
obstacle_height = 40
obstacle_x = WIDTH
speed = 5

# Initialize session state
if "obstacles" not in st.session_state:
    st.session_state.obstacles = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "jump" not in st.session_state:
    st.session_state.jump = False
if "block_y" not in st.session_state:
    st.session_state.block_y = block_y

# Mouse jump control
mouse_y = st.slider("Move block with slider (simulate mouse)", 0, HEIGHT - block_size, HEIGHT - block_size)
st.session_state.block_y = mouse_y

# Update obstacles
new_obstacles = []
for x, h in st.session_state.obstacles:
    x -= speed
    if x + obstacle_width > 0:
        new_obstacles.append((x, h))
st.session_state.obstacles = new_obstacles

# Add new obstacle randomly
if np.random.rand() < 0.02:
    st.session_state.obstacles.append((WIDTH, np.random.randint(50, HEIGHT-50)))

# Create image
img = Image.new("RGB", (WIDTH, HEIGHT), color="white")
draw = ImageDraw.Draw(img)

# Draw block
draw.rectangle([block_x, st.session_state.block_y, block_x+block_size, st.session_state.block_y+block_size], fill="blue")

# Draw obstacles
for x, h in st.session_state.obstacles:
    draw.rectangle([x, HEIGHT-h, x+obstacle_width, HEIGHT], fill="red")
    # Check collision
    if block_x + block_size > x and block_x < x + obstacle_width:
        if st.session_state.block_y + block_size > HEIGHT - h:
            st.warning(f"Game Over! Score: {st.session_state.score}")
            st.session_state.obstacles = []
            st.session_state.score = 0
            break

# Display score
st.write(f"Score: {st.session_state.score}")

# Show image
st.image(img)

# Update score
st.session_state.score += 1

# Auto-refresh
time.sleep(0.05)
st.experimental_rerun()

