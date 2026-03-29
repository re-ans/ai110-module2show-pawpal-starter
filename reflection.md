# PawPal+ Project Reflection

## 1. System Design

**Core User Actions**

The following three core actions define what users should be able to perform in PawPal+:

1. **Enter and manage owner/pet information** - Users can input basic details about themselves and their pet (e.g., pet name, type, owner availability/preferences). This establishes the context for task planning.

2. **Add and edit pet care tasks** - Users can create, modify, and organize pet care tasks (e.g., walks, feeding, medication, grooming). Each task should have properties like duration and priority to inform scheduling decisions.

3. **Generate and view a daily schedule** - Users can request an optimized daily plan that arranges their pet care tasks based on constraints (available time, task priority, owner preferences) and receive a clear display of the proposed schedule with explanations of why tasks are scheduled in a particular order.

**a. Initial design**

**UML Overview:**
I designed a four-class system to separate concerns and enable clean data flow:

1. **Owner** — Manages owner information and constraints
   - Attributes: name, available_hours_per_day, preferences (dict)
   - Responsibilities: Track owner availability and update preferences
   - Methods: get_available_time(), update_preferences()

2. **Pet** — Represents a pet that receives care
   - Attributes: name, species, age, special_needs (list)
   - Responsibilities: Hold pet information needed for task prioritization
   - Methods: get_info()

3. **Task** — Represents a single pet care activity
   - Attributes: name, duration (minutes), priority (1-5), category (walk/feeding/meds/etc.), frequency
   - Responsibilities: Encapsulate task details and provide priority/string representations
   - Methods: get_priority(), to_string()

4. **Scheduler** — Orchestrates daily planning by combining owner availability, pet needs, and task constraints
   - Attributes: owner (Owner), pets (List[Pet]), tasks (List[Task])
   - Responsibilities: Generate feasible daily schedules, validate plans, calculate feasibility scores
   - Methods: generate_daily_plan(), validate_schedule(), calculate_feasibility()

**Relationships:**
- Owner owns one or more Pets
- Scheduler references an Owner, manages Pets, and schedules Tasks
- This separation allows Tasks to be independent of specific owners/pets initially, then bound during scheduling

**b. Design changes**

**Changes made after Copilot code review:**

1. **Added pet_name to Task** — Tasks now explicitly reference which pet they're for (e.g., pet_name="Buddy"). This creates a clear many-to-one relationship and prevents the scheduler from assigning a "walk" task meant for a dog to a cat.

2. **Added time-window constraints to Task** — Added earliest_time and latest_time attributes to capture scheduling windows (e.g., walks only between 6-8am, medications always at noon). This allows the scheduler to respect pet-specific timing needs without adding a separate constraint class.

3. **Added validation with __post_init__** — Implemented dataclass post-initialization to validate priority (1-5), positive duration, and valid time ranges. This catches invalid data early and prevents invalid schedules during generation.

**Why these changes help:**
- **Clarity:** Tasks now explicitly bind to pets, making the Scheduler's logic simpler
- **Flexibility:** Time windows remove the need for a separate Constraint class while capturing the most common constraints
- **Robustness:** Validation prevents garbage data from propagating to the scheduler

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

**Constraints the Scheduler Considers:**

1. **Time Constraints** — Each task has `earliest_time` and `latest_time` (0-23 hours), defining when it can be scheduled
2. **Owner Availability** — Owner has `available_hours_per_day` limiting total tasks that fit
3. **Task Priority** — Priority 1-5 (5 = highest) determines scheduling order
4. **Pet Identity** — Tasks are bound to specific pets; conflict detection flags same-pet overlaps as warnings
5. **Task Frequency** — "daily", "weekly", "twice_daily" tasks recur automatically when marked complete
6. **Completion Status** — Completed tasks are excluded from future plans

**Decision Hierarchy (What Mattered Most):**

1. **Priority is primary** — The core sort key; highest priority tasks scheduled first
2. **Time windows are secondary** — Used as tiebreaker; within same priority, earlier tasks go first
3. **Pet identity is tertiary** — Especially important for conflict warnings (same-pet conflicts < cross-pet conflicts)
4. **Owner availability is a hard constraint** — The scheduler validates that total task duration ≤ available time
5. **Recurrence and completion are automation** — They enable the initial plan to be maintained over days without manual re-entry

**Why This Hierarchy:**
Pet owners care most about *what* they'll do (priority) and *when* (time window). Pet identity matters for task coordination. Owner availability is a deal-breaker if exceeded. Recurrence and completion tracking are nice-to-have automations that reduce manual work.

