from pawpal_system import Owner, Pet, Task, Scheduler

# --- Example Usage ---
if __name__ == "__main__":
    # 1. Create owner and pets
    owner = Owner(name="Alex", available_time=90)
    buddy = Pet(name="Buddy", species="Dog")
    whiskers = Pet(name="Whiskers", species="Cat")

    # 2. Add tasks directly to each pet
    buddy.add_task(Task(name="Morning walk", duration=30, priority=1))
    buddy.add_task(Task(name="Play fetch", duration=25, priority=2))
    buddy.add_task(Task(name="Feed Buddy breakfast", duration=10, priority=1))
    
    whiskers.add_task(Task(name="Clean litter box", duration=5, priority=1))
    whiskers.add_task(Task(name="Feed Whiskers breakfast", duration=10, priority=1))
    whiskers.add_task(Task(name="Laser pointer fun", duration=15, priority=3))

    # Add a completed task to ensure it's ignored by the scheduler
    completed_task = Task(name="Give monthly flea medicine", duration=5, priority=1, completed=True)
    buddy.add_task(completed_task)

    # 3. Add pets to the owner
    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    print(f"Owner: {owner.name} has {owner.get_availability()} minutes available.")
    print(f"Total tasks to consider: {len(owner.get_all_tasks())}")
    print("-" * 20)

    # 4. Initialize the scheduler and generate a plan from the owner object
    scheduler = Scheduler()
    scheduler.generate_plan(owner)

    # 5. Display the generated plan
    scheduler.display_plan()

    # --- Test a scenario with not enough time ---
    print("\n" + "-" * 20)
    print("Testing with only 45 minutes available...")
    owner.set_availability(45)
    scheduler.generate_plan(owner)
    scheduler.display_plan()