import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+** — your pet care planning assistant.

This app helps you organize and optimize daily pet care tasks based on time, priority, and preferences.
"""
)

st.divider()

# ============================================================================
# STEP 1: Initialize Session State (Persistent Memory)
# ============================================================================
# st.session_state acts like a "vault" that persists across Streamlit reruns
# Check if Owner exists; if not, create one

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Pet Owner", available_hours_per_day=4.0)
    st.session_state.owner.pets = []

if "selected_pet" not in st.session_state:
    st.session_state.selected_pet = None

# ============================================================================
# STEP 2: Owner Management Section
# ============================================================================
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("👤 Owner Information")
    new_owner_name = st.text_input(
        "Owner name", 
        value=st.session_state.owner.name,
        key="owner_name_input"
    )
    
    new_available_hours = st.number_input(
        "Available hours per day",
        min_value=1.0,
        max_value=24.0,
        value=st.session_state.owner.available_hours_per_day,
        step=0.5,
        key="available_hours_input"
    )
    
    if st.button("Update Owner Info"):
        st.session_state.owner.name = new_owner_name
        st.session_state.owner.available_hours_per_day = new_available_hours
        st.success(f"✓ Owner updated: {new_owner_name} ({new_available_hours}h/day)")

with col2:
    st.metric("Available Time (min)", int(st.session_state.owner.get_available_time()))
    st.metric("Pets", len(st.session_state.owner.pets))

st.divider()

# ============================================================================
# STEP 3: Pet Management Section
# ============================================================================
st.subheader("🐾 Manage Pets")

col1, col2, col3 = st.columns(3)

with col1:
    pet_name = st.text_input("Pet name", value="Buddy", key="new_pet_name")
with col2:
    species = st.selectbox("Species", ["Dog", "Cat", "Rabbit", "Bird", "Other"], key="pet_species")
with col3:
    age = st.number_input("Age (years)", min_value=0, max_value=30, value=3, key="pet_age")

special_needs_input = st.text_input(
    "Special needs (comma-separated):",
    placeholder="e.g., high energy, sensitive stomach",
    key="special_needs"
)

if st.button("Add Pet"):
    # Check if pet already exists
    if any(p.name == pet_name for p in st.session_state.owner.pets):
        st.warning(f"A pet named '{pet_name}' already exists!")
    else:
        special_needs = [need.strip() for need in special_needs_input.split(",") if need.strip()]
        new_pet = Pet(
            name=pet_name,
            species=species,
            age=age,
            special_needs=special_needs
        )
        st.session_state.owner.add_pet(new_pet)
        st.success(f"✓ Added {pet_name} the {species} to your pets!")
        st.rerun()

# Display existing pets
if st.session_state.owner.pets:
    st.write("**Your Pets:**")
    for pet in st.session_state.owner.pets:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(pet.get_info())
            with col2:
                if st.button(f"Manage {pet.name}", key=f"btn_manage_{pet.name}"):
                    st.session_state.selected_pet = pet.name
                    st.rerun()
else:
    st.info("No pets yet. Add one above to get started!")

st.divider()

# ============================================================================
# STEP 4: Task Management Section (for selected pet)
# ============================================================================
if st.session_state.owner.pets:
    st.subheader("📋 Add Tasks to Pet")
    
    pet_names = [p.name for p in st.session_state.owner.pets]
    selected_pet_name = st.selectbox(
        "Select pet to add task:",
        pet_names,
        key="task_pet_selector"
    )
    
    selected_pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet_name)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        task_name = st.text_input("Task name", value="Morning walk", key="task_name")
    with col2:
        task_duration = st.number_input(
            "Duration (min)", 
            min_value=1, 
            max_value=240, 
            value=30,
            key="task_duration"
        )
    with col3:
        task_priority = st.selectbox(
            "Priority",
            [5, 4, 3, 2, 1],
            format_func=lambda x: "⭐" * x,
            key="task_priority"
        )
    with col4:
        task_category = st.selectbox(
            "Category",
            ["walk", "feeding", "medication", "grooming", "enrichment"],
            key="task_category"
        )
    
    col1, col2 = st.columns(2)
    with col1:
        earliest_hour = st.slider(
            "Earliest time (hour of day)",
            0, 23, 6,
            key="task_earliest"
        )
    with col2:
        latest_hour = st.slider(
            "Latest time (hour of day)",
            0, 23, 22,
            key="task_latest"
        )
    
    if st.button("Add Task"):
        try:
            new_task = Task(
                name=task_name,
                duration=task_duration,
                priority=task_priority,
                category=task_category,
                pet_name=selected_pet.name,
                earliest_time=earliest_hour,
                latest_time=latest_hour
            )
            selected_pet.add_task(new_task)
            st.success(f"✓ Added '{task_name}' to {selected_pet.name}'s tasks!")
            st.rerun()
        except ValueError as e:
            st.error(f"Invalid task: {e}")
    
    # Display tasks for selected pet
    if selected_pet.tasks:
        st.write(f"**{selected_pet.name}'s Tasks:**")
        task_display = []
        for task in selected_pet.tasks:
            task_display.append({
                "Task": task.name,
                "Duration": f"{task.duration}m",
                "Priority": "⭐" * task.priority,
                "Category": task.category,
                "Window": f"{task.earliest_time}:00 - {task.latest_time}:00",
                "Status": "✓ Done" if task.completed else "○ Pending"
            })
        st.table(task_display)
    else:
        st.info(f"No tasks added yet for {selected_pet.name}.")

st.divider()

# ============================================================================
# STEP 5: Generate and Display Schedule
# ============================================================================
st.subheader("📅 Generate Daily Schedule")

if len(st.session_state.owner.pets) == 0:
    st.warning("Please add at least one pet and some tasks before generating a schedule.")
elif not st.session_state.owner.get_all_tasks():
    st.warning("Please add tasks to your pets before generating a schedule.")
else:
    if st.button("Generate Schedule", type="primary"):
        # Create scheduler instance
        scheduler = Scheduler(owner=st.session_state.owner)
        
        # Generate the plan
        daily_plan = scheduler.generate_daily_plan()
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_time = sum(t.duration for t in daily_plan)
            st.metric("Total Time Needed", f"{total_time} min")
        
        with col2:
            available_time = int(st.session_state.owner.get_available_time())
            st.metric("Available Time", f"{available_time} min")
        
        with col3:
            feasibility = scheduler.calculate_feasibility()
            st.metric("Feasibility", f"{feasibility * 100:.0f}%")
        
        with col4:
            is_valid = scheduler.validate_schedule(daily_plan)
            status = "✓ Valid" if is_valid else "✗ Overload"
            st.metric("Schedule Status", status)
        
        st.divider()
        
        # Display schedule
        if daily_plan:
            st.write("**Today's Optimized Schedule:**")
            
            schedule_display = []
            cumulative_time = 0
            
            for i, task in enumerate(daily_plan, 1):
                start_hour = task.earliest_time
                end_hour = start_hour + (task.duration // 60)
                
                schedule_display.append({
                    "#": i,
                    "Task": task.name,
                    "Pet": task.pet_name,
                    "Time": f"{start_hour}:00 - {end_hour}:00",
                    "Duration": f"{task.duration}m",
                    "Priority": "⭐" * task.priority,
                    "Category": task.category.capitalize()
                })
                cumulative_time += task.duration
            
            st.table(schedule_display)
            
            if not is_valid:
                st.error(
                    f"⚠️ Schedule exceeds available time! "
                    f"Tasks need {total_time}m but only {available_time}m available. "
                    f"Consider removing lower-priority tasks or increasing available time."
                )
            else:
                time_remaining = available_time - total_time
                st.success(
                    f"✓ Schedule fits! {time_remaining}m remaining for breaks or flexibility."
                )
        else:
            st.info("All tasks are already completed for today!")

st.divider()

# ============================================================================
# HELPER SECTION: Show session state for debugging
# ============================================================================
with st.expander("🔧 Debug Info"):
    st.write("**Owner:**", st.session_state.owner.name)
    st.write("**Pets:**", [p.name for p in st.session_state.owner.pets])
    st.write("**Total Tasks:**", len(st.session_state.owner.get_all_tasks()))
    
    if st.button("Reset All Data"):
        st.session_state.owner = Owner(name="Pet Owner", available_hours_per_day=4.0)
        st.session_state.selected_pet = None
        st.success("✓ All data reset!")
        st.rerun()

