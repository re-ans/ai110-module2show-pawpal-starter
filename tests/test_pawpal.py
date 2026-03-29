"""
Unit tests for PawPal+ system components.
Tests core functionality including task completion, task addition, and scheduling.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def assert_raises(exception_type, callable_fn, *args, **kwargs):
    """Helper function to check if a callable raises an exception."""
    try:
        callable_fn(*args, **kwargs)
        raise AssertionError(f"Expected {exception_type.__name__} to be raised")
    except exception_type:
        pass


class TestTask:
    """Test cases for the Task class."""
    
    def test_task_completion_marks_complete(self):
        """Verify that calling mark_complete() changes task's completed status."""
        task = Task(
            name="Morning Walk",
            duration=45,
            priority=5,
            category="walk",
            pet_name="Buddy",
            earliest_time=6,
            latest_time=9
        )
        
        # Task should start as not completed
        assert task.completed == False
        
        # Mark as complete
        task.mark_complete()
        assert task.completed == True
        
        # Mark as incomplete again
        task.mark_incomplete()
        assert task.completed == False
    
    def test_task_priority_validation(self):
        """Verify that priority must be between 1 and 5."""
        def create_task_priority_6():
            Task(
                name="Test",
                duration=10,
                priority=6,  # Invalid: > 5
                category="feeding",
                pet_name="Buddy"
            )
        
        def create_task_priority_0():
            Task(
                name="Test",
                duration=10,
                priority=0,  # Invalid: < 1
                category="feeding",
                pet_name="Buddy"
            )
        
        assert_raises(ValueError, create_task_priority_6)
        assert_raises(ValueError, create_task_priority_0)
    
    def test_task_duration_validation(self):
        """Verify that duration must be positive."""
        def create_task_negative_duration():
            Task(
                name="Test",
                duration=-5,
                priority=3,
                category="feeding",
                pet_name="Buddy"
            )
        
        assert_raises(ValueError, create_task_negative_duration)
    
    def test_task_to_string(self):
        """Verify task string representation is formatted correctly."""
        task = Task(
            name="Walk",
            duration=30,
            priority=5,
            category="walk",
            pet_name="Buddy"
        )
        
        task_str = task.to_string()
        assert "Walk" in task_str
        assert "30m" in task_str
        assert "Buddy" in task_str
        assert "5★" in task_str


class TestPet:
    """Test cases for the Pet class."""
    
    def test_task_addition_increases_count(self):
        """Verify that adding a task to a pet increases that pet's task count."""
        pet = Pet(name="Buddy", species="Dog", age=3)
        
        # Initially, pet should have no tasks
        assert len(pet.tasks) == 0
        
        # Add a task
        task1 = Task(
            name="Walk",
            duration=30,
            priority=5,
            category="walk",
            pet_name="Buddy"
        )
        pet.add_task(task1)
        assert len(pet.tasks) == 1
        
        # Add another task
        task2 = Task(
            name="Feeding",
            duration=10,
            priority=4,
            category="feeding",
            pet_name="Buddy"
        )
        pet.add_task(task2)
        assert len(pet.tasks) == 2
        
        # Verify the tasks are the ones we added
        assert task1 in pet.tasks
        assert task2 in pet.tasks
    
    def test_pet_info_formatting(self):
        """Verify pet info returns properly formatted string."""
        pet = Pet(
            name="Whiskers",
            species="Cat",
            age=5,
            special_needs=["indoor", "sensitive stomach"]
        )
        
        info = pet.get_info()
        assert "Whiskers" in info
        assert "Cat" in info
        assert "5" in info
        assert "indoor" in info
    
    def test_get_tasks_by_category(self):
        """Verify filtering tasks by category works correctly."""
        pet = Pet(name="Buddy", species="Dog", age=3)
        
        walk_task = Task("Walk", 30, 5, "walk", "Buddy")
        feed_task = Task("Feeding", 10, 4, "feeding", "Buddy")
        play_task = Task("Playtime", 20, 4, "enrichment", "Buddy")
        
        pet.add_task(walk_task)
        pet.add_task(feed_task)
        pet.add_task(play_task)
        
        walk_tasks = pet.get_tasks_by_category("walk")
        assert len(walk_tasks) == 1
        assert walk_task in walk_tasks
        
        enrichment_tasks = pet.get_tasks_by_category("enrichment")
        assert len(enrichment_tasks) == 1
        assert play_task in enrichment_tasks


