import sys
import os
import asyncio

# Add the current directory to sys.path to make app module available
sys.path.append(os.getcwd())

try:
    from app.features.profiles.repository import ProfileRepository
    from app.features.training_exercise_items.repository import TrainingExerciseItemRepository
    from app.features.training_plan.repository import TrainingPlanRepository
    print("Imports successful")
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
