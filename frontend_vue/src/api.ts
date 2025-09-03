import axios from 'axios'
import type { RouteParamValue } from 'vue-router'

// export const HOST = 'http://localhost:5550/'
// export const API_BASE_URL = 'http://localhost:5550/api/';
export const API_BASE_URL = 'http://192.168.1.58:5550/api/';
// export const API_POSTER_URL = (posterFileName: string) => `http://localhost:5550/api/posters/${posterFileName}`;
export const API_POSTER_URL = (posterFileName: string) => `http://192.168.1.58:5550/api/posters/${posterFileName}`;
export const API_URL = {
  categories: `get-categories`,
  videocards: (category: string | RouteParamValue[]) => `get-list-video/${category}`,
  serialcards: (base: string, file_id: number) => `/get-list-multiseries/${base}/${file_id}`,
  playingvideo: (base: string | RouteParamValue[], file_id: number) => `/play-video/${base}/${file_id}`,
  status_vlc: `check_vlc_status`,
  remote:  (command: string) => `remote/${command}`,
  library_list: `library/get-list`,
  library_update: (library_name: string) => `library/update/${library_name}`,
  library_path_delete: (path_id: number) => `library/delete/${path_id}`,
  library_get_path: `library/getPath`,
  library_add_path: `library/add`,
  iptv_group: `iptv/group`,
  iptv_channels: (group: string) => `iptv/channels/${group}`,
  iptv_epg_now: (group: string) => `iptv/epg/${group}`,
  iptv_epg_channel: (channel_id: string) => `iptv/epg-channel/${channel_id}`,
  iptv_play: `iptv/play`,
  kp_info: `kpinfo`,
  kp_info_update: (id: number) => `kpinfo/${id}`,
  local_db: `local-db`,
  local_db_multiseries: (record_id: number) => `multiseries/${record_id}`,
  local_db_multiseries_update: `update-multiseries`,
  admin_page_backup_list: `get-backups`,
  admin_page_action: (action: string, record_id: string) => `admin-page/${action}?q=${record_id}`,
  admin_settings: `playlist`,
  poster_url: (poster_filename: string) => `posters/${poster_filename}`,
}

export const http  = axios.create({
    baseURL: API_BASE_URL,
    timeout: 300000,
})

export const multi_file_video: string[] = ['Serials', 'Seasons']
