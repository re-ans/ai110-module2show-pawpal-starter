# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling: Advanced Features

PawPal+ includes intelligent algorithms to make pet care planning more efficient:

### Filtering & Organization
- **Filter by Pet** — View only tasks for a specific pet
- **Filter by Status** — Show pending or completed tasks
- **Filter by Category** — Group tasks by type (walks, feeding, grooming, etc.)

### Time-Aware Scheduling
- **Sort by Time** — Organize tasks by time window (earliest-first) for chronological planning
- **Conflict Detection** — Identify overlapping time windows and warn when tasks conflict (especially for the same pet)

### Recurring Tasks
- **Auto-recurrence** — When a "daily" or "weekly" task is marked complete, the system automatically creates the next occurrence
- **Supported Frequencies** — daily, weekly, twice_daily

### Design Philosophy
- **Clarity over Performance** — Algorithms use readable Python patterns (list comprehensions, sorted()) rather than complex optimizations
- **Lightweight Conflict Detection** — Checks for exact time-window overlaps rather than partial overlaps, balancing simplicity with usefulness
- **Non-intrusive Recurrence** — New recurring instances are added immediately upon completion, ready for the UI to distribute across future days

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
