export interface ILibrary {
  id: number;
  category_path: string;
  category_id: number;
}

export interface ILibraryList {
  [key: string]: ILibrary[];
}

export interface IPathList {
  dir_name: string;
  dir_path: string;
}
