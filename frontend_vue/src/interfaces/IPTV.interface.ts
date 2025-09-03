export interface IChannels {
  id: number;
  channel_name: string;
  category_id: number;
  timeshift: number;
  catchup_days: number;
  catchup_type: string;
  tvg_id: string;
  group_title: string;
  tvg_logo: string;
  url: string;
  favorite: boolean;
  active: boolean;
}

export interface IEpgNow {
  [key: number]: string;
}

export interface IEpgChannel {
  start: string;
  end: string;
  title: string;
  desc: string;
  url: string;
}
