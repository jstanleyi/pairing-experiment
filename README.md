# The Pairing Experiment

An animated six-person, three-pair group assignment website.

- **Python** randomly and uniformly creates three disjoint pairs from six classmates.
- **HTML Canvas / JavaScript** animates each participant wandering, mixing, and being pulled toward their partner.
- **Same URL and seed -> same group assignments** on every device, with independent playback.
- Press **Begin pairing** or **Replay the experiment** to control your own animation. Replaying does *not* change the actual assignments.

## Customize

Open `app.py`, replace the six names under `PEOPLE` with your classmates' names, and save.

## Run on your computer

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Put it online and share the link

1. Create a GitHub repository and upload `app.py`, `scene.html`, and `requirements.txt`.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/) and select **Create app**.
3. Choose the GitHub repository and `app.py` as the entrypoint, then deploy.
4. Share the resulting `https://...streamlit.app/` URL with classmates.

Everyone using the same URL will see the **same pairs**. Each person independently clicks the arrow to watch the animation.

### Changing the draw for a different class session

Append a new `seed` query parameter to the deployed link, e.g.

`https://your-app.streamlit.app/?seed=week2`

Use the **exact same seed-containing link** for all classmates during that session. If you have no `seed` query parameter, the app uses its fixed default (`class-2026-11-17`). This prevents contradictory results without needing a shared database.

**Important:** The seed makes the grouping reproducible, not secret. Anyone with access to the page and code can inspect the assigned pairs. If the group allocations must stay hidden until a live, shared reveal, a server-side reveal mechanism is required.
