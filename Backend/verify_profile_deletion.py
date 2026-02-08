import asyncio
import httpx
import uuid
import sys

BASE_URL = "http://localhost:8000"

async def main():
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        # 1. Create Profile
        profile_name = f"Cascade Test {uuid.uuid4()}"
        print(f"Creating profile: {profile_name}")
        resp = await client.post("/profiles", json={"name": profile_name})
        if resp.status_code != 201:
            print(f"Failed to create profile: {resp.text}")
            sys.exit(1)
        profile_id = resp.json()["id"]
        print(f"Profile created: {profile_id}")

        # 2. Create Training Plan linked to Profile
        plan_name = f"Plan for {profile_name}"
        plan_data = {
            "name": plan_name,
            "profile_id": profile_id,
            "training_exercises": [] # No exercises needed for this test, just the plan-profile link
        }
        print(f"Creating training plan: {plan_data}")
        resp = await client.post("/training-plans", json=plan_data)
        if resp.status_code != 201:
            print(f"Failed to create plan: {resp.text}")
            sys.exit(1)
        plan_id = resp.json()["id"]
        print(f"Plan created: {plan_id}")

        # 3. Delete Profile
        print(f"Deleting profile {profile_id}")
        resp = await client.delete(f"/profiles/{profile_id}")
        if resp.status_code != 204:
            print(f"Failed to delete profile: {resp.status_code} {resp.text}")
            sys.exit(1)
        print("Profile deleted successfully")

        # 4. Verify Profile is gone
        resp = await client.get(f"/profiles/{profile_id}")
        assert resp.status_code == 404, f"Profile still exists: {resp.status_code}"
        print("Verified profile is gone")

        # 5. Verify Training Plan is gone (Cascade)
        resp = await client.get(f"/training-plans/{plan_id}")
        if resp.status_code == 404:
            print("Verified training plan is gone (Cascade successful)")
        else:
            print(f"Training plan still exists or error: {resp.status_code} {resp.text}")
            # Depending on implementation, it might throw 500 if the relationship is broken but row exists? 
            # But if cascade works, it should be 404.
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
