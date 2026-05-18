import pytest
from pawpal_system import Pet, Task

def test_task_completion():
    """
    Tests that calling mark_complete() on a Task changes its
    'completed' status to True.
    """
    # 1. Setup: Create a new task
    task = Task(name="Test Task", duration=10, priority=1)
    
    # Pre-condition check: Ensure the task starts as not completed
    assert not task.completed, "Task should be incomplete initially"
    
    # 2. Action: Mark the task as complete
    task.mark_complete()
    
    # 3. Verification: Check that the 'completed' attribute is now True
    assert task.completed, "Task should be marked as complete"

def test_add_task_to_pet():
    """
    Tests that adding a task to a Pet object correctly increases
    the number of tasks associated with that pet.
    """
    # 1. Setup: Create a new pet
    pet = Pet(name="Test Pet", species="Dog")
    
    # Pre-condition check: Ensure the pet starts with zero tasks
    assert len(pet.tasks) == 0, "Pet should have no tasks initially"
    
    # 2. Action: Add a new task to the pet
    new_task = Task(name="New Task", duration=15, priority=2)
    pet.add_task(new_task)
    
    # 3. Verification: Check that the pet's task count is now 1
    assert len(pet.tasks) == 1, "Pet should have one task after addition"
    assert pet.tasks[0] == new_task, "The correct task should be in the pet's task list"
