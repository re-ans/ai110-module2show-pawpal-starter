import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# Initialize the session state for owner and scheduler
if 'owner' not in st.session_state:
    st.session_state.owner = Owner(name="New Owner")
if 'scheduler' not in st.session_state:
    st.session_state.scheduler = Scheduler()

# --- Owner and Pet Management ---
st.subheader("Owner & Pet Details")
owner_name = st.text_input("Owner Name", value=st.session_state.owner.name)
st.session_state.owner.name = owner_name

# Allow setting available time
available_time = st.number_input(
    "Your Available Time (minutes)", 
    min_value=0, 
    value=st.session_state.owner.get_availability()
)
st.session_state.owner.set_availability(available_time)

st.markdown("---")

# --- Pet Creation ---
with st.expander("Add a New Pet"):
    col1, col2 = st.columns(2)
    with col1:
        pet_name = st.text_input("Pet's Name", key="pet_name_input")
    with col2:
        species = st.selectbox("Species", ["Dog", "Cat", "Other"], key="species_input")
    
    if st.button("Add Pet"):
        if pet_name:
            new_pet = Pet(name=pet_name, species=species)
            st.session_state.owner.add_pet(new_pet)
            st.success(f"Added {pet_name} the {species}!")
        else:
            st.warning("Please enter a name for the pet.")

# Display current pets
if st.session_state.owner.pets:
    st.markdown("### Your Pets")
    pet_names = [p.name for p in st.session_state.owner.pets]
    # Create a dropdown to select which pet to add tasks to
    st.session_state.selected_pet_name = st.selectbox("Manage Tasks for:", pet_names)
else:
    st.info("No pets added yet. Add a pet above to start managing tasks.")

st.markdown("### Add a Task")
# Only show task form if a pet has been added and selected
if 'selected_pet_name' in st.session_state:
    # Find the selected pet object
    selected_pet = next((p for p in st.session_state.owner.pets if p.name == st.session_state.selected_pet_name), None)

    if selected_pet:
        col1, col2, col3 = st.columns(3)
        with col1:
            task_title = st.text_input("Task Title", value="Morning walk")
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        with col3:
            # Using numbers for priority for easier sorting
            priority = st.selectbox("Priority", [1, 2, 3], index=0, help="1=High, 2=Medium, 3=Low")

        if st.button("Add Task"):
            new_task = Task(name=task_title, duration=int(duration), priority=priority)
            selected_pet.add_task(new_task)
            st.success(f"Added task '{task_title}' for {selected_pet.name}.")

# Display all tasks for all pets
if st.session_state.owner.pets:
    st.markdown("### Current Task List")
    for pet in st.session_state.owner.pets:
        if pet.tasks:
            st.markdown(f"**Tasks for {pet.name}:**")
            # Create a list of dictionaries for st.table
            task_data = [
                {"Task": t.name, "Duration": t.duration, "Priority": t.priority, "Completed": t.completed}
                for t in pet.tasks
            ]
            st.table(task_data)
        else:
            st.info(f"No tasks for {pet.name} yet.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button will call your scheduling logic.")

if st.button("Generate Schedule"):
    if not st.session_state.owner.pets:
        st.warning("Please add at least one pet and some tasks before generating a schedule.")
    else:
        # Call the scheduler with the owner object
        scheduler = st.session_state.scheduler
        scheduler.generate_plan(st.session_state.owner)
        
        st.success("Schedule Generated!")
        
        if scheduler.scheduled_tasks:
            st.markdown("### Your Daily Plan")
            
            plan_data = [
                {"Task": t.name, "Duration": t.duration, "Priority": t.priority}
                for t in scheduler.scheduled_tasks
            ]
            st.table(plan_data)
            
            st.metric(label="Total Time Required", value=f"{scheduler.get_total_duration()} minutes")
            
            time_left = st.session_state.owner.get_availability() - scheduler.get_total_duration()
            st.metric(label="Time to Spare", value=f"{time_left} minutes")
        else:
            st.info("No tasks could be scheduled with the available time. Try increasing your available time.")
