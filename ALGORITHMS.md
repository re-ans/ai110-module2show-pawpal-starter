# PawPal+ Algorithms Documentation

## Overview
This document summarizes the intelligent algorithms implemented in PawPal+ to make pet care scheduling more efficient, user-friendly, and automated.

---

## Implemented Algorithms

### 1. FILTERING ALGORITHMS

#### Purpose
Allow users and the scheduler to view focused subsets of tasks based on different criteria.

#### Methods Implemented

**`filter_by_pet(pet_name: str) → List[Task]`**
- Returns all tasks for a specific pet
- Time Complexity: O(n) where n = total tasks
- Use case: "Show me everything Buddy needs today"

**`filter_by_status(completed: bool) → List[Task]`**
- Returns all pending (completed=False) or completed (completed=True) tasks
- Time Complexity: O(n)
- Use case: "Show me what's left to do" vs. "Show me what I've done"

**`filter_by_category(category: str) → List[Task]`**
- Returns all tasks in a category: "walk", "feeding", "medication", "grooming", "enrichment"
- Time Complexity: O(n)
- Use case: "How many walks does Buddy need today?"

#### Design Rationale
- **Readability First:** List comprehensions are easy to understand and modify
- **Composable:** Filters can be chained: `scheduler.filter_by_pet("Buddy").filter_by_status(False)`
  - Wait, actually they can't chain directly, but the results can be filtered further
  - Better approach: Get all Buddy's tasks, then manually filter status
- **Performance:** O(n) is acceptable for typical use (5-100 tasks/day)

---

### 2. SORTING ALGORITHM

#### Purpose
Organize tasks by time window to create chronologically logical schedules.

#### Method Implemented

**`sort_by_time(tasks: List[Task]) → List[Task]`**
- Sorts tasks by `earliest_time` ascending (with priority descending as tiebreaker)
- Sort key: `(earliest_time, -priority)`
- Time Complexity: O(n log n) via Python's Timsort
- Output: Tasks ordered 6:00 AM first, then 7:00 AM, etc.

```python
# Example
tasks = [
    Task("Evening Walk", earliest_time=18),    # Will be 3rd
    Task("Morning Walk", earliest_time=6),     # Will be 1st
    Task("Lunch Prep", earliest_time=12),      # Will be 2nd
]

sorted_tasks = scheduler.sort_by_time(tasks)
# Result: [Morning Walk, Lunch Prep, Evening Walk]
```

#### Design Rationale
- **Natural chronological ordering:** Helps owners visualize their day
- **Tiebreaker logic:** Within same hour, higher priority tasks come first
- **Not date-aware:** All tasks treated as same day (good for daily planning, not weekly)

---

### 3. CONFLICT DETECTION ALGORITHM

#### Purpose
Identify when two tasks are scheduled for overlapping time windows, helping owners avoid over-booking.

#### Method Implemented

**`detect_conflicts(plan: Optional[List[Task]]) → List[Tuple[Task, Task, str]]`**

**Algorithm Logic:**
```
FOR each task i from 0 to n-1:
    FOR each task j from i+1 to n-1:
        IF task_i.earliest_time <= task_j.latest_time AND task_j.earliest_time <= task_i.latest_time:
            IF task_i and task_j are for same pet:
                FLAG as "SAME PET" conflict (higher severity)
            ELSE:
                FLAG as "TIMING CONFLICT" (owner might be double-booked)
            ADD to results with explanatory message
RETURN list of (task1, task2, message) tuples
```

**Time Complexity:** O(n²) - necessary for comparing all pairs

**Example:**
```python
conflicts = scheduler.detect_conflicts(plan)
# Example output:
# [
#   (morning_walk, afternoon_walk, "SAME PET: 'Morning Walk' and 'Afternoon Walk' 
#                                   for Buddy overlap in time window 6h-21h"),
#   (buddy_walk, whiskers_feeding, "TIMING CONFLICT: 'Morning Walk' (Buddy) and 
#                                   'Cat Feeding' (Whiskers) scheduled in same 
#                                   time window (6h-12h)")
# ]
```

#### Design Rationale

**Tradeoff: Exact Time Windows vs. Duration-Based Overlap**

- **Our Approach (Exact Windows):** Check if scheduled time windows overlap, not actual task durations
- **Alternative:** Calculate precise time taken by each task and check if durations overlap
- **Why Exact Windows?**
  - Simplicity: One-line comparison vs. complex duration math
  - Good enough: Time windows already provide buffer; 45-minute task in 6-9 window leaves flex room
  - User-friendly: "Walk 6-9 and Feed 8-12" overlap" clearly tells owner *when* to adjust
  - Fits daily planning: Not solving for minute-level precision; owner decision-making is the real scheduler

