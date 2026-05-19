import pytest
from pawpal_system import Pet, Task, Owner, Scheduler
from datetime import timedelta

# def test_task_completion():
#     """
#     Tests that calling mark_complete() on a Task changes its
#     'completed' status to True.
#     """
#     # 1. Setup: Create a new task
#     task = Task(name="Test Task", duration=10, priority=1)
    
#     # Pre-condition check: Ensure the task starts as not completed
#     assert not task.completed, "Task should be incomplete initially"
    
#     # 2. Action: Mark the task as complete
#     task.mark_complete()
    
#     # 3. Verification: Check that the 'completed' attribute is now True
#     assert task.completed, "Task should be marked as complete"

# def test_add_task_to_pet():
#     """
#     Tests that adding a task to a Pet object correctly increases
#     the number of tasks associated with that pet.
#     """
#     # 1. Setup: Create a new pet
#     pet = Pet(name="Test Pet", species="Dog")
    
#     # Pre-condition check: Ensure the pet starts with zero tasks
#     assert len(pet.tasks) == 0, "Pet should have no tasks initially"
    
#     # 2. Action: Add a new task to the pet
#     new_task = Task(name="New Task", duration=15, priority=2)
#     pet.add_task(new_task)
    
#     # 3. Verification: Check that the pet's task count is now 1
#     assert len(pet.tasks) == 1, "Pet should have one task after addition"
#     assert pet.tasks[0] == new_task, "The correct task should be in the pet's task list"

def test_sorting_correctness():
    """
    Tests that the scheduler returns tasks in chronological order based on start time.
    """
    # 1. Setup: Create an owner and a scheduler
    owner = Owner(name="Test Owner", available_time=120)
    scheduler = Scheduler()

    # 2. Action: Add tasks with different priorities and durations
    task1 = Task(name="Low Prio, Short Dur", duration=10, priority=3)
    task2 = Task(name="High Prio, Long Dur", duration=30, priority=1)
    task3 = Task(name="Mid Prio, Mid Dur", duration=20, priority=2)
    
    owner.add_pet(Pet(name="Dog", species="Canine", tasks=[task1, task2, task3]))

    # Generate the plan, which also sorts and schedules the tasks
    plan = scheduler.generate_plan(owner)

    # 3. Verification: Check that tasks are sorted by start_time
    # The plan should be [task2, task3, task1] based on priority
    # task2: start_time=0, duration=30
    # task3: start_time=30, duration=20
    # task1: start_time=50, duration=10
    assert plan.scheduled_tasks[0].name == "High Prio, Long Dur"
    assert plan.scheduled_tasks[1].name == "Mid Prio, Mid Dur"
    assert plan.scheduled_tasks[2].name == "Low Prio, Short Dur"
    
    start_times = [task.start_time for task in plan.scheduled_tasks]
    assert start_times == sorted(start_times), "Tasks should be sorted by start_time"

def test_recurrence_logic():
    """
    Tests that completing a daily task creates a new task for the next day.
    """
    # 1. Setup: Create a pet and a daily task
    pet = Pet(name="Buddy", species="Dog")
    original_task = Task(name="Daily Walk", duration=30, priority=1, frequency="daily")
    pet.add_task(original_task)
    
    # 2. Action: Mark the daily task as complete
    original_task.mark_complete(pet)
    
    # 3. Verification: Check for a new task on the following day
    assert len(pet.tasks) == 2, "A new task should have been added"
    
    new_task = pet.tasks[1]
    assert new_task.name == original_task.name, "New task should have the same name"
    assert not new_task.completed, "New task should be incomplete"
    expected_due_date = original_task.due_date + timedelta(days=1)
    assert new_task.due_date == expected_due_date, "New task due date should be the next day"

def test_conflict_detection():
    """
    Tests that the scheduler can detect tasks scheduled at the same time.
    """
    # 1. Setup: Create a scheduler and two tasks with the same start time
    scheduler = Scheduler()
    task1 = Task(name="Task A", duration=30, priority=1)
    task2 = Task(name="Task B", duration=45, priority=2)

    # Manually set the same start time to create a conflict
    task1.start_time = 0
    task2.start_time = 0
    
    scheduler.scheduled_tasks.extend([task1, task2])

    # 2. Action: Detect conflicts
    conflicts = scheduler.detect_conflicts()
    
    # 3. Verification: Check that a conflict is detected
    assert len(conflicts) == 1, "Should detect one conflict"
    assert (task1, task2) in conflicts or (task2, task1) in conflicts, "The correct conflicting tasks should be identified"
