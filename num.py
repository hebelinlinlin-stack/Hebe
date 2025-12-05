import streamlit as st
from PIL import Image, ImageDraw
import random

st.set_page_config(layout="centered")

WIDTH, HEIGHT = 400, 300
BLOCK_SIZE = 20
OBSTACLE_WIDTH = 20
SPEED = 5

# Session state
if "block_y" not in st.session_state:
    st.session_state.block_y = HEIGHT - BLOCK_SIZE
if "obstacles" not in st.session_state:
    st.session_state.obstacles = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "jump" not in st.session_state:
    st.session_state.jump = False

# Mouse-controlled jump
jump = st.button("Jump!")
if jump:
    st.session_state.jump = True

# Update block position
if st.session_state.jump:
    st.session_state.block_y -= 40
    st.session_state.jump = False
else:
    # Gravity
    if st.session_state.block_y < HEIGHT - BLOCK_SIZE:
        st.session_state.block_y += 5

# Move obstacles
new_obstacles = []
for x, h in st.session_state.obstacles:
    x -= SPEED
    if x + OBSTACLE_WIDTH > 0:
        new_obstacles.append((x, h))
st.session_state.obstacles = new_obstacles

# Add new obstacle
if random.random() < 0.02:
    st.session_state.obstacles.append((WIDTH, random.randint(40, 100)))

# Create game image
img = Image.new("RGB", (WIDTH, HEIGHT), "white")
draw = ImageDraw.Draw(img)

# Draw block
draw.rectangle(
    [50, st.session_state.block_y, 50 + BLOCK_SIZE, st.session_state.block_y + BLOCK_SIZE],
    fill="blue"
)

# Draw obstacles
for x, h in
