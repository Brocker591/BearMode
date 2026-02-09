import httpx
import uuid
import json
import random

BASE_URL = "http://localhost:8000"

def create_dummy_data():
    # Helper to create some data if none exists
    try:
        # Create Profile
        pid = str(uuid.uuid4())
        resp = httpx.post(f"{BASE_URL}/profiles", json={"name": f"TestUser_{pid[:8]}"})
        if resp.status_code == 201:
            profile_id = resp.json()['id']
            print(f"Created profile: {profile_id}")
            
            # Create Exercise Item
            eid = str(uuid.uuid4())
            resp = httpx.post(f"{BASE_URL}/training-exercise-items", json={
                "description": f"Pushups_{eid[:8]}",
                "video_url": "http://example.com"
            })
            if resp.status_code == 201:
                item_id = resp.json()['id']
                print(f"Created item: {item_id}")
                
                # Create Plan
                resp = httpx.post(f"{BASE_URL}/training-plans", json={
                    "name": f"Plan_{pid[:8]}",
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
                })
                if resp.status_code == 201:
                    print(f"Created plan: {resp.json()['id']}")
    except Exception as e:
        print(f"Setup failed: {e}")

def list_training_plans():
    print("\nTesting list_training_plans...")
    url = f"{BASE_URL}/training-plans"
    try:
        response = httpx.get(url)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            plans = response.json()
            print(f"Found {len(plans)} plans")
            if len(plans) > 0:
                print("First plan sample:", json.dumps(plans[0], indent=2))
                
                # Check if fields are correct
                plan = plans[0]
                if 'exercises' not in plan:
                    print("ERROR: 'exercises' field missing in plan")
                elif not plan['exercises']:
                    print("WARNING: 'exercises' list is empty in plan (might be creating plans without exercises or loading failed)")
                else:
                    for ex in plan['exercises']:
                        if 'training_exercise_item' not in ex:
                            print("ERROR: 'training_exercise_item' field missing in exercise")
                        else:
                             print("Structure looks OK for exercises.")
            else:
                print("No plans found. Running setup...")
                create_dummy_data()
                # Try again
                response = httpx.get(url)
                plans = response.json()
                print(f"Found {len(plans)} plans after setup")
                if len(plans) > 0:
                    print("First plan sample:", json.dumps(plans[0], indent=2))

        else:
            print("Error:", response.text)
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    list_training_plans()
