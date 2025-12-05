import streamlit as st
import time
import random

st.set_page_config(page_title="Parkour Game", page_icon="🎮")

# Initialize session state
if "player_y" not in st.session_state:
    st.session_state.player_y = 0
if "obstacles" not in st.session_state:
    st.session_state.obstacles = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False

st.title("🏃 Parkour Game (Streamlit Edition)")

# Jump button
if st.button("Jump"):
    if st.session_state.player_y == 0:
        st.session_state.player_y = 2  # jump height

game_area = st.empty()
score_area = st.empty()

# Reset
if st.button("Restart Game"):
    st.session_state.player_y = 0
    st.session_state.obstacles = []
    st.session_state.score = 0
    st.session_state.game_over = False

# GAME LOOP (runs every rerun)
if not st.session_state.game_over:

    # Move player down
    if st.session_state.player_y > 0:
        st.session_state.player_y -= 1

    # Spawn obstacles
    if random.random() < 0.15:
        st.session_state.obstacles.append(20)

    # Move obstacles left
    st.session_state.obstacles = [x - 1 for x in st.session_state.obstacles if x > 0]

    # Collision check
    if 1 in st.session_state.obstacles and st.session_state.player_y == 0:
        st.session_state.game_over = True

    # Draw world
    ground = ["_" for _ in range(21)]
    world = [" " for _ in range(21)]

    # player
    world[1] = "P" if st.session_state.player_y == 0 else "p"

    # obstacles
    for x in st.session_state.obstacles:
        if 0 <= x < 21:
            world[x] = "▓"

    game_area.text("".join(world) + "\n" + "".join(ground))

    st.session_state.score += 1
    score_area.markdown(f"**Score:** {st.session_state.score}")

    # Soft delay to animate
    time.sleep(0.1)

else:
    st.error("Game Over")
    st.write(f"Your Score: {st.session_state.score}")
    st.write("Press **Restart Game** to play again.")
