export interface Profile {
  id: string;
  name: string;
  emoji?: string;
}

export interface ProfileCreate {
  name: string;
  emoji?: string;
}

export interface ProfileUpdate {
  name?: string;
  emoji?: string;
}
