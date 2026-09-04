import streamlit as st
import random
import time
import json
import os
from datetime import datetime

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="BT Wheel Of Names",
    page_icon="🏆",
    layout="centered"
)

# --------------------------------------------------
# FILES
# --------------------------------------------------

HISTORY_FILE = "winner_history.json"

# --------------------------------------------------
# LOAD WINNER HISTORY
# --------------------------------------------------

if os.path.exists(HISTORY_FILE):
    try:
        with open(HISTORY_FILE, "r") as f:
            saved_history = json.load(f)
    except:
        saved_history = []
else:
    saved_history = []

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "winner" not in st.session_state:
    st.session_state.winner = None

if "winner_history" not in st.session_state:
    st.session_state.winner_history = saved_history

# --------------------------------------------------
# PARTICIPANTS
# --------------------------------------------------

participants = [
    "Harsha",
    "Harish",
    "Sudhakar",
    "Basava",
    "Ranjit",
    "Smriti",
    "Shiva",
    "Akshay",
    "Abhay",
    "Gopi",
    "Pragalath",
    "Atanu",
    "Sharana"
]

# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown("""
<style>

.main-title{
    text-align:center;
    font-size:48px;
    font-weight:bold;
    color:#ff4b4b;
}

.sub-title{
    text-align:center;
    color:gray;
    margin-bottom:20px;
}

.spin-card{
    background:linear-gradient(135deg,#111827,#1F2937);
    color:white;
    text-align:center;
    border-radius:20px;
    padding:50px;
    margin-top:15px;
    margin-bottom:15px;
    font-size:42px;
    font-weight:bold;
    border:3px solid #ff4b4b;
}

.winner-card{
    background:linear-gradient(135deg,#FFD700,#FFA500);
    color:black;
    text-align:center;
    padding:35px;
    border-radius:25px;
    font-size:32px;
    font-weight:bold;
    box-shadow:0px 5px 20px rgba(0,0,0,0.3);
}

.history-box{
    background:#f4f4f4;
    border-radius:15px;
    padding:15px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🎡 Wheel Of Names</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Spin & Select a Champion</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# PARTICIPANTS LIST
# --------------------------------------------------

with st.expander("👥 Participants", expanded=True):
    st.write(", ".join(participants))

# --------------------------------------------------
# BUTTONS
# --------------------------------------------------

col1, col2 = st.columns(2)

spin = col1.button(
    "🎯 SPIN WHEEL",
    use_container_width=True
)

reset = col2.button(
    "🗑 RESET HISTORY",
    use_container_width=True
)

# --------------------------------------------------
# RESET
# --------------------------------------------------

if reset:
    st.session_state.winner_history = []
    st.session_state.winner = None

    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

    st.success("History Reset Successfully")

# --------------------------------------------------
# SPIN AREA
# --------------------------------------------------

spin_area = st.empty()

# --------------------------------------------------
# SPIN LOGIC
# --------------------------------------------------

if spin:

    recent_winners = [
        item["name"]
        for item in st.session_state.winner_history
    ]

    eligible_names = [
        p for p in participants
        if p not in recent_winners
    ]

    if len(eligible_names) == 0:
        eligible_names = participants

    winner = random.choice(eligible_names)

    speed = 0.04

    for _ in range(45):

        random_name = random.choice(participants)

        spin_area.markdown(
            f"""
            <div class="spin-card">
                🎡<br><br>
                {random_name}
            </div>
            """,
            unsafe_allow_html=True
        )

        time.sleep(speed)
        speed += 0.004

    # Stop wheel on the actual winner
    spin_area.markdown(
        f"""
        <div class="spin-card">
            🏆<br><br>
            {winner}
        </div>
        """,
        unsafe_allow_html=True
    )

    winner_time = datetime.now().strftime(
        "%d-%b-%Y %I:%M:%S %p"
    )

    winner_record = {
        "name": winner,
        "date": winner_time
    }

    st.session_state.winner = winner_record

    st.session_state.winner_history.insert(
        0,
        winner_record
    )

    st.session_state.winner_history = (
        st.session_state.winner_history[:4]
    )

    with open(HISTORY_FILE, "w") as f:
        json.dump(
            st.session_state.winner_history,
            f,
            indent=4
        )

# --------------------------------------------------
# RECOVER LAST WINNER AFTER RESTART
# --------------------------------------------------

if (
    st.session_state.winner is None
    and len(st.session_state.winner_history) > 0
):
    st.session_state.winner = (
        st.session_state.winner_history[0]
    )

# --------------------------------------------------
# WINNER DISPLAY
# --------------------------------------------------

if st.session_state.winner:

    st.balloons()

    st.markdown(
        f"""
        <div class="winner-card">
            🏆 WINNER 🏆
            <br><br>
            👑 {st.session_state.winner['name']}
            <br><br>
            🎉 Congratulations 🎉
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# LAST 4 WINNERS
# --------------------------------------------------

st.markdown("---")

st.subheader("🏅 Last 4 Winners")

if st.session_state.winner_history:

    st.markdown(
        '<div class="history-box">',
        unsafe_allow_html=True
    )

    for i, item in enumerate(
        st.session_state.winner_history,
        start=1
    ):
        st.write(
            f"{i}. 🏆 {item['name']} | 📅 {item['date']}"
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

else:
    st.info("No winners yet.")

# --------------------------------------------------
# STATS
# --------------------------------------------------

st.markdown("---")

st.metric(
    "👥 Total Participants",
    len(participants)
)