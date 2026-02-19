import { BodyCategory } from "./body-category";

export interface TrainingExerciseItem {
    id: string;
    description: string;
    video_url: string | null;
    body_category: BodyCategory;
}

export interface TrainingExerciseItemCreate {
    description: string;
    video_url?: string | null;
    body_category_id: string;
}

export interface TrainingExerciseItemUpdate {
    description: string;
    video_url?: string | null;
    body_category_id: string;
}
