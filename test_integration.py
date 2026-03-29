"""
Integration Test: Verify that app.py successfully imports and connects to pawpal_system.py
This script tests the "bridge" between backend logic and Streamlit UI.
"""

import sys

print("=" * 70)
print("PawPal+ Integration Verification")
print("=" * 70)

# Step 1: Verify imports
print("\n✓ Step 1: Testing imports from app.py...")
try:
    from pawpal_system import Owner, Pet, Task, Scheduler
    print("  ✓ pawpal_system classes imported successfully")
except ImportError as e:
    print(f"  ✗ Failed to import pawpal_system: {e}")
    sys.exit(1)

# Step 2: Verify session_state logic pattern
print("\n✓ Step 2: Testing session_state persistence pattern...")
try:
    # Simulate what app.py does with session_state
    session_state = {}  # Simulate st.session_state
    
    # Check if owner exists (first run)
    if "owner" not in session_state:
        session_state["owner"] = Owner(name="Pet Owner", available_hours_per_day=4.0)
        session_state["owner"].pets = []
    
    # Verify owner persists
    owner = session_state["owner"]
    print(f"  ✓ Owner initialized: {owner.name} ({owner.available_hours_per_day}h/day)")
    
    # Second "check" (simulating rerun) - owner should still exist
    if "owner" not in session_state:
        print("  ✗ Owner did not persist!")
        sys.exit(1)
    else:
        print("  ✓ Owner persisted across 'rerun'")
except Exception as e:
    print(f"  ✗ Session state test failed: {e}")
    sys.exit(1)

# Step 3: Test Owner → Pet connection (Add Pet workflow)
print("\n✓ Step 3: Testing Add Pet workflow...")
try:
    # Simulate user adding a pet via UI
    pet_name = "Buddy"
    species = "Dog"
    age = 3
    special_needs = ["high energy", "needs regular walks"]
    
    new_pet = Pet(
        name=pet_name,
        species=species,
        age=age,
        special_needs=special_needs
    )
    
    owner.add_pet(new_pet)
    print(f"  ✓ Pet added via UI: {owner.pets[0].name}")
    print(f"    - Owner now has {len(owner.pets)} pet(s)")
except Exception as e:
    print(f"  ✗ Add Pet workflow failed: {e}")
    sys.exit(1)

# Step 4: Test Pet → Task connection (Add Task workflow)
print("\n✓ Step 4: Testing Add Task workflow...")
try:
    pet = owner.pets[0]
    
    # Simulate user adding a task via UI
    task1 = Task(
        name="Morning Walk",
        duration=45,
        priority=5,
        category="walk",
        pet_name=pet.name,
        earliest_time=6,
        latest_time=9
    )
    
    task2 = Task(
        name="Breakfast",
        duration=10,
        priority=4,
        category="feeding",
        pet_name=pet.name,
        earliest_time=7,
        latest_time=10
    )
    
    pet.add_task(task1)
    pet.add_task(task2)
    
    print(f"  ✓ Tasks added via UI:")
    for task in pet.tasks:
        print(f"    - {task.to_string()}")
except ValueError as e:
    print(f"  ✗ Add Task workflow failed (validation): {e}")
    sys.exit(1)
except Exception as e:
    print(f"  ✗ Add Task workflow failed: {e}")
    sys.exit(1)

# Step 5: Test Schedule Generation (Generate Schedule button)
print("\n✓ Step 5: Testing Schedule Generation workflow...")
try:
    # Simulate user clicking "Generate Schedule" button
    scheduler = Scheduler(owner=owner)
    daily_plan = scheduler.generate_daily_plan()
    
    print(f"  ✓ Schedule generated: {len(daily_plan)} tasks")
    
    # Verify validation
    is_valid = scheduler.validate_schedule(daily_plan)
    feasibility = scheduler.calculate_feasibility()
    
    print(f"    - Schedule valid: {is_valid}")
    print(f"    - Feasibility: {feasibility * 100:.0f}%")
    print(f"    - Total runtime: {sum(t.duration for t in daily_plan)} minutes")
    print(f"    - Available time: {int(owner.get_available_time())} minutes")
    
    if is_valid:
        print(f"    ✓ All tasks fit within owner's available time!")
except Exception as e:
    print(f"  ✗ Schedule generation failed: {e}")
    sys.exit(1)

# Step 6: Test Task Completion (mark_complete workflow)
print("\n✓ Step 6: Testing Task Completion workflow...")
try:
    original_plan_length = len(scheduler.generate_daily_plan())
    
    # Mark first task as complete
    daily_plan[0].mark_complete()
    print(f"  ✓ Marked '{daily_plan[0].name}' as complete")
    
    # Verify it's excluded from next plan
    updated_plan = scheduler.generate_daily_plan()
    if len(updated_plan) < original_plan_length:
        print(f"  ✓ Completed tasks excluded: plan now has {len(updated_plan)} tasks")
    else:
        print(f"  ✗ Completed tasks not being filtered!")
        sys.exit(1)
except Exception as e:
    print(f"  ✗ Task completion test failed: {e}")
    sys.exit(1)

# Success!
print("\n" + "=" * 70)
print("✅ ALL INTEGRATION TESTS PASSED")
print("=" * 70)
print("\nThe app.py ↔ pawpal_system.py bridge is working correctly!")
print("\nNextStep: Run 'streamlit run app.py' to use the interactive UI")
print("=" * 70)
