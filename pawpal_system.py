# pawpal_system.py
from dataclasses import dataclass, field
from typing import List

@dataclass
class Pet:
    """A simple data class to hold information about a pet."""
    name: str
    species: str

    def get_pet_details(self) -> str:
        """Returns a string with the pet's details."""
        return f"{self.name} ({self.species})"

@dataclass
class Task:
    """A data class for a single care task."""
    name: str
    duration: int  # in minutes
    priority: int  # lower number means higher priority

    def get_task_info(self) -> str:
        """Returns a string with the task's details."""
        return f"Task: {self.name}, Duration: {self.duration} mins, Priority: {self.priority}"

class Plan:
    """Represents the final, generated schedule for the day."""
    def __init__(self):
        self.scheduled_tasks: List[Task] = []
        self.total_duration: int = 0

    def add_task(self, task: Task):
        """Adds a task to the plan and updates the total duration."""
        self.scheduled_tasks.append(task)
        self.total_duration += task.duration

    def get_total_duration(self) -> int:
        """Returns the total time commitment for the plan."""
        return self.total_duration

    def display_plan(self):
        """Prints the formatted schedule to the console for debugging."""
        if not self.scheduled_tasks:
            print("No tasks in the plan.")
            return
        
        print("--- Daily Pet Care Plan ---")
        for task in self.scheduled_tasks:
            print(f"- {task.name} ({task.duration} minutes)")
        print(f"--------------------------")
        print(f"Total Time: {self.total_duration} minutes")

class Owner:
    """Represents the user and their constraints."""
    def __init__(self, name: str, available_time: int = 0):
        self.name = name
        self.available_time = available_time

    def set_availability(self, minutes: int):
        """Sets the owner's total available time for pet care."""
        self.available_time = minutes

    def get_availability(self) -> int:
        """Returns the owner's available time."""
        return self.available_time

class Scheduler:
    """The core logic engine that generates a schedule."""
    def generate_plan(self, tasks: List[Task], available_time: int) -> Plan:
        """
        Creates a schedule by selecting and ordering tasks based on
        priority and the owner's available time.
        
        This is the main logic to be implemented.
        """
        # The core scheduling logic will go here.
        # For now, it just returns an empty plan.
        plan = Plan()
        
        # --- IMPLEMENTATION NEEDED ---
        # 1. Sort tasks by priority.
        # 2. Iterate through sorted tasks.
        # 3. For each task, check if it fits in the remaining available time.
        # 4. If it fits, add it to the plan and reduce the available time.
        # 5. Return the completed plan.
        
        pass # Replace this with your implementation

        return plan