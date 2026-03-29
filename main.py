"""
PawPal+ Demo Script
Demonstrates the core functionality: creating pets, tasks, and generating a daily schedule.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    """Run the PawPal+ demo."""
    
    # Step 1: Create an Owner
    print("=" * 60)
    print("PawPal+ - Daily Pet Care Schedule Generator")
    print("=" * 60)
    
    owner = Owner(name="Alice", available_hours_per_day=4.0)
    print(f"\nOwner: {owner.name}")
    print(f"Available time: {owner.get_available_time()} minutes/day")
    
    # Step 2: Create Pets
    print("\n" + "-" * 60)
    print("PETS")
    print("-" * 60)
    
    buddy = Pet(name="Buddy", species="Golden Retriever", age=3, 
                special_needs=["high energy", "needs regular walks"])
    owner.add_pet(buddy)
    
    whiskers = Pet(name="Whiskers", species="Cat", age=5,
                   special_needs=["indoor only", "sensitive stomach"])
    owner.add_pet(whiskers)
    
    print(buddy.get_info())
    print(whiskers.get_info())
    
    # Step 3: Add Tasks to Pets
    print("\n" + "-" * 60)
    print("TASKS")
    print("-" * 60)
    
    # Buddy's tasks (high priority for active dog)
    buddy_walk = Task(
        name="Morning Walk",
        duration=45,
        priority=5,
        category="walk",
        pet_name="Buddy",
        frequency="daily",
        earliest_time=6,
        latest_time=9
    )
    buddy.add_task(buddy_walk)
    
    buddy_feeding = Task(
        name="Breakfast",
        duration=10,
        priority=4,
        category="feeding",
        pet_name="Buddy",
        frequency="daily",
        earliest_time=7,
        latest_time=10
    )
    buddy.add_task(buddy_feeding)
    
    buddy_play = Task(
        name="Playtime",
        duration=30,
        priority=4,
        category="enrichment",
        pet_name="Buddy",
        frequency="daily",
        earliest_time=14,
        latest_time=18
    )
    buddy.add_task(buddy_play)
    
    # Whiskers' tasks (cat, lower priority but still important)
    whiskers_feeding = Task(
        name="Breakfast",
        duration=5,
        priority=5,
        category="feeding",
        pet_name="Whiskers",
        frequency="daily",
        earliest_time=7,
        latest_time=10
    )
    whiskers.add_task(whiskers_feeding)
    
    whiskers_litter = Task(
        name="Litter Box Clean",
        duration=5,
        priority=4,
        category="grooming",
        pet_name="Whiskers",
        frequency="daily",
        earliest_time=8,
        latest_time=20
    )
    whiskers.add_task(whiskers_litter)
    
    # Print all tasks
    all_tasks = owner.get_all_tasks()
    for task in all_tasks:
        print(task.to_string())
    
    # Step 4: Generate Daily Schedule
    print("\n" + "-" * 60)
    print("TODAY'S SCHEDULE (Optimized by Priority)")
    print("-" * 60)
    
    scheduler = Scheduler(owner=owner)
    daily_plan = scheduler.generate_daily_plan()
    
    print(f"\nScheduling {len(daily_plan)} tasks")
    print(f"Owner's available time: {owner.get_available_time()} minutes")
    
    total_duration = 0
    for i, task in enumerate(daily_plan, 1):
        total_duration += task.duration
        print(f"{i}. {task.to_string()}")
    
    print(f"\nTotal time needed: {total_duration} minutes")
    print(f"Feasibility: {scheduler.calculate_feasibility() * 100:.1f}%")
    print(f"Schedule valid: {scheduler.validate_schedule(daily_plan)}")
    
    # Step 5: Mark a task as complete and show updated schedule
    print("\n" + "-" * 60)
    print("Simulating task completion...")
    print("-" * 60)
    
    buddy_walk.mark_complete()
    print(f"\nMarked '{buddy_walk.name}' as complete!")
    
    print("\nUpdated Schedule:")
    updated_plan = scheduler.generate_daily_plan()
    total_duration = 0
    for i, task in enumerate(updated_plan, 1):
        total_duration += task.duration
        print(f"{i}. {task.to_string()}")
    
    print(f"\nTotal time needed: {total_duration} minutes")
    print(f"Feasibility: {scheduler.calculate_feasibility() * 100:.1f}%")
    print("=" * 60)


if __name__ == "__main__":
    main()
