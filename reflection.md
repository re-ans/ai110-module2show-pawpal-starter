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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
