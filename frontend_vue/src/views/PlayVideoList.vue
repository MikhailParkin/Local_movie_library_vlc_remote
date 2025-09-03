<script setup lang="ts">

import VideoCard from '@/components/VideoCard.vue'
import { useVideoCardsStore } from '@/stores/videocards.store.ts'
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { API_BASE_URL, API_URL, multi_file_video } from '@/api.ts'
import { usePlayingVideoStore } from '@/stores/PlayingVideo.store.ts'
import { useCategoriesStore } from '@/stores/Categories.store.ts'
import router from '@/router/routes.ts'


const store = useVideoCardsStore();
const route = useRoute();
const playing = ref< number| undefined >();
const playingStore = usePlayingVideoStore();

const category = computed(() => {
  const param = route.params.category;
  return Array.isArray(param) ? param[0] : param;
});
onMounted(() => {
  store.fetchVideoCards(route.params.category)
})

function cardAction(id: number) {
  if (category.value === 'Serials') {
    // console.log('!Serial', id)
    router.push(`/list-videos/Seasons`)
    store.fetchSerialsCards('Seasons', id)
  }
  if (category.value === 'Seasons') {
    // console.log('!Seasons', id)
    router.push(`/list-videos/Series`)
    store.fetchSerialsCards('Series', id)
  }
  else if (category.value !== 'Serials' && category.value !== 'Seasons') {
    playing.value = id;
    playingStore.fetchPlayingVideo(route.params.category, id)

    // console.log('PLAY VIDEO ID: ', playingStore.playingvideo);
  }


}

</script>

<template>
  <div class="videocards-list" v-if="store.videocards">
    <VideoCard  v-for="item in store.videocards"
                :key="item.id"
                :file_name="item.file_name"
                :poster="`${API_BASE_URL}${API_URL.poster_url(item.poster)}`"
                :id="item.id"
                :rate="String(item.rate)"
                :year="item.year" @click="cardAction(item.id)"/>
  </div>
</template>

<style scoped>
@media (max-width: 390px) {
.videocards-list {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 5px;
}}

@media (min-width: 768px) {
  .videocards-list {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 5px;
  }}

</style>
