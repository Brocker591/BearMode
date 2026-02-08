import sys
import os

# Add the Backend directory to sys.path
sys.path.append(os.path.abspath("/home/brocker/dev/BearMode/Backend"))

try:
    print("Attempting to import app.main...")
    from app.main import app
    print("Successfully imported app.main")
    
    print("Attempting to import routers...")
    from app.features.profiles.router import router as profiles_router
    from app.features.training_exercise_items.router import router as exercise_items_router
    from app.features.training_plan.router import router as training_plan_router
    print("Successfully imported routers")

except Exception as e:
    print(f"Error during import: {e}")
    sys.exit(1)
