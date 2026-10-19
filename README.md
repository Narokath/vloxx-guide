# Vloxx CM & LCM guide

Encounter guide with phase mechanics, green formations and interactive rehearsals.
[Read the live guide](https://narokath.github.io/vloxx-guide/), or open **Vloxx_Guide.html** offline.

The guide opens as simple mechanic cards. The view button restores focused mechanic browsing. Timings and opening sequences come from our own 426 CM and 45 LCM recordings, through 18 October 2026. Older detailed audits retain their original sample sizes.

## Review and editing

- `guide-body.html`, `guide.css`, `guide.js`: guide content, styling and interactions.
- `field-guide.css`, `field-guide.js`: simple reading view and layout controls.
- `guide-findings.json`: aggregate cast timing and opening summaries; no player-level data.
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

## Direct rehearsals

- [Staff movement](https://narokath.github.io/vloxx-guide/staff-simulator.html)
- [Excision Extremis](https://narokath.github.io/vloxx-guide/excision-simulator.html)
- [P4 crossover (CM)](https://narokath.github.io/vloxx-guide/p4-simulator.html)
