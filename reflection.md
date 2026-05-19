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
Yes
- If yes, describe at least one change and why you made it.
If the system needed to support multiple pets, each with their own specific tasks, this relationship would be essential. You would likely want to add pets: List[Pet] to the Owner class.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
The scheduler considers the following constraints:
- Time: The total available time the owner has for pet care tasks.
- Priority: Each task has a priority level that indicates its importance.
- Preferences: The owner may have specific preferences for certain tasks or times of day.
- How did you decide which constraints mattered most?
I prioritized time and task priority as the most critical constraints. Time is a hard constraint because the owner can only dedicate a certain amount of time to pet care each day, so the scheduler must ensure that the total duration of scheduled tasks does not exceed this limit. Task priority is also crucial because it helps the scheduler determine which tasks are more important and should be scheduled first when there are time constraints. Preferences are considered but are secondary to ensuring that high-priority tasks fit within the available time.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI tools primarily for design brainstorming and debugging. During the initial design phase, I used AI to help generate ideas for how to structure the classes and their relationships in the UML diagram. This helped me think through the responsibilities of each class and how they would interact with each other. Additionally, I used AI to assist with debugging when I encountered issues with the scheduling logic. The AI provided suggestions for potential causes of bugs and offered ideas for how to fix them.
- What kinds of prompts or questions were most helpful?
Prompts that asked for suggestions on how to structure the scheduling algorithm or how to handle specific edge cases were particularly helpful. For example, asking "How can I optimize the scheduling algorithm to better handle overlapping tasks?" or "What are some common pitfalls when implementing a task scheduler?" provided useful insights and guidance.

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
I am pretty confident that the scheduler works correctly for the basic cases, as I have tested it with a variety of tasks and constraints. However, I recognize that there may be edge cases or more complex scenarios that I have not yet tested, so I would like to continue expanding my test suite to cover those situations.
- What edge cases would you test next if you had more time?
I would test edge cases such as:
- Tasks that have overlapping time requirements, to ensure the scheduler correctly identifies and handles conflicts.
- Tasks that exceed the owner's total available time, to see how the scheduler prioritizes and selects tasks in such scenarios.
- Tasks with the same priority level, to verify that the scheduler correctly sorts

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
Being able to see a complete end-to-end system that includes both the scheduling logic and the Streamlit UI was very rewarding. It was great to see how the different components (Owner, Pet, Task, Scheduler) came together to create a functional app that can generate a daily plan for pet care. The testing process also gave me confidence in the correctness of the scheduling logic, which is a crucial part of the app's functionality.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would improve the scheduling algorithm to be more sophisticated, perhaps by implementing a more advanced optimization technique that can better handle complex constraints and priorities. Additionally, I would enhance the user interface to provide more detailed explanations of why certain tasks were scheduled at specific times, which would help users understand the reasoning behind the generated plan.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
One important takeaway is the value of iterative design and testing when working with AI. While AI can provide useful suggestions and help with brainstorming, it's crucial to critically evaluate those suggestions and verify their correctness through testing. This project reinforced the importance of maintaining a clear separation of concerns in system design, which made it easier to implement and test the scheduling logic independently from the user interface.

- Which Copilot features were most helpful for you?
The code generation feature was particularly helpful for quickly creating class stubs and implementing the scheduling logic. The debugging suggestions were also valuable when I encountered issues with the scheduling algorithm, as they provided insights into potential causes of bugs and offered ideas for how to fix them. Overall, the AI tools helped streamline the development process and allowed me to focus more on the design and logic rather than getting bogged down in syntax and implementation details.

- What I learned about being the lead architect:
Even though I don't have much experience right now, I learned that being the lead architect means making key decisions about the overall structure of the system and how different components will interact. It also involves being responsible for ensuring that the design is coherent and that the implementation aligns with the intended architecture. This role requires a balance of creativity in designing the system and critical thinking in evaluating AI suggestions and making informed decisions about which ones to accept or modify. With more experience, I hope to become more confident in making these architectural decisions and in guiding the development process effectively.