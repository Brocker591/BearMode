export interface TrainingExercise {
    id?: string; // Optional because it might not be present in all contexts or strictly needed on frontend if we use index
    order: number;
    equipment?: string | null;
    sets?: number | null;
    reps?: number | null;
    break_time_seconds?: number | null;
    training_exercise_item?: {
        item_id?: string;
        item_description?: string;
        video_url?: string;
    } | null;
    // For backward compatibility or ease of use in forms, we might still want to track the ID separately if needed, 
    // but the backend response sends 'training_exercise_item'.
}

export interface TrainingPlan {
    id: string;
    name: string;
    profile_id: string;
    training_exercises: TrainingExercise[];
}

export interface TrainingPlanCreate {
    name: string;
    profile_id: string;
    training_exercises: TrainingExerciseCreate[];
}

export interface TrainingPlanUpdate {
    name?: string;
    profile_id?: string;
    training_exercises?: TrainingExerciseCreate[];
}

// Helper types for strict typing if needed, mirroring backend schemas
export interface TrainingExerciseCreate {
    order: number;
    equipment?: string | null;
    sets?: number | null;
    reps?: number | null;
    break_time_seconds?: number | null;
    training_exercise_item_id?: string | null;
}
