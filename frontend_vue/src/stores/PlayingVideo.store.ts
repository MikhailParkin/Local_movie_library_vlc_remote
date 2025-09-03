import { defineStore } from 'pinia'
import { ref } from 'vue'
import { API_URL, http } from '@/api.ts'
import type { IPlayingVideo } from '@/interfaces/PlayingVideo.interface.ts'
import type { RouteParamValue } from 'vue-router'

export const usePlayingVideoStore = defineStore('plaingvideo', () => {
  const playingvideo  = ref<IPlayingVideo>()
  async function fetchPlayingVideo(base: string | RouteParamValue[], file_id: number) {
    const { data } =  await http.get<IPlayingVideo>(API_URL.playingvideo(base, file_id))
    playingvideo.value = data
  }

  return { playingvideo, fetchPlayingVideo }
})
