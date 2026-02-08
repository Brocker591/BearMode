import asyncio
import httpx
import uuid
import sys

BASE_URL = "http://localhost:8000"

async def main():
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        # 1. Create Profile
        profile_name = f"Validation Test {uuid.uuid4()}"
        print(f"Creating profile: {profile_name}")
        resp = await client.post("/profiles", json={"name": profile_name})
        if resp.status_code != 201:
            print(f"Failed to create profile: {resp.text}")
            sys.exit(1)
        profile_id = resp.json()["id"]

        # 2. Create Exercise Item
        item_desc = f"Item {uuid.uuid4()}"
        resp = await client.post("/training-exercise-items", json={"description": item_desc})
        item_id = resp.json()["id"]

        # 3. Create Training Plan with NULL sets/reps (Should default to 1)
        print("Testing Plan creation with NULL sets/reps...")
        plan_data_null = {
            "name": f"Plan Null Test {uuid.uuid4()}",
            "profile_id": profile_id,
            "training_exercises": [
                {
                    "order": 1,
                    "Equipment": "Bar",
                    "Sets": None, # Should become 1
                    "Reps": None, # Should become 1
                    "training_exercise_item_id": item_id
                }
            ]
        }
        resp = await client.post("/training-plans", json=plan_data_null)
        if resp.status_code == 201:
            data = resp.json()
            print(f"Data keys: {data.keys()}")
            ex = data["training_exercises"][0]
            print(f"Success! Result: Sets={ex['Sets']}, Reps={ex['Reps']}")
            assert ex['Sets'] == 1, f"Expected Sets=1, got {ex['Sets']}"
            assert ex['Reps'] == 1, f"Expected Reps=1, got {ex['Reps']}"
        else:
            print(f"Failed (Unexpected): {resp.status_code} {resp.text}")
            sys.exit(1)

        # 4. Create Training Plan with 0 sets/reps (Should default to 1 based on my implementation)
        print("Testing Plan creation with 0 sets/reps...")
        plan_data_zero = {
            "name": f"Plan Zero Test {uuid.uuid4()}",
            "profile_id": profile_id,
            "training_exercises": [
                {
                    "order": 1,
                    "Equipment": "Bar",
                    "Sets": 0,
                    "Reps": 0,
                    "training_exercise_item_id": item_id
                }
            ]
        }
        resp = await client.post("/training-plans", json=plan_data_zero)
        if resp.status_code == 201:
            data = resp.json()
            ex = data["training_exercises"][0]
            print(f"Success! Result: Sets={ex['Sets']}, Reps={ex['Reps']}")
            assert ex['Sets'] == 1, f"Expected Sets=1, got {ex['Sets']}"
            assert ex['Reps'] == 1, f"Expected Reps=1, got {ex['Reps']}"
        else:
            print(f"Failed (Unexpected): {resp.status_code} {resp.text}")
            sys.exit(1)
            
        print("Verification Passed.")

if __name__ == "__main__":
    asyncio.run(main())
