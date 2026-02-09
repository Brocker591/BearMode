import httpx
import uuid
import json

BASE_URL = "http://localhost:8000"

def create_profile():
    url = f"{BASE_URL}/profiles"
    payload = {"name": f"Test Profile {uuid.uuid4()}"}
    response = httpx.post(url, json=payload)
    response.raise_for_status()
    print("Profile created:", response.json()['id'])
    return response.json()['id']

def create_exercise_item():
    url = f"{BASE_URL}/training-exercise-items"
    payload = {
        "description": f"Test Exercise {uuid.uuid4()}",
        "video_url": "https://example.com/video"
    }
    response = httpx.post(url, json=payload)
    response.raise_for_status()
    print("Exercise Item created:", response.json()['id'])
    return response.json()['id']

def create_training_plan(profile_id, item_id):
    url = f"{BASE_URL}/training-plans"
    payload = {
        "name": "Initial Plan",
        "profile_id": profile_id,
        "training_exercises": [
            {
                "order": 1,
                "training_exercise_item_id": item_id,
                "sets": 3,
                "reps": 10,
                "break_time_seconds": 60,
                "equipment": "None"
            }
        ]
    }
    response = httpx.post(url, json=payload)
    response.raise_for_status()
    print("Training Plan created:", response.json()['id'])
    return response.json()

def update_training_plan(plan_id, profile_id, item_id):
    url = f"{BASE_URL}/training-plans/{plan_id}"
    
    # Construct update payload matching TrainingPlanUpdate schema
    # TrainingExerciseUpdate requires: id, profile_id, training_plan_id, etc.
    exercise_id = str(uuid.uuid4())
    
    payload = {
        "id": plan_id,
        "name": "Updated Plan Name",
        "profile_id": profile_id,
        "training_exercises": [
            {
                "id": exercise_id,
                "profile_id": profile_id,
                "training_plan_id": plan_id,
                "order": 1,
                "training_exercise_item_id": item_id,
                "sets": 5,
                "reps": 5,
                "break_time_seconds": 120,
                "equipment": "Barbell"
            }
        ]
    }
    
    print(f"Updating plan {plan_id} with payload: {json.dumps(payload, indent=2)}")
    response = httpx.put(url, json=payload)
    if response.status_code != 200:
        print("Update failed:", response.status_code, response.text)
    response.raise_for_status()
    print("Training Plan updated.")
    return response.json()

def delete_training_plan(plan_id):
    url = f"{BASE_URL}/training-plans/{plan_id}"
    response = httpx.delete(url)
    if response.status_code != 204:
        print("Delete failed:", response.status_code, response.text)
    response.raise_for_status()
    print("Training Plan deleted.")

def main():
    try:
        profile_id = create_profile()
        item_id = create_exercise_item()
        plan_data = create_training_plan(profile_id, item_id)
        plan_id = plan_data['id']
        
        updated_plan = update_training_plan(plan_id, profile_id, item_id)
        
        # Verify update
        assert updated_plan['name'] == "Updated Plan Name"
        assert len(updated_plan['exercises']) == 1
        assert updated_plan['exercises'][0]['sets'] == 5
        print("Verification Successful!")
        
        delete_training_plan(plan_id)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
