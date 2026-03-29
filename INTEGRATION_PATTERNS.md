# PawPal+ Integration Patterns (Quick Reference)

## Pattern 1: Session State Initialization

**Problem:** Streamlit reruns your script on every interaction. Objects created in the script get recreated.

**Solution:** Use `st.session_state` to persist data across reruns.

```python
# At app start, check if object exists in session state
if "owner" not in st.session_state:
    # First run: create and store
    st.session_state.owner = Owner(name="Pet Owner", available_hours_per_day=4.0)
else:
    # Subsequent runs: use existing object (data persists!)
    owner = st.session_state.owner
```

**Why this works:** `st.session_state` is a dictionary that survives across Streamlit reruns. It's like a "vault" that keeps your data alive.

---

## Pattern 2: Import and Wire UI Input to Class Methods

**Flow:** User Input → Form Capture → Class Instantiation → Method Call → Update UI

```python
# Step 1: Import classes
from pawpal_system import Owner, Pet, Task, Scheduler

# Step 2: Get session owner
owner = st.session_state.owner

# Step 3: Capture user input from form
pet_name = st.text_input("Pet name", value="Buddy")
species = st.selectbox("Species", ["Dog", "Cat", "Other"])
age = st.number_input("Age", min_value=0, max_value=30, value=3)

# Step 4: On button click, create instance and call class method
if st.button("Add Pet"):
    new_pet = Pet(name=pet_name, species=species, age=age)
    owner.add_pet(new_pet)  # ← Calls the class method
    st.success(f"✓ Added {pet_name}!")
    st.rerun()  # Make UI update immediately
```

**Key points:**
- Validate inputs in the class (`Task.__post_init__()`)
- Catch exceptions and show errors via `st.error()`
- Call `st.rerun()` to refresh the display after state changes

---

## Pattern 3: Call Logic Methods and Display Results

**Flow:** Trigger → Instantiate Class → Call Methods → Extract Results → Display

```python
# User clicks "Generate Schedule"
if st.button("Generate Schedule"):
    # Create scheduler instance with session owner
    scheduler = Scheduler(owner=st.session_state.owner)
    
    # Call methods to get results
    daily_plan = scheduler.generate_daily_plan()  # Returns sorted list of Tasks
    is_valid = scheduler.validate_schedule(daily_plan)  # Returns bool
    feasibility = scheduler.calculate_feasibility()  # Returns 0.0-1.0
    
    # Extract data for display
    total_time = sum(task.duration for task in daily_plan)
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Time Needed", f"{total_time} min")
    with col2:
        st.metric("Feasibility", f"{feasibility * 100:.0f}%")
    with col3:
        st.metric("Valid", "✓ Yes" if is_valid else "✗ No")
    
    # Display results table
    st.table([
        {
            "Task": task.name,
            "Pet": task.pet_name,
            "Duration": f"{task.duration}m",
            "Priority": "⭐" * task.priority
        }
        for task in daily_plan
    ])
```

---

## Common Pitfalls to Avoid

❌ **DON'T** create your Owner/Pet at the top of the script without checking session_state
- It will be recreated on every button click, losing data

✅ **DO** check `if "owner" not in st.session_state:` first

---

❌ **DON'T** forget to call `st.rerun()` after modifying state
- UI won't update to show changes

✅ **DO** call `st.rerun()` after adding a pet or task

---

❌ **DON'T** create complex UI logic without validation
- Bad data will cause confusing errors

✅ **DO** let the class validation (like `Task.__post_init__()`) catch errors
- Wrap in `try/except` and show with `st.error()`

---

## Testing the Integration

```bash
# Run this to verify all three patterns work
python3 test_integration.py
```

Expected output:
```
✓ Step 1: Testing imports...
✓ Step 2: Testing session_state persistence...
✓ Step 3: Testing Add Pet workflow...
✓ Step 4: Testing Add Task workflow...
✓ Step 5: Testing Schedule Generation...
✓ Step 6: Testing Task Completion...

✅ ALL INTEGRATION TESTS PASSED
```

---

## Architecture Diagram

```
User clicks button in Streamlit UI
            ↓
UI captures form inputs (text, numbers, selections)
            ↓
Check: Does object exist in st.session_state?
    ├─ NO  → Create new instance
    └─ YES → Use existing instance
            ↓
Update instance via class methods (e.g., add_pet(), add_task())
            ↓
Call Scheduler methods (generate_daily_plan(), validate_schedule())
            ↓
Display results in UI (metrics, tables, messages)
            ↓
st.rerun() triggers Streamlit to refresh the display
            ↓
Data persists in st.session_state for next interaction
```

---

**TL;DR** The integration works by:
1. Storing Owner/Pet/Task data in `st.session_state` so it persists
2. Wiring UI buttons to class methods via `st.session_state.owner.add_pet()`
3. Calling Scheduler methods to generate schedules and display results