class TestOwner:
    """Test cases for the Owner class."""
    
    def test_owner_available_time_conversion(self):
        """Verify owner's available time is correctly converted from hours to minutes."""
        owner = Owner(name="Alice", available_hours_per_day=3.5)
        
        # 3.5 hours = 210 minutes
        assert owner.get_available_time() == 210.0
    
    def test_owner_add_pets(self):
        """Verify adding pets to owner works correctly."""
        owner = Owner(name="Alice", available_hours_per_day=4)
        
        assert len(owner.pets) == 0
        
        pet1 = Pet("Buddy", "Dog", 3)
        pet2 = Pet("Whiskers", "Cat", 5)
        
        owner.add_pet(pet1)
        assert len(owner.pets) == 1
        
        owner.add_pet(pet2)
        assert len(owner.pets) == 2
    
    def test_owner_get_all_tasks(self):
        """Verify retrieving all tasks from all pets."""
        owner = Owner(name="Alice", available_hours_per_day=4)
        
        pet1 = Pet("Buddy", "Dog", 3)
        task1 = Task("Walk", 30, 5, "walk", "Buddy")
        task2 = Task("Feed", 10, 4, "feeding", "Buddy")
        pet1.add_task(task1)
        pet1.add_task(task2)
        
        pet2 = Pet("Whiskers", "Cat", 5)
        task3 = Task("Feed", 5, 5, "feeding", "Whiskers")
        pet2.add_task(task3)
        
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        all_tasks = owner.get_all_tasks()
        assert len(all_tasks) == 3
        assert task1 in all_tasks
        assert task2 in all_tasks
        assert task3 in all_tasks
    
    def test_owner_update_preferences(self):
        """Verify updating owner preferences."""
        owner = Owner(name="Alice", available_hours_per_day=4)
        
        assert len(owner.preferences) == 0
        
        owner.update_preferences({"schedule": "morning"})
        assert owner.preferences["schedule"] == "morning"
        
        owner.update_preferences({"priority": "walks_first"})
        assert owner.preferences["schedule"] == "morning"
        assert owner.preferences["priority"] == "walks_first"


