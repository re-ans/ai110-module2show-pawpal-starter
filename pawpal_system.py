"""
PawPal+ System - Core logic layer with Owner, Pet, Task, and Scheduler classes.
Includes sorting, filtering, recurring tasks, and conflict detection algorithms.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta


@dataclass
class Owner:
    """Represents a pet owner with availability and preferences."""
    
    name: str
    available_hours_per_day: float
    preferences: Dict[str, str] = field(default_factory=dict)
    pets: List['Pet'] = field(default_factory=list)
    
    def get_available_time(self) -> float:
        """Return owner's available time in minutes (convert from hours)."""
        return self.available_hours_per_day * 60
    
    def update_preferences(self, pref: Dict[str, str]) -> None:
        """Update owner's preferences with new dictionary values."""
        self.preferences.update(pref)
    
    def add_pet(self, pet: 'Pet') -> None:
        """Add a pet to the owner's list."""
        self.pets.append(pet)
    
    def get_all_tasks(self) -> List['Task']:
        """Retrieve all tasks from all owned pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


@dataclass
class Pet:
    """Represents a pet that needs care."""
    
    name: str
    species: str
    age: int
    special_needs: List[str] = field(default_factory=list)
    tasks: List['Task'] = field(default_factory=list)
    
    def get_info(self) -> str:
        """Return a string representation of pet information."""
        needs_str = ", ".join(self.special_needs) if self.special_needs else "None"
        return f"{self.name} ({self.species}, age {self.age}) - Special needs: {needs_str}"
    
    def add_task(self, task: 'Task') -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)
    
    def get_tasks_by_category(self, category: str) -> List['Task']:
        """Retrieve all tasks of a specific category for this pet."""
        return [t for t in self.tasks if t.category == category]


@dataclass
class Task:
    """Represents a pet care task."""
    
    name: str
    duration: int  # in minutes
    priority: int  # 1-5, where 5 is highest priority
    category: str  # e.g., "walk", "feeding", "medication", "grooming", "enrichment"
    pet_name: str  # which pet needs this task
    frequency: str = "daily"  # e.g., "daily", "weekly", "twice_daily"
    earliest_time: int = 0  # earliest hour of day (0-23) task can be scheduled
    latest_time: int = 23  # latest hour of day (0-23) task can be scheduled
    completed: bool = False  # whether task is completed for today
    
    def __post_init__(self):
        """Validate task attributes after initialization."""
        if not 1 <= self.priority <= 5:
            raise ValueError("Priority must be between 1 and 5")
        if self.duration <= 0:
            raise ValueError("Duration must be positive")
        if not 0 <= self.earliest_time <= self.latest_time <= 23:
            raise ValueError("Time range must be valid (0-23)")
    
    def get_priority(self) -> int:
        """Get the priority level of this task (1-5)."""
        return self.priority
    
    def to_string(self) -> str:
        """Get a formatted string representation of this task."""
        status = "✓" if self.completed else "○"
        return f"{status} [{self.priority}★] {self.name} ({self.duration}m) - {self.pet_name}"
    
    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True
    
    def mark_incomplete(self) -> None:
        """Mark this task as not completed."""
        self.completed = False


@dataclass
class Scheduler:
    """
    Generates an optimized daily schedule for pet care tasks.
    Considers time constraints, task priorities, and owner preferences.
    """
    
    owner: Owner
    pets: List[Pet] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize scheduler with owner's pets and their tasks."""
        if not self.pets and self.owner:
            self.pets = self.owner.pets
        if not self.tasks and self.owner:
            self.tasks = self.owner.get_all_tasks()
    
    def generate_daily_plan(self) -> List[Task]:
        """
        Generate an optimized daily schedule of tasks ordered by priority and feasibility.
        Sorts tasks by priority (highest first) and ensures they fit within time windows.
        
        Returns:
            List of tasks ordered for the day.
        """
        # Filter tasks that haven't been completed and can run today
        available_tasks = [t for t in self.tasks if not t.completed]
        
        # Sort by priority (descending), then by earliest_time (ascending)
        sorted_tasks = sorted(available_tasks, 
                            key=lambda t: (-t.priority, t.earliest_time))
        
        return sorted_tasks
    
    def validate_schedule(self, plan: List[Task]) -> bool:
        """
        Check if a proposed schedule fits within owner's available time.
        
        Args:
            plan: List of scheduled tasks
            
        Returns:
            True if schedule is feasible, False otherwise.
        """
        total_duration = sum(task.duration for task in plan)
        available_minutes = self.owner.get_available_time()
        return total_duration <= available_minutes
    
    def calculate_feasibility(self) -> float:
        """
        Calculate how feasible it is to complete all tasks given time constraints.
        
        Returns:
            Feasibility score (0.0 to 1.0, where 1.0 is fully feasible).
        """
        available_minutes = self.owner.get_available_time()
        total_duration = sum(task.duration for task in self.tasks if not task.completed)
        
        if total_duration == 0:
            return 1.0
        
        feasibility = available_minutes / total_duration
        return min(feasibility, 1.0)  # Cap at 1.0
    
    # ========================================================================
    # STEP 2: SORTING AND FILTERING ALGORITHMS
    # ========================================================================
    
    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """
        Sort tasks by their time window (earliest_time ascending).
        Useful for time-aware scheduling where tasks should happen in chronological order.
        
        Args:
            tasks: List of tasks to sort
            
        Returns:
            New list sorted by earliest_time (then by priority descending as tiebreaker)
        """
        return sorted(tasks, key=lambda t: (t.earliest_time, -t.priority))
    
    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """
        Get all tasks for a specific pet.
        
        Args:
            pet_name: Name of the pet to filter by
            
        Returns:
            List of tasks belonging to that pet
        """
        return [t for t in self.tasks if t.pet_name == pet_name]
    
    def filter_by_status(self, completed: bool = False) -> List[Task]:
        """
        Get all tasks with a specific completion status.
        
        Args:
            completed: If True, return completed tasks; if False, return pending tasks
            
        Returns:
            List of tasks matching the status
        """
        return [t for t in self.tasks if t.completed == completed]
    
    def filter_by_category(self, category: str) -> List[Task]:
        """
        Get all tasks in a specific category.
        
        Args:
            category: Category to filter by (e.g., "walk", "feeding", "medication")
            
        Returns:
            List of tasks in that category
        """
        return [t for t in self.tasks if t.category == category]
    
    # ========================================================================
    # STEP 4: CONFLICT DETECTION ALGORITHM
    # ========================================================================
    
    def detect_conflicts(self, plan: Optional[List[Task]] = None) -> List[Tuple[Task, Task, str]]:
        """
        Detect tasks scheduled at the same time for the same or different pets.
        Returns a list of conflicts with explanation.
        
        Algorithm: Check if any two tasks overlap in their time windows.
        Overlap occurs if: task1.earliest_time <= task2.latest_time AND task2.earliest_time <= task1.latest_time
        
        Args:
            plan: List of tasks to check (if None, checks all incomplete tasks)
            
        Returns:
            List of tuples (task1, task2, conflict_message) for each conflict found
        """
        if plan is None:
            plan = self.filter_by_status(completed=False)
        
        conflicts = []
        
        # Compare each task with every other task
        for i in range(len(plan)):
            for j in range(i + 1, len(plan)):
                task1 = plan[i]
                task2 = plan[j]
                
                # Check for time overlap
                # Conflict if: task1_start <= task2_end AND task2_start <= task1_end
                if task1.earliest_time <= task2.latest_time and task2.earliest_time <= task1.latest_time:
                    # Only flag if same pet or owner can't do both at once
                    if task1.pet_name == task2.pet_name:
                        msg = f"SAME PET: '{task1.name}' and '{task2.name}' for {task1.pet_name} overlap in time window {task1.earliest_time}h-{task2.latest_time}h"
                    else:
                        msg = f"TIMING CONFLICT: '{task1.name}' ({task1.pet_name}) and '{task2.name}' ({task2.pet_name}) scheduled in same time window ({task1.earliest_time}h-{task2.latest_time}h)"
                    
                    conflicts.append((task1, task2, msg))
        
        return conflicts
    
    # ========================================================================
    # STEP 3: RECURRING TASK AUTOMATION
    # ========================================================================
    
    def create_recurring_task(self, task: Task) -> Optional[Task]:
        """
        Create the next occurrence of a recurring task.
        For "daily" tasks, creates a copy for tomorrow.
        For "weekly" tasks, creates a copy for next week.
        
        Args:
            task: The completed task to recur
            
        Returns:
            New Task instance for next occurrence, or None if not recurring
        """
        if task.frequency not in ["daily", "weekly", "twice_daily"]:
            return None  # Task doesn't recur
        
        # Create a copy of the task
        next_task = Task(
            name=task.name,
            duration=task.duration,
            priority=task.priority,
            category=task.category,
            pet_name=task.pet_name,
            frequency=task.frequency,
            earliest_time=task.earliest_time,
            latest_time=task.latest_time,
            completed=False
        )
        
        return next_task
    
    def mark_task_complete_with_recurrence(self, task: Task, pet: Pet) -> None:
        """
        Mark a task as complete and auto-create the next occurrence if it's recurring.
        
        Args:
            task: Task to mark complete
            pet: Pet that owns this task (so we can add the new recurring instance)
        """
        task.mark_complete()
        
        # If task recurs, create and add the next occurrence
        if task.frequency in ["daily", "weekly", "twice_daily"]:
            next_task = self.create_recurring_task(task)
            if next_task:
                pet.add_task(next_task)