**Severities:**
- **SAME PET conflicts:** Highest priority (one pet can't do two things at once)
- **TIMING CONFLICTS:** Informational (owner is doing two things simultaneously but with different pets—may be feasible)

---

### 4. RECURRING TASK AUTOMATION

#### Purpose
Automatically regenerate recurring tasks when they're marked complete, reducing manual data entry.

#### Methods Implemented

**`create_recurring_task(task: Task) → Optional[Task]`**
- Creates a copy of a recurring task (daily, weekly, twice_daily)
- Returns None if task frequency is not recurring
- Does NOT add to any list; just creates the instance

**`mark_task_complete_with_recurrence(task: Task, pet: Pet) → None`**
- Marks task as complete
- If task recurs, calls `create_recurring_task()` and auto-adds to pet's task list
- Enables "fire and forget" task tracking

**Supported Frequencies:**
- `"daily"` — Task repeats every time it's marked complete
- `"weekly"` — Task repeats (same logic, UI would distribute across weeks)
- `"twice_daily"` — Task repeats (e.g., morning and evening feeds merge into one recurrence)

**Example Flow:**
```
User marks "Daily Morning Walk" complete
    ↓
mark_task_complete_with_recurrence() called
    ↓
Task marked as completed=True
    ↓
create_recurring_task() creates copy with completed=False
    ↓
New copy added to buddy.tasks
    ↓
Next day's schedule automatically includes new copy
```

#### Design Rationale

**Tradeoff: Same-Day Addition vs. Date-Aware Generation**

- **Our Approach:** Creates new task immediately, added to same pet's task list (not date-aware)
- **Alternative:** Calculate next occurrence date (tomorrow for daily, +7 days for weekly)
- **Why Immediate Same-Day?**
  - Simplicity: No datetime/timedelta complexity needed
  - Fits architecture: UI responsible for distributing across days, not backend
  - Stateless: Each day's view shows tasks to do; recurring instances just sit in the queue
  - Easier testing: No mocking of system date/time

**Limitation:** UI needs to show "today's tasks" (filter_by_status) and exclude next-day tasks from display

---

## Algorithm Performance Summary

| Algorithm | Time Complexity | Space Complexity | Typical Input Size | Result Time |
|-----------|-----------------|------------------|--------------------|------------|
| filter_by_pet | O(n) | O(m)* | 20 tasks | <1ms |
| filter_by_status | O(n) | O(m)* | 20 tasks | <1ms |
| filter_by_category | O(n) | O(m)* | 20 tasks | <1ms |
| sort_by_time | O(n log n) | O(n) | 20 tasks | <1ms |
| detect_conflicts | O(n²) | O(k)** | 20 tasks | <5ms |
| create_recurring_task | O(1) | O(1) | 1 task | <1ms |

*m = size of result set
**k = number of conflicts found (typically small)

---

## Usage Examples

### Example 1: Show pending tasks for Buddy, sorted by time

```python
scheduler = Scheduler(owner=alice)
pending = scheduler.filter_by_status(completed=False)
buddy_pending = [t for t in pending if t.pet_name == "Buddy"]
sorted_tasks = scheduler.sort_by_time(buddy_pending)

for task in sorted_tasks:
    print(f"{task.earliest_time}:00 - {task.name}")
# Output:
# 6:00 - Morning Walk
# 7:00 - Breakfast
# 14:00 - Playtime
```

### Example 2: Check for conflicts before finalizing schedule

```python
conflicts = scheduler.detect_conflicts(daily_plan)

if conflicts:
    print("⚠️  Schedule has conflicts:")
    for task1, task2, msg in conflicts:
        print(f"  • {msg}")
else:
    print("✓ No conflicts detected")
```

### Example 3: Complete a daily task and auto-regenerate

```python
morning_walk = buddy.tasks[0]  # Get the task

# Before: buddy.tasks has 5 items
scheduler.mark_task_complete_with_recurrence(morning_walk, buddy)
# After: buddy.tasks has 6 items (new recurring instance added)

# Next refresh of schedule will include new instance
new_plan = scheduler.generate_daily_plan()
```

---

## Future Improvements

1. **Date-Aware Recurrence** — Store recurrence rules with dates instead of immediate copying
2. **Conflict Resolution** — Suggest auto-scheduling conflicting tasks to free time slots
3. **Optimization** — Use event-driven updates instead of O(n²) collision detection
4. **Priority Learning** — Adjust priority based on user's actual completion patterns
5. **Preferences Integration** — Use owner.preferences to auto-weight certain task types

---

## Design Philosophy

**Clarity > Perfect Optimization**

- Algorithms use readable Python patterns (list comprehensions, sorted(), lambda functions)
- O(n log n) preferred over specialized algorithms if more understandable
- Messages explain *what* and *why* conflicts exist, not just that they do
- Recurring tasks use simple copy pattern, delegating distribution logic to UI

**Fits the Use Case**

- Pet owners typically have 5-50 tasks/day (not thousands)
- Daily planning is the focus (not multi-week or multi-pet facilities)
- User decision-making drives scheduling (algorithms inform, don't dictate)

