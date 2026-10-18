# Vloxx CM & LCM guide

Encounter guide with phase mechanics, green formations and interactive rehearsals.
Open **Vloxx_Guide.html** in a browser. The guide is self-contained and works offline.

## Review and editing

- `guide-body.html`, `guide.css`, `guide.js`: guide content, styling and interactions.
- `echo-model.js`, `echo-controller.js`: Echoing Blade rehearsal.
- `weapon-movement-sim.js`: conceptual Staff movement rehearsal.
- `mechanic-browser.js`: phase mechanic selection.
- `excision-simulator.html`, `p4-simulator.html`: standalone rehearsals embedded at build time.
- `diagrams/green-strategy-*.svg`: editable phase and combined diagrams.
- `diagrams/share/`: ready-to-share PNG diagrams.

Build with Python 3 (standard library only):

```sh
python build_guide.py
```

To change formation geometry, edit `make_diagrams.py` and `style_green_diagrams.py`,
then run `python style_green_diagrams.py` followed by the guide build.
The PNGs are exports of the SVGs and should be refreshed after artwork changes.

## Checks

```sh
python check_styled_greens.py
python check_phase_layout.py
node check_green_strategy.cjs
node check_mechanic_browser.cjs
node check_echo_playback.cjs
node check_echo_finish.cjs
node check_weapon_movement.cjs
node check_weapon_movement_ui.cjs
```

Simulations are geometry and behaviour rehearsals, not complete combat replays.
Measured findings and model limits are described alongside the relevant mechanics.

This review repository excludes raw combat logs, player-level audit data, local
file inventories, downloaded references, old revisions and development previews.