class TestScheduler:
    """Test cases for the Scheduler class."""
    
    def test_scheduler_validates_schedule(self):
        """Verify schedule validation checks total duration against available time."""
        owner = Owner(name="Alice", available_hours_per_day=2)  # 120 minutes
        pet = Pet("Buddy", "Dog", 3)
        
        task1 = Task("Walk", 60, 5, "walk", "Buddy")
        task2 = Task("Feed", 30, 4, "feeding", "Buddy")
        
        pet.add_task(task1)
        pet.add_task(task2)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner=owner)
        
        # Plan with 90 minutes should validate (< 120)
        plan = [task1, task2]
        assert scheduler.validate_schedule(plan) == True
        
        # Plan with 120+ minutes should not validate
        task3 = Task("Play", 40, 3, "enrichment", "Buddy")
        plan_overload = [task1, task2, task3]
        assert scheduler.validate_schedule(plan_overload) == False
    
    def test_scheduler_calculate_feasibility(self):
        """Verify feasibility calculation."""
        owner = Owner(name="Alice", available_hours_per_day=2)  # 120 minutes
        pet = Pet("Buddy", "Dog", 3)
        
        task1 = Task("Walk", 60, 5, "walk", "Buddy")
        task2 = Task("Feed", 30, 4, "feeding", "Buddy")
        
        pet.add_task(task1)
        pet.add_task(task2)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner=owner)
        
        # 90 minutes of tasks, 120 available = 0.75 feasibility
        # But it's capped at 1.0 since 120 >= 90
        feasibility = scheduler.calculate_feasibility()
        assert feasibility == 1.0  # Feasible because we can fit all tasks
    
    def test_scheduler_excludes_completed_tasks(self):
        """Verify that completed tasks are excluded from daily plan."""
        owner = Owner(name="Alice", available_hours_per_day=4)
        pet = Pet("Buddy", "Dog", 3)
        
        task1 = Task("Walk", 30, 5, "walk", "Buddy")
        task2 = Task("Feed", 10, 4, "feeding", "Buddy")
        
        pet.add_task(task1)
        pet.add_task(task2)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner=owner)
        
        # Initially, both tasks should be in plan
        plan = scheduler.generate_daily_plan()
        assert len(plan) == 2
        
        # Mark one as complete
        task1.mark_complete()
        plan = scheduler.generate_daily_plan()
        assert len(plan) == 1
        assert task1 not in plan
        assert task2 in plan


