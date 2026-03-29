"""
PawPal+ Advanced Demo - Showcasing Algorithms
Demonstrates: sorting, filtering, recurring tasks, and conflict detection.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'=' * 70}")
    print(f"{title}")
    print('=' * 70)


def print_subsection(title):
    """Print a formatted subsection header."""
    print(f"\n{'-' * 70}")
    print(f"{title}")
    print('-' * 70)


def main():
    """Run the advanced PawPal+ demo."""
    
    print_section("PawPal+ Advanced Algorithms Demo")
    
    # ========================================================================
    # SETUP: Create Owner, Pets, and Tasks (with some out of order)
    # ========================================================================
    
    owner = Owner(name="Alice", available_hours_per_day=5.0)
    print(f"Owner: {owner.name} ({owner.get_available_time()} minutes/day)")
    
    # Create pets
    buddy = Pet(name="Buddy", species="Golden Retriever", age=3)
    whiskers = Pet(name="Whiskers", species="Cat", age=5)
    owner.add_pet(buddy)
    owner.add_pet(whiskers)
    print(f"Pets: {', '.join([p.name for p in owner.pets])}")
    
    # Create tasks OUT OF ORDER (to demo sorting)
    print_subsection("Adding Tasks (Out of Order)")
    
    tasks_to_add = [
        Task("Afternoon Walk", 40, 4, "walk", "Buddy", earliest_time=14, latest_time=18),
        Task("Morning Walk", 45, 5, "walk", "Buddy", earliest_time=6, latest_time=9),
        Task("Breakfast", 10, 4, "feeding", "Buddy", earliest_time=7, latest_time=10),
        Task("Cat Feeding", 5, 5, "feeding", "Whiskers", earliest_time=8, latest_time=12),
        Task("Playtime", 30, 3, "enrichment", "Buddy", earliest_time=16, latest_time=20),
        Task("Litter Box", 5, 4, "grooming", "Whiskers", earliest_time=9, latest_time=21),
        Task("Evening Walk", 30, 5, "walk", "Buddy", earliest_time=18, latest_time=21),
    ]
    
    for task in tasks_to_add:
        if task.pet_name == "Buddy":
            buddy.add_task(task)
        else:
            whiskers.add_task(task)
        print(f"  + {task.to_string()}")
    
    scheduler = Scheduler(owner=owner)
    
    # ========================================================================
    # DEMO 1: FILTERING BY PET
    # ========================================================================
    
    print_section("DEMO 1: Filtering by Pet")
    
    buddy_tasks = scheduler.filter_by_pet("Buddy")
    print(f"Tasks for Buddy ({len(buddy_tasks)} tasks):")
    for task in buddy_tasks:
        print(f"  {task.to_string()}")
    
    whiskers_tasks = scheduler.filter_by_pet("Whiskers")
    print(f"\nTasks for Whiskers ({len(whiskers_tasks)} tasks):")
    for task in whiskers_tasks:
        print(f"  {task.to_string()}")
    
    # ========================================================================
    # DEMO 2: FILTERING BY STATUS
    # ========================================================================
    
    print_section("DEMO 2: Filtering by Status")
    
    pending = scheduler.filter_by_status(completed=False)
    print(f"Pending Tasks ({len(pending)} tasks):")
    for task in pending:
        print(f"  {task.to_string()}")
    
    # Complete some tasks
    print("\nMarking some tasks as complete...")
    buddy_tasks[0].mark_complete()  # First task
    buddy_tasks[2].mark_complete()  # Third task
    print(f"  ✓ Marked '{buddy_tasks[0].name}' as complete")
    print(f"  ✓ Marked '{buddy_tasks[2].name}' as complete")
    
    completed = scheduler.filter_by_status(completed=True)
    pending = scheduler.filter_by_status(completed=False)
    print(f"\nAfter completion:")
    print(f"  Completed: {len(completed)} tasks")
    print(f"  Pending: {len(pending)} tasks")
    
    # ========================================================================
    # DEMO 3: SORTING BY TIME
    # ========================================================================
    
    print_section("DEMO 3: Sorting by Time")
    
    pending_tasks = scheduler.filter_by_status(completed=False)
    print(f"Pending tasks sorted by time window (earliest_time ascending):")
    sorted_by_time = scheduler.sort_by_time(pending_tasks)
    for task in sorted_by_time:
        time_window = f"{task.earliest_time:02d}:00 - {task.latest_time:02d}:00"
        print(f"  {time_window} | {task.to_string()}")
    
    # ========================================================================
    # DEMO 4: FILTERING BY CATEGORY
    # ========================================================================
    
    print_section("DEMO 4: Filtering by Category")
    
    walks = scheduler.filter_by_category("walk")
    print(f"All walk tasks ({len(walks)} tasks):")
    for task in walks:
        print(f"  {task.to_string()}")
    
    feeding = scheduler.filter_by_category("feeding")
    print(f"\nAll feeding tasks ({len(feeding)} tasks):")
    for task in feeding:
        print(f"  {task.to_string()}")
    
    # ========================================================================
    # DEMO 5: CONFLICT DETECTION
    # ========================================================================
    
    print_section("DEMO 5: Conflict Detection")
    
    # Add a conflicting task (same pet, overlapping time)
    print("Creating a schedule with intentional conflicts...")
    print("  Adding: 'Dinner' (Buddy, 19:00-20:00)")
    dinner = Task("Dinner", 20, 4, "feeding", "Buddy", earliest_time=19, latest_time=20)
    buddy.add_task(dinner)
    
    # Refresh scheduler
    scheduler = Scheduler(owner=owner)
    all_pending = scheduler.filter_by_status(completed=False)
    
    conflicts = scheduler.detect_conflicts(all_pending)
    
    if conflicts:
        print(f"\n⚠️  Found {len(conflicts)} conflict(s):")
        for task1, task2, message in conflicts:
            print(f"  • {message}")
    else:
        print("\n✓ No conflicts detected!")
    
    # ========================================================================
    # DEMO 6: RECURRING TASKS
    # ========================================================================
    
    print_section("DEMO 6: Recurring Tasks Automation")
    
    # Create a recurring task
    daily_walk = Task(
        "Daily Morning Walk",
        duration=45,
        priority=5,
        category="walk",
        pet_name="Buddy",
        frequency="daily",
        earliest_time=6,
        latest_time=9,
        completed=False
    )
    buddy.add_task(daily_walk)
    
    print(f"Created recurring task: {daily_walk.to_string()}")
    print(f"Task frequency: {daily_walk.frequency}")
    
    scheduler = Scheduler(owner=owner)
    print(f"Total pending tasks before completion: {len(scheduler.filter_by_status(False))}")
    
    # Mark as complete and auto-create next occurrence
    print(f"\nMarking '{daily_walk.name}' as complete (daily recurrence)...")
    scheduler.mark_task_complete_with_recurrence(daily_walk, buddy)
    
    # Refresh scheduler to see new task
    scheduler = Scheduler(owner=owner)
    print(f"Total pending tasks after completion: {len(scheduler.filter_by_status(False))}")
    
    pending = scheduler.filter_by_status(False)
    print("\nNew recurring instance created:")
    for task in pending:
        if task.name == "Daily Morning Walk" and not task.completed:
            print(f"  ✓ {task.to_string()}")
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    
    print_section("Summary: Algorithm Features Demonstrated")
    
    print("""
