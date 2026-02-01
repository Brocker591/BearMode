export interface Profile {
  id: string;
  name: string;
}

export interface ProfileCreate {
  name: string;
}

export interface ProfileUpdate {
  name?: string;
}