class TestSchedulerAlgorithms:
    """Test cases for Scheduler algorithmic methods (sorting, filtering, conflicts, recurrence)."""
    
    # ========================================================================
    # SORTING TESTS
    # ========================================================================
    
    def test_sort_by_time_chronological_order(self):
        """Verify tasks are sorted chronologically by earliest_time."""
        owner = Owner(name="Alice", available_hours_per_day=8)
        pet = Pet("Buddy", "Dog", 3)
        
        # Add tasks out of order
        task_14 = Task("Afternoon Walk", 30, 4, "walk", "Buddy", earliest_time=14, latest_time=18)
        task_6 = Task("Morning Walk", 45, 5, "walk", "Buddy", earliest_time=6, latest_time=9)
        task_19 = Task("Evening Walk", 30, 5, "walk", "Buddy", earliest_time=19, latest_time=21)
        task_12 = Task("Lunch Time", 15, 3, "feeding", "Buddy", earliest_time=12, latest_time=14)
        
        pet.add_task(task_14)
        pet.add_task(task_6)
        pet.add_task(task_19)
        pet.add_task(task_12)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner=owner)
        tasks_to_sort = [task_14, task_6, task_19, task_12]
        
        sorted_tasks = scheduler.sort_by_time(tasks_to_sort)
        
        # Verify chronological order
        assert sorted_tasks[0].earliest_time == 6
        assert sorted_tasks[1].earliest_time == 12
        assert sorted_tasks[2].earliest_time == 14
        assert sorted_tasks[3].earliest_time == 19
        
        # Verify they're the same tasks, just reordered
        assert sorted_tasks[0] == task_6
        assert sorted_tasks[1] == task_12
        assert sorted_tasks[2] == task_14
        assert sorted_tasks[3] == task_19
    
    def test_sort_by_time_tiebreaker_priority(self):
        """Verify that within same time window, higher priority tasks come first."""
        owner = Owner(name="Alice", available_hours_per_day=8)
        pet = Pet("Buddy", "Dog", 3)
        
        # Two tasks with same earliest_time but different priorities
        task_low_priority = Task("Grooming", 30, 2, "grooming", "Buddy", earliest_time=9, latest_time=12)
        task_high_priority = Task("Feeding", 10, 5, "feeding", "Buddy", earliest_time=9, latest_time=12)
        
        owner.add_pet(pet)
        scheduler = Scheduler(owner=owner)
        
        # Add in low-first order
        tasks = [task_low_priority, task_high_priority]
        sorted_tasks = scheduler.sort_by_time(tasks)
        
        # High priority should come first (tiebreaker)
        assert sorted_tasks[0].priority == 5
        assert sorted_tasks[1].priority == 2
    
    # ========================================================================
    # FILTERING TESTS
    # ========================================================================
    
    def test_filter_by_pet_returns_correct_tasks(self):
        """Verify filter_by_pet returns only tasks for that pet."""
        owner = Owner(name="Alice", available_hours_per_day=8)
        buddy = Pet("Buddy", "Dog", 3)
        whiskers = Pet("Whiskers", "Cat", 5)
        
        buddy_walk = Task("Walk", 30, 5, "walk", "Buddy")
        buddy_feed = Task("Feed", 10, 4, "feeding", "Buddy")
        whiskers_feed = Task("Feed", 5, 5, "feeding", "Whiskers")
        
        buddy.add_task(buddy_walk)
        buddy.add_task(buddy_feed)
        whiskers.add_task(whiskers_feed)
        
        owner.add_pet(buddy)
        owner.add_pet(whiskers)
        
        scheduler = Scheduler(owner=owner)
        
        buddy_tasks = scheduler.filter_by_pet("Buddy")
        whiskers_tasks = scheduler.filter_by_pet("Whiskers")
        
        assert len(buddy_tasks) == 2
        assert len(whiskers_tasks) == 1
        assert buddy_walk in buddy_tasks
        assert buddy_feed in buddy_tasks
        assert whiskers_feed in whiskers_tasks
        assert whiskers_feed not in buddy_tasks
    
    def test_filter_by_status_separates_completed(self):
        """Verify filter_by_status correctly separates pending and completed tasks."""
        owner = Owner(name="Alice", available_hours_per_day=8)
        pet = Pet("Buddy", "Dog", 3)
        
        task1 = Task("Walk", 30, 5, "walk", "Buddy")
        task2 = Task("Feed", 10, 4, "feeding", "Buddy")
        task3 = Task("Play", 20, 3, "enrichment", "Buddy")
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner=owner)
        
        # Initially all pending
        pending = scheduler.filter_by_status(completed=False)
        completed = scheduler.filter_by_status(completed=True)
        
        assert len(pending) == 3
        assert len(completed) == 0
        
        # Mark two as complete
        task1.mark_complete()
        task2.mark_complete()
        
        pending = scheduler.filter_by_status(completed=False)
        completed = scheduler.filter_by_status(completed=True)
        
        assert len(pending) == 1
        assert len(completed) == 2
        assert task3 in pending
        assert task1 in completed
        assert task2 in completed
    
    def test_filter_by_category_groups_tasks(self):
        """Verify filter_by_category returns only tasks in that category."""
        owner = Owner(name="Alice", available_hours_per_day=8)
        pet = Pet("Buddy", "Dog", 3)
        
        walk1 = Task("Morning Walk", 30, 5, "walk", "Buddy")
        walk2 = Task("Evening Walk", 30, 5, "walk", "Buddy")
        feed = Task("Feeding", 10, 4, "feeding", "Buddy")
        play = Task("Playtime", 20, 3, "enrichment", "Buddy")
        
        pet.add_task(walk1)
        pet.add_task(walk2)
        pet.add_task(feed)
        pet.add_task(play)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner=owner)
        
        walks = scheduler.filter_by_category("walk")
        feedings = scheduler.filter_by_category("feeding")
        enrichment = scheduler.filter_by_category("enrichment")
        
        assert len(walks) == 2
        assert len(feedings) == 1
        assert len(enrichment) == 1
        assert walk1 in walks
        assert walk2 in walks
        assert feed in feedings
        assert play in enrichment
    
    # ========================================================================
    # CONFLICT DETECTION TESTS
    # ========================================================================
    
    def test_detect_conflicts_finds_same_pet_overlap(self):
        """Verify conflict detection finds tasks for the same pet with overlapping times."""
        owner = Owner(name="Alice", available_hours_per_day=8)
        pet = Pet("Buddy", "Dog", 3)
        
        # Two tasks that overlap (6-9 and 8-12 overlap)
        task1 = Task("Morning Walk", 45, 5, "walk", "Buddy", earliest_time=6, latest_time=9)
        task2 = Task("Training", 30, 4, "enrichment", "Buddy", earliest_time=8, latest_time=12)
        
        pet.add_task(task1)
        pet.add_task(task2)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner=owner)
        conflicts = scheduler.detect_conflicts([task1, task2])
        
        assert len(conflicts) == 1
        conflict_task1, conflict_task2, msg = conflicts[0]
        assert "SAME PET" in msg
        assert "Morning Walk" in msg
        assert "Training" in msg
    
    def test_detect_conflicts_no_false_positives_non_overlapping(self):
        """Verify no conflict detected for non-overlapping tasks."""
        owner = Owner(name="Alice", available_hours_per_day=8)
        pet = Pet("Buddy", "Dog", 3)
        
        # Non-overlapping: 6-9 and 10-12
        task1 = Task("Morning Walk", 30, 5, "walk", "Buddy", earliest_time=6, latest_time=9)
        task2 = Task("Lunch Feed", 10, 4, "feeding", "Buddy", earliest_time=10, latest_time=12)
        
        pet.add_task(task1)
        pet.add_task(task2)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner=owner)
        conflicts = scheduler.detect_conflicts([task1, task2])
        
        assert len(conflicts) == 0
    
    def test_detect_conflicts_different_pets_informational(self):
        """Verify conflicts for different pets are marked as TIMING CONFLICT (not SAME PET)."""
        owner = Owner(name="Alice", available_hours_per_day=8)
        buddy = Pet("Buddy", "Dog", 3)
        whiskers = Pet("Whiskers", "Cat", 5)
        
        buddy_walk = Task("Walk", 30, 5, "walk", "Buddy", earliest_time=6, latest_time=9)
        whiskers_feed = Task("Feed", 10, 4, "feeding", "Whiskers", earliest_time=8, latest_time=12)
        
        buddy.add_task(buddy_walk)
        whiskers.add_task(whiskers_feed)
        owner.add_pet(buddy)
        owner.add_pet(whiskers)
        
        scheduler = Scheduler(owner=owner)
        conflicts = scheduler.detect_conflicts([buddy_walk, whiskers_feed])
        
        assert len(conflicts) == 1
        conflict_task1, conflict_task2, msg = conflicts[0]
        assert "TIMING CONFLICT" in msg  # Different pets, so TIMING CONFLICT not SAME PET
        assert "Buddy" in msg
        assert "Whiskers" in msg
    
    # ========================================================================
    # RECURRING TASK TESTS
    # ========================================================================
    
    def test_create_recurring_task_copies_daily_task(self):
        """Verify create_recurring_task creates a new incomplete copy of a daily task."""
        owner = Owner(name="Alice", available_hours_per_day=8)
        pet = Pet("Buddy", "Dog", 3)
        
        daily_walk = Task(
            name="Daily Morning Walk",
            duration=45,
            priority=5,
            category="walk",
            pet_name="Buddy",
            frequency="daily",
            earliest_time=6,
            latest_time=9,
            completed=False
        )
        
        pet.add_task(daily_walk)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner=owner)
        
        # Create recurring instance
        next_walk = scheduler.create_recurring_task(daily_walk)
        
        assert next_walk is not None
        assert next_walk.name == daily_walk.name
        assert next_walk.duration == daily_walk.duration
        assert next_walk.priority == daily_walk.priority
        assert next_walk.completed == False
        assert next_walk.category == daily_walk.category
        assert next_walk.pet_name == daily_walk.pet_name
    
    def test_create_recurring_task_returns_none_for_non_recurring(self):
        """Verify create_recurring_task returns None for one-time tasks."""
        owner = Owner(name="Alice", available_hours_per_day=8)
        pet = Pet("Buddy", "Dog", 3)
        
        one_time_task = Task(
            name="One-time grooming",
            duration=60,
            priority=3,
            category="grooming",
            pet_name="Buddy",
            frequency="once"  # Non-recurring
        )
        
        pet.add_task(one_time_task)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner=owner)
        next_task = scheduler.create_recurring_task(one_time_task)
        
        assert next_task is None
    
    def test_mark_task_complete_with_recurrence_auto_creates_next(self):
        """Verify mark_task_complete_with_recurrence marks task done and creates next instance."""
        owner = Owner(name="Alice", available_hours_per_day=8)
        pet = Pet("Buddy", "Dog", 3)
        
        daily_walk = Task(
            name="Daily Walk",
            duration=45,
            priority=5,
            category="walk",
            pet_name="Buddy",
            frequency="daily",
            earliest_time=6,
            latest_time=9
        )
        
        pet.add_task(daily_walk)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner=owner)
        
        # Initially 1 task
        assert len(pet.tasks) == 1
        
        # Mark complete with recurrence
        scheduler.mark_task_complete_with_recurrence(daily_walk, pet)
        
        # Now 2 tasks: original marked complete + new copy
        assert len(pet.tasks) == 2
        assert pet.tasks[0].completed == True  # Original is done
        assert pet.tasks[1].completed == False  # New copy is pending
        assert pet.tasks[1].name == daily_walk.name
    
    # ========================================================================
    # EDGE CASES
    # ========================================================================
    
    def test_empty_pet_has_no_tasks(self):
        """Verify a pet with no tasks returns empty list from scheduler."""
        owner = Owner(name="Alice", available_hours_per_day=8)
        pet = Pet("Buddy", "Dog", 3)  # No tasks added
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner=owner)
        
        plan = scheduler.generate_daily_plan()
        assert len(plan) == 0
    
    def test_all_tasks_completed_returns_empty_plan(self):
        """Verify plan is empty when all tasks are marked complete."""
        owner = Owner(name="Alice", available_hours_per_day=8)
        pet = Pet("Buddy", "Dog", 3)
        
        task1 = Task("Walk", 30, 5, "walk", "Buddy")
        task2 = Task("Feed", 10, 4, "feeding", "Buddy")
        
        pet.add_task(task1)
        pet.add_task(task2)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner=owner)
        
        # Mark all complete
        task1.mark_complete()
        task2.mark_complete()
        
        plan = scheduler.generate_daily_plan()
        assert len(plan) == 0
    
    def test_single_task_schedule(self):
        """Verify scheduling works correctly with just one task."""
        owner = Owner(name="Alice", available_hours_per_day=1)  # Only 60 minutes
        pet = Pet("Buddy", "Dog", 3)
        
        single_task = Task("Quick Walk", 45, 5, "walk", "Buddy")
        
        pet.add_task(single_task)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner=owner)
        
        plan = scheduler.generate_daily_plan()
        assert len(plan) == 1
        assert plan[0] == single_task
        assert scheduler.validate_schedule(plan) == True


if __name__ == "__main__":
    import sys
    sys.path.insert(0, '/Users/anngo/Code/codepath/ai110-module2show-pawpal-starter')
    
    # Run all tests
    test_classes = [TestTask, TestPet, TestOwner, TestScheduler]
    total_passed = 0
    total_failed = 0
    
    for test_class in test_classes:
        instance = test_class()
        test_methods = [m for m in dir(instance) if m.startswith('test_')]
        
        for method_name in test_methods:
            try:
                method = getattr(instance, method_name)
                method()
                print(f"✓ {test_class.__name__}.{method_name}")
                total_passed += 1
            except Exception as e:
                print(f"✗ {test_class.__name__}.{method_name}: {e}")
                total_failed += 1
    
    print(f"\nResults: {total_passed} passed, {total_failed} failed")

