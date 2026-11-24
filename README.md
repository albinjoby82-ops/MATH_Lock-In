# MATH Lock-In

Cram site for **MATH20290 Multivariable Calculus for Engineers** (UCD, 2026/27).

Two modes:

- **Exam path** (default): core questions matched to the official exam topic list (6 questions, see Exam info), plus a fully explained walkthrough of the sample exam at the end. Each topic starts with a short from-scratch explanation and a quick check question.
- **Off the exam path**: the rest of the homework on the exam topics, by chapter (69 parts). Level curves come last (not named on the exam sheet). First order ODEs, variation of parameters and n-th order ODEs are not on the final, so they are left off the site (still in `content/full/`).

**Exam info** (button at the top of the contents, press E, or open `#exam`): date, time, place, countdown, marking rules, each exam question linked to its topics, and what is not on the exam. `exam-info.png` is the original sheet.

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
