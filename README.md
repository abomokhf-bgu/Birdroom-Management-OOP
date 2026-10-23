# Birdroom Management — Python OOP

A **Python university OOP workshop project** modeling birds, cages, and their placement in a birdroom. Originally developed for a course and later refactored and documented for a software development portfolio.

## Features
- **8 classes** and multilevel inheritance: `Bird` → `Finch` / `Parrot` → four bird species.
- Overridden methods and Python comparison operators.
- Validated bird IDs, dates, colors, species and cage dimensions.
- Cage capacity checks and species compatibility.
- Birdroom placement with **2D rectangle collision detection**.
- Text-based room visualization and aggregate bird statistics.
- Automated unit tests using Python's standard library.

## Run

Requires Python 3.9 or later. No external dependencies.

```bash
python demo.py
python -m unittest discover -s tests -v
```

## Files
- `birdroom.py` — core classes and business rules
- `demo.py` — runnable usage example
- `tests/test_birdroom.py` — automated tests
- `.gitignore` — ignores Python cache and local environment files

## Architecture
```text
Bird
├── Finch
│   ├── Zebrafinch
│   └── Gouldianfinch
└── Parrot
    ├── Budgerigar
    └── Lovebird

Cage      — contains compatible birds and enforces volume
Birdroom  — positions cages and checks collisions
```

Cage dimensions are measured in **centimeters**; birdroom dimensions in **meters**. Room placement is a **2D front elevation** (length × height), not a full 3D simulation. The assignment's bird equality rule compares species, not IDs.

## Improvements after the workshop
Refactored validation, improved date handling, added duplicate checks, corrected small nest-box rendering, made placement and layout boundaries more consistent, and added documentation, a demo and unit tests.

**Academic note:** This is a university learning project, not a production animal-care system. The code was cleaned up after the original exercise; it should not be mistaken for the untouched original submission.
