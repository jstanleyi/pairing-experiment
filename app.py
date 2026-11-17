"""The Pairing Experiment — pick a number to create reproducible pairs.

Deploy with Streamlit Community Cloud. The page URL includes ?seed=<number>.
Everyone opening the same URL gets the same pairs but controls their own animation.
"""

from __future__ import annotations

import json
import random
import secrets
from pathlib import Path

import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(
    page_title="The Pairing Experiment",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# The six classmate names, preserved from the existing GitHub repository.
PEOPLE = [
    "Stanley",
    "Hasmig",
    "Aleiya",
    "Hannah",
    "Joanna",
    "Colleen",
]

if len(PEOPLE) != 6 or len(set(PEOPLE)) != 6:
    st.error("Please set six different names in the PEOPLE list in app.py.")
    st.stop()

st.markdown(
    """<style>
      #MainMenu, footer, header[data-testid="stHeader"] {visibility:hidden;}
      .block-container {padding-top: .65rem !important; padding-bottom: 1rem !important; max-width: 1330px;}
      div[data-testid="stAppViewContainer"] {background:#080d1c; color:#e9ecff;}
      div[data-testid="stVerticalBlock"] {gap: .45rem;}
      div[data-testid="stForm"] {border:1px solid rgba(181,194,255,.18); border-radius:17px; background:#11182e; padding:13px 18px 5px;}
      div[data-testid="stTextInput"] input {background:#0b1228; color:#e9ecff; border:1px solid rgba(181,194,255,.3);}
      div[data-testid="stTextInput"] label {color:#e9ecff;}
      div[data-testid="stFormSubmitButton"] button {border-radius:10px; font-weight:700;}
      iframe {border-radius:22px;}
    </style>""",
    unsafe_allow_html=True,
)

# Unlike the original version, the user chooses the seed. The URL preserves
# the choice so a classmate opening the exact same link gets the same draw.
url_seed = str(st.query_params.get("seed", ""))
url_seed_valid = url_seed.isascii() and url_seed.isdigit() and len(url_seed) <= 9
initial_value = str(int(url_seed)) if url_seed_valid else ""

st.markdown(
    '<div style="font-size:11px;letter-spacing:.19em;color:#b8a4fe;font-weight:800;'
    'margin:8px 0 0">01 / SET YOUR RANDOM SEED</div>',
    unsafe_allow_html=True,
)
with st.form("choose_pairing_number", clear_on_submit=False):
    field, apply_col, surprise_col = st.columns([3, 1.35, 1.35], vertical_alignment="bottom")
    with field:
        entered = st.text_input(
            "Enter a whole number (0–999999999)",
            value=initial_value,
            placeholder="e.g. 42",
            max_chars=9,
        )
    with apply_col:
        apply_clicked = st.form_submit_button("Use this number →", use_container_width=True)
    with surprise_col:
        surprise_clicked = st.form_submit_button("Surprise me ↻", use_container_width=True)

seed = initial_value if initial_value else None
if surprise_clicked:
    seed = str(secrets.randbelow(1_000_000_000))
    st.query_params["seed"] = seed
elif apply_clicked:
    raw = entered.strip()
    if not (raw.isascii() and raw.isdigit() and len(raw) <= 9):
        st.error("Please enter a whole number from 0 to 999999999.")
        st.stop()
    seed = str(int(raw))
    st.query_params["seed"] = seed

if seed is None:
    st.info("Choose a number and click 'Use this number' to start your experiment, or let the app pick one for you.")
    st.stop()

st.caption(
    f"Draw number: **{seed}** · Share the current page URL to reproduce the same pairs on another device. "
    "To draw again, enter another number or click Surprise me."
)

# A deterministic, uniform Fisher-Yates shuffle of six participant indices.
# Each distinct set of three unordered pairs has equal probability.
rng = random.Random(seed)
shuffled = list(range(6))
rng.shuffle(shuffled)
pairs = [shuffled[i:i + 2] for i in range(0, 6, 2)]

palette = ["#FFBB91", "#9CD4D5", "#C7B4FF", "#F2A9C1", "#B2DF9F", "#F4D58E"]
config = {
    "people": [
        {
            "name": name,
            "initial": "".join(x[0].upper() for x in name.split()[:2]),
            "color": palette[i],
        }
        for i, name in enumerate(PEOPLE)
    ],
    "pairs": pairs,
    "session": seed,
}

template = Path(__file__).with_name("scene.html").read_text(encoding="utf-8")
json_config = json.dumps(config, ensure_ascii=False).replace("<", "\\u003c")
html(template.replace("__PAIRING_CONFIG__", json_config), height=775, scrolling=False)
