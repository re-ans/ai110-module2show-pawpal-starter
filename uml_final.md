# PawPal+ Final System Architecture (UML)

## Complete Class Diagram with Algorithms

```mermaid
classDiagram
    class Owner {
        - name: str
        - available_hours_per_day: float
        - preferences: Dict[str, str]
        - pets: List[Pet]
        + get_available_time(): float
        + update_preferences(pref: Dict): None
        + add_pet(pet: Pet): None
        + get_all_tasks(): List[Task]
    }

    class Pet {
        - name: str
        - species: str
        - age: int
        - special_needs: List[str]
        - tasks: List[Task]
        + get_info(): str
        + add_task(task: Task): None
        + get_tasks_by_category(category: str): List[Task]
    }

    class Task {
        - name: str
        - duration: int
        - priority: int (1-5)
        - category: str
        - pet_name: str
        - frequency: str
        - earliest_time: int (0-23)
        - latest_time: int (0-23)
        - completed: bool
        + get_priority(): int
        + to_string(): str
        + mark_complete(): None
        + mark_incomplete(): None
    }

    class Scheduler {
        - owner: Owner
        - pets: List[Pet]
        - tasks: List[Task]
        
        CORE METHODS:
        + generate_daily_plan(): List[Task]
        + validate_schedule(plan: List[Task]): bool
        + calculate_feasibility(): float
        
        SORTING & FILTERING (Algorithm Phase):
        + sort_by_time(tasks: List[Task]): List[Task]
        + filter_by_pet(pet_name: str): List[Task]
        + filter_by_status(completed: bool): List[Task]
        + filter_by_category(category: str): List[Task]
        
        CONFLICT DETECTION (Algorithm Phase):
        + detect_conflicts(plan): List[Tuple[Task, Task, str]]
        
        RECURRING TASKS (Algorithm Phase):
        + create_recurring_task(task: Task): Optional[Task]
        + mark_task_complete_with_recurrence(task: Task, pet: Pet): None
    }

    Owner "1" --> "*" Pet : owns
    Owner "1" --> "1" Scheduler : uses
    Pet "1" --> "*" Task : contains
    Scheduler --> Pet : manages
    Scheduler --> Task : schedules
    Task "many" --> "1" Pet : belongs to (via pet_name)
```

## Data Flow Diagram

```mermaid
graph LR
    A["👤 Owner\n(Input: name, hours/day)"] -->|owns| B["🐾 Pet\n(Input: name, species, age)"]
    B -->|has| C["📋 Task\n(Input: name, duration, priority, category, time window)"]
    
    A -->|feeds| D["🔧 Scheduler\n(Core)"]
    B -->|feeds| D
    C -->|feeds| D
    
    D -->|generate_daily_plan| E["📅 Raw Plan\n(priority-sorted)"]
    E -->|sort_by_time| F["⏰ Time-sorted Plan\n(chronological)"]
    
    D -->|detect_conflicts| G["⚠️ Conflict Warnings\n(same-pet / timing)"]
    D -->|filter_by_*| H["🔍 Filtered Views\n(by pet/status/category)"]
    
    F -->|validate_schedule| I{"✓ Fits in\navailable time?"}
    I -->|Yes| J["✅ Valid Schedule"]
    I -->|No| K["❌ Time Overload"]
    
    E -->|recurring tasks| L["🔄 Next Occurrences\n(daily/weekly)"]
    
    J -->|display| M["📺 Streamlit UI\n(app.py)"]
    K -->|display| M
    G -->|display| M
    F -->|display| M
```

## System Layers

```mermaid
graph TB
    subgraph "Layer 1: Data Model (pawpal_system.py)"
        Owner["Owner"]
        Pet["Pet"]
        Task["Task"]
        Scheduler["Scheduler"]
    end
    
    subgraph "Layer 2: Core Scheduling Logic"
        GenPlan["generate_daily_plan()"]
        Validate["validate_schedule()"]
        Feasibility["calculate_feasibility()"]
    end
    
    subgraph "Layer 3: Smart Algorithms"
        Sort["sort_by_time()"]
        FilterPet["filter_by_pet()"]
        FilterStatus["filter_by_status()"]
        FilterCat["filter_by_category()"]
        Conflicts["detect_conflicts()"]
        Recur["Recurring Tasks\n(create/mark_complete)"]
    end
    
    subgraph "Layer 4: User Interface (app.py - Streamlit)"
        OwnerUI["Owner Info Form"]
        PetUI["Pet Management"]
        TaskUI["Task Creation"]
        AnalysisUI["Advanced Analysis\n(Filtering)"]
        ScheduleUI["Schedule Display\n(with Conflicts)"]
    end
    
    Owner --> GenPlan
    Pet --> GenPlan
    Task --> GenPlan
    Scheduler --> GenPlan
    
    GenPlan --> Validate
    GenPlan --> Feasibility
    
    GenPlan --> Sort
    GenPlan --> FilterPet
    GenPlan --> FilterStatus
    GenPlan --> FilterCat
    GenPlan --> Conflicts
    GenPlan --> Recur
    
    Owner --> OwnerUI
    Pet --> PetUI
    Task --> TaskUI
    
    Sort --> AnalysisUI
    FilterPet --> AnalysisUI
    FilterStatus --> AnalysisUI
    FilterCat --> AnalysisUI
    
    Conflicts --> ScheduleUI
    Sort --> ScheduleUI
    Validate --> ScheduleUI
    Feasibility --> ScheduleUI
    Recur --> ScheduleUI
```

## Key Design Patterns

### 1. Session State Management (Streamlit)
- **Pattern**: Dictionary-based vault in `st.session_state.owner`
- **Purpose**: Persist Owner object across Streamlit reruns
- **Code**: `if "owner" not in st.session_state: create else: use`

### 2. Validation via Post-Init
- **Pattern**: Dataclass `__post_init__()` method
- **Purpose**: Validate Task attributes (priority 1-5, positive duration, valid time ranges)
- **Benefit**: Catch invalid data early before scheduling

### 3. Algorithmic Separation
- **Pattern**: Distinct methods for each algorithm (sort, filter, detect, recur)
- **Purpose**: Enable UI to call different algorithms without tight coupling
- **Benefit**: Easy to test, extend, and compose

### 4. Conflict Messaging
- **Pattern**: Return tuples with (task1, task2, message) including severity
- **Purpose**: Distinguish same-pet conflicts (impossible) from timing conflicts (owner decision)
- **Benefit**: UI can display different warnings appropriately

---

## Evolution Summary

| Phase | Key Additions | Impact |
|-------|---------------|--------|
| **Phase 1** | 4 core classes (Owner, Pet, Task, Scheduler) | Foundation for all logic |
| **Phase 2** | pet_name binding, time windows, validation | Prevents invalid schedules |
| **Phase 3** | generate_daily_plan, validate, feasibility | Core scheduling works |
| **Phase 4** | 7 algorithms (sort, filter×3, detect_conflicts, recurring) | Smart, composable scheduling |
| **Phase 5** | UI integration, test suite, algorithmic display | User-facing smart features |
