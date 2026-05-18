# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
Initial design is centered around five main classes: "Owner", "Pet", "Task", "Scheduler", and "Plan".
This separates the data, the core logic, and the final output. 

- What classes did you include, and what responsibilities did you assign to each?
Owner: Represents the user, holding their name and key constraints, such as their total available time for pet care.
Pet: Represents the pet and stores basic information like its name and type.
Task: Represents a single care activity, containing attributes like its name, duration, and priority level.

Main logic classes:
Scheduler class. Its job is to take a list of all Task objects and the Owner's constraints (like available time) and apply a scheduling algorithm to figure out which tasks can be done.
Finally, the output of the Scheduler is a Schedule object. This class represents the generated daily plan, holding a finalized list of Task objects that fit within the owner's constraints, sorted by priority.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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
