# pawpal_system.py
from dataclasses import dataclass, field
from typing import List
from datetime import date, timedelta

@dataclass
class Task:
    """A data class for a single care task."""
    name: str
    duration: int  # in minutes
    priority: int  # lower number means higher priority
    frequency: str = "daily"  # e.g., "daily", "weekly"
    completed: bool = False
    due_date: date = field(default_factory=date.today)
    start_time: int = 0 # Time in minutes from the start of the schedule

    def mark_complete(self, pet: "Pet"):
        """
        Marks the task as completed and, if it is a recurring task (daily/weekly),
        creates a new instance of the task for the next scheduled occurrence.

        Args:
            pet (Pet): The pet to whom the recurring task will be added.
        """
        self.completed = True
        
        new_task = None
        if self.frequency == "daily":
            new_due_date = self.due_date + timedelta(days=1)
            new_task = Task(name=self.name, duration=self.duration, priority=self.priority, frequency=self.frequency, due_date=new_due_date)
        elif self.frequency == "weekly":
            new_due_date = self.due_date + timedelta(days=7)
            new_task = Task(name=self.name, duration=self.duration, priority=self.priority, frequency=self.frequency, due_date=new_due_date)
        
        if new_task:
            pet.add_task(new_task)

    def get_task_info(self) -> str:
        """
        Returns a formatted string with the task's details, including its
        completion status, duration, priority, due date, and scheduled start time.
        """
        status = "✓" if self.completed else "✗"
        return f"[{status}] {self.name} ({self.duration} mins, P{self.priority}, due: {self.due_date.strftime('%Y-%m-%d')}, start: {self.start_time} minutes)"

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

        # 2. Sort tasks by priority (primary) and duration (secondary)
        sorted_tasks = sorted(all_tasks, key=lambda task: (task.priority, task.duration))
        
        remaining_time = available_time
        
        # 3. Iterate through sorted tasks and add them to the plan if they fit
        for task in sorted_tasks:
            if task.duration <= remaining_time:
                self._add_task(task)
                remaining_time -= task.duration
        
        return self

    def _add_task(self, task: Task):
        """
        An internal method to add a task to the schedule.

        This method appends a task to the `scheduled_tasks` list, sets the task's
        `start_time` based on the current total duration of the plan, and updates
        the `total_duration`.

        Args:
            task (Task): The task to be added to the schedule.
        """
        task.start_time = self.total_duration # Set start time before adding duration
        self.scheduled_tasks.append(task)
        self.total_duration += task.duration

    def get_total_duration(self) -> int:
        """Returns the total duration of all scheduled tasks."""
        return self.total_duration

    def sort_by_time(self):
        """Sorts the scheduled tasks by their duration."""
        self.scheduled_tasks.sort(key=lambda task: task.duration)
    
    def filter_by_completion(self, completed: bool) -> List[Task]:
        """Returns a list of tasks filtered by their completion status."""
        return [task for task in self.scheduled_tasks if task.completed == completed]

    def detect_conflicts(self) -> List[tuple[Task, Task]]:
        """
        Detects if any two tasks in the schedule have overlapping times.

        This method iterates through all pairs of scheduled tasks and checks for
        any overlap in their start and end times. Because the current scheduling
        logic is a simple back-to-back sequence, a true conflict can only occur
        if two tasks have the exact same start time.

        Returns:
            List[tuple[Task, Task]]: A list of tuples, where each tuple contains
            two tasks that are in conflict with each other. An empty list is
            returned if no conflicts are found.
        """
        conflicts = []
        # Sort tasks by start time to make comparison easier
        sorted_plan = sorted(self.scheduled_tasks, key=lambda t: t.start_time)
        
        for i in range(len(sorted_plan)):
            for j in range(i + 1, len(sorted_plan)):
                task1 = sorted_plan[i]
                task2 = sorted_plan[j]
                
                # An overlap occurs if one task starts before the other one ends
                if task1.start_time < (task2.start_time + task2.duration) and \
                   (task1.start_time + task1.duration) > task2.start_time:
                    # In our current simple model, a conflict is only possible if start times are identical
                    if task1.start_time == task2.start_time:
                        conflicts.append((task1, task2))
        return conflicts

    def display_plan(self):
        """
        Prints the formatted schedule to the console and warns about conflicts.

        This method first checks if there are any scheduled tasks. If so, it
        prints each task's name and duration, followed by the total time for
        the entire plan. It then automatically calls `detect_conflicts()` and,
        if any are found, prints a formatted warning to the console.
        """
        if not self.scheduled_tasks:
            print("No tasks could be scheduled with the available time.")
            return
        
        print("--- Daily Pet Care Plan ---")
        for task in self.scheduled_tasks:
            print(f"- {task.name} ({task.duration} minutes)")
        print(f"--------------------------")
        print(f"Total Time: {self.total_duration} minutes")

        # Add a warning for any scheduling conflicts
        conflicts = self.detect_conflicts()
        if conflicts:
            print("\n--- WARNING: Scheduling Conflicts Detected! ---")
            for task1, task2 in conflicts:
                print(f"  - Conflict: '{task1.name}' and '{task2.name}' are scheduled at the same time.")
            print("---------------------------------------------")