✓ FILTERING:
  - filter_by_pet(name) → Get all tasks for a specific pet
  - filter_by_status(completed) → Get pending or completed tasks
  - filter_by_category(cat) → Get tasks in a specific category

✓ SORTING:
  - sort_by_time(tasks) → Sort tasks by time window (6:00, 7:00, etc.)
  - Natural tiebreaker: higher priority tasks scheduled first in same window

✓ CONFLICT DETECTION:
  - detect_conflicts(plan) → Find overlapping time windows
  - Specifically flags same-pet conflicts as high-priority warnings
  - Lightweight: O(n²) comparison, returns descriptive messages

✓ RECURRING TASKS:
  - create_recurring_task(task) → Create next occurrence
  - mark_task_complete_with_recurrence() → Auto-create next instance
  - Supports: daily, weekly, twice_daily frequencies

✓ ALGORITHM DESIGN CHOICES:
  - Sorting: O(n log n) efficient for daily use
  - Filtering: O(n) list comprehensions for clarity over performance
  - Conflict detection: Exact time-window overlap (not duration overlap)
    (Tradeoff: simpler to understand but may miss partial overlaps)
  - Recurring: Simple copy pattern (not date-aware, adds to same day's tasks)
    (Tradeoff: UI will need to distribute across multiple days)
    """)
    
    print('=' * 70)


if __name__ == "__main__":
    main()
