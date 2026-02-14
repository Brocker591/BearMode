export interface TrainingExercise {
    id?: string;
    order: number;
    equipment?: string | null;
    sets?: number | null;
    reps?: number | null;
    break_time_seconds?: number | null;
    training_exercise_item?: {
        id: string;
        description: string;
        video_url?: string | null;
    } | null;
}

export interface TrainingPlan {
    id: string;
    name: string;
    profile_id: string;
    exercises: TrainingExercise[];
}

export interface TrainingPlanCreate {
    name: string;
    profile_id: string;
    training_exercises: TrainingExerciseCreate[];
}

export interface TrainingPlanUpdate {
    id: string;
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

export interface TrainingExerciseExecuteResponse {
    id: string;
    exercise_id: string;
    order: number;
    equipment?: string | null;
    reps: number;
    break_time_seconds: number;
    training_exercise_description: string;
    training_exercise_video_url?: string | null;
}

export interface TrainingPlanExecuteResponse {
    id: string;
    name: string;
    profile_id: string;
    exercises: TrainingExerciseExecuteResponse[];
}


export interface TrainingExerciseCompletion {
    id: string;
    profile_id: string;
    training_plan_id: string;
    exercise_id: string;
    order: number;
    equipment?: string | null;
    reps: number;
    break_time_seconds: number;
    exercise_description: string;
    exercise_video_url?: string | null;
    training_day?: string | null;
}
