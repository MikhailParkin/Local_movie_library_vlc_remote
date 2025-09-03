export interface ISeasons {
  season_id: number
  season_name: string
  series: IEpisode[]
}

export interface IEpisode {
  episode_id: number
  episode_name: string
}

