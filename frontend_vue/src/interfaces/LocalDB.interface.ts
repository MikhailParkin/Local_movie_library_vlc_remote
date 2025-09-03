export interface ILocalDb {
  id: number;
  category: string;
  file_path: string;
  file_name: string;
  favorite: boolean;
  active: boolean;
  video_length: number;
  last_position: number;
  poster: string;
  poster_filename: string;
  kpinfo_id: number;
}
