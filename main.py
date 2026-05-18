from pawpal_system import Owner, Pet, Task, Scheduler

# --- Example Usage ---
if __name__ == "__main__":
    # 1. Create owner and pets
    owner = Owner(name="Alex", available_time=90)
    buddy = Pet(name="Buddy", species="Dog")
    whiskers = Pet(name="Whiskers", species="Cat")

    # 2. Add tasks, including two with identical priority and duration to test conflicts
    whiskers.add_task(Task(name="Laser pointer fun", duration=15, priority=3))
    buddy.add_task(Task(name="Play fetch", duration=25, priority=2))
    whiskers.add_task(Task(name="Feed Whiskers breakfast", duration=10, priority=1))
    buddy.add_task(Task(name="Morning walk", duration=30, priority=1))
    whiskers.add_task(Task(name="Clean litter box", duration=5, priority=1))
    
    # -- Add two tasks with the same priority and duration to test conflict detection --
    buddy.add_task(Task(name="Feed Buddy breakfast", duration=10, priority=1))
    whiskers.add_task(Task(name="Brush Whiskers", duration=10, priority=1)) # New conflicting task

    # Add a completed task to ensure it's ignored by the scheduler
    completed_task = Task(name="Give monthly flea medicine", duration=5, priority=1, completed=True)
    buddy.add_task(completed_task)

    # 3. Add pets to the owner
    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    print(f"Owner: {owner.name} has {owner.get_availability()} minutes available.")
    print(f"Total tasks to consider: {len(owner.get_all_tasks())}")
    print("-" * 20)

    # 4. Initialize the scheduler and generate a plan
    scheduler = Scheduler()
    scheduler.generate_plan(owner)

    # --- Simulate a scheduling conflict for testing purposes ---
    # Manually set two tasks to have the same start time to test the warning.
    # In a more advanced scheduler, this might happen due to fixed-time appointments.
    if len(scheduler.scheduled_tasks) > 3:
        print("--- (Simulating a conflict for testing) ---")
        # Find two tasks of the same duration to make the conflict realistic
        task1_to_conflict = scheduler.scheduled_tasks[1] # Feed Whiskers
        task2_to_conflict = scheduler.scheduled_tasks[2] # Feed Buddy
        
        # Set the second task's start time to be the same as the first one
        task2_to_conflict.start_time = task1_to_conflict.start_time
        print(f"Manually setting '{task2_to_conflict.name}' to start at the same time as '{task1_to_conflict.name}'.")
        print("-" * 20)


    # 5. Display the generated plan (which will now show a conflict warning)
    scheduler.display_plan()

    # --- Test a scenario with not enough time ---
    print("\n" + "-" * 20)
    print("Testing with only 45 minutes available...")
    owner.set_availability(45)
    scheduler.generate_plan(owner)
    scheduler.display_plan()

