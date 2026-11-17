"""The Pairing Experiment — six classmates, three shared pairs.

Run locally:
    pip install -r requirements.txt
    streamlit run app.py

Share a deployed URL with the SAME ?seed= value to ensure everybody
sees the same pairing while controlling their own animation.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(
    page_title="The Pairing Experiment",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# EDIT THESE SIX NAMES. Initials are generated automatically.
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

# Identical seed = identical grouping, even if everyone opens the link separately.
# You can choose a NEW session by appending a seed to the link: ?seed=class-2
seed = st.query_params.get("seed", "class-2026-11-17")
seed = str(seed)[:120]

rng = random.Random(seed)
shuffled = list(range(6))
rng.shuffle(shuffled)
pairs = [shuffled[i:i + 2] for i in range(0, 6, 2)]

palette = ["#FFBB91", "#9CD4D5", "#C7B4FF", "#F2A9C1", "#B2DF9F", "#F4D58E"]

config = {
    "people": [
        {"name": name, "initial": "".join(x[0].upper() for x in name.split()[:2]),
         "color": palette[i]}
        for i, name in enumerate(PEOPLE)
    ],
    "pairs": pairs,
    "session": seed,
}

st.markdown(
    """<style>
      #MainMenu, footer, header[data-testid="stHeader"] {visibility:hidden;}
      .block-container {padding-top: .65rem !important; padding-bottom: 0 !important; max-width: 1330px;}
      div[data-testid="stAppViewContainer"] {background:#080d1c;}
      div[data-testid="stVerticalBlock"] {gap: 0;}
      iframe {border-radius: 22px;}
    </style>""",
    unsafe_allow_html=True,
)

template = Path(__file__).with_name("scene.html").read_text(encoding="utf-8")
# Prevent accidental HTML/script closing if a person's name contains markup.
json_config = json.dumps(config, ensure_ascii=False).replace("<", "\\u003c")
html(template.replace("__PAIRING_CONFIG__", json_config), height=775, scrolling=False)
