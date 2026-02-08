import asyncio
import httpx
import uuid
import sys

BASE_URL = "http://localhost:8000"

async def main():
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        # 1. Create Profile (Dependency)
        profile_name = f"Test Profile {uuid.uuid4()}"
        print(f"Creating profile: {profile_name}")
        resp = await client.post("/profiles", json={"name": profile_name})
        if resp.status_code != 201:
            print(f"Failed to create profile: {resp.text}")
            sys.exit(1)
        profile_id = resp.json()["id"]
        print(f"Profile created: {profile_id}")

        # 2. Create Training Exercise Item (Dependency)
        item_desc = f"Test Item {uuid.uuid4()}"
        print(f"Creating exercise item: {item_desc}")
        resp = await client.post("/training-exercise-items", json={"description": item_desc})
        if resp.status_code != 201:
            print(f"Failed to create item: {resp.text}")
            sys.exit(1)
        item_id = resp.json()["id"]
        print(f"Item created: {item_id}")

        # 3. Create Training Plan
        plan_name = "My Training Plan"
        plan_data = {
            "name": plan_name,
            "profile_id": profile_id,
            "training_exercises": [
                {
                    "order": 1,
                    "Equipment": "Dumbbells",
                    "Sets": 3,
                    "Reps": 12,
                    "break_time_seconds": 60,
                    "training_exercise_item_id": item_id
                }
            ]
        }
        print(f"Creating training plan: {plan_data}")
        resp = await client.post("/training-plans", json=plan_data)
        if resp.status_code != 201:
             print(f"Failed to create plan: {resp.text}")
             sys.exit(1)
        plan = resp.json()
        plan_id = plan["id"]
        print(f"Plan created: {plan}")
        assert len(plan["training_exercises"]) == 1, f"Expected 1 exercise, got {len(plan['training_exercises'])}"

        # 4. Get Plan
        print(f"Getting plan {plan_id}")
        resp = await client.get(f"/training-plans/{plan_id}")
        assert resp.status_code == 200
        print(f"Got plan: {resp.json()}")

        # 5. Update Plan
        print(f"Updating plan {plan_id}")
        update_data = {
            "name": "Updated Plan Name",
            "training_exercises": [] # Clear exercises
        }
        resp = await client.put(f"/training-plans/{plan_id}", json=update_data)
        assert resp.status_code == 200
        updated_plan = resp.json()
        print(f"Updated plan: {updated_plan}")
        assert updated_plan["name"] == "Updated Plan Name"
        assert len(updated_plan["training_exercises"]) == 0
        
        # 6. Delete Plan
        print(f"Deleting plan {plan_id}")
        resp = await client.delete(f"/training-plans/{plan_id}")
        assert resp.status_code == 204
        
        # Verify deletion
        resp = await client.get(f"/training-plans/{plan_id}")
        assert resp.status_code == 404
        print("Plan deleted successfully")

        # Cleanup Profile (Optional)
        # await client.delete(f"/profiles/{profile_id}")

if __name__ == "__main__":
    asyncio.run(main())
