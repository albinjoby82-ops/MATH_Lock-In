# MATH Lock-In

Cram site for **MATH20290 Multivariable Calculus for Engineers** (UCD, 2026/27).

Two modes:

- **Pass path** (default): 45 core questions in 14 topics. Each topic starts with a short from-scratch explanation and a quick check question. Built for someone who missed the lectures and needs to pass.
- **All homework**: every question from Problem Sheets 1 to 5 (145 parts) in 22 topics.

**Live site:** https://albinjoby82-ops.github.io/MATH_Lock-In/

## How to use it

1. Pick a topic, read the Method box.
2. Try the question on paper.
3. Reveal steps one at a time (Space). Mark it "Got it" or "Need to redo".

Progress is saved in your browser.

## Editing

Questions live in `content/core/*.txt` (pass path) and `content/full/*.txt` (all homework). After editing, run `python3 build.py` to regenerate `data.js`.

Sheets 1 to 3 follow the official solutions. Sheets 4 and 5 have no official full solutions yet: those were worked by hand, checked against the sheet's short answers and verified with a computer algebra system.