**b. Tradeoffs**

**Tradeoff 1: Conflict Detection — Exact Time Windows vs. Duration Overlap**

My scheduler uses "exact time window overlap" detection: two tasks conflict if their scheduled time windows overlap (e.g., one scheduled 6:00-9:00, another 8:00-12:00).

- **Pro:** Simple to understand and implement; one-liner logic
- **Con:** Misses partial overlaps; if tasks take 45 minutes but windows are loose, the algorithm doesn't check actual durations

**Why it's reasonable:** 
For a pet owner's daily planning, loose time windows buffer against delays. The warning "Morning Walk (6-9) and Cat Feeding (8-12) overlap" gives the user enough information to manually adjust. A perfect duration-overlap detector would be overkill for this use case.

**Tradeoff 2: Recurring Tasks — Same-Day Addition vs. Date-Aware Generation**

When a "daily" task is marked complete, `create_recurring_task()` immediately adds a new instance to the same pet's task list (not date-aware).

- **Pro:** Simple, deterministic; no date calculations needed
- **Con:** All recurring instances end up on the same day; UI needs to distribute them

**Why it's reasonable:**
PawPal+ is designed for *daily* planning, not multi-week scheduling. Recurring tasks are meant to be placeholders that the UI displays day-by-day. A date-aware system would require datetime management and calendar logic, adding complexity for limited benefit in a daily-focused app.

**Tradeoff 3: Sorting — Readability over Performance**

`sort_by_time()` uses Python's `sorted()` with a lambda key: `sorted(tasks, key=lambda t: (t.earliest_time, -t.priority))`.

- **Pro:** Readable; easy to modify sort order later
- **Con:** O(n log n) instead of O(n) specialized algorithms

**Why it's reasonable:**
Pet owners have 5-20 tasks/day. O(n log n) on 20 items is negligible (<1ms). Readability matters more than micro-optimizations. A future developer can instantly understand what this sort does.

**Tradeoff 4: Filtering — List Comprehensions over Indexing**

Filtering methods like `filter_by_pet()` iterate through all tasks: `[t for t in self.tasks if t.pet_name == pet_name]`

- **Pro:** Clear intent; works with any task list size; easy to combine filters
- **Con:** O(n) for every filter; no indices to speed up repeated queries

**Why it's reasonable:**
For typical pet owner usage (< 100 tasks), linear filtering is fast. Index-based lookups would require maintaining separate data structures (hash tables per pet), adding complexity without noticeable speed improvement.

---

## 3. UI Integration (Backend → Streamlit)

**a. Session State Management**

Streamlit reruns the entire script on every user interaction, which means objects would normally "die" and be recreated. To solve this:
- Used `st.session_state` as a persistent "vault" that survives across reruns
- Initialized `st.session_state.owner` once and stored the Owner object there
- Checked `if "owner" not in st.session_state:` before creating a new Owner, ensuring data persists

**b. UI Components Wired to Class Methods**

The app now connects UI actions directly to backend logic:
1. **Owner Management** — Text inputs update `st.session_state.owner.name` and `.available_hours_per_day` via `Update Owner Info` button
2. **Pet Management** — "Add Pet" button calls `Owner.add_pet()` with a Pet instance created from form inputs
3. **Task Management** — "Add Task" button calls `Pet.add_task()`, creating a Task with validated priority (1-5) and time windows
4. **Schedule Generation** — "Generate Schedule" button instantiates Scheduler and calls `.generate_daily_plan()`, displaying sorted tasks with feasibility metrics

**c. Data Flow Example**

User clicks "Add Pet" → form values captured → `new_pet = Pet(...)` created → `st.session_state.owner.add_pet(new_pet)` called → UI updates to show new pet → `st.rerun()` refreshes display

**d. Validation and Feedback**

- Task validation happens in Task `__post_init__()` (priority 1-5, positive duration, valid time windows)
- Bad inputs show `st.error()` messages caught from ValueError exceptions
- Success messages confirm actions (e.g., "✓ Added Buddy the Dog")
- Duplicate pet checking warns if you try to add a pet with the same name

**e. Schedule Display**

When user generates a schedule:
- Scheduler filters incomplete tasks, sorts by priority (descending) then by earliest hour
- Displays total time needed vs. available, feasibility %, and whether schedule is valid
- Shows each task with start/end times, duration, priority stars, and category
- Warns if overloaded (needs more time than available) with actionable advice

---

## 4. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 5. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 6. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
