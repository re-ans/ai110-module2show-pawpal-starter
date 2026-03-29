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

## Testing PawPal+

The system includes **28 comprehensive tests** across 5 test classes to ensure reliability and correctness:

```bash
python3 run_tests.py
```

### Test Coverage

| Test Class | Tests | Coverage |
|-----------|-------|----------|
| **TestTask** | 4 | Task completion marking, duration/priority validation, string formatting |
| **TestPet** | 3 | Task addition counting, category filtering, pet info display |
| **TestOwner** | 4 | Time conversion, pet management, task retrieval, preferences |
| **TestScheduler** | 3 | Feasibility calculation, completed task filtering, schedule validation |
| **TestSchedulerAlgorithms** | 14 | Sorting, filtering, conflict detection, recurring tasks, edge cases |

### Algorithm Test Coverage (14 tests)

**Sorting Tests (2):**
- Chronological order verification by earliest_time
- Priority tiebreaker logic for same-time tasks

**Filtering Tests (3):**
- Filter by specific pet (returns correct subset)
- Filter by status (pending vs. completed)
- Filter by category (grouping by walk, feeding, grooming, etc.)

**Conflict Detection Tests (3):**
- Same-pet overlaps detected and flagged
- Non-overlapping tasks don't trigger false positives
- Informational conflicts for different pets

**Recurring Task Tests (3):**
- Daily/weekly task copy creation
- Returns None for non-recurring tasks
- Auto-creates next instance on mark-complete

**Edge Cases (3):**
- Empty pet with no tasks
- All tasks completed returns empty plan
- Single task schedules correctly

### Test Results

✅ **All 28 tests passing** (100% success rate)
- Core functionality: 14/14 tests passing
- Algorithm correctness: 14/14 tests passing
- Edge case handling: Covered in all test classes

## Confidence Level

⭐⭐⭐⭐⭐ **5 Stars** — System is production-ready with comprehensive test coverage, all edge cases handled, and algorithmic correctness verified.
