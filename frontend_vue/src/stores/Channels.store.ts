import { defineStore } from 'pinia'
import { ref } from 'vue'
import { API_URL, http } from '@/api.ts'
import type { IChannels, IEpgChannel, IEpgNow } from '@/interfaces/IPTV.interface.ts'


export const useChannelStore = defineStore('iptvChannels', () => {
    const channels  = ref<IChannels[]>()
    async function fetchChannels(group: string) {
      const { data } =  await http.get<IChannels[]>(API_URL.iptv_channels(group))
      channels.value = data
    }
  return { channels, fetchChannels}
});

export const useEpgNowStore = defineStore('epgNow', () => {
  const epgNow  = ref<IEpgNow[]>()
  async function fetchEpgNow(group: string) {
    const { data } =  await http.get<IEpgNow[]>(API_URL.iptv_epg_now(group))
    epgNow.value = data
  }
  return { epgNow, fetchEpgNow}
});

export const useEpgChannelStore = defineStore('epgChannel', () => {
  const epgChannel  = ref<IEpgChannel[]>()
  async function fetchEpgChannel(channel_id: string) {
    const { data } =  await http.get<IEpgChannel[]>(API_URL.iptv_epg_channel(channel_id))
    epgChannel.value = data
  }
  return { epgChannel, fetchEpgChannel}
});
