# pawpal_system.py
from dataclasses import dataclass, field
from typing import List

@dataclass
class Task:
    """A data class for a single care task."""
    name: str
    duration: int  # in minutes
    priority: int  # lower number means higher priority
    frequency: str = "daily"  # e.g., "daily", "weekly"
    completed: bool = False

    def mark_complete(self):
        """Marks the task as completed."""
        self.completed = True

    def get_task_info(self) -> str:
        """Returns a formatted string with the task's details."""
        status = "✓" if self.completed else "✗"
        return f"[{status}] {self.name} ({self.duration} mins, P{self.priority}, {self.frequency})"

@dataclass
class Pet:
    """A data class to hold information about a pet and its tasks."""
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Adds a task to this pet's list of tasks."""
        self.tasks.append(task)

    def get_pet_details(self) -> str:
        """Returns a formatted string with the pet's details."""
        return f"{self.name} ({self.species})"

class Owner:
    """Represents the user, manages pets, and provides access to all tasks."""
    def __init__(self, name: str, available_time: int = 0):
        """Initializes an Owner with a name and optional available time."""
        self.name = name
        self.available_time = available_time
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Adds a pet to the owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Returns a single list of all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def set_availability(self, minutes: int):
        """Sets the owner's total available time for pet care."""
        self.available_time = minutes

    def get_availability(self) -> int:
        """Returns the owner's available time in minutes."""
        return self.available_time

class Scheduler:
    """The "Brain" that retrieves, organizes, and manages tasks across pets."""
    def __init__(self):
        """Initializes the Scheduler with an empty plan."""
        self.scheduled_tasks: List[Task] = []
        self.total_duration: int = 0

    def generate_plan(self, owner: Owner) -> "Scheduler":
        """Generates a schedule based on the owner's tasks and availability."""
        # Reset the plan before generating a new one
        self.scheduled_tasks = []
        self.total_duration = 0
        
        # 1. Get all tasks from the owner that are not yet completed
        all_tasks = [task for task in owner.get_all_tasks() if not task.completed]
        available_time = owner.get_availability()

        # 2. Sort tasks by priority
        sorted_tasks = sorted(all_tasks, key=lambda task: task.priority)
        
        remaining_time = available_time
        
        # 3. Iterate through sorted tasks and add them to the plan if they fit
        for task in sorted_tasks:
            if task.duration <= remaining_time:
                self._add_task(task)
                remaining_time -= task.duration
        
        return self

    def _add_task(self, task: Task):
        """Adds a single task to the scheduler's plan."""
        self.scheduled_tasks.append(task)
        self.total_duration += task.duration

    def get_total_duration(self) -> int:
        """Returns the total duration of all scheduled tasks."""
        return self.total_duration

    def display_plan(self):
        """Prints the formatted schedule to the console."""
        if not self.scheduled_tasks:
            print("No tasks could be scheduled with the available time.")
            return
        
        print("--- Daily Pet Care Plan ---")
        for task in self.scheduled_tasks:
            print(f"- {task.name} ({task.duration} minutes)")
        print(f"--------------------------")
        print(f"Total Time: {self.total_duration} minutes")


