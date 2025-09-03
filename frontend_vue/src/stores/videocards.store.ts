import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { IVideoCard } from '@/interfaces/VideoCard.interface.ts'
import { API_URL, http } from '@/api.ts'

export const useVideoCardsStore = defineStore('videoCard', () => {
    const videocards  = ref<IVideoCard[]>([])
    async function fetchVideoCards(categoryName: string | string []) {
      const { data } =  await http.get<IVideoCard[]>(API_URL.videocards(categoryName))
      videocards.value = data
    }
    async function fetchSerialsCards(base: string, file_id: number) {
      const { data } =  await http.get<IVideoCard[]>(API_URL.serialcards(base, file_id))
      videocards.value = data
    }
    return { videocards, fetchVideoCards, fetchSerialsCards }
})
