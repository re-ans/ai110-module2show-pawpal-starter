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

