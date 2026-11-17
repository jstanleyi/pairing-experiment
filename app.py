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
