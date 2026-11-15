# MATH Lock-In

Cram site for **MATH20290 Multivariable Calculus for Engineers** (UCD, 2026/27).

Two modes:

- **Exam path** (default): core questions matched to the official sample exam, plus a fully explained walkthrough of that sample exam at the end. Each topic starts with a short from-scratch explanation and a quick check question.
- **Off the exam path**: every homework question that is not on the exam path (96 parts). New topics come first (level curves, continuity, variation of parameters, direction problems, max/min on a region, higher order ODEs), each with a from-scratch explanation, then extra practice by chapter.

**Live site:** https://albinjoby82-ops.github.io/MATH_Lock-In/

## How to use it

1. Pick a topic, read the Method box.
2. Try the question on paper.
3. Reveal steps one at a time (Space). Mark it "Got it" or "Need to redo".

Progress is saved in your browser.

Every exam-path question has a **Similar question** button (or press S): the same method with new numbers and a full worked solution.

## Editing

Questions live in `content/core/*.txt` (pass path) and `content/full/*.txt` (all homework; the site shows the part of it that is off the exam path). Similar questions live in `content/sim/*.txt`, keyed by question id (`@sim c-limits-0`). After editing, run `python3 build.py` to regenerate `data.js`.

Sheets 1 to 3 follow the official solutions. Sheets 4 and 5 have no official full solutions yet: those were worked by hand, checked against the sheet's short answers and verified with a computer algebra system.
