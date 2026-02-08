export interface TrainingExercise {
    order: number;
    equipment?: string | null;
    sets_x_reps?: string | null;
    break_time_seconds?: number | null;
    training_exercise_item_id: string; // Required to link to the specific exercise item
}

export interface TrainingPlan {
    id: string;
    name: string;
    profile_id: string;
    // exercises: TrainingExercise[]; // Backend sends 'training_exercises'
    training_exercises: TrainingExercise[];
}

export interface TrainingPlanCreate {
    name: string;
    profile_id: string;
    training_exercises: TrainingExercise[];
}

export interface TrainingPlanUpdate {
    name?: string;
    profile_id?: string;
    training_exercises?: TrainingExercise[];
}

// Helper types for strict typing if needed, mirroring backend schemas
export interface TrainingExerciseCreate {
    order: number;
    equipment?: string | null;
    sets_x_reps?: string | null;
    break_time_seconds?: number | null;
    training_exercise_item_id?: string | null;
}
