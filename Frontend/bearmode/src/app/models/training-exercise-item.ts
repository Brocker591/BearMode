export interface TrainingExerciseItem {
    id: string;
    description: string;
    video_url: string | null;
}

export interface TrainingExerciseItemCreate {
    description: string;
    video_url?: string | null;
}

export interface TrainingExerciseItemUpdate {
    description: string;
    video_url?: string | null;
}
